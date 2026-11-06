# Gates: EN default + DE toggle translation (homepage only)

Scope: Overwrite eezyinn.de.html — English default content (from German) with client-side EN|DE switch; German available via toggle + dictionary, other live pages stay German; assets/JS/CSS logic untouched except toggle block.

- [x] G1: File defaults to English
  CHECK: python check.py
  EXPECT: en: True
  EVIDENCE: script_len: 3103694 | valid_json_dict: True | entries: 141

- [x] G2: hreflang and og locale use en/de, canonical points to /
  CHECK: python check.py
  EXPECT: id_hreflang_absent: True
  EVIDENCE: script_len: 3103694 | valid_json_dict: True | entries: 141

- [x] G3: No visible German CTA text remains in default (scripts excluded)
  CHECK: python check.py
  EXPECT: no_potenzial: True
  EVIDENCE: script_len: 3103694 | valid_json_dict: True | entries: 141

- [x] G4: EN↔DE dictionary exists and is used (positional text-node + attr pairs, longest-first)
  CHECK: python check.py
  EXPECT: dict: True
  EVIDENCE: script_len: 3103694 | valid_json_dict: True | entries: 141

- [x] G5: Toggle logic + storage wired (localStorage, aria-current, lang attr)
  CHECK: python check.py
  EXPECT: ls: True
  EVIDENCE: script_len: 3103694 | valid_json_dict: True | entries: 141

- [x] G6: Assets preserved (file size sane 3MB)
  CHECK: python check.py
  EXPECT: size: 3103979
  EVIDENCE: script_len: 3103694 | valid_json_dict: True | entries: 141

- [x] G7: Switch shows EN active and DE option, no ID remnants
  CHECK: python check.py
  EXPECT: de_switch: True
  EVIDENCE: script_len: 3103694 | valid_json_dict: True | entries: 141
