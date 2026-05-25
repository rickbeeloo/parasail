#!/usr/bin/env python3
"""Insert parasail_sg_{qb_dx,qe_dx,qx_db,qx_de} declarations into parasail.h."""

import re
import sys

OLD = "parasail_sg_qe_de"
NEW_ALGS = [
    "parasail_sg_qb_dx",
    "parasail_sg_qe_dx",
    "parasail_sg_qx_db",
    "parasail_sg_qx_de",
]


def is_sg_qe_de_decl(line):
    return OLD in line and line.strip().startswith("extern")


def is_sg_flags_decl(line):
    return "parasail_sg_flags" in line and line.strip().startswith("extern")


def read_block(lines, start):
    block = []
    i = start
    while i < len(lines):
        block.append(lines[i])
        if lines[i].strip().endswith(");"):
            return block, i + 1
        i += 1
    raise ValueError("unterminated declaration at line %d" % (start + 1))


def patch(lines):
    out = []
    i = 0
    pending = []

    while i < len(lines):
        if is_sg_qe_de_decl(lines[i]):
            block, i = read_block(lines, i)
            pending.append(block)
            continue

        if pending and is_sg_flags_decl(lines[i]):
            for block in pending:
                out.extend(block)
            for new_alg in NEW_ALGS:
                for block in pending:
                    out.extend(ln.replace(OLD, new_alg) for ln in block)
            pending = []

        out.append(lines[i])
        i += 1

    if pending:
        for block in pending:
            out.extend(block)

    return out


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "../parasail.h"
    with open(path, "r", encoding="utf-8") as fh:
        lines = fh.readlines()

    before = sum(1 for ln in lines if OLD in ln)
    patched = patch(lines)
    after = sum(1 for ln in patched if OLD in ln)
    added = len(patched) - len(lines)

    with open(path, "w", encoding="utf-8") as fh:
        fh.writelines(patched)

    print("%s: %d -> %d lines matching %s (+%d lines)" % (
        path, before, after, OLD, added))


if __name__ == "__main__":
    main()
