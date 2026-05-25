#!/bin/bash
# Run Python-2-style util codegen scripts under Python 3.
set -euo pipefail
cd "$(dirname "$0")"
PY=/home/rick/miniforge3/bin/python3
FIX="$(dirname "$0")/fix_py2_print.py"

run() {
    local script=$1
    local out=$2
    "$PY" "$FIX" "$script" | "$PY" - > "$out"
    echo "wrote $out"
}

run funcs.py ../parasail/function_lookup.h
run func_groups.py ../tests/func_verify.h
run func_group_tables.py ../tests/func_verify_tables.h
run func_group_rowcols.py ../tests/func_verify_rowcols.h
run func_group_traces.py ../tests/func_verify_traces.h
run makedef.py ../cmake/parasail.def
