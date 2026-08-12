import re
import sys
import xml.dom.minidom

FILES = [
    "Task1/dfd-as-is.drawio",
    "Task1/dfd-to-be.drawio",
    "Task2/c4-context-to-be.drawio",
    "Task4/ishikawa.drawio",
    "Task6/c2-data-classification-engine.drawio",
]

failed = False

for path in sys.argv[1:] or FILES:
    try:
        doc = xml.dom.minidom.parse(path)
    except Exception as err:
        print("FAIL  %s: %s" % (path, err))
        failed = True
        continue

    pages = doc.getElementsByTagName("diagram")
    src = open(path, encoding="utf-8").read()
    problems = []

    for i, page in enumerate(src.split("<diagram ")[1:], 1):
        name = re.search(r'name="([^"]*)"', page)
        name = name.group(1) if name else "page %d" % i
        ids = re.findall(r'<mxCell id="([^"]+)"', page)
        dups = sorted({x for x in ids if ids.count(x) > 1})
        if dups:
            problems.append("%s: дубли id %s" % (name, dups))
        nodes = set(re.findall(r'<mxCell id="([^"]+)"[^>]*vertex="1"', page))
        for src_id, dst_id in re.findall(r'source="([^"]+)" target="([^"]+)"', page):
            if src_id not in nodes:
                problems.append("%s: связь ссылается на несуществующий узел %s" % (name, src_id))
            if dst_id not in nodes:
                problems.append("%s: связь ссылается на несуществующий узел %s" % (name, dst_id))

    if problems:
        failed = True
        print("FAIL  %s (%d стр.)" % (path, len(pages)))
        for problem in problems:
            print("      " + problem)
    else:
        print("OK    %s — %d стр., %d элементов" % (path, len(pages), src.count("<mxCell ")))

sys.exit(1 if failed else 0)
