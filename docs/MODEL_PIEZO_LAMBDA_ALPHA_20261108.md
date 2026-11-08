# Modelling the piezoelectric in the λ/α equation

**Filed:** 2026-11-08
**Script:** `tools/piezo_model.py` (run with `.venv/bin/python`)
**Answers:** the operator's question "can we model the piezoelectric in the equation?"
**Companions:** `PROCUREMENT_PIEZO_RESONANCE_BENCH_20261108.md` (the bench);
`REALITY_USER_MANUAL/src/phase2/-33.md` §II–III (the Diamond Approach and the
granite→current pathway this model tests)
**Labels:** [his] = operator-authored; [standard] = checkable; [measured] = a named
measurement opened; [modelled] = inferred

---

## 0. Short answer

Yes. The symbol set carries a correct piezoelectric model, and it needs **two
corrections and one relocation**:

1. **Drop `α²`.** α is a phase, therefore dimensionless. `α²` contributes no units
   and cannot move the expression toward charge or current.
2. **Drop the standalone `μ`.** `μά` already *is* the differential `dα`. Writing
   `μ dα` doubles it. This is the term that drove the earlier form to kilograms.
3. **Move the integral off the acoustic phase and onto crystal orientation.** This
   is the substantive find. An angle integral belongs in this problem, but not
   where it was placed — and where it does belong, it decides whether §III of
   `-33.md` works at all.

With those three changes every term lands on a real SI unit, and `ὼν` turns out to
be load-bearing rather than ornamental.

---

## I. The assignment, with units carried

[standard] Units tracked as exponents of (kg, m, s, A) by the `Dim` class in the
script, so the check is executed rather than asserted.

| his term | assignment | dimension |
|---|---|---|
| `λ` | `d`, the transduction operator | `s³·A/kg·m` (= C/N) |
| `α` | acoustic phase, α = ωt | dimensionless |
| `μά` | `dα`, the differential of phase | dimensionless |
| `ὼν` | ω, angular frequency | `1/s` |
| `άνω` | the band edge (see §IV) | `1/s` |

**The form as previously written:**

```
integral lambda * alpha^2 * mu  d-alpha   ->   [s^3.A/kg.m]
```

It never leaves C/N, because the only dimensioned symbol in it is λ. Stress was
missing. That is the whole defect — not an arithmetic slip, a missing physical
quantity.

**Charge.** The direct effect is `D = d·T`, so on an electrode of area A:

```
Q = lambda . T-hat . A . sin(alpha)        ->  [s.A] = coulomb        OK
```

**Current.** This is where `ὼν` enters, and it enters as a multiplier:

```
i = dQ/dt = (dQ/d-alpha)(d-alpha/dt)
i = omega-n . lambda . T-hat . A . cos(alpha)   ->  [A] = ampere      OK
```

[standard] So output current is **linear in ω**. `ὼν` is not decoration and it is
not merely the resonance label — it is the gain. A piezoelectric element driven at
twice the frequency at the same stress delivers twice the current. That is the
single most useful consequence of the whole assignment.

**Voltage.** With `C = εA/t`, the area cancels:

```
g = lambda / eps                            ->  [m^2/s.A] = V.m/N
V = g . T-hat . t . sin(alpha)              ->  [kg.m^2/s^3.A] = volt  OK
```

[standard] **Area sets the charge; thickness sets the voltage.** A wider granite
block gives more coulombs. A *thicker* one gives more volts. Nothing in `-33.md`
§III uses this, and it changes what the King's Chamber geometry would be for.

---

## II. Where the angle integral belongs

[standard] `d` is a third-rank tensor, so the effective longitudinal modulus
depends on direction. For α-quartz (trigonal class 32), along a direction with
cosines (n₁, n₂, n₃):

```
d_long(n) = d11 * (n1^3 - 3*n1*n2^2)
```

Independent of n₃, and **odd in n₁**. That single fact decides §III.

[standard] Quadrature over orientation, with the sin θ solid-angle weight
(`orientation_average` in the script):

| fabric | ⟨d⟩/d₁₁ | rms/d₁₁ |
|---|---|---|
| near-perfect alignment (0.5°) | 0.999886 | 0.9999 |
| strong texture (10° cone) | 0.954965 | 0.9555 |
| moderate texture (30° cone) | 0.641204 | 0.6848 |
| weak texture (60° cone) | 0.046444 | 0.5305 |
| hemisphere | −0.125138 | 0.4781 |
| **random fabric (full sphere)** | **0.000000** | **0.4782** |

[standard] **Quadrature validated analytically.** The hemisphere entry has a closed
form: ⟨n₁³⟩ − 3⟨n₁n₂²⟩ = 1/4 − 3(1/4)(1/2) = **−1/8 = −0.125**, against −0.125138
numerically. The negative sign is not a bug: the cross term outweighs the direct
one over a hemisphere.

### The consequence for `-33.md` §III

[standard] An untextured granite has **no coherent piezoelectric response.** The
mean is exactly zero by symmetry, and the quadrature confirms it to six places.

[standard] But the **rms is 0.478 d₁₁, which is not zero.** That is incoherent:
grain-local charge that cancels across any electrode larger than a grain. So the
honest statement is not "granite is not piezoelectric." It is:

> **A random granite hisses at the drive frequency. It does not generate.**

[modelled] That is a testable discrimination, and it is the right experiment for
the bench in the procurement document: a coherent output is phase-locked to the
drive and scales with electrode area; an incoherent one is not phase-locked and
scales with the *square root* of the number of grains, i.e. it washes out as the
electrode grows. E3 can tell those apart with a lock-in reference, which the
procurement doc already lists.

[standard] Note how fast the coherent part dies. At a 60° cone the mean is already
down to 0.046 while the rms is still 0.53 — **weak texture is almost all noise.**
Preferred orientation has to be strong, not merely present.

[modelled] Preferred crystallographic orientation in a rock is a measured property
(EBSD, or a texture goniometer), not an assumption. If Aswan granite has a quartz
texture, that is a literature question with a real answer, and it is the single
number on which §III turns. It has not been opened in this pass.

---

## III. Magnitudes

[modelled] At `-33.md` §III's own assumed drive of 10 kPa, at 30 Hz, for a 1 m²
by 1 m element. The 10 kPa is an assumption there and remains one here.

| case | Q (C) | i (A) | V (V) |
|---|---|---|---|
| aligned single-crystal quartz | 2.300e−08 | 4.335e−06 | 5.747e+02 |
| granite, 28% quartz, perfect texture | 6.440e−09 | 1.214e−06 | 1.609e+02 |
| granite, 28% quartz, random fabric | 0 | 0 | 0 |

[standard] `g₁₁ = d₁₁/ε = 0.0575 V·m/N`.

So the aligned case is **hundreds of volts at microamps** — a high-impedance,
low-current source. Several hundred volts is a genuinely large number and is where
the intuition that "something could happen here" comes from. The power is
milliwatts per square metre, and only with texture.

---

## IV. `ὼν` and `άνω` are the two edges of one band

[his] The operator's diagram labelled `άνω` as the upper cutoff and gave `ὼν` the
undamped natural frequency.

[standard] A piezoelectric element is a **band-pass**, and both terms are needed
because they are the two different edges:

- **Lower edge, electrical.** The element is a charge source with its own
  capacitance. Into a load R the response rolls off below `f_c = 1/(2πRC)`.
- **Upper edge, mechanical.** The resonance `ω_n`. Usable response stops below it
  (conventionally ~1/3 of it) unless resonance is the thing being used.

[standard] For the 1 m² × 1 m granite element, `C = εA/t = 4.00e−11 F` (40 pF):

| load | high-pass corner |
|---|---|
| 1 MΩ | 3.98e+03 Hz |
| 1 GΩ | 3.98e+00 Hz |
| 1 TΩ | 3.98e−03 Hz |

[standard] **This is a hard bench consequence.** A 30 Hz drive into a 1 MΩ input is
*four kilohertz below the corner* — the signal is gone. Granite's capacitance is
~35× smaller than the DT1-028K film in the procurement document (1.38 nF), so the
corner is ~35× higher at the same load. Low-frequency work on a granite element
needs **gigohm-class input impedance** (an electrometer or charge amplifier), not
the 1–10 MΩ front end that suffices for PVDF film.

---

## V. The corrected equation

[standard] Assembling it, with his symbols kept:

```
   i(alpha)  =  omega-n  .  <lambda>_fabric  .  T-hat  .  A  .  cos(alpha)

   <lambda>_fabric  =  integral over orientation of  d_long(n)  dOmega
                       -------------------------------------------------
                                integral of  dOmega
```

The integral survives, over `dΩ` rather than `dα`. `μά` is the differential.
`α` appears once, as the phase, to first power. `ὼν` multiplies. And the
orientation average out front is the term that is zero for random granite — the
model's own answer to whether §III works.

---

## VI. What was not checked

- Whether Aswan pink granite has measurable quartz texture. This is the one
  number that decides §III and it has not been opened.
- The 10 kPa acoustic drive. Carried from `-33.md` §III as an assumption.
- `d₁₁ = 2.3 pC/N` and `ε_r = 4.52` are standard table values, propagated here,
  not measured.
- The King's Chamber resonance. 30 Hz is used as a round placeholder, not a
  citation. Published figures vary and none were opened in this pass.
- The acoustic→EM "beam formation" step of `-33.md` §V. Still missing a
  mechanism, as the interlocutor in that file said and the operator did not
  contest. This model does not address it and does not rescue it.
