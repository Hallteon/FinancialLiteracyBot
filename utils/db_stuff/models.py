from peewee import *
import peewee_async

db = SqliteDatabase('database.db')


class User(Model):
    username = CharField()
    points = IntegerField(default=0)

    class Meta:
        database = db
