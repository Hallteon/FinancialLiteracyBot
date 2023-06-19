from peewee import *

db = SqliteDatabase('database.db')


class User(Model):
    user_id = CharField(unique=True)
    username = CharField()
    points = IntegerField(default=0)
    passed_test = BooleanField(default=False)

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


def get_all_questions():
    questions = {}
    i = 1

    for question in list(Question.select().execute()):
        questions[i] = {'question': question.question, 'answer': question.answer, 'points': question.points}
        i += 1

    return questions


def get_all_sections():
    sections = [{section.name: [0, section.all_points]} for section in Section.select().execute()]

    return sections


def get_all_sections_questions_data():
    data = {}
    sections = Section.select().execute()
    query = QuestionSection.select(QuestionSection, Question, Section).join(Section).switch(QuestionSection).join(
        Question).order_by(Question.id)
    sections_iterator = 1
    questions_iterator = 1

    for section in sections:
        data[section.id] = {'section_name': section.name, 'total_points': 0, 'all_points': section.all_points, 'questions': {}}
        sections_iterator += 1

    for question_section in query:
        data[question_section.section.id]['questions'][questions_iterator] = {
            'question': question_section.question.question,
            'answer': question_section.question.answer,
            'points': question_section.question.points
        }

        questions_iterator += 1

    return data


def delete_section_by_id(section_id):
    query = Question.select().join(QuestionSection).join(Section).where(Section.id == section_id)

    for question in query:
        quest = Question.delete().where(Question.id == question.id)
        quest.execute()

    section = Section.delete().where(Section.id == section_id)
    section.execute()

    question_section = QuestionSection.delete().where(QuestionSection.section_id == section_id)
    question_section.execute()


def set_user_points(user_id, points):
    user = User.get(user_id=user_id)
    user.points = points

    if not user.passed_test:
        user.passed_test = True

    user.save()