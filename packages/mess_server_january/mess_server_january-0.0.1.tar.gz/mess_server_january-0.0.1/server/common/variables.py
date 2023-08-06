import logging

# Порт по умолчанию для сетевого взаимодействия
BY_DEFAULT_PORT = 7777
# IP адрес по умолчанию для подключения клиента
BY_DEFAULT_IP_ADDRESS = '127.0.0.1'
# Максимальная очередь подключений
MAX_CONNECT = 5
# Максимальная длина сообщений в байтах
MAX_PACKAGE_LETTER = 1024
# Кодировка проекта
CODING = 'utf-8'
# Текущий уровень журналирования
LOGGING_LEVEL = logging.DEBUG
# База данных для хранения данных с сервера:
SERVER_DB = 'server.ini'

# Протокол JIM основные ключи:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'from'
DESTINATION = 'to'
DATA = 'bin'
PUBLIC_KEY = 'pubkey'

# Прочие ключи, используемые в протоколе
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
MESSAGE_TEXT = 'message_text'
EXIT = 'exit'
CONTACTS_GET = 'contacts_get'
INFO_LIST = 'info_list'
CONTACT_REMOVE = 'remove'
CONTACT_ADD = 'add'
REQUEST_USERS = 'request_users'
PUBLIC_KEY_REQUEST = 'pubkey_need'

# Словари - ответы:
# 200
RESPONSE_200 = {RESPONSE: 200}
# 202
RESPONSE_202 = {RESPONSE: 202,
                INFO_LIST: None
                }
# 400
RESPONSE_400 = {
    RESPONSE: 400,
    ERROR: None
}
# 205
RESPONSE_205 = {
    RESPONSE: 205
}

# 511
RESPONSE_511 = {
    RESPONSE: 511,
    DATA: None
}
