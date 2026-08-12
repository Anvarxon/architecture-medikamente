#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

PY=${PY:-python3}

echo "==> Генерация диаграмм"
$PY tools/gen_asis.py Task1/dfd-as-is.drawio
$PY tools/gen_tobe.py Task1/dfd-to-be.drawio
$PY tools/gen_c4.py Task2/c4-context-to-be.drawio
$PY tools/gen_ishikawa.py Task4/ishikawa.drawio
$PY tools/gen_c2.py Task6/c2-data-classification-engine.drawio

echo "==> Проверка диаграмм"
$PY tools/validate.py

echo "==> Проверка документов"
$PY tools/check_docs.py

if [ "${1:-}" != "--with-png" ]; then
    echo "==> Готово (PNG-превью не пересобирались, запустите с --with-png)"
    exit 0
fi

DRAWIO=${DRAWIO:-}
if [ -z "$DRAWIO" ]; then
    for candidate in \
        "/Applications/draw.io.app/Contents/MacOS/draw.io" \
        "$HOME/Applications/draw.io.app/Contents/MacOS/draw.io" \
        "$(command -v drawio || true)"; do
        if [ -n "$candidate" ] && [ -x "$candidate" ]; then
            DRAWIO="$candidate"
            break
        fi
    done
fi

if [ -z "$DRAWIO" ]; then
    echo "draw.io не найден. Установите desktop-версию или задайте путь: DRAWIO=/path/to/drawio $0 --with-png"
    exit 1
fi

echo "==> Экспорт PNG через $DRAWIO"
mkdir -p Task1/preview Task2/preview Task4/preview Task6/preview

for page in 1 2 3 4 5 6; do
    "$DRAWIO" -x -f png --scale 0.8 --page-index "$page" -o "Task1/preview/as-is-$page.png" Task1/dfd-as-is.drawio
    "$DRAWIO" -x -f png --scale 0.8 --page-index "$page" -o "Task1/preview/to-be-$page.png" Task1/dfd-to-be.drawio
done

"$DRAWIO" -x -f png --scale 0.8 --page-index 1 -o Task2/preview/c4-context.png Task2/c4-context-to-be.drawio
"$DRAWIO" -x -f png --scale 0.8 --page-index 2 -o Task2/preview/c4-containers.png Task2/c4-context-to-be.drawio
"$DRAWIO" -x -f png --scale 0.7 --page-index 1 -o Task4/preview/ishikawa.png Task4/ishikawa.drawio
"$DRAWIO" -x -f png --scale 0.8 --page-index 1 -o Task6/preview/c2-engine.png Task6/c2-data-classification-engine.drawio

echo "==> Готово"
