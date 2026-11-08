#!/usr/bin/env python3
"""Piezoelectric transduction under the lambda-alpha symbol assignment.

Answers two questions kept separate on purpose:

  1. Does the operator's symbol set (lambda, alpha, mu-acute, omega-n, ano)
     carry a dimensionally correct piezoelectric model? Section A.
     The previous written form, integral of lambda*alpha^2*mu d-alpha,
     evaluated to kilograms. This checks every candidate term's units
     instead of asserting them.

  2. For granite (quartz in a random aggregate), what is the coherent
     output? Section B. This is the make-or-break number for the
     piezoelectric pathway in REALITY_USER_MANUAL/src/phase2/-33.md III.

Sources for constants are named at point of use. No constant here is
measured by this script; the script only propagates them.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

# --------------------------------------------------------------------------
# Units: exponents of (kg, m, s, A). Enough for mechanics + electricity.
# --------------------------------------------------------------------------

BASE = ("kg", "m", "s", "A")


@dataclass(frozen=True)
class Dim:
    kg: int = 0
    m: int = 0
    s: int = 0
    A: int = 0

    def __mul__(self, o: "Dim") -> "Dim":
        return Dim(self.kg + o.kg, self.m + o.m, self.s + o.s, self.A + o.A)

    def __truediv__(self, o: "Dim") -> "Dim":
        return Dim(self.kg - o.kg, self.m - o.m, self.s - o.s, self.A - o.A)

    def __str__(self) -> str:
        num = [f"{b}^{e}" if e != 1 else b
               for b, e in zip(BASE, (self.kg, self.m, self.s, self.A)) if e > 0]
        den = [f"{b}^{-e}" if e != -1 else b
               for b, e in zip(BASE, (self.kg, self.m, self.s, self.A)) if e < 0]
        if not num and not den:
            return "1 (dimensionless)"
        return (".".join(num) or "1") + ("/" + ".".join(den) if den else "")


DIMLESS = Dim()
KG = Dim(kg=1)
M = Dim(m=1)
S = Dim(s=1)
AMP = Dim(A=1)

NEWTON = KG * M / (S * S)             # kg.m/s^2
PASCAL = NEWTON / (M * M)             # stress
COULOMB = AMP * S
VOLT = KG * M * M / (COULOMB * S * S)
FARAD = COULOMB / VOLT
D_COEFF = COULOMB / NEWTON            # piezoelectric charge constant d
G_COEFF = VOLT * M / NEWTON           # piezoelectric voltage constant g
RAD_PER_S = DIMLESS / S


# --------------------------------------------------------------------------
# Constants, each with its source
# --------------------------------------------------------------------------

D11_QUARTZ = 2.3e-12       # C/N. alpha-quartz d11. Value as cited in -33.md III
                           # and standard tables (Bechmann 1958). Not measured here.
EPS0 = 8.8541878128e-12    # F/m, SI defined
EPS_R_QUARTZ = 4.52        # relative permittivity along x for alpha-quartz
QUARTZ_FRACTION = 0.28     # Aswan granite quartz by volume, figure used in -33.md III


# --------------------------------------------------------------------------
# Section A: the symbol assignment, with units carried
# --------------------------------------------------------------------------

def section_a() -> None:
    print("=" * 74)
    print("A. SYMBOL ASSIGNMENT, UNITS CARRIED")
    print("=" * 74)
    print()
    print("  Operator's terms, from the lambano decomposition:")
    print("    lambda   the function / operator")
    print("    alpha    an angle")
    print("    mu-acute the smallest possible angle  (mu infinitesimal + acute)")
    print("    omega-n  undamped natural frequency")
    print("    ano      top; upper limit; the filter edge")
    print()

    assignment = [
        ("lambda", "d, the transduction operator", D_COEFF),
        ("alpha", "acoustic phase, alpha = omega*t", DIMLESS),
        ("mu-acute", "d-alpha, the differential of phase", DIMLESS),
        ("omega-n", "omega, angular frequency", RAD_PER_S),
        ("T-hat", "stress amplitude", PASCAL),
        ("A", "electrode area", M * M),
    ]
    print("  Assignment:")
    for sym, meaning, dim in assignment:
        print(f"    {sym:<9} {meaning:<34} [{dim}]")
    print()

    # The written form that failed.
    print("  The form as previously written:")
    bad = D_COEFF * DIMLESS * DIMLESS * DIMLESS      # lambda * alpha^2 * mu * d-alpha
    print(f"    integral lambda*alpha^2*mu d-alpha  ->  [{bad}]")
    print("    alpha is dimensionless, so alpha^2 contributes nothing, and mu")
    print("    duplicates d-alpha. The expression cannot reach charge or current.")
    print()

    # Charge.
    print("  Charge on the electrodes (direct effect, Q = d.T.A):")
    q = D_COEFF * PASCAL * (M * M)
    print(f"    Q = lambda . T-hat . A . sin(alpha)      ->  [{q}]  = coulomb")
    assert q == COULOMB, q
    print("    OK: reaches coulomb.")
    print()

    # Current: where omega_n enters.
    print("  Current (dQ/dt = (dQ/d-alpha)(d-alpha/dt), so omega multiplies):")
    i = RAD_PER_S * D_COEFF * PASCAL * (M * M)
    print(f"    i = omega-n . lambda . T-hat . A . cos(alpha)  ->  [{i}]  = ampere")
    assert i == AMP, i
    print("    OK: reaches ampere. omega-n is a gain on the output, not decoration.")
    print()

    # Voltage: area cancels.
    print("  Voltage (V = Q/C with C = eps.A/t, so A cancels and t survives):")
    g = D_COEFF / (FARAD / M)
    v = g * PASCAL * M
    print(f"    g = lambda / eps                        ->  [{g}]")
    print(f"    V = g . T-hat . t . sin(alpha)           ->  [{v}]  = volt")
    assert g == G_COEFF, g
    assert v == VOLT, v
    print("    OK. Area sets the charge, thickness sets the voltage.")
    print()


# --------------------------------------------------------------------------
# Section B: the orientation integral -- where an angle integral belongs
# --------------------------------------------------------------------------

def d_eff_quartz(n1: np.ndarray, n2: np.ndarray) -> np.ndarray:
    """Longitudinal piezoelectric modulus of alpha-quartz (class 32) along a
    direction with cosines (n1, n2, n3).

        d_long(n) = d11 * (n1^3 - 3*n1*n2^2)

    Standard result for trigonal class 32; independent of n3. Note it is ODD
    in n1, which is the whole story for a random aggregate.
    """
    return D11_QUARTZ * (n1**3 - 3.0 * n1 * n2**2)


def orientation_average(cone_half_angle_deg: float, n_theta: int = 2000,
                        n_phi: int = 2000) -> tuple[float, float]:
    """Mean and RMS of d_long over directions inside a cone about +x.

    cone_half_angle_deg = 180 is the full sphere (perfectly random fabric).
    Deterministic quadrature with the sin(theta) solid-angle weight.
    """
    beta = math.radians(cone_half_angle_deg)
    theta = np.linspace(0.0, beta, n_theta)          # polar angle FROM the x axis
    phi = np.linspace(0.0, 2.0 * math.pi, n_phi)
    th, ph = np.meshgrid(theta, phi, indexing="ij")

    n1 = np.cos(th)
    n2 = np.sin(th) * np.cos(ph)

    d = d_eff_quartz(n1, n2)
    w = np.sin(th)                                    # solid-angle weight

    wsum = w.sum()
    mean = float((d * w).sum() / wsum)
    rms = float(math.sqrt((d**2 * w).sum() / wsum))
    return mean, rms


def section_b() -> None:
    print("=" * 74)
    print("B. THE ORIENTATION INTEGRAL (granite)")
    print("=" * 74)
    print()
    print("  An integral over an angle DOES belong in this model, but not over")
    print("  the acoustic phase -- over crystal orientation. d is a tensor, so")
    print("  the effective modulus depends on direction:")
    print()
    print("      d_long(n) = d11 * (n1^3 - 3*n1*n2^2)      [quartz, class 32]")
    print()
    print("  This is odd in n1. Integrated over a full sphere it must vanish.")
    print()

    print(f"  {'fabric':<34} {'<d> / d11':>12} {'rms/d11':>10}")
    print("  " + "-" * 58)
    for beta, label in [
        (0.5, "near-perfect alignment (0.5 deg)"),
        (10.0, "strong texture (10 deg cone)"),
        (30.0, "moderate texture (30 deg cone)"),
        (60.0, "weak texture (60 deg cone)"),
        (90.0, "hemisphere"),
        (180.0, "random fabric (full sphere)"),
    ]:
        mean, rms = orientation_average(beta)
        print(f"  {label:<34} {mean / D11_QUARTZ:>12.6f} {rms / D11_QUARTZ:>10.4f}")
    print()

    mean_rand, rms_rand = orientation_average(180.0)
    print(f"  Random fabric coherent mean: {mean_rand:.3e} C/N")
    print(f"  Random fabric RMS:           {rms_rand:.3e} C/N"
          f"  ({rms_rand / D11_QUARTZ:.3f} x d11)")
    print()
    print("  Reading: an untextured granite has NO coherent piezoelectric")
    print("  response. It has a non-zero RMS, which is incoherent -- grain-local")
    print("  charge that cancels at any electrode larger than a grain. Such a")
    print("  block hisses at the drive frequency; it does not generate.")
    print("  A coherent output requires crystallographic preferred orientation,")
    print("  which is a measurable property of a rock, not an assumption.")
    print()


# --------------------------------------------------------------------------
# Section C: magnitudes, aligned single crystal vs granite
# --------------------------------------------------------------------------

def section_c(stress_pa: float = 1.0e4, thickness_m: float = 1.0,
              area_m2: float = 1.0, freq_hz: float = 30.0) -> None:
    print("=" * 74)
    print("C. MAGNITUDES")
    print("=" * 74)
    print()
    print(f"  Drive:   T-hat = {stress_pa:.0f} Pa ({stress_pa/1e3:.0f} kPa),"
          f"  f = {freq_hz:.0f} Hz,  omega = {2*math.pi*freq_hz:.1f} rad/s")
    print(f"  Element: A = {area_m2:.0f} m^2,  t = {thickness_m:.0f} m")
    print("  (The 10 kPa figure is the 'modest' value assumed in -33.md III.")
    print("   It is an assumption there and remains one here.)")
    print()

    omega = 2.0 * math.pi * freq_hz
    eps = EPS0 * EPS_R_QUARTZ
    g11 = D11_QUARTZ / eps

    mean_rand, rms_rand = orientation_average(180.0)

    cases = [
        ("aligned single-crystal quartz", D11_QUARTZ),
        ("granite, 28% quartz, PERFECT texture", D11_QUARTZ * QUARTZ_FRACTION),
        ("granite, 28% quartz, random fabric", mean_rand * QUARTZ_FRACTION),
    ]

    print(f"  {'case':<40} {'Q (C)':>11} {'i (A)':>11} {'V (V)':>11}")
    print("  " + "-" * 76)
    for label, d in cases:
        q = d * stress_pa * area_m2
        i = omega * q
        v = (d / eps) * stress_pa * thickness_m
        print(f"  {label:<40} {q:>11.3e} {i:>11.3e} {v:>11.3e}")
    print()
    print(f"  g11 = d11/eps = {g11:.4f} V.m/N  (voltage constant, aligned quartz)")
    print()

    print("  The band the signal has to live in (both of the operator's edges):")
    # High-pass corner from the element's own capacitance into a load R.
    cap = eps * area_m2 / thickness_m
    print(f"    element capacitance C = eps.A/t = {cap:.3e} F")
    for r_ohm, rlabel in [(1e6, "1 Mohm"), (1e9, "1 Gohm"), (1e12, "1 Tohm")]:
        fc = 1.0 / (2.0 * math.pi * r_ohm * cap)
        print(f"      into {rlabel:<7} -> high-pass corner f_c = {fc:>12.3e} Hz")
    print("    'ano' as the UPPER edge is the mechanical resonance omega-n;")
    print("    the RC corner is the LOWER edge. A piezo sensor is a band-pass")
    print("    between them, which is why both of his terms are needed.")
    print()


def main() -> None:
    section_a()
    section_b()
    section_c()
    print("=" * 74)
    print("All dimension assertions passed.")
    print("=" * 74)


if __name__ == "__main__":
    main()
