import json
import sys
from common.variables import MAX_PACKAGE_LETTER, CODING
import logging


# метод определения модуля, источника запуска.
# Метод find () возвращает индекс первого вхождения искомой подстроки,
# если он найден в данной строке.
# Если его не найдено, - возвращает -1.
# os.path.split(sys.argv[0])[1]
if sys.argv[0].find('client') == -1:
    # если не клиент то сервер!
    LOGGER = logging.getLogger('server')
else:
    # ну, раз не сервер, то клиент
    LOGGER = logging.getLogger('client')


# Реализация в виде функции
def log(func_to_log):
    """Функция-декоратор"""
    def log_saver(*args, **kwargs):
        ret = func_to_log(*args, **kwargs)
        LOGGER.debug(f'Была вызвана функция {func_to_log.__name__} '
                     f'c параметрами {args}, {kwargs}. '
                     f'Вызов из модуля {func_to_log.__module__}')
        return ret
    return log_saver


@log
def get_report(client):
    '''
    Функция приёма сообщений от удалённых компьютеров.
    Принимает сообщения JSON, декодирует полученное сообщение
    и проверяет что получен словарь.
    :param client: сокет для передачи данных.
    :return: словарь - сообщение.
    '''
    encoded_answer = client.recv(MAX_PACKAGE_LETTER)
    json_answer = encoded_answer.decode(CODING)
    answer = json.loads(json_answer)
    if isinstance(answer, dict):
        return answer
    else:
        raise TypeError


@log
def send_report(sock, report):
    '''
    Функция отправки словарей через сокет.
    Кодирует словарь в формат JSON и отправляет через сокет.
    :param sock: сокет для передачи
    :param message: словарь для передачи
    :return: ничего не возвращает
    '''
    js_report = json.dumps(report)
    encoded_report = js_report.encode(CODING)
    sock.send(encoded_report)
