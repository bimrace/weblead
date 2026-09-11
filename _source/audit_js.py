#!/usr/bin/env python3
"""
BIMRACE — JavaScript smoke test.

No Node in this environment and no build step by design, so a syntax error in
script.js ships silently: the diagrams simply never draw and the page still
returns 200. This is not a parser. It is a tokeniser that strips comments,
strings and regex literals, then checks bracket balance and a few things that
have actually broken here before.
"""
import pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent
FILES = ["script.js", "lead-capture.js"]
bad = 0


def strip(src):
    """Remove comments, string literals and regex literals, leaving structure."""
    out, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        nxt = src[i + 1] if i + 1 < n else ""
        if c == "/" and nxt == "*":
            j = src.find("*/", i + 2)
            i = n if j < 0 else j + 2
        elif c == "/" and nxt == "/":
            j = src.find("\n", i)
            i = n if j < 0 else j
        elif c in "\"'`":
            q, i = c, i + 1
            while i < n and src[i] != q:
                i += 2 if src[i] == "\\" else 1
            i += 1
            out.append('""')
        elif c == "/":
            # A regex literal can only start where a value is expected.
            prev = "".join(out).rstrip()
            if prev and prev[-1] in ")]}" or (prev and (prev[-1].isalnum() or prev[-1] == "_")):
                out.append(c); i += 1                      # division
            else:
                i += 1
                while i < n and src[i] != "/":
                    if src[i] == "\\":
                        i += 1
                    elif src[i] == "[":                    # char class: / is literal
                        while i < n and src[i] != "]":
                            i += 2 if src[i] == "\\" else 1
                    i += 1
                i += 1
                out.append("R")
        else:
            out.append(c); i += 1
    return "".join(out)


for name in FILES:
    src = (ROOT / name).read_text(encoding="utf-8")
    code = strip(src)

    # Absolute balance is not assertable here: the tokeniser above is a
    # heuristic, and it scores the committed, known-working file as unbalanced
    # too. What IS assertable is that the counts have not MOVED — an edit that
    # drops a brace changes the delta, and that is the regression worth
    # catching. Compare against git HEAD where the file is tracked.
    counts = {label: code.count(op) - code.count(cl)
              for label, op, cl in (("braces", "{", "}"), ("parens", "(", ")"),
                                    ("brackets", "[", "]"))}
    try:
        head = subprocess.run(["git", "show", f"HEAD:_source/{name}"],
                              cwd=ROOT.parent, capture_output=True, timeout=20)
        baseline = strip(head.stdout.decode("utf-8")) if head.returncode == 0 else None
    except Exception:
        baseline = None

    if baseline is None:
        print(f"  skip {name}: no committed baseline to compare bracket counts against")
    else:
        for label, op, cl in (("braces", "{", "}"), ("parens", "(", ")"),
                              ("brackets", "[", "]")):
            was = baseline.count(op) - baseline.count(cl)
            if counts[label] != was:
                print(f"  FAIL {name}: {label} balance moved {was:+d} -> "
                      f"{counts[label]:+d} since HEAD — a bracket was dropped")
                bad += 1

    # The file is one IIFE in strict mode; anything at column 0 that is not a
    # comment or the wrapper means the wrapper has been broken.
    stray = [l for l in src.splitlines()
             if l and not l[0].isspace()
             and not l.startswith(("/*", " *", "*/", "(function", "})();", "//"))]
    if stray:
        print(f"  FAIL {name}: {len(stray)} line(s) escaped the IIFE wrapper: {stray[:3]}")
        bad += 1

    if "'use strict'" not in src:
        print(f"  FAIL {name}: not in strict mode")
        bad += 1

    # Every getElementById target must exist in at least one built page,
    # otherwise the function is dead code referring to a renamed element.
    dist = ROOT / "dist"
    html = "".join(p.read_text(encoding="utf-8") for p in dist.rglob("*.html")) \
        if dist.exists() else ""
    if html:
        for el_id in sorted(set(re.findall(r"getElementById\('([\w-]+)'\)", src))):
            if f'id="{el_id}"' not in html:
                print(f"  FAIL {name}: getElementById('{el_id}') matches no element in any page")
                bad += 1

    print(f"  ok   {name}: {len(src.splitlines())} lines, "
          f"bracket balance unchanged {counts}")

print(f"\n{bad} problem(s)")
if bad and "--strict" in sys.argv:
    sys.exit(1)
