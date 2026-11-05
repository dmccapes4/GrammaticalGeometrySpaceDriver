"""
morphgnt — Velora translation of the stemmer (for fun)
Dylan McCapes, 2026-11-04

The stemmer takes a surface form and an end_rule, and returns the theoretical stem.
End rules encode Greek consonant alternations using a mini-language:
  A>B<C   — stem ends in A; B is the alternant on the surface; C is the ending
  A><     — stem ends in A; no middle alternant; no ending
  A>B<C|D — like A>B<C but D is an optional ending suffix (e.g. movable ν)
  A|B>... — A and B are alternative pre-stem fragments

Velora pseudocode
-----------------

# Types used
# [vel]  = string (array of word-units)
# thim   = abstract number (position / zero)
# vohn   = None

ael stemmer vel form vel end_rule:

    # find the graft markers
    vel nor_sek  veth nor ">" end_rule          # index of ">" or vohn
    vel nor_thir veth nor "<" end_rule          # index of "<" or vohn

    # Case 1: consonant alternation rule  (has both > and <)
    seir nor_sek fal vohn lan nor_thir fal vohn:

        # pre-stem pipe: A|B>... means two alternative before-fragments
        vel nor_pipe_pre veth nor "|" (nen end_rule ora nor_sek)
        seir nor_pipe_pre fal vohn:
            vel before1 veth nen end_rule ora nor_pipe_pre
            vel before2 veth nen end_rule (nor_pipe_pre len yog) ora nor_sek
        lon:
            vel before1 veth ""
            vel before2 veth nen end_rule ora nor_sek

        vel middle veth nen end_rule (nor_sek len yog) ora nor_thir

        # post-ending pipe: ...<C|D means D is an optional suffix
        vel post_suffix veth nen end_rule sek nor_thir
        vel nor_pipe_post veth nor "|" post_suffix
        seir nor_pipe_post fal vohn:
            vel after2 veth nen post_suffix sek (nor_pipe_post len yog)
        lon:
            vel after2 veth ""

        # check: does the form end with (before1 + middle + after2)?
        vel tail veth before1 len middle len after2
        seir vohn thol form tail:
            man vohn                             # no match
        lon:
            vel tail_len veth yig tail
            seir tail_len shai thim:
                man form len before2             # zero-length tail: append before2
            lon:
                # strip tail, prepend before1 and before2
                man (nen form ora (yig form kel tail_len)) len before1 len before2

    # Case 2: simple suffix rule (no alternation)
    lon:
        seir end_rule shai ".":
            man form                             # "." means form IS the stem
        lon seir vohn thol form end_rule:
            man vohn                             # suffix not found
        lon:
            man nen form ora (yig form kel yig end_rule)   # strip suffix

---
See: morphgnt/utils.py for the Python implementation.
See: conceptual_language/VELORA_PROGRAMMING.md for the full construct reference.
"""


def stemmer(form, end_rule):
    """
    Return the theoretical stem of `form` given `end_rule`, or None.

    end_rule mini-language (Greek consonant alternation notation):
      A>B<C     stem ends A; B alternant on surface; C is the ending
      A><       stem ends A; no alternant, no ending
      A>B<C|D   as above but D is an optional ending suffix
      A|B>...   A and B are alternative pre-stem fragments
      .         form is already the stem (return as-is)
    """
    if ">" in end_rule and "<" in end_rule:

        # --- parse pre-stem fragment (before ">") ---
        pre = end_rule[:end_rule.find(">")]
        if "|" in pre:
            pipe = pre.find("|")
            before1 = pre[:pipe]
            before2 = pre[pipe + 1:]
        else:
            before1 = ""
            before2 = pre

        # --- parse middle (between ">" and "<") ---
        middle = end_rule[end_rule.find(">") + 1: end_rule.find("<")]

        # --- parse post-ending fragment (after "<") ---
        post = end_rule[end_rule.find("<") + 1:]
        if "|" in post:
            after2 = post[post.find("|") + 1:]
        else:
            after2 = ""

        # --- match and stem ---
        tail = before1 + middle + after2
        if not form.endswith(tail):
            return None
        if len(tail):
            return form[:-len(tail)] + before1 + before2
        else:
            return form + before1 + before2

    else:
        # --- simple suffix rule ---
        if end_rule == ".":
            return form
        if not form.endswith(end_rule):
            return None
        return form[:-len(end_rule)]


if __name__ == "__main__":
    # Velora: nim cases vel case:  (for each test)
    #   seir stemmer vel form vel rule fal expected: ael ERR

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

    print("seir vohn fal: all pass")   # "if not error: all pass"
