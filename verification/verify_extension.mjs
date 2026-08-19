#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
function requireCheck(condition, message) {
  if (!condition) throw new Error(`VERIFICATION FAILED: ${message}`);
}
class Q {
  constructor(n, d = 1n) {
    if (d === 0n) throw new Error("zero denominator");
    if (d < 0n) { n = -n; d = -d; }
    const g = Q.gcd(n < 0n ? -n : n, d);
    this.n = n / g; this.d = d / g;
  }
  static gcd(a, b) { while (b !== 0n) [a, b] = [b, a % b]; return a === 0n ? 1n : a; }
  add(o) { return new Q(this.n * o.d + o.n * this.d, this.d * o.d); }
  sub(o) { return new Q(this.n * o.d - o.n * this.d, this.d * o.d); }
  mul(o) { return new Q(this.n * o.n, this.d * o.d); }
  div(o) { return new Q(this.n * o.d, this.d * o.n); }
  pow(k) { return new Q(this.n ** BigInt(k), this.d ** BigInt(k)); }
  lt(o) { return this.n * o.d < o.n * this.d; }
  le(o) { return this.n * o.d <= o.n * this.d; }
  eq(o) { return this.n === o.n && this.d === o.d; }
  toString() { return this.d === 1n ? `${this.n}` : `${this.n}/${this.d}`; }
}
const q = (n, d = 1n) => new Q(BigInt(n), BigInt(d));
function decimal(s) {
  requireCheck(typeof s === "string" && /^-?\d+(?:\.\d+)?$/.test(s), `bad decimal ${s}`);
  const neg = s.startsWith("-"); const u = neg ? s.slice(1) : s;
  const [a, b = ""] = u.split(".");
  let n = BigInt(a + b); if (neg) n = -n;
  return new Q(n, 10n ** BigInt(b.length));
}
function exactHex(s) {
  const m = /^([+-]?)0x([0-9a-f]+)(?:\.([0-9a-f]+))?p([+-]?\d+)$/i.exec(s);
  requireCheck(m !== null, "bad hexadecimal binary64 token");
  const frac = m[3] || "";
  let n = BigInt(`0x${m[2]}${frac}`);
  const e = Number(m[4]) - 4 * frac.length;
  let out = e >= 0 ? new Q(n * (2n ** BigInt(e))) : new Q(n, 2n ** BigInt(-e));
  return m[1] === "-" ? new Q(-out.n, out.d) : out;
}
function load(name) { return JSON.parse(fs.readFileSync(path.join(here, name), "utf8")); }
function loadLock(name) {
  const entries = {};
  for (const line of fs.readFileSync(path.join(here, name), "utf8").split("\n")) {
    if (!line.trim()) continue;
    requireCheck(line.includes("="), `malformed lock line ${line}`);
    const idx = line.indexOf("=");
    const key = line.slice(0, idx);
    requireCheck(!(key in entries), `duplicate lock key ${key}`);
    entries[key] = line.slice(idx + 1);
  }
  return entries;
}
try {
  const cert = load("extension_certificate.json");
  requireCheck(cert.schema === "non-scattering-positive-frequency-extension-v3", "schema");
  requireCheck(cert.upstream_snapshot === "upstream_snapshot.json", "snapshot path");
  const upstream = load(cert.upstream_snapshot);
  requireCheck(upstream.schema === "non-scattering-upstream-snapshot-v2", "snapshot schema");

  const lock = loadLock("upstream.lock");
  for (const label of ["center", "inverse", "certificate", "source_manifest"]) {
    const token = upstream.authenticated_files[`${label}_sha256`];
    requireCheck(/^[0-9a-f]{64}$/.test(token || ""), `malformed hash for ${label}`);
    requireCheck(token === lock[`${label}_sha256`], `snapshot/lock hash disagreement for ${label}`);
  }
  requireCheck(upstream.paper.commit === lock.commit, "snapshot/lock commit disagreement");
  requireCheck(upstream.paper.repository === lock.repository, "snapshot/lock repository disagreement");

  const Y = decimal(upstream.majorants.Y), Z = decimal(upstream.majorants.Z);
  const C2 = decimal(upstream.majorants.C2), C3 = decimal(upstream.majorants.C3);
  const r = decimal(upstream.majorants.radius);
  requireCheck(Y.eq(q(159n, 10n ** 12n)) && Z.eq(q(621n, 1000n)) && C2.eq(q(122n))
    && C3.eq(q(3n, 250n)) && r.eq(q(1n, 10n ** 6n)), "upstream majorants changed");

  const b = exactHex(upstream.center.p0_hex_binary64);
  const p0Lo = decimal(upstream.center.p0_lower);
  const p0Hi = decimal(upstream.center.p0_upper);
  const pNorm = decimal(upstream.center.weighted_p_upper);
  requireCheck(p0Lo.eq(q(31n)) && p0Hi.eq(q(32n)), "p0 interval bounds");
  requireCheck(p0Lo.lt(b) && b.lt(p0Hi), "p0 interval");
  requireCheck(b.add(r.div(q(2n).mul(p0Lo))).lt(p0Hi), "ball p0 upper bound");
  requireCheck(pNorm.eq(q(55n)), "shape-norm bound");

  const alpha = decimal(cert.extension_majorants.preconditioner_norm_upper);
  const a = decimal(cert.extension_majorants.value_perturbation_coefficient);
  const d = decimal(cert.extension_majorants.derivative_perturbation_coefficient);
  const phi2 = decimal(cert.extension_majorants.conformal_square_norm_upper);
  requireCheck(alpha.eq(q(1180n)), "alpha value");
  requireCheck(C3.mul(q(96n)).mul(q(32n).pow(2)).lt(alpha), "alpha derivation");
  requireCheck(a.eq(q(1906n)) && d.eq(q(3n)) && phi2.eq(q(5n, 4n)), "extension majorants changed");

  const tau = decimal(cert.parameter_interval.tau_upper);
  requireCheck(tau.eq(q(1n, 10n ** 13n)), "tau endpoint");

  const psi = q(1n).add(pNorm.sub(p0Lo).div(q(11n).mul(p0Lo)));
  requireCheck(psi.lt(q(11n, 10n)), "psi bound");
  requireCheck(psi.pow(2).lt(phi2), "conformal square bound");
  const uMax = tau.mul(phi2).div(q(4n));
  requireCheck(uMax.le(q(1n, 2n)), "Bessel majorant condition");
  const datum = q(2n).mul(phi2.div(q(4n))).add(q(2n).div(p0Lo.pow(2)));
  requireCheck(datum.lt(q(63n, 100n)), "datum deviation bound");
  requireCheck(pNorm.pow(2).mul(q(63n, 100n)).lt(a), "value coefficient derivation");
  const xi = q(1n).div(q(2n).mul(p0Lo));
  const dpsi = q(1n, 11n).mul(xi.div(p0Lo).add(pNorm.mul(xi).div(p0Lo.pow(2))));
  requireCheck(dpsi.lt(q(1n, 7000n)), "dpsi bound");
  const dsquare = q(2n).mul(q(11n, 10n)).mul(q(1n, 7000n));
  requireCheck(dsquare.lt(q(1n, 3000n)), "dsquare bound");
  const dH = q(1n, 4n).mul(q(1n, 3000n)).mul(q(4n));
  const derivDerived = q(2n).mul(pNorm).mul(xi).mul(q(63n, 100n))
    .add(pNorm.pow(2).mul(dH))
    .add(pNorm.pow(2).mul(q(2n)).mul(xi).mul(q(2n)).div(p0Lo.pow(3)));
  requireCheck(derivDerived.lt(d), "derivative coefficient derivation");

  const baseR = Y.add(Z.mul(r)).add(C2.mul(r.pow(2))).add(C3.mul(r.pow(3))).sub(r);
  const baseL = Z.add(q(2n).mul(C2).mul(r)).add(q(3n).mul(C3).mul(r.pow(2)));
  const endR = baseR.add(alpha.mul(a).mul(tau));
  const endL = baseL.add(alpha.mul(d).mul(tau));
  requireCheck(baseR.eq(decimal(cert.expected_exact_values.base_radii)), "base radii exact value");
  requireCheck(baseL.eq(decimal(cert.expected_exact_values.base_lipschitz)), "base Lipschitz exact value");
  requireCheck(endR.eq(decimal(cert.expected_exact_values.endpoint_radii)), "endpoint radii exact value");
  requireCheck(endL.eq(decimal(cert.expected_exact_values.endpoint_lipschitz)), "endpoint Lipschitz exact value");
  requireCheck(endR.lt(q(0n)), "radii endpoint");
  requireCheck(endL.lt(q(1n)), "contraction endpoint");
  console.log("POSITIVE-FREQUENCY EXTENSION: VERIFIED (Node/BigInt)");
  console.log(`psi bound = ${psi} < 11/10`);
  console.log(`conformal square bound = ${psi.pow(2)} < ${phi2}`);
  console.log(`value coefficient derivation = ${pNorm.pow(2).mul(q(63n, 100n))} < ${a}`);
  console.log(`derivative coefficient derivation = ${derivDerived} < ${d}`);
  console.log(`endpoint radii = ${endR} < 0`);
  console.log(`endpoint Lipschitz = ${endL} < 1`);
} catch (error) {
  console.error(error.message);
  process.exit(1);
}
