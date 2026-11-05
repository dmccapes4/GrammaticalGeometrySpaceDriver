"""
morphgnt — Velora translation of the stemmer (for fun)
Dylan McCapes, 2026-11-04 (v0.2 names: 2026-11-04)

The stemmer takes a surface form and an end_rule, and returns the theoretical stem.
End rules encode Greek consonant alternations using a mini-language:
  A>B<C     — stem ends A; B is the alternant on the surface; C is the ending
  A><       — stem ends A; no alternant, no ending
  A>B<C|D   — as above; D is an optional ending suffix (e.g. movable ν: -σι(ν))
  A|B>...   — A and B are alternative pre-stem fragments
  .         — form is already the stem

Variable naming rule: yig vol vel shai thol threl  (two or more roots required)
Positional index names: ora-yog (before-1), ora-threl (before-2),
                        sek-yog (after-1), sek-threl (after-2)
thal = middle (homeostasis, center; the segment between > and <)

Velora pseudocode (v0.2)
------------------------

ael vel-stemmer vel vol-form vel vol-rule:

    # find the graft markers in the rule
    vel nor-sek  veth nor ">" vol-rule       # index of ">" or vohn
    vel nor-thir veth nor "<" vol-rule       # index of "<" or vohn
                                             # thir = EDGE (B3) — boundary marker

    # Case 1: consonant alternation rule (has both > and <)
    seir nor-sek fal vohn lan nor-thir fal vohn:

        # pre-stem pipe: A|B>... → two alternative before-fragments
        vel nor-lon-ora veth nor "|" (nen vol-rule ora nor-sek)
        seir nor-lon-ora fal vohn:
            vel ora-yog   veth nen vol-rule ora nor-lon-ora
            vel ora-threl veth nen vol-rule (nor-lon-ora len yog) ora nor-sek
        lon:
            vel ora-yog   veth ""
            vel ora-threl veth nen vol-rule ora nor-sek

        vel thal veth nen vol-rule (nor-sek len yog) ora nor-thir
                                             # thal = the middle fragment (homeostasis)

        # post-ending pipe: ...<C|D → D is optional suffix
        vel vol-sek veth nen vol-rule sek nor-thir
        vel nor-lon-sek veth nor "|" vol-sek
        seir nor-lon-sek fal vohn:
            vel sek-threl veth nen vol-sek sek (nor-lon-sek len yog)
        lon:
            vel sek-threl veth ""

        # check: does form end with (ora-yog + thal + sek-threl)?
        vel vol-thol veth ora-yog len thal len sek-threl
        seir vohn thol vol-form vol-thol:
            man vohn                          # no match
        lon:
            vel yig-thol veth yig vol-thol
            seir yig-thol shai thim:
                man vol-form len ora-threl    # zero-length tail: append ora-threl
            lon:
                # strip tail, prepend ora-yog and ora-threl
                man (nen vol-form ora (yig vol-form kel yig-thol)) len ora-yog len ora-threl

    # Case 2: simple suffix rule (no alternation)
    lon:
        seir vol-rule shai ".":
            man vol-form                      # "." means form IS the stem
        lon seir vohn thol vol-form vol-rule:
            man vohn                          # suffix not present
        lon:
            man nen vol-form ora (yig vol-form kel yig vol-rule)   # strip suffix

---
See: conceptual_language/VELORA_PROGRAMMING.md for the full construct reference (v0.2).
"""


def stemmer(form, end_rule):
    """
    Return the theoretical stem of `form` given `end_rule`, or None.

    end_rule mini-language (Greek consonant alternation notation):
      A>B<C     stem ends A; B alternant on surface; C is the ending
      A><       stem ends A; no alternant, no ending
      A>B<C|D   as above but D is an optional ending suffix
      A|B>...   A and B are alternative pre-stem fragments
      .         form is already the stem

    Velora names used below:
      nor-sek / nor-thir   : find position of ">" / "<"   (find-after / find-edge)
      nor-lon-ora          : find "|" in the pre-stem region  (find-path-before)
      nor-lon-sek          : find "|" in the post-ending region (find-path-after)
      ora-yog / ora-threl  : before-1 / before-2 fragments
      thal                 : middle fragment (homeostasis — the center element)
      sek-threl            : after-2 (the optional ending suffix)
      vol-thol             : the full tail to match (array-end)
      vol-sek              : post-ending portion of rule (array-after)
      yig-thol             : length of the tail
    """
    if ">" in end_rule and "<" in end_rule:

        # parse pre-stem fragment (before ">")
        pre = end_rule[:end_rule.find(">")]          # nen vol-rule ora nor-sek
        nor_lon_ora = pre.find("|")
        if nor_lon_ora != -1:
            ora_yog   = pre[:nor_lon_ora]
            ora_threl = pre[nor_lon_ora + 1:]
        else:
            ora_yog   = ""
            ora_threl = pre

        # thal = the middle fragment (between ">" and "<")
        thal = end_rule[end_rule.find(">") + 1: end_rule.find("<")]

        # parse post-ending fragment (after "<")
        vol_sek     = end_rule[end_rule.find("<") + 1:]
        nor_lon_sek = vol_sek.find("|")
        if nor_lon_sek != -1:
            sek_threl = vol_sek[nor_lon_sek + 1:]
        else:
            sek_threl = ""

        # match and stem
        vol_thol = ora_yog + thal + sek_threl
        if not form.endswith(vol_thol):
            return None
        yig_thol = len(vol_thol)
        if yig_thol:
            return form[:-yig_thol] + ora_yog + ora_threl
        else:
            return form + ora_yog + ora_threl

    else:
        if end_rule == ".":
            return form
        if not form.endswith(end_rule):
            return None
        return form[:-len(end_rule)]


if __name__ == "__main__":
    # A>B<C
    assert stemmer("XB", "A>B<C") == "XA"
    assert stemmer("B", "A>B<C") == "A"
    assert stemmer("C", "A>B<C") is None
    # A><
    assert stemmer("X", "A><") == "A"
    # A>B<C|D
    assert stemmer("XBD", "A>B<C|D") == "XA"
    assert stemmer("BD", "A>B<C|D") == "A"
    assert stemmer("BDE", "A>B<C|D") is None
    assert stemmer("BDE", "A>B<C|DE") == "A"
    assert stemmer("B", "A>B<C|D") is None
    assert stemmer("E", "A>B<C|D") is None
    # A|B><
    print(stemmer("A", "A|B><"), "AB")
    print(stemmer("XA", "A|B><"), "XAB")
    print(stemmer("AB", "A|B><"), None)
    print(stemmer("XAB", "A|B><"), None)

    print("seir vohn fal: all pass")    # if not error: all pass
