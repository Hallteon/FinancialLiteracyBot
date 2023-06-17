from peewee import *

db = SqliteDatabase('database.db')


class User(Model):
    id = CharField(primary_key=True)
    username = CharField()
    points = IntegerField(default=0)

    class Meta:
        database = db


class Question(Model):
    question = TextField()
    answer = BooleanField()
    points = IntegerField()

    class Meta:
        database = db


class Section(Model):
    name = CharField()
    questions = ManyToManyField(Question, backref='section')
    all_points = IntegerField(default=0)

    class Meta:
        database = db


QuestionSection = Section.questions.get_through_model()

