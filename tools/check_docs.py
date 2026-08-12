import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINK = re.compile(r'\[[^\]]*\]\(([^)]+)\)')

problems = []
checked = 0

for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in (".git", ".claude")]
    for name in sorted(filenames):
        if not name.endswith(".md"):
            continue
        path = os.path.join(dirpath, name)
        rel = os.path.relpath(path, ROOT)
        checked += 1
        lines = open(path, encoding="utf-8").read().splitlines()

        for target in LINK.findall("\n".join(lines)):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target = target.split("#")[0]
            if not target:
                continue
            resolved = os.path.normpath(os.path.join(dirpath, target))
            if not os.path.exists(resolved):
                problems.append("%s: битая ссылка -> %s" % (rel, target))

        in_table = False
        width = 0
        start = 0
        for number, line in enumerate(lines, 1):
            stripped = line.strip()
            is_row = stripped.startswith("|") and stripped.endswith("|")
            if is_row and not in_table:
                in_table, width, start = True, stripped.count("|"), number
            elif is_row and in_table:
                if stripped.count("|") != width:
                    problems.append("%s:%d: в таблице со строки %d другое число колонок"
                                    % (rel, number, start))
            elif not is_row:
                in_table = False

for problem in problems:
    print("FAIL  " + problem)

print("Проверено файлов: %d, проблем: %d" % (checked, len(problems)))
sys.exit(1 if problems else 0)
