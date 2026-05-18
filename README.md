# 📄 Парсер документации PEP

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4.12%2B-yellow)](https://www.crummy.com/software/BeautifulSoup/)

**Парсер документации PEP** — инструмент для сбора и анализа информации о документах Python Enhancement Proposals с официального сайта Python.

Проект разработан в рамках обучения на курсе **«Python-разработчик расширенный»** в Яндекс Практикуме.

---

## 📋 Содержание

- [Описание](#-описание)
- [Функции](#-функции)
- [Технологии](#-технологии)
- [Как запустить проект](#-как-запустить-проект)
- [Режимы работы](#-режимы-работы)
- [Аргументы командной строки](#-аргументы-командной-строки)
- [Примеры работы](#-примеры-работы)
- [Автор](#-автор)

---

## 📖 Описание

Парсер собирает данные обо всех документах PEP, сравнивает статус на странице PEP со статусом в общем списке, подсчитывает количество PEP в каждом статусе и общее количество PEP. Результат сохраняется в табличном виде в CSV-файл.

---

## ⚙️ Функции

- Сбор ссылок на статьи о нововведениях в Python
- Сбор информации о версиях Python
- Скачивание архива с актуальной документацией
- Сбор статусов документов PEP и подсчёт статусов
- Вывод информации в терминал (в обычном и табличном виде)
- Сохранение результатов в формате CSV
- Логирование работы парсера
- Обработка ошибок в работе парсера

---

## 🛠 Технологии

- Python
- BeautifulSoup4
- CSV
- argparse
- logging
- Git / GitHub

---

## 🚀 Как запустить проект

**1. Клонировать репозиторий**

```bash
git clone git@github.com:vasilekx/bs4_parser_pep.git
```

```bash
cd bs4_parser_pep
```

**2. Создать и активировать виртуальное окружение**

```bash
python3 -m venv venv
```

* Linux/MacOS

    ```bash
    source venv/bin/activate
    ```

* Windows

    ```bash
    source venv/scripts/activate
    ```

**3. Установить зависимости из файла requirements.txt**

```bash
python3 -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

## Работа с парсером

### Режимы работы
Сброр ссылок на статьи о нововведениях в Python:
```bash
python main.py whats-new
```
Сброр информации о версиях Python:
```bash
python main.py latest-versions
```
Скачивание архива с актуальной документацией:
```bash
python main.py download
```
Сброр статусов документов PEP и подсчёт статусов:
```bash
python main.py pep
```

### Аргументы командной строки
Полный список аргументов:
```bash
python main.py -h
```
```bash
usage: main.py [-h] [-c] [-o {pretty,file}] {whats-new,latest-versions,download,pep}

Парсер документации Python

positional arguments:
  {whats-new,latest-versions,download,pep}
                        Режимы работы парсера

optional arguments:
  -h, --help            show this help message and exit
  -c, --clear-cache     Очистка кеша
  -o {pretty,file}, --output {pretty,file}
                        Дополнительные способы вывода данных
```

## Примеры работы парсинга:

Сброр статусов документов PEP и подсчёт статусов документов с опцией вывода результата в csv-файл:
```bash
python main.py pep -o file
```
```bash
"13.01.2026 16:18:04 - [INFO] - Парсер запущен!"
"13.01.2026 16:18:04 - [INFO] - Аргументы командной строки: Namespace(mode='pep', clear_cache=False, output='file')"
100%|██████████████████████████████████████████████████████████████████████████████████| 711/711 [00:15<00:00, 44.91it/s]
"13.01.2026 16:18:21 - [INFO] - Несовпадающие статусы:"

https://peps.python.org/pep-0401/
Статус в карточке: April Fool!
Ожидаемые статусы: ['Rejected']
"13.01.2026 16:18:21 - [INFO] - Файл с результатами был сохранён: C:\Dev\bs4_parser_pep\src\results\pep_2026-01-13_16-18-21.csv"
"13.01.2026 16:18:21 - [INFO] - Парсер завершил работу."
```
Содержимое файла находится в папке results.


## Автор
Попова Валерия
