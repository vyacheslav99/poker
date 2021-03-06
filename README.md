# Poker
Игра Расписной покер

Версия 1.0.0

Группа проектов

## Структура папок

* `/clients` проекты клиентов к серверу
    * `/mobile` мобильный клиент: `java (android sdk)`
    * `/web` браузерный клиент: `html, JavaScript`
    * `/windows` старая архивная версия игры, оконное приложение Windows: `Delphi`
* `/doc` проектная документация
* `/poker` проект самой игры: `python`
    * `/configs` все конфиги приложения
    * `/controllers` регистрация обработчиков маршрутов для игрового сервера (web-сервис)
    * `/server` движок игрового сервера (web-сервис)
    * `/routers` логика игрового сервера (web-сервис)
    * `/game` игровой движок
    * `/gui` оконное приложение `pyQt5`

## Сервер

Требования:
* python 3.6
* pipenv

#### Развертывание

* утановить/обновить зависимости одной из команд:
  * `python -m pip install -r requirements.txt`
  или для запуска через `pipenv`:
  * `pipenv install`
  * `pipenv update`
* создать файл конфига `config.py` в папке `configs/` скопировав `config.py.tmpl` в `config.py`
* настроить конфиг в полученном файле `configs/config.py`
* запустить сервер командой:

  `python httpd.py`
  или для запуска через `pipenv`:
  `pipenv run python httpd.py`
  
Параметры запуска:
* --debug_mode, -dbg: Включить вывод отладочной информации
* --listen_addr address, -a address: Хост сервера. По умолчанию config.LISTEN_ADDR
* --port port, -p port: Порт сервера. По умолчанию config.LISTEN_PORT
* --log_file filename, -l filename: Перенаправить вывод логов в указанный файл.
По умолчанию настройки логирования прописаны в конфиге

## Приложения

#### gui

Требования:
* python 3.6
* pipenv
* pyQt5

Развертывание и запуск

* утановить/обновить зависимости одной из команд:
  * `python -m pip install -r requirements.txt`
  или для запуска через `pipenv`:
  * `pipenv install`
  * `pipenv update`
* запустить игру:
  `python poker.py`
  или для запуска через `pipenv`:
  `pipenv run python poker.py`
