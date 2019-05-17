import os
import logging


DEBUG = False
LISTEN_ADDR = 'localhost'
LISTEN_PORT = 2100

# INIT_HANDLERS: кол-во дочерних потоков, создаваемых сразу при инициализации сервера -
# т.е. размер пула обработчиков соединений (workers). Если выставить число меньше 1 - обработчики при старте инициализированы не будут,
# их инициализация будет происходить только при подключении клиента.
# MAX_HANDLERS: максимальное кол-во возможных обработчиков.
# Если в пуле не будет обработчиков, готовых принять соединение, будут создаваться новые обработчики, пока их кол-во
# не достигнет MAX_HANDLERS, больше котрого будет происходить действие, заданное параметром WHEN_REACHED_LIMIT.
# После завершения соединения обработчик вернется в пул свободных обработчиков, т.о. пул может быть расширен
# до размера MAX_HANDLERS. Если установить значение меньше 1, кол-во будет не ограничено.
INIT_HANDLERS = 5
MAX_HANDLERS = 50

# HANDLERS_CLEAN_POLICY: Политика очистки пула. При любом варианте пул может быть очищен до размеров init_handlers, никак не меньше:
# 0 - не очищать. Размер пула будет такой, до какого он вырос в процессе работы сервера, но не более MAX_HANDLERS (т.к. он дальше не растет).
# 1 - очищать немедленно. Все свободные обработчики, кол-во которых первысило init_handlers, будут удалены из пула немедленно.
# 2 - удалять неиспользовавшиеся дольше заданного времени. Обработчик будет удален, если он не был выдан из пула ни разу за указанный
# промежуток времени (время задается параметром HANDLERS_CLEAN_TIME, в минутах).
HANDLERS_CLEAN_POLICY = 2
HANDLERS_CLEAN_TIME = 3

# Поведение, когда кол-во занятых обработчиков достигло MAX_HANDLERS:
# 0 - каждое новое входящее соединеие будет сбрасываться до тех пор, пока не освободиться какой-нибудь обработчик;
# 1 - каждое новое соединение будет добавляться в очередь случайно выбранному занятому обработчику, и т.о. будет обработано позже.
WHEN_REACHED_LIMIT = 1

LOGGING = {
    'filename': None,
    'level': logging.DEBUG if DEBUG else logging.INFO,
    'format': '[%(asctime)s] %(levelname).1s %(message)s',
    'datefmt': '%Y.%m.%d %H:%M:%S'
}