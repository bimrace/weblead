#!/usr/bin/env bash
# The Store-installed python.exe on this machine mangles argv when given a
# script path, so the generator is launched through runpy instead.
# Usage: bash _source/build.sh [--install]
set -e
cd "$(dirname "$0")/.."
python -c "
import sys, runpy
sys.argv = ['build.py'] + $( [ "$1" = "--install" ] && echo "['--install']" || echo "[]" )
runpy.run_path('_source/build.py', run_name='__main__')
"
