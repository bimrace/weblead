#!/usr/bin/env bash
# Renders _source/og-source.html headless at 1200x630 -> _source/og-image.png,
# so the share card is generated from the live design tokens rather than drawn
# by hand. The wordmark path is inlined first because fetch() is blocked on
# file:// origins.
set -e
cd "$(dirname "$0")/.."
python -c "
import pathlib, re
root = pathlib.Path('_source')
d = re.search(r'<path d=\"(.*?)\"', (root/'logo.svg').read_text(), re.S).group(1)
src = (root/'og-source.html').read_text(encoding='utf-8')
(root/'_og-render.html').write_text(src.replace('<path id=\"wmpath\"/>', '<path d=\"%s\"/>' % d), encoding='utf-8')
"
EDGE="/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
"$EDGE" --headless=new --disable-gpu --hide-scrollbars --force-prefers-reduced-motion \
  --window-size=1200,630 --virtual-time-budget=9000 \
  --screenshot="c:/Users/sbaste/Downloads/BIMRACE-LEAD/BIMRACE-LEAD-ENGINE/_source/og-image.png" \
  "file:///c:/Users/sbaste/Downloads/BIMRACE-LEAD/BIMRACE-LEAD-ENGINE/_source/_og-render.html" >/dev/null 2>&1
rm -f _source/_og-render.html
echo "og-image.png written"
