from peewee import *
from flask_login import UserMixin


DATABASE = SqliteDatabase('homefind.sqlite')


class User(Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User]), safe = True)
    print("TABLES CREATED")
    DATABASE.close()
