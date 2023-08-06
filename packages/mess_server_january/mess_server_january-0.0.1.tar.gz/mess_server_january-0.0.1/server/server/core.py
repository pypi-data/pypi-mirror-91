import threading
import logging
import select
import socket
import json
import hmac
import binascii
import os
from common.metaclasses import ServerVerifier
from common.descrptrs import Port
from common.variables import BY_DEFAULT_PORT, BY_DEFAULT_IP_ADDRESS, \
    MAX_CONNECT, MAX_PACKAGE_LETTER, CODING, LOGGING_LEVEL, SERVER_DB, \
    ACTION, TIME, USER, ACCOUNT_NAME, SENDER, DESTINATION, PRESENCE, \
    RESPONSE, ERROR, MESSAGE, MESSAGE_TEXT, EXIT, CONTACTS_GET, INFO_LIST, \
    CONTACT_REMOVE, CONTACT_ADD, REQUEST_USERS, RESPONSE_200, RESPONSE_202, \
    RESPONSE_400, RESPONSE_511, DATA, PUBLIC_KEY, PUBLIC_KEY_REQUEST, \
    RESPONSE_205
from common.utils import send_report, get_report
from common.decos import login_required


# Реализация в виде функции
def log(func_to_log):
    """Функция-декоратор"""
    def log_saver(*args, **kwargs):
        ret = func_to_log(*args, **kwargs)
        SERVER_LOGGER.debug(f'Была вызвана функция {func_to_log.__name__} '
                            f'c параметрами {args}, {kwargs}. '
                            f'Вызов из модуля {func_to_log.__module__}')
        return ret
    return log_saver


# Инициализация логирования сервера.
SERVER_LOGGER = logging.getLogger('server')


class MessageProcessor(threading.Thread):
    '''
    Основной класс сервера. Принимает соединения, словари - пакеты
    от клиентов, обрабатывает поступающие сообщения.
    Работает в качестве отдельного потока.
    '''
    port = Port()

    def __init__(self, listen_address, listen_port, db):
        # Параметры подключения
        self.addr = listen_address
        self.port = listen_port

        # База данных сервера
        self.db = db

        # Список подключённых клиентов.
        self.clients = []

        # Сокеты
        self.listen_sockets = None
        self.error_sockets = None

        # Флаг продолжения работы
        self.running = True

        # Словарь содержащий сопоставленные имена и соответствующие им сокеты.
        self.names = dict()

        # Конструктор предка
        super().__init__()

    def run(self):
        '''Метод основной цикл потока.'''
        # Инициализация Сокета
        self.initialization_socket()

        # Основной цикл программы сервера
        while self.running:
            # Ждём подключения, если таймаут вышел, ловим исключение.
            try:
                client, client_address = self.sock.accept()
            except OSError:
                pass
            else:
                SERVER_LOGGER.info(f'Установлено соедение с ПК '
                                   f'{client_address}')
                client.settimeout(5)
                self.clients.append(client)

            recv_data_lst = []
            send_data_lst = []
            err_lst = []
            # Проверяем на наличие ждущих клиентов
            try:
                if self.clients:
                    recv_data_lst, self.listen_sockets, self.error_sockets = \
                        select.select(
                        self.clients, self.clients, [], 0)
            except OSError as err:
                SERVER_LOGGER.error(f'Ошибка работы с сокетами: {err}')

            # принимаем сообщения и если там есть сообщения,
            # кладём в словарь, если ошибка, исключаем клиента.
            if recv_data_lst:
                for client_with_message in recv_data_lst:
                    try:
                        self.process_client_report(get_report(
                            client_with_message), client_with_message)
                    except (OSError, json.JSONDecodeError, TypeError) as err:
                        SERVER_LOGGER.debug(f'Getting data from client '
                                            f'exception.', exc_info=err)
                        self.remove_client(client_with_message)

    def remove_client(self, client):
        '''
        Метод обработчик клиента с которым прервана связь.
        Ищет клиента и удаляет его из списков и базы:
        '''
        SERVER_LOGGER.info(f'Клиент {client.getpeername()} отключился '
                           f'от сервера.')
        for name in self.names:
            if self.names[name] == client:
                self.db.logout_user(name)
                del self.names[name]
                break
        self.clients.remove(client)
        client.close()

    def initialization_socket(self):
        '''Метод инициализатор сокета.'''
        SERVER_LOGGER.info(
            f'Запущен сервер, порт для подключений: {self.port}, '
            f'адрес с которого принимаются подключения: {self.addr}. '
            f'Если адрес не указан, принимаются соединения с любых адресов.')

        # Готовим сокет
        carriage = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        carriage.bind((self.addr, self.port))
        carriage.settimeout(0.5)

        # Слушаем сокет
        self.sock = carriage
        self.sock.listen(MAX_CONNECT)

    def process_report(self, report):
        '''
        Метод отправки сообщения клиенту.
        '''
        if report[DESTINATION] in self.names and \
                self.names[report[DESTINATION]] in self.listen_sockets:
            try:
                send_report(self.names[report[DESTINATION]], report)
                SERVER_LOGGER.info(f'Отправлено сообщение пользователю '
                                   f'{report[DESTINATION]} '
                                   f'от пользователя {report[SENDER]}.')
            except OSError:
                self.remove_client(report[DESTINATION])
        elif report[DESTINATION] in self.names and \
                self.names[report[DESTINATION]] not in self.listen_sockets:
            SERVER_LOGGER.error(
                f'Связь с клиентом {report[DESTINATION]} была потеряна. '
                f'Соединение закрыто, доставка невозможна.')
            self.remove_client(self.names[report[DESTINATION]])
        else:
            SERVER_LOGGER.error(
                f'Пользователь {report[DESTINATION]} не зарегистрирован '
                f'на сервере, отправка сообщения невозможна.')

    @login_required
    def process_client_report(self, report, client):
        '''
        Метод обработчик поступающих сообщений
        '''
        SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {report}')
        # Если это сообщение о присутствии, принимаем и отвечаем
        if ACTION in report and report[ACTION] == PRESENCE and \
                TIME in report and USER in report:
            # Если сообщение о присутствии то вызываем функцию авторизации.
            self.user_autorize(report, client)
        # Если это сообщение, то отправляем его получателю
        elif ACTION in report and report[ACTION] == MESSAGE and \
                DESTINATION in report and TIME in report \
                and SENDER in report and MESSAGE_TEXT in report and \
                self.names[report[SENDER]] == client:
            if report[DESTINATION] in self.names:
                self.db.process_report(report[SENDER], report[DESTINATION])
                self.process_report(report)
                try:
                    send_report(client, RESPONSE_200)
                except OSError:
                    self.remove_client(client)
            else:
                response = RESPONSE_400
                response[ERROR] = 'Пользователь не зарегистрирован на сервере.'
                try:
                    send_report(client, response)
                except OSError:
                    pass
            return

        # Если клиент выходит
        elif ACTION in report and report[ACTION] == EXIT and ACCOUNT_NAME in \
                report and self.names[report[ACCOUNT_NAME]] == client:
            self.remove_client(client)

        # Если это запрос контакт-листа
        elif ACTION in report and report[ACTION] == CONTACTS_GET and USER in \
                report and self.names[report[USER]] == client:
            response = RESPONSE_202
            response[INFO_LIST] = self.db.contacts_get(report[USER])
            try:
                send_report(client, response)
            except OSError:
                self.remove_client(client)

        # Если это добавление контакта
        elif ACTION in report and report[ACTION] == CONTACT_ADD and \
                ACCOUNT_NAME in report and USER in report and \
                self.names[report[USER]] == client:
            self.db.contact_add(report[USER], report[ACCOUNT_NAME])
            try:
                send_report(client, RESPONSE_200)
            except OSError:
                self.remove_client(client)

        # Если это удаление контакта
        elif ACTION in report and report[ACTION] == CONTACT_REMOVE and \
                ACCOUNT_NAME in report and USER in report and \
                self.names[report[USER]] == client:
            self.db.contact_remove(report[USER], report[ACCOUNT_NAME])
            try:
                send_report(client, RESPONSE_200)
            except OSError:
                self.remove_client(client)

        # Если это запрос известных пользователей
        elif ACTION in report and report[ACTION] == REQUEST_USERS and \
                ACCOUNT_NAME in report and \
                self.names[report[ACCOUNT_NAME]] == client:
            response = RESPONSE_202
            response[INFO_LIST] = [user[0] for user in self.db.list_users()]
            try:
                send_report(client, response)
            except OSError:
                self.remove_client(client)

        # Если это запрос публичного ключа пользователя
        elif ACTION in report and report[ACTION] == PUBLIC_KEY_REQUEST and \
                ACCOUNT_NAME in report:
            response = RESPONSE_511
            response[DATA] = self.db.get_pubkey(report[ACCOUNT_NAME])
            # может быть, что ключа ещё нет (пользователь никогда не логинился,
            # тогда шлём 400)
            if response[DATA]:
                try:
                    send_report(client, response)
                except OSError:
                    self.remove_client(client)
            else:
                response = RESPONSE_400
                response[ERROR] = 'Нет публичного ключа для ' \
                                  'данного пользователя'
                try:
                    send_report(client, response)
                except OSError:
                    self.remove_client(client)

        # Иначе отдаём Bad request
        else:
            response = RESPONSE_400
            response[ERROR] = 'Запрос некорректен.'
            try:
                send_report(client, response)
            except OSError:
                self.remove_client(client)

    def user_autorize(self, report, sock):
        '''Метод реализующий авторизцию пользователей.'''
        # Если имя пользователя уже занято то возвращаем 400
        SERVER_LOGGER.debug(f'Start auth process for {report[USER]}')
        if report[USER][ACCOUNT_NAME] in self.names.keys():
            response = RESPONSE_400
            response[ERROR] = 'Имя пользователя уже занято.'
            try:
                SERVER_LOGGER.debug(f'Username busy, sending {response}')
                send_report(sock, response)
            except OSError:
                SERVER_LOGGER.debug('OS Error')
                pass
            self.clients.remove(sock)
            sock.close()
        # Проверяем что пользователь зарегистрирован на сервере.
        elif not self.db.check_user(report[USER][ACCOUNT_NAME]):
            response = RESPONSE_400
            response[ERROR] = 'Пользователь не зарегистрирован.'
            try:
                SERVER_LOGGER.debug(f'Unknown username, sending {response}')
                send_report(sock, response)
            except OSError:
                pass
            self.clients.remove(sock)
            sock.close()
        else:
            SERVER_LOGGER.debug('Correct username, starting passwd check.')
            # Иначе отвечаем 511 и проводим процедуру авторизации
            # Словарь - заготовка
            message_auth = RESPONSE_511
            # Набор байтов в hex представлении
            random_str = binascii.hexlify(os.urandom(64))
            # В словарь байты нельзя, декодируем (json.dumps -> TypeError)
            message_auth[DATA] = random_str.decode('ascii')
            # Создаём хэш пароля и связки с рандомной строкой, сохраняем
            # серверную версию ключа
            hash = hmac.new(self.db.get_hash(report[USER][ACCOUNT_NAME]),
                            random_str, 'MD5')
            digest = hash.digest()
            SERVER_LOGGER.debug(f'Auth message = {message_auth}')
            try:
                # Обмен с клиентом
                send_report(sock, message_auth)
                ans = get_report(sock)
            except OSError as err:
                SERVER_LOGGER.debug('Error in auth, data:', exc_info=err)
                sock.close()
                return
            client_digest = binascii.a2b_base64(ans[DATA])
            # Если ответ клиента корректный, то сохраняем его в список
            # пользователей.
            if RESPONSE in ans and ans[RESPONSE] == 511 and \
                    hmac.compare_digest(digest, client_digest):
                self.names[report[USER][ACCOUNT_NAME]] = sock
                client_ip, client_port = sock.getpeername()
                try:
                    send_report(sock, RESPONSE_200)
                except OSError:
                    self.remove_client(report[USER][ACCOUNT_NAME])
                # добавляем пользователя в список активных и если у него
                # изменился открытый ключ
                # сохраняем новый
                self.db.login_user(
                    report[USER][ACCOUNT_NAME],
                    client_ip,
                    client_port,
                    report[USER][PUBLIC_KEY])
            else:
                response = RESPONSE_400
                response[ERROR] = 'Неверный пароль.'
                try:
                    send_report(sock, response)
                except OSError:
                    pass
                self.clients.remove(sock)
                sock.close()

    def service_update_lists(self):
        '''Метод реализующий отправки сервисного сообщения 205 клиентам.'''
        for client in self.names:
            try:
                send_report(self.names[client], RESPONSE_205)
            except OSError:
                self.remove_client(self.names[client])
