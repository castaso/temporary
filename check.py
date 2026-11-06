import json, re, sys
from pathlib import Path

s = Path("eezyinn.de.html").read_text(encoding="utf-8")
no_scripts = re.sub(r"<script.*?</script>", "", s, flags=re.S)

en = '<html lang="en"' in s
id_hreflang = 'hreflang="id"' in s
de_hreflang = 'hreflang="de"' in s
og_en = 'property="og:locale" content="en_US"' in s
og_alt = 'property="og:locale:alternate" content="de_DE"' in s
canonical_root = 'rel="canonical" href="https://eezyinn.de/"' in s
potenzial = "Potenzial checken" in no_scripts
ls = "localStorage" in s and "eezy-lang" in s
aria = 'aria-current="true"' in s and 'data-lang="en"' in s
langattr = "html.setAttribute('lang'" in s
size = len(s.encode("utf-8"))
de_switch = 'data-lang="de"' in s
id_switch = 'data-lang="id"' in s
switch_en_active = s.count('data-lang="en"') >= 2

# extract dictionary
d = None
try:
    i = s.index("i18nDictionary = [")
    start = s.index("[", i)
    depth = 0
    end = None
    instr = False; esc = False
    for j in range(start, len(s)):
        c = s[j]
        if instr:
            if esc: esc = False
            elif c == "\\": esc = True
            elif c == '"': instr = False
        else:
            if c == '"': instr = True
            elif c == "[": depth += 1
            elif c == "]":
                depth -= 1
                if depth == 0: end = j; break
    d = json.loads(s[start:end + 1])
except Exception as e:
    print("dict parse error:", e)

print(f"script_len: {len(s)}")
print(f"valid_json_dict: {d is not None}")
print(f"entries: {len(d) if d else 0}")
print(f"en: {en} | id_hreflang_absent: {not id_hreflang} | de_hreflang: {de_hreflang}")
print(f"og_en: {og_en} | og_alt: {og_alt} | canonical_root: {canonical_root}")
print(f"no_potenzial: {not potenzial} | ls: {ls} | langattr: {langattr}")
print(f"size: {size} | switch_en_active: {switch_en_active} | de_switch: {de_switch} | id_switch_absent: {not id_switch}")

checks = [
    ("G1 en default", en),
    ("G2 de hreflang, no id", (not id_hreflang) and de_hreflang and og_en and og_alt and canonical_root),
    ("G3 no German CTA in default", not potenzial),
    ("G4 dict valid", d is not None and len(d) > 100),
    ("G5 storage+aria+lang wired", ls and aria and langattr),
    ("G6 size sane (3MB)", 2_500_000 < size < 3_500_000),
    ("G7 EN active + DE option", switch_en_active and de_switch and not id_switch),
]
ok = all(v for _, v in checks)
for name, v in checks:
    print(("PASS " if v else "FAIL ") + name)
sys.exit(0 if ok else 1)
