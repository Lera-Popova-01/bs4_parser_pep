# Проект парсинга pep

## Описание
Парсер собирает дданные обо всех документах PEP,сравнивает статус на странице PEP со статусом в общем списке, посчитывает количество PEP в каждом статусе и общее количество PEP, сохранияет результат в табличном виде в csv-файл.

### Функции парсера:

* Сброр ссылок на статьи о нововведениях в Python;
* Сброр информации о версиях Python;
* Скачивание архива с актуальной документацией;
* Сброр статусов документов PEP и подсчёт статусов документов;
* Вывод информации в терминал (в обычном и табличном виде) и сохранение результатов работы парсинга в формате csv;
* Логирование работы парсинга;
* Обработка ошибок в работе парсинга.

## Применяемые технологии

Beautiful Soup 4

### Запуск проекта

Клонировать репозиторий и перейти в папку в проектом:

```bash
git clone git@github.com:vasilekx/bs4_parser_pep.git
```

```bash
cd bs4_parser_pep
```

Создать и активировать виртуальное окружение:

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

Установить зависимости из файла requirements.txt:

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