#!/usr/bin/env python3
"""
BIMRACE — stylesheet coverage audit.

Two failure modes, both silent in a browser:
  1. markup uses a class the stylesheet never defines  -> unstyled element
  2. the stylesheet defines a class no page ever uses  -> dead CSS

Neither throws an error, so neither gets noticed until someone looks at the
page on a device nobody tested. This looks.
"""
import collections, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
DIST = ROOT / "dist"
CSS = (ROOT / "style.css").read_text(encoding="utf-8")

# Classes the stylesheet defines.
defined = set(re.findall(r"\.([A-Za-z][\w-]*)", re.sub(r"/\*.*?\*/", "", CSS, flags=re.S)))

# Classes the markup uses.
used = collections.Counter()
for p in DIST.rglob("*.html"):
    for attr in re.findall(r'class="([^"]+)"', p.read_text(encoding="utf-8")):
        for c in attr.split():
            used[c] += 1

# Classes referenced by script.js (added at runtime, never present in the HTML).
JS = (ROOT / "script.js").read_text(encoding="utf-8") + \
     (ROOT / "lead-capture.js").read_text(encoding="utf-8")
js_classes = set(re.findall(r"['\"]([a-z][\w-]*(?:__[\w-]+)?(?:--[\w-]+)?)['\"]", JS))

unstyled = sorted(c for c in used if c not in defined)
# SVG classes are set from JS and styled via element selectors in some cases.
dead = sorted(c for c in defined if c not in used and c not in js_classes)

print(f"{len(used)} distinct classes in markup, {len(defined)} defined in CSS\n" + "=" * 70)

if unstyled:
    print(f"\nUNSTYLED — used in markup, absent from style.css ({len(unstyled)})")
    for c in unstyled:
        print(f"  {c:<32} used {used[c]}x")
else:
    print("\nUNSTYLED: none")

if dead:
    print(f"\nUNUSED — defined in style.css, never emitted ({len(dead)})")
    for c in dead:
        print(f"  {c}")
else:
    print("\nUNUSED: none")

if unstyled and "--strict" in sys.argv:
    sys.exit(1)
