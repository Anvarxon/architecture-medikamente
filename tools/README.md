# Инструменты: генерация и проверка диаграмм

Все диаграммы репозитория собираются из кода — файлы `.drawio` не редактировались руками.
Это даёт воспроизводимость (одинаковый вход → байт-в-байт одинаковый выход), понятный diff в пул-реквесте
и возможность быстро перестроить все схемы после правки текста или структуры.

## Состав

| Файл | Что делает | Куда пишет |
|---|---|---|
| `dfdlib.py` | Библиотека: стили, сетка, узлы, границы доверия, маршрутизация связей, сборка mxGraph-XML | — |
| `gen_asis.py` | Диаграммы потоков данных AS-IS, 6 процессов | `Task1/dfd-as-is.drawio` |
| `gen_tobe.py` | Диаграммы потоков данных TO-BE с мерами защиты, 6 процессов | `Task1/dfd-to-be.drawio` |
| `gen_c4.py` | C4: контекст (L1) и контейнеры (L2) | `Task2/c4-context-to-be.drawio` |
| `gen_ishikawa.py` | Диаграмма Исикавы | `Task4/ishikawa.drawio` |
| `gen_c2.py` | C2 движка классификации данных | `Task6/c2-data-classification-engine.drawio` |
| `validate.py` | Проверка XML: корректность, число страниц, дубли идентификаторов, висящие связи | вывод в терминал |
| `check_docs.py` | Проверка документов: битые относительные ссылки и «поехавшие» таблицы в Markdown | вывод в терминал |
| `build.sh` | Полная пересборка: генерация → проверка диаграмм → проверка документов → (опционально) экспорт PNG | все файлы диаграмм |

## Требования

- Python 3.8+ (внешних зависимостей нет, используется только стандартная библиотека);
- draw.io Desktop — только для экспорта PNG-превью; для генерации `.drawio` не нужен.
  Скачать: https://github.com/jgraph/drawio-desktop/releases

## Быстрый старт

Пересобрать все диаграммы и проверить результат:

```bash
./tools/build.sh
```

Пересобрать диаграммы и заодно обновить PNG-превью:

```bash
./tools/build.sh --with-png
```

## Отдельные команды

Сгенерировать конкретную диаграмму:

```bash
python3 tools/gen_asis.py Task1/dfd-as-is.drawio
```

```bash
python3 tools/gen_tobe.py Task1/dfd-to-be.drawio
```

```bash
python3 tools/gen_c4.py Task2/c4-context-to-be.drawio
```

```bash
python3 tools/gen_ishikawa.py Task4/ishikawa.drawio
```

```bash
python3 tools/gen_c2.py Task6/c2-data-classification-engine.drawio
```

Проверить все диаграммы (корректность XML, дубли идентификаторов, связи в никуда):

```bash
python3 tools/validate.py
```

Проверить одну диаграмму:

```bash
python3 tools/validate.py Task1/dfd-to-be.drawio
```

Проверить документацию — относительные ссылки и разметку таблиц:

```bash
python3 tools/check_docs.py
```

Убедиться, что содержимое репозитория воспроизводится из кода (после пересборки `git diff` должен быть пуст):

```bash
./tools/build.sh && git diff --stat
```

## Экспорт PNG вручную

Экспорт одной страницы (нумерация страниц с 1):

```bash
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f png --scale 0.8 --page-index 1 -o Task1/preview/as-is-1.png Task1/dfd-as-is.drawio
```

Если draw.io установлен в другое место, путь задаётся переменной окружения:

```bash
DRAWIO=/path/to/drawio ./tools/build.sh --with-png
```

Экспорт в PDF (например, для приложения к отчёту):

```bash
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f pdf --crop -o Task2/c4-context.pdf Task2/c4-context-to-be.drawio
```

## Просмотр и правка

Открыть диаграмму локально:

```bash
open -a draw.io Task1/dfd-as-is.drawio
```

Онлайн: https://app.diagrams.net → File → Open From → Device → выбрать `.drawio`.

Диаграммы многостраничные: каждый процесс — отдельная вкладка внизу окна draw.io.

Важно: ручные правки в `.drawio` будут потеряны при следующем запуске `build.sh`.
Изменения вносятся в соответствующий `gen_*.py`, после чего диаграмма пересобирается.
