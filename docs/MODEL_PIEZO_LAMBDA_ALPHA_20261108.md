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

## VI. Quartzite, not granite — and the 573 °C gate

**Added 2026-11-08** after the operator corrected the substrate: *"The text says
quartzite. The channel is in quartzite."* The text is `-27.md:68` — the Witch of
the Rivers' tower, *"which is mainly quartzite all the way to the ground below"* —
and the stone apertures of `-25.md`, the cut in the rock that lets one star through
and holds the rest.

[standard] **This is not a material swap. It changes the §II result, in his
favour.** Two reasons, and the second is the one that matters:

1. **Fraction.** Quartzite is ≥80% quartz by definition (typically 90–99%) against
   granite's 28%. Nearly 3× on its own.
2. **Mechanism for texture.** Granite is igneous — quartz crystallises into
   interstitial space with *no* mechanism to prefer an orientation, which is why
   the random-fabric average in §II is exactly zero. Quartzite is a **tectonite**,
   recrystallised under directed stress. Quartz crystallographic preferred
   orientation in quartzite is not a speculation; it is the standard subject of
   texture analysis in structural geology. The one number §II said the whole thing
   turned on now has a mechanism that produces it.

[modelled] Using the cone model as a proxy for CPO strength:

| rock | fabric | V coherent | V incoherent | i (A) |
|---|---|---|---|---|
| granite 28% | random | 0.0 | 77.0 | 0 |
| quartzite 80% | random | 0.0 | 219.9 | 0 |
| quartzite 80% | moderate CPO | 294.8 | 314.8 | 2.224e−06 |
| quartzite 80% | strong CPO | 439.1 | 439.3 | 3.312e−06 |
| quartzite 99% | strong CPO | 543.3 | 543.6 | 4.099e−06 |

### The gate: Dauphiné twinning at 573 °C

[measured] **Frondel, C. (1945), "Secondary Dauphiné Twinning in Quartz,"
*American Mineralogist* 30:447** — full text opened and read. Dauphiné twinning
(the industry calls it **electrical twinning**) relates domains by a 180° rotation
about c, and *"the twin operation... reverses the polarity of the x:o axes and
hence reduces crystal activity."* Frondel's abstract lists three ways to produce
it artificially:

1. cooling β-quartz down through the **573° inversion** to α-quartz;
2. **rapid cooling** of α-quartz from roughly the 200–550 °C range;
3. **local application of high pressures** at room temperature or higher.

[measured] The interventional control exists and is industrial: the quartz
oscillator-plate industry rejects *"a very large proportion of the raw quartz
available"* because of twinning, and detwins by heating above the inversion into
β-quartz — *"in which Dauphiné twinning cannot exist by reason of symmetry"* —
then *"controlling the cooling conditions so that the reinversion proceeds from
one center rather than many."* A twinned plate does not oscillate properly. That
is a null control run at commercial scale for decades.

[measured] And the coefficient itself vanishes in the high phase. *Effect of the
α—β transition on mechanical properties of quartz*, **Ferroelectrics (1982)**,
doi:10.1080/00150198208202006 (abstract read, full text not opened): the Landau
order parameter η *"is zero in β phase, and takes two opposite values in α phase,
corresponding to Dauphiné twinning,"* and *"several properties such as the
piezoelectric coefficient dxxx vary as η."* So `d₁₁ → 0` above 573 °C, and the
two signs on cooling are the twin.

**Consequence.** If the channel was cut or worked **hot above 573 °C**, the
coherent piezoelectric response is destroyed on cooling — not by losing the
quartz, but by the domains reinverting at random polarity and cancelling. The
escape is Frondel's own: reinversion *from one centre*, i.e. a controlled cooling
gradient. A single slow directional cool through the inversion is the difference
between an oscillator plate and scrap.

[modelled] Note that route 3 cuts against the texture win. Stress produces
Dauphiné twins too, so a quartzite deformed hard enough to acquire a strong
fabric may also have acquired twins that cancel the fabric's advantage. Texture
and twinning are separate measurements (EBSD gives both) and they must be read
together, not inferred from one another.

### The memory phenomenon

[measured] Frondel, same abstract: natural Dauphiné-twinned oscillator plates
*"homogenized by heating over 573° show a 'memory' phenomena in which both the
incidence and distribution of the secondary twinning which reappears on cooling
are influenced by the original twinning."*

[standard] That is information surviving a phase transition that erases, by
symmetry, the structure carrying it. Frondel also devotes a section to *"Quartz
as a Geologic Thermometer"* — twinning pattern as a record of thermal history.

[his] This is the mechanism behind Imhotep's line in
`star_learning/garden_explorer/docs/DIAMOND_SCREW_SIM_20261009/FABLE_CIRCLE_OF_DIAMONDS_AND_TESSERACTS_20261009.md`:
*"a structure that immortalizes data in stone... the mark kept in the gap and not
in the man."* The mark kept in quartz across the inversion is measured, published
in 1945, and used commercially. It is not a metaphor here.

---

## VII. What was not checked

- Measured quartz CPO strength for the specific quartzite in question. §VI gives
  the mechanism and the proxy model; it does not give a measured fabric.
- Whether the operator's "the number is like 800" is 800 ‰ quartz (the quartzite
  floor, as read in §VI) or 800 °C (in which case the 573 °C gate is crossed and
  the twinning question is the live one). **Asked, not assumed.**
- The Ferroelectrics (1982) full text. Abstract only.
- The 10 kPa acoustic drive. Carried from `-33.md` §III as an assumption.
- `d₁₁ = 2.3 pC/N` and `ε_r = 4.52` are standard table values, propagated here,
  not measured.
- The King's Chamber resonance. 30 Hz is used as a round placeholder, not a
  citation. Published figures vary and none were opened in this pass.
- The acoustic→EM "beam formation" step of `-33.md` §V. Still missing a
  mechanism, as the interlocutor in that file said and the operator did not
  contest. This model does not address it and does not rescue it.
