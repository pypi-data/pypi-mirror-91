import datetime
from sqlalchemy import create_engine, Table, Column, Integer, String, \
    MetaData, ForeignKey, \
    DateTime, Text
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.sql import default_comparator


class StorageServer:
    '''
    Класс - оболочка для работы с базой данных сервера.
    Использует SQLite базу данных, реализован с помощью
    SQLAlchemy ORM и используется классический подход.
    '''
    class UsersAll:
        '''Класс - отображение таблицы всех пользователей.'''
        def __init__(self, username, passwd_hash):
            self.name = username
            self.last_login = datetime.datetime.now()
            self.passwd_hash = passwd_hash
            self.pubkey = None
            self.id = None

    class UsersActive:
        '''Класс - отображение таблицы активных пользователей.'''
        def __init__(self, user_id, ip_address, port, login_time):
            self.user = user_id
            self.ip_address = ip_address
            self.port = port
            self.login_time = login_time
            self.id = None

    class HistoryLogin:
        '''Класс - отображение таблицы истории входов.'''
        def __init__(self, name, date, ip, port):
            self.id = None
            self.name = name
            self.date_time = date
            self.ip = ip
            self.port = port

    class ContactsUsers:
        '''Класс - отображение таблицы контактов пользователей.'''
        def __init__(self, user, contact):
            self.id = None
            self.user = user
            self.contact = contact

    class HistoryUsers:
        '''Класс - отображение таблицы истории действий.'''
        def __init__(self, user):
            self.id = None
            self.user = user
            self.sent = 0
            self.accepted = 0

    def __init__(self, path):
        # Создаём движок базы данных
        self.db_engine = create_engine(
            f'sqlite:///{path}',
            echo=False,
            pool_recycle=7200,
            connect_args={
                'check_same_thread': False})

        # Создаём объект MetaData
        self.metadata = MetaData()

        # Создаём таблицу пользователей
        table_users = Table('Users', self.metadata,
                            Column('id', Integer, primary_key=True),
                            Column('name', String, unique=True),
                            Column('last_login', DateTime),
                            Column('passwd_hash', String),
                            Column('pubkey', Text)
                            )

        # Создаём таблицу активных пользователей
        table_active_users = Table('Activ_users', self.metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('user', ForeignKey('Users.id'),
                                          unique=True),
                                   Column('ip_address', String),
                                   Column('port', Integer),
                                   Column('login_time', DateTime)
                                   )

        # Создаём таблицу истории входов
        history_login_user = Table('History_login', self.metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('name', ForeignKey('Users.id')),
                                   Column('date_time', DateTime),
                                   Column('ip', String),
                                   Column('port', String)
                                   )

        # Создаём таблицу контактов пользователей
        contacts_users = Table('Contacts_users', self.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('user', ForeignKey('Users.id')),
                         Column('contact', ForeignKey('Users.id'))
                         )

        # Создаём таблицу истории пользователей
        history_users_table = Table('History_users', self.metadata,
                                    Column('id', Integer, primary_key=True),
                                    Column('user', ForeignKey('Users.id')),
                                    Column('sent', Integer),
                                    Column('accepted', Integer)
                                    )

        # Создаём таблицы
        self.metadata.create_all(self.db_engine)

        # Создаём отображения
        # Связываем класс в ORM с таблицей
        mapper(self.UsersAll, table_users)
        mapper(self.UsersActive, table_active_users)
        mapper(self.HistoryLogin, history_login_user)
        mapper(self.ContactsUsers, contacts_users)
        mapper(self.HistoryUsers, history_users_table)

        # Создаём сессию
        session = sessionmaker(bind=self.db_engine)
        self.session = session()

        # Если в таблице активных пользователей есть записи,
        # то их необходимо удалить Когда устанавливаем соединение,
        # очищаем таблицу активных пользователей
        self.session.query(self.UsersActive).delete()
        self.session.commit()

    def login_user(self, username, ip_address, port, key):
        '''
        Метод, выполняющийся при входе пользователя, записывает в базу
        факт входа. Обновляет открытый ключ пользователя при его изменении.
        '''
        # Запрос в таблицу пользователей на наличие там пользователя
        # с таким именем
        rez = self.session.query(self.UsersAll).filter_by(name=username)

        # Если имя пользователя уже присутствует в таблице, обновляем время
        # последнего входа
        # и проверяем корректность ключа. Если клиент прислал новый ключ,
        # сохраняем его.
        if rez.count():
            user = rez.first()
            user.last_login = datetime.datetime.now()
            if user.pubkey != key:
                user.pubkey = key
            # Если нету, то генерируем исключение
        else:
            raise ValueError('Пользователь не зарегистрирован.')

        # Теперь можно создать запись в таблицу активных пользователей
        # о факте входа.
        new_user_active = self.UsersActive(
            user.id, ip_address, port, datetime.datetime.now())
        self.session.add(new_user_active)

        # и сохранить в историю входов
        history = self.HistoryLogin(
            user.id, datetime.datetime.now(), ip_address, port)
        self.session.add(history)

        # Сохраняем изменения
        self.session.commit()

    def add_user(self, name, passwd_hash):
        '''
        Метод регистрации пользователя.
        Принимает имя и хэш пароля, создаёт запись в таблице статистики.
        '''
        user_row = self.UsersAll(name, passwd_hash)
        self.session.add(user_row)
        self.session.commit()
        history_row = self.HistoryUsers(user_row.id)
        self.session.add(history_row)
        self.session.commit()

    def remove_user(self, name):
        '''Метод удаляющий пользователя из базы.'''
        user = self.session.query(self.UsersAll).filter_by(name=name).first()
        self.session.query(self.UsersActive).filter_by(user=user.id).delete()
        self.session.query(self.HistoryLogin).filter_by(name=user.id).delete()
        self.session.query(self.ContactsUsers).filter_by(user=user.id).delete()
        self.session.query(
            self.ContactsUsers).filter_by(
            contact=user.id).delete()
        self.session.query(self.HistoryUsers).filter_by(user=user.id).delete()
        self.session.query(self.UsersAll).filter_by(name=name).delete()
        self.session.commit()

    def get_hash(self, name):
        '''Метод получения хэша пароля пользователя.'''
        user = self.session.query(self.UsersAll).filter_by(name=name).first()
        return user.passwd_hash

    def get_pubkey(self, name):
        '''Метод получения публичного ключа пользователя.'''
        user = self.session.query(self.UsersAll).filter_by(name=name).first()
        return user.pubkey

    def check_user(self, name):
        '''Метод проверяющий существование пользователя.'''
        if self.session.query(self.UsersAll).filter_by(name=name).count():
            return True
        else:
            return False

    def logout_user(self, username):
        '''Метод, фиксирующий отключения пользователя.'''
        # Запрашиваем пользователя, что покидает нас
        # получаем запись из таблицы UsersAll
        user = self.session.query(self.UsersAll).filter_by(
            name=username).first()

        # Удаляем его из таблицы активных пользователей.
        # Удаляем запись из таблицы UsersActive
        self.session.query(self.UsersActive).filter_by(user=user.id).delete()

        # Применяем изменения
        self.session.commit()

    def process_report(self, sender, recipient):
        '''Метод записывающий в таблицу статистики факт передачи сообщения.'''
        sender = self.session.query(self.UsersAll).filter_by(
            name=sender).first().id
        recipient = self.session.query(self.UsersAll).filter_by(
            name=recipient).first().id
        # Запрашиваем строки из истории и увеличиваем счётчики
        sender_row = self.session.query(self.HistoryUsers).filter_by(
            user=sender).first()
        #try:
        sender_row.sent += 1
        #except AttributeError:
        #    pass
        recipient_row = self.session.query(self.HistoryUsers).filter_by(
            user=recipient).first()
        #try:
        recipient_row.accepted += 1
        #except AttributeError:
            #pass

        self.session.commit()

    def contact_add(self, user, contact):
        '''Метод добавления контакта для пользователя.'''
        # Получаем ID пользователей
        user = self.session.query(self.UsersAll).filter_by(
            name=user).first()
        contact = self.session.query(self.UsersAll).filter_by(
            name=contact).first()

        # Проверяем что не дубль и что контакт может существовать
        # (полю пользователь мы доверяем)
        if not contact or self.session.query(self.ContactsUsers).filter_by(
                user=user.id, contact=contact.id).count():
            return

        # Создаём объект и заносим его в базу
        contact_row = self.ContactsUsers(user.id, contact.id)
        self.session.add(contact_row)
        self.session.commit()

    def contact_remove(self, user, contact):
        '''Метод удаления контакта пользователя.'''
        # Получаем ID пользователей
        user = self.session.query(self.UsersAll).filter_by(
            name=user).first()
        contact = self.session.query(self.UsersAll).filter_by(
            name=contact).first()

        # Проверяем что контакт может существовать
        # (полю пользователь мы доверяем)
        if not contact:
            return

        # Удаляем требуемое
        print(self.session.query(self.ContactsUsers).filter(
            self.ContactsUsers.user == user.id,
            self.ContactsUsers.contact == contact.id
        ).delete())
        self.session.commit()

    def list_users(self):
        '''Метод возвращающий список известных пользователей со временем
        последнего входа.'''
        query = self.session.query(
            self.UsersAll.name,
            self.UsersAll.last_login,
        )
        # Возвращаем список кортежей
        return query.all()

    def list_active_users(self):
        '''Метод возвращающий список активных пользователей.'''
        # Запрашиваем соединение таблиц и собираем кортежи имя, адрес,
        # порт, время.
        query = self.session.query(
            self.UsersAll.name,
            self.UsersActive.ip_address,
            self.UsersActive.port,
            self.UsersActive.login_time
        ).join(self.UsersAll)
        # Возвращаем список кортежей
        return query.all()

    def history_login(self, username=None):
        '''Метод возвращающий историю входов.'''
        # Запрашиваем историю входа
        query = self.session.query(self.UsersAll.name,
                                    self.HistoryLogin.date_time,
                                    self.HistoryLogin.ip,
                                    self.HistoryLogin.port
                                    ).join(self.UsersAll)
        # Если было указано имя пользователя, то фильтруем по нему
        if username:
            query = query.filter(self.UsersAll.name == username)
        return query.all()

    def contacts_get(self, username):
        '''Метод возвращающий список контактов пользователя.'''
        # Запрашивааем указанного пользователя
        user = self.session.query(self.UsersAll).filter_by(name=username).one()

        # Запрашиваем его список контактов
        query = self.session.query(self.ContactsUsers, self.UsersAll.name). \
            filter_by(user=user.id). \
            join(self.UsersAll, self.ContactsUsers.contact == self.UsersAll.id)

        # выбираем только имена пользователей и возвращаем их.
        return [contact[1] for contact in query.all()]

    def message_history(self):
        '''Метод возвращающий статистику сообщений.'''
        query = self.session.query(
            self.UsersAll.name,
            self.UsersAll.last_login,
            self.HistoryUsers.sent,
            self.HistoryUsers.accepted
        ).join(self.UsersAll)
        # Возвращаем список кортежей
        return query.all()

"""# Отладка
if __name__ == '__main__':
    test_db = StorageServer()
    # выполняем 'подключение' пользователя
    test_db.login_user('test1', '192.168.1.102', 7777)
    test_db.login_user('test2', '192.168.1.107', 5555)
    print(test_db.list_users())
    # выполянем 'отключение' пользователя
    # test_db.logout_user('test1')
    # выводим список активных пользователей
    # print(test_db.list_active_users())
    # запрашиваем историю входов по пользователю
    # test_db.history_login('test1')
    # выводим список известных пользователей
    # test_db.message_process('test2', 'test1')
    # print(test_db.message_history())"""
