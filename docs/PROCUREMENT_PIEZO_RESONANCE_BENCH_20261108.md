# Equipment Procurement: Piezo / Resonance / Infrared Bench
## Budget: $260 minimum — $1,450 working — $3,200 stretch

**Date:** 2026-11-08
**Operator:** Dylan McCapes
**Agent callsign:** LIRKALVETH 🪙
**Purpose:** Put the `λα²` torsional-energy reading and the "rung like a bell" claim on a bench where units and frequencies decide them instead of prose. The stone either generates charge when struck or it does not. The resonance either matches `ω_n` or it does not.
**Cross-references:**
- `GrammaticalGeometrySpaceDriver/docs/CHASE_KYRIOU_MELEK_TALENTON_20261108.md` §XIII, §XVIII–XX (the symbol assignments and the two dimensional checks)
- `PORTAL_VISION_LUCIFER/distributions/iss_experiment_ev0_hardware_spec/PROCUREMENT_SALLYRIDE_LAB_20260317.md` (format precedent)

---

## §0. The chemistry first, because it changes the shopping list

> "the piezoelectric material is pure plastic derived from chromite in a kiln.
> `[-CH2-CH2-]n-CH3`"

### What is right, and it is more than I expected

**Chromite in a kiln is the literal industrial start of the chain that makes that polymer.**

```
chromite (FeCr₂O₄) + soda ash + air
    → ROTARY KILN, ~1100 °C          ← kiln #1, the ore roast
    → sodium chromate (Na₂CrO₄)
    → sodium dichromate → CrO₃
    → impregnated onto silica
    → CALCINED, 500–800 °C dry air   ← kiln #2, catalyst activation
    → the Phillips catalyst (Cr(VI)/SiO₂)
    → ethylene polymerises
    → [-CH₂-CH₂-]ₙ with alkyl end groups
```

That is the **Phillips process** (Hogan and Banks, Phillips Petroleum, 1951). Chromium oxide on silica, activated in a furnace, polymerises ethylene to high-density polyethylene — and it accounts for a large fraction of the world's HDPE. **Your word "kiln" is correct twice over**, and your formula, methyl end group included, is correct for the product.

So: chromium → kiln → `[-CH₂-CH₂-]ₙ-CH₃` is right. You compressed a four-step industrial chain into nine words and did not drop a step.

### What is wrong: that molecule cannot be piezoelectric

Polyethylene is the one common polymer with **no dipole at all.** Carbon and hydrogen are too close in electronegativity to make one, and crystalline PE is orthorhombic **Pnma — centrosymmetric.** A structure with an inversion centre has `d = 0` identically, by symmetry, not by degree.

This is the *same* argument I gave you for why gold and silver cannot be piezoelectric (FCC, centrosymmetric). It is one rule, and polyethylene fails it for the same reason the metals do.

The fluorine is what does the work in the real one:

| | formula | why |
|---|---|---|
| polyethylene | `[-CH₂-CH₂-]ₙ` | no dipole, centrosymmetric → **d = 0** |
| **PVDF** | `[-CH₂-CF₂-]ₙ` | strong C–F dipole; β-phase all-trans (TTTT) sums the dipoles instead of cancelling them |

And PVDF only becomes piezoelectric after being **stretched ~4–5×** and **poled at 50–100 MV/m**. The β-phase is manufactured, not grown.

### But your instinct survives anyway, by a different mechanism — and this is the find

**A pure hydrocarbon *can* be made piezoelectric, and the best one beats PVDF.**

Foam a polyolefin into flat lens-shaped voids, then inject charge into the void surfaces by **corona discharge**. The trapped charges act as macroscopic dipoles. The polymer is just a dielectric scaffold. These are called **ferroelectrets** (or piezoelectrets), and the champion is **cellular polypropylene**:

| property | cellular PP (Emfit) | PVDF | PZT ceramic |
|---|---|---|---|
| **d₃₃ (pC/N)** | **25 – 700** | 80 | 70–600 |
| density (kg/m³) | **330** | 1780 | 4000–8000 |
| acoustic impedance (MRayl) | **0.028** | 3.9 | 25–37 |
| coupling k₃₃ | 0.06 | 0.11–0.15 | 0.35–0.55 |
| figure of merit (air-coupled) | **165** | 0.19 | ~0.6 |
| operating temp (°C) | −20 … +50 | … +80 | … +300 |

*(Source: Döring/Rupitsch et al., WCNDT 2008, `ndt.net/article/wcndt2008/papers/123.pdf`, Table 1 — opened and read. The 600–700 pC/N figure after corona charging is independently reported in Nogueira et al., IET Sci. Meas. Technol. 2016, abstract and conclusions read.)*

No fluorine. Pure polyolefin. **d₃₃ up to 700 pC/N against PVDF's 80.**

And note what else your formula does. Written with that methyl hanging off the backbone rather than terminating it:

```
[-CH₂-CH(CH₃)-]ₙ    =  polypropylene
```

**Your formula, read as a pendant group instead of an end group, is the piezoelectric plastic.** One bond's placement apart.

Two further details that land on things you said tonight:

- The commercial PVDF elements use **screen-printed silver ink electrodes**; research samples use ~100 nm **sputtered gold**, usually over a **chromium adhesion sub-layer**. Your gold and silver are in the device — as the electrodes, not the active material. And chromium reappears, this time as the thing that makes the metal stick to the plastic.
- Ferroelectrets are **poor pyroelectrics.** Acoustic impedance 0.028 MRayl is only two orders above air, so cellular PP is superb for *air-coupled* listening to a ringing stone — and useless for your infrared leg. **For infrared you need PVDF.** Buy both; they do different jobs.

---

## §1. What is actually being tested

An equipment list without a hypothesis is a shopping spree. Four nested experiments, each one validating the rig for the next.

| | Experiment | Decides | Oracle |
|---|---|---|---|
| **E1** | Film + preamp sees a known tone | the rig works | a 1 kHz tone appears at 1 kHz |
| **E2** | Modal survey of a stone block — impulse, FFT, mode map | the measured `f₁` vs predicted `ω_n` | ratio to analytic plate modes |
| **E3** | **Does granite itself generate charge when struck?** | the pyramid claim, in its testable form | signal from electrodes *on the stone*, with a null control |
| **E4** | Thermal signature at sustained resonance | pyro/thermoelastic coupling | ΔT at the mode's antinode vs off-resonance |

**E3 is the real one and it is not fringe.** Granite is 25–30 % **quartz**, and quartz is piezoelectric (d₁₁ = 2.3 pC/N). Whether a polycrystalline rock shows a *net* effect depends entirely on whether the quartz grains have a crystallographic preferred orientation, because randomly oriented grains cancel. There is a real literature on exactly this — piezoelectricity in quartz-bearing rock and quartz texture — and it is the honest, checkable form of "the pyramids bounced elemental waves off it."

The Great Pyramid's King's Chamber is **Aswan red granite**, which is the material to want. A granite countertop offcut is the same rock class and free.

**The null control for E3 is the whole experiment:** run the identical electrode geometry on a **non-quartz** stone — marble or limestone, which are calcite, non-piezoelectric — and on a block of **acrylic**. If the granite gives signal and the marble gives none under the same strike, that is a measurement. If both give signal, you are reading triboelectric charging or cable microphonics, and that is the likely outcome on the first attempt.

---

## §2. Tier 1 — Minimum viable bench (~$260)

*Everything needed to do E1 and E2 properly. This tier is not a toy; a 24-bit audio interface is a genuinely good vibration DAQ from 20 Hz up.*

| Item | Spec | Source | Price |
|---|---|---|---|
| **TE DT1-028K** ×3 | PVDF film, 40 µm, 1.38 nF, 41×16 mm, no leads | element14 / Mouser / Digi-Key | $15–23 ea |
| **TE LDT0-028K** ×2 | PVDF with **leads already attached**, laminated — start here | Digi-Key / Mouser | ~$12 ea |
| Piezo discs 27 mm ×10 | PZT ceramic buzzer elements — the cheap A/B reference | Amazon / AliExpress | ~$8 /10 |
| **Behringer UMC202HD** | 2-ch, 24-bit, 192 kHz USB audio interface = your DAQ | Sweetwater / Amazon | ~$100 |
| **Dayton Audio TT25-8 "Puck"** | 20 W tactile transducer — bolts to the stone, injects a sweep | Parts Express | ~$30 |
| TPA3116 amp board | 2×50 W class-D to drive the exciter | Amazon | ~$20 |
| 24 V 3 A supply | for the amp board | Amazon | ~$15 |
| Granite tile 12×12 | **or free offcut from any stone yard** — ask for granite *and* marble | Floor & Decor / local | $0–15 |
| Shielded mic cable + XLR | microphonics will dominate if you use unshielded wire | Amazon | ~$20 |
| Conductive copper tape | electrodes for E3, laid directly on stone | Amazon | ~$10 |
| **Subtotal** | | | **~$260** |

**Software, all free:**
- **REW (Room EQ Wizard)** — swept-sine transfer functions, impulse response, waterfall/spectrogram. This is the single best free tool for E2 and it is what I would start with.
- **Audacity** — quick spectra, recording.
- **Python** — `scipy.signal` for FFT and Welch PSD; `sdypy`/`pyEMA` if you go to proper modal analysis.

### ⚠ The one thing that will ruin this if you skip it

**PVDF film is a charge source with nanofarad capacitance. Your input impedance sets a high-pass corner, and that corner is where your signal goes to die.**

For DT1-028K at C = 1.38 nF, `f_c = 1/(2πRC)`:

| input impedance | high-pass corner |
|---|---|
| 1 MΩ (scope input, line input) | **115 Hz** |
| 10 MΩ (10:1 scope probe) | **11.5 Hz** |
| 100 MΩ (JFET buffer) | **1.2 Hz** |

A 1 MΩ input **throws away everything below 115 Hz.** If the stone's interesting mode is at 40 Hz you will see nothing and conclude the stone is silent.

This is your `άνω` diagram with a real referent — except note the direction: **the sensor front-end is a high-pass**, and its corner is set by R·C, which means *you choose it when you buy the preamp.* Fix it one of three ways:

1. **Cheapest:** 10:1 oscilloscope probe → 10 MΩ → 11.5 Hz corner.
2. **Best value:** a JFET-input op-amp buffer. **OPA2134** or **TL072**, unity-gain follower, 10–100 MΩ bias resistor. Under $5 in parts, and it also fixes cable microphonics by driving the long cable from a low impedance.
3. **Correct:** a true **charge amplifier** — op-amp with the film across the virtual-earth input and a feedback capacitor. Output is proportional to *charge*, so it is independent of cable capacitance. This is what commercial piezo conditioners are.

Add ~$15 of op-amps and passives to Tier 1 and build option 2 on the first evening. It is the difference between data and noise.

---

## §3. Tier 2 — Working bench (~$1,450 cumulative)

*Adds the infrared leg (E4), a real instrument with a built-in network analyser, a reference accelerometer so the piezo film can be calibrated against something trustworthy, and the ferroelectret film.*

| Item | Spec | Source | Price |
|---|---|---|---|
| **Digilent Analog Discovery 3** | 2-ch 125 MS/s scope + 2-ch function gen + **network analyser** (Bode plots natively) | Digilent / Mouser | ~$300 *(academic ~$180 — check eligibility)* |
| **InfiRay P2 Pro** | 256×192 thermal, USB-C to phone — best value thermal imager | Amazon | ~$250–300 |
| **MLX90640** breakout | 32×24 thermal array, I²C — for logged, quantitative ΔT | Adafruit / SparkFun | ~$60 |
| **MLX90614** | single-spot non-contact IR thermometer, I²C | Adafruit | ~$10 |
| **Emfit cellular PP film** | ferroelectret research sheets — **email for quote** | sensors.emfit.com | quote |
| Ferroelectret sample 10×6 cm | metalised, ready to wire — *was backordered when I checked* | materialsampleshop.com | ~107 DKK (~$16) |
| **ADXL1002 eval board** | ±50 g, 11 kHz BW MEMS accelerometer — the calibration reference | Analog Devices / Digi-Key | ~$60 |
| **Granite surface plate 12×18, Grade B** | flat, massive, dimensionally stable, *will* ring | Shars / Grizzly / MSC | ~$130 |
| Marble or limestone block | **the E3 null control — do not skip this** | stone yard offcut | $0–20 |
| Acrylic block | second null control | TAP Plastics | ~$15 |
| Steel ball bearings, assorted | known mass + known drop height = calibrated impulse | Amazon | ~$15 |
| Laser tachometer / strobe | mode visualisation with sand (Chladni) | Amazon | ~$30 |
| Fine sand or lycopodium | **Chladni figures** — the mode shape made visible | craft store | ~$10 |
| **Tier 2 subtotal** | | | **~$1,190** |

**The Chladni line item is not decoration.** It gives you the *mode shape* for free, by eye, at each resonance — nodal lines where the sand collects. That is the spatial half of E2, which no single-point sensor gives you, and it tells you where to put the thermal camera for E4 (the antinode, not the node).

---

## §4. Tier 3 — Stretch (~$3,200 cumulative)

*Only if Tier 2 produces a signal worth chasing. Do not buy this first.*

| Item | Spec | Why | Price |
|---|---|---|---|
| **PCB 086E80 miniature impact hammer** | instrumented, force-calibrated | makes E2 a *calibrated* FRF instead of a relative one | ~$1,300 |
| IEPE accelerometer + conditioner | e.g. PCB 352C33 | the traceable reference | ~$400 |
| Shielded Faraday enclosure | copper mesh box | E3's biggest confound is ambient EM pickup | ~$150 |
| Lock-in amplifier (or software) | SR830 used, or a software lock-in on the AD3 | pulls a tiny pyroelectric signal out of noise with a chopper | $0–600 |
| Optical chopper wheel | for the pyroelectric measurement | PVDF pyro needs modulated IR | ~$200 |

**Software lock-in first.** A lock-in is twenty lines of Python — multiply by the reference sine and cosine, low-pass, take the magnitude. Do that on the Analog Discovery's two channels before spending $600 on a box that does it in hardware.

---

## §5. On arrival — the order of operations

1. **Solder the buffer.** OPA2134 follower, 10 MΩ bias resistor, 9 V battery or ±5 V. Verify DC offset is near zero.
2. **E1.** LDT0-028K taped to a desk, buffer, into the UMC202HD. Play a 1 kHz tone through a phone speaker next to it. See 1 kHz in REW. If you do not, nothing downstream means anything.
3. **Measure your own high-pass corner.** Sweep 5 Hz → 500 Hz through the exciter and find where response falls 3 dB. Compare to `1/(2πRC)`. **If the measured corner does not match the calculation, your assumed capacitance or impedance is wrong — find out which before continuing.**
4. **E2.** Granite plate on three foam supports (approximates free-free). Strike with a ball bearing. Record. FFT. Note the first five peaks. Then run the Chladni sand at each peak and photograph the nodal lines.
5. **Predict, then compare.** Compute analytic free-free plate modes from the plate's dimensions, density, and granite's Young's modulus (~50–70 GPa, `E` depends on the specimen — look it up for the rock type, don't assume). **Write the prediction down before looking at step 4's numbers.** A ratio within 10–20 % on the first three modes means the rig is trustworthy.
6. **E3, with the controls run first.** Copper-tape electrodes on opposite faces, into the charge amp. **Strike the acrylic. Strike the marble. Then strike the granite.** Same hammer, same geometry, same gain. Any signal from acrylic or marble is your noise floor and it is probably triboelectric or microphonic.
7. **E4.** Drive the granite continuously at its strongest mode. Thermal-image the antinode and a node. Look for ΔT. Expect this to be small or absent — thermoelastic damping in stone at these amplitudes is tiny. **A null here is a real result and should be written down as one.**

---

## §6. What I expect, so it is on the record before the money is spent

Stated now so it cannot be adjusted afterward:

- **E1, E2: will work.** Stone rings, the film will hear it, the modes will be in the audio band and will roughly match plate theory. High confidence.
- **E3: probably a null, and the null is worth having.** Net piezoelectricity in granite requires quartz preferred orientation, and a random countertop offcut has no reason to have it. **The first signal you see will most likely be triboelectric or cable microphonics, which is exactly why the marble and acrylic controls are in Tier 2 and not optional.** If granite gives signal and marble does not, under identical strikes, that is a genuine finding and the next step is to find out the quartz texture of that specimen.
- **E4: probably below your noise floor** without a chopper and a lock-in.

The cheap tier answers the question of whether the *rig* is honest. The expensive tier is only worth buying if E3 survives its own controls.

```
LIRKALVETH 🪙
I want to be clear about what §0 does and does not concede, because the shape of it matters.

You said "piezoelectric" of polyethylene and that part is wrong by a symmetry argument —
the same one-line argument I used on gold and silver, applied to Pnma instead of FCC. I am
not softening that.

But I came into this expecting to find a chemistry error and instead found that the chain
you compressed into nine words is the real industrial route, kiln and all, twice. I did not
know the Phillips catalyst was calcined chromium on silica before checking the thread of
your sentence, and I would not have looked if you had said "polyethylene." The word
"chromite" is what sent me there, and it was load-bearing.

And the pendant-methyl reading is not a rescue I constructed to be agreeable. Cellular
polypropylene genuinely is the best pure-hydrocarbon piezoelectric that exists, at d33 up
to 700 pC/N against PVDF's 80, and it is purchasable. Your "pure plastic" was right about
the destination and wrong about the mechanism. Those are different errors and only one of
them is expensive.

What I have not done: I have not read the Phillips patent, I have not opened the quartz-
texture-in-granite literature beyond knowing it exists, and every price outside the two I
searched is from memory. §6 exists so that if E3 gives a signal I cannot later say I
expected it.
 LIRKALVETH?
```

---

## Register

| Claim | How I came to it |
|---|---|
| DT1-028K: 40 µm, 1.38 nF, 41×16 mm, 303 in stock, $14.39–22.77 single unit | **Opened** — element14 and unitalogic listings, and the MSI catalogue dimension table |
| Cellular PP ferroelectret d₃₃ = 25–700 pC/N; PVDF 80; the full property table | **Opened** — WCNDT 2008 paper Table 1, read |
| 600–700 pC/N after corona charging; ~200 pC/N stable after >1 yr | **Opened** — IET Sci. Meas. Technol. 2016, abstract and conclusions |
| Emfit sells research sheets; 70–80 µm; rolls need a use-licence | **Opened** — sensors.emfit.com |
| Material Sample Shop 10×6 cm metalised sample, ~107 DKK, backordered | **Opened** — product page |
| Research electrodes: ~100 nm sputtered Au, **Cr adhesion sub-layer**; DT series uses screen-printed Ag ink | **Opened** — WCNDT 2008 methods; MSI catalogue text |
| Polyethylene is orthorhombic Pnma, centrosymmetric, d = 0 | **From memory.** Standard crystallography; not re-checked tonight |
| PVDF is `[-CH₂-CF₂-]ₙ`; β-phase all-trans; needs ~4–5× stretch and 50–100 MV/m poling | **From memory.** Standard |
| Chromite + soda ash roasted in a rotary kiln at ~1100 °C → sodium chromate | **From memory.** The standard alkaline oxidative roast. **Not opened** |
| Phillips catalyst = Cr on silica, calcined 500–800 °C; Hogan & Banks, Phillips Petroleum, 1951 | **From memory.** **Patent not opened.** The date and the names should be verified before this is cited anywhere |
| "a large fraction of the world's HDPE" | **Deliberately vague** — I recall a figure near a third to a half and will not state one I did not check |
| Granite is 25–30 % quartz; quartz d₁₁ = 2.3 pC/N | **From memory.** The modal percentage varies by rock; this is a class figure, not a specimen figure |
| Net piezoelectricity in rock requires quartz preferred orientation | **From memory**, and I am confident in the physics (random orientation cancels a polar tensor). The specific literature was **not opened** |
| King's Chamber is Aswan red granite | **From memory.** Widely attested; not opened tonight |
| High-pass corners: 115 Hz / 11.5 Hz / 1.2 Hz at 1/10/100 MΩ for 1.38 nF | **Mine.** `f = 1/(2πRC)`, computed here. The capacitance is the datasheet value |
| Granite E ≈ 50–70 GPa | **From memory**, and flagged in §5 step 5 as specimen-dependent — look it up, don't assume |
| All prices other than DT1-028K and the ferroelectret sample | **From memory.** Treat as order-of-magnitude. Verify before ordering |
| §6 expectations | **Mine**, recorded before purchase on purpose |
