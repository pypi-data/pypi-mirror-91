import datetime
import os
from sqlalchemy import create_engine, Table, Column, Integer, Text, String, \
    MetaData, DateTime
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.sql import default_comparator


class StorageClient:
    '''
    Класс - оболочка для работы с базой данных клиента.
    Использует SQLite базу данных, реализован с помощью
    SQLAlchemy ORM и используется классический подход.
    '''
    class UsersKnow:
        '''
        Класс - отображение для таблицы всех пользователей.
        '''
        def __init__(self, user):
            self.id = None
            self.username = user

    class StatMessage:
        '''
        Класс - отображение для таблицы статистики переданных сообщений.
        '''
        def __init__(self, contact, direction, message):
            self.id = None
            self.contact = contact
            self.direction = direction
            self.message = message
            self.date = datetime.datetime.now()

    class ListContacts:
        '''
        Класс - отображение для таблицы контактов.
        '''
        def __init__(self, contact):
            self.id = None
            self.name = contact

    # Конструктор класса;
    def __init__(self, name):
        # Создаём движок базы данных, поскольку разрешено несколько
        # клиентов одновременно, каждый должен иметь свою БД
        # Поскольку клиент мультипоточный необходимо отключить
        # проверки на подключения с разных потоков,
        # иначе sqlite3.ProgrammingError
        path = os.getcwd()
        # path = os.path.dirname(os.path.realpath(__file__))
        filename = f'client_{name}.db3'
        self.database_engine = create_engine(
            f'sqlite:///{os.path.join(path, filename)}',
            echo=False,
            pool_recycle=7200,
            connect_args={
                'check_same_thread': False})

        # создаем объект MetaData
        self.metadata = MetaData()

        # создаем таблицу известных пользователей
        know_users = Table('know_users', self.metadata,
                           Column('id', Integer, primary_key=True),
                           Column('username', String))

        # создаем таблицу истории сообщений
        history_message = Table('history_message', self.metadata,
                                Column('id', Integer, primary_key=True),
                                Column('contact', String),
                                Column('direction', String),
                                Column('message', Text),
                                Column('date', DateTime)
                                )

        # создаем таблицу контактов
        list_contacts = Table('list_contacts', self.metadata,
                              Column('id', Integer, primary_key=True),
                              Column('name', String, unique=True))

        # создаем таблицы

        self.metadata.create_all(self.database_engine)

        # создаем отображения
        mapper(self.UsersKnow, know_users)
        mapper(self.StatMessage, history_message)
        mapper(self.ListContacts, list_contacts)

        # создаем сессию
        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

        # необходимо очистить таблицу контактов, так как при запуске они
        # подтягиваются с сервера.
        self.session.query(self.ListContacts).delete()
        self.session.commit()

    def contact_add(self, contact):
        '''Метод добавляющий контакт в базу данных.'''
        if not self.session.query(
                self.ListContacts).filter_by(
                name=contact).count():
            contact_row = self.ListContacts(contact)
            self.session.add(contact_row)
            self.session.commit()

    def contacts_clear(self):
        '''Метод очищающий таблицу со списком контактов.'''
        self.session.query(self.ListContacts).delete()

    def contact_del(self, contact):
        '''Метод очищающий таблицу со списком контактов.'''
        self.session.query(self.ListContacts).filter_by(name=contact).delete()

    def users_add(self, list_users):
        '''Метод заполняющий таблицу известных пользователей.'''
        self.session.query(self.UsersKnow).delete()
        for user in list_users:
            user_row = self.UsersKnow(user)
            self.session.add(user_row)
        self.session.commit()

    def message_save(self, contact, direction, message):
        '''Метод сохраняющий сообщение в базе данных.'''
        message_row = self.StatMessage(contact, direction, message)
        self.session.add(message_row)
        self.session.commit()

    def contacts_get(self):
        '''Метод возвращающий список всех контактов.'''
        return [contact[0] for contact in self.session.query(
            self.ListContacts.name).all()]

    def users_get(self):
        '''Метод возвращающий список всех известных пользователей.'''
        return [user[0] for user in self.session.query(
            self.UsersKnow.username).all()]

    def user_check(self, user):
        '''Метод проверяющий существует ли пользователь.'''
        if self.session.query(self.UsersKnow).filter_by(username=user).count():
            return True
        else:
            return False

    def contact_check(self, contact):
        '''Метод проверяющий существует ли контакт.'''
        if self.session.query(self.ListContacts).filter_by(
                name=contact).count():
            return True
        else:
            return False

    def history_get(self, contact):
        '''Метод, возвращающий историю сообщений с определённым
        пользователем.'''
        query = self.session.query(
            self.StatMessage).filter_by(
            contact=contact)
        return [(history_row.contact,
                 history_row.direction,
                 history_row.message,
                 history_row.date) for history_row in query.all()]


# отладка
if __name__ == '__main__':
    test_db = StorageClient('test_1')
    # for i in ['test3', 'test4', 'test5']:
    #     test_db.contact_add(i)
    # test_db.contact_add('test4')
    # test_db.users_add(['test1', 'test2', 'test3', 'test4', 'test5'])
    # print(test_db.contacts_get())
    # print(test_db.users_get())
    # print(test_db.user_check('test1'))
    # print(test_db.user_check('test10'))
    # print(test_db.history_get('test2'))
    # print(test_db.history_get(to_who='test2'))
    # print(test_db.history_get('test3'))
    print(sorted(test_db.history_get('test2'), key=lambda item: item[3]))
    # test_db.contact_del('test4')
    # print(test_db.contacts_get())
