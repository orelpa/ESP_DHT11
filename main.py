import requests
import psycopg2
from threading import Timer
import threading
import time

base_url = 'http://10.33.6.174'


def resp(url):
    respone = requests.get(f"{base_url}/temp")
    # print(respone.json())
    rezult = respone.json()
    return rezult
    # print(rezult['type'])
    # print(rezult['value'])


# for res in rezult.json().key():
#    print(res)

class DB:
    'Модель подключения, чтения, записи в БД'

    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database

        self.result_box = {}
        self.result_paper = {}
        self.result_all = {}
        # Соединяемся с БД

        self.con = psycopg2.connect(user=self.user, password=self.password, host=self.host, port=self.port,
                                    database=self.database)

        # Автоматическое сохранение изменений
        self.con.autocommit = True
        # создаём курсор для работы с БД
        self.cur = self.con.cursor()

        # создаём таблицу если её не существует

        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS esp32temphumi (id serial PRIMARY KEY, type TEXT, value FLOAT, posting_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP)"
        )


    def insert(self, typez, valuez):

        "Метод создания новой сторки на новый день"
        queru = """INSERT INTO esp32temphumi (type, value) VALUES(%s,%s)"""
        inst = (typez, valuez)
        self.cur.execute(
            queru, inst
        )


my_bd = DB("postgres", "postgres", "127.0.0.1", "5432", "esp32")


# my_bd.insert('tempz', 25)

# resultat= resp(url=base_url)
def parsing():
    resultat = resp(url=base_url)
    my_bd.insert(resultat['type'], round(resultat['value'], 2))
    t = Timer(30.0, parsing)
    t.start()


# print(resp(url=base_url))
# parsing()
t = Timer(30.0, parsing)
t.start()

# t.start()
while True:
    pass

# for key, value in dict.items():
#    print(key)
# print(resultat['type'])
# print()

# my_bd.insert(resultat['type'],round(resultat['value'], 2))