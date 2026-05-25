#!/usr/bin/env python3
"""Rewrite Python-2 print statements to print() for one-shot codegen scripts."""
import re
import sys


def fix_source(source):
    lines = source.splitlines(keepends=True)
    out = []
    i = 0
    while i < len(lines):
        m = re.match(r'^(\s*)print\s+(.*)$', lines[i])
        if not m or m.group(2).lstrip().startswith('('):
            out.append(lines[i])
            i += 1
            continue

        indent, rest = m.group(1), m.group(2)
        if rest.endswith('\n'):
            rest = rest[:-1]
        if rest.endswith('\r'):
            rest = rest[:-1]

        parts = [rest]
        i += 1
        combined = rest
        while i < len(lines):
            if combined.count('"""') % 2 == 1 or combined.count("'''") % 2 == 1:
                parts.append(lines[i].rstrip('\n\r'))
                combined += lines[i]
                i += 1
                continue
            if parts[-1].rstrip().endswith('\\'):
                parts.append(lines[i].rstrip('\n\r'))
                combined += lines[i]
                i += 1
                continue
            break

        expr = ' '.join(p.strip() for p in parts).strip()
        if expr.endswith('\\'):
            expr = expr[:-1].rstrip()
        out.append('%sprint(%s)\n' % (indent, expr))
    return ''.join(out)


def main():
    path = sys.argv[1]
    with open(path, 'r', encoding='utf-8') as fh:
        sys.stdout.write(fix_source(fh.read()))


if __name__ == '__main__':
    main()
