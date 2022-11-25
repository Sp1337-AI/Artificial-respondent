import numpy as np
from mimesis import Person
from mimesis.locales import Locale
from mimesis.enums import Gender
from dataInterfaces import googleFormsInterface as gFormParser
from answer_fill import MethodicFiller


def generate_name(gender):
    ru = Person(locale=Locale.RU)
    if gender == 'female':
        name = ru.full_name(gender=Gender.FEMALE)
        return name
    elif gender == 'male':
        name = ru.full_name(gender=Gender.MALE)
        return name
    else:
        print('There are only two genders!')


def invert_permutation(p):
    p = np.asanyarray(p)
    s = np.empty_like(p)
    s[p] = np.arange(p.size)
    return s


def cut_number_of_question_order(question):
    out_question = "".join(filter(lambda c: c != '.' and c != ';', question))
    while True:
        if not out_question[0].isdigit():
            break
        out_question = out_question[1:]
    if out_question[0] == ' ':
        out_question = out_question[1:]
    if out_question[-1] == ' ':
        out_question = out_question[:-1]

    return out_question


class RespondentGenerator(object):
    def fill_age(self) -> int:
        if self.education == 'Среднее':
            return np.random.choice([np.random.randint(16, 19), np.random.randint(19, 26), np.random.randint(26, 51)],
                                    p=[0.9, 0.075, 0.025])
        elif self.education == 'Среднее специальное':
            return np.random.choice([np.random.randint(16, 19), np.random.randint(19, 26), np.random.randint(26, 51)],
                                    p=[0.5, 0.25, 0.25])
        elif self.education == 'Неоконченное высшее, Бакалавр (еще учусь)':
            return np.random.choice([np.random.randint(19, 26), np.random.randint(26, 51)], p=[0.9, 0.1])
        elif self.education == 'Высшее, Бакалавр (уже закончил)':
            return np.random.choice([np.random.randint(19, 26), np.random.randint(26, 51)], p=[0.4, 0.6])
        elif self.education == 'Научная степень':
            return np.random.choice([np.random.randint(23, 26), np.random.randint(26, 61)], p=[0.4, 0.6])
        else:
            raise ValueError("Wrong education value")

    def fill_course(self):
        if self.education == 'Научная степень':
            return np.random.randint(1, 3)
        else:
            raise np.random.randint(1, 5)

    def fill_nation(self):
        if self.gender == 'Женский':
            return np.random.choice(['Русская', 'Узбечка', 'Татарка', 'Таджичка', 'Немка', 'Еврейка'],
                                    p=[0.2, 0.6, 0.15, 0.02, 0.01, 0.02])
        elif self.gender == 'Мужской':
            return np.random.choice(['Русский', 'Узбек', 'Татарин', 'Таджик', 'Немец', 'Еврей'],
                                    p=[0.2, 0.6, 0.15, 0.02, 0.01, 0.02])

    def fill_job_exp(self):
        if 16 <= self.age <= 18:
            return np.random.choice([0, 1], p=[0.85, 0.15])
        elif 18 < self.age <= 30:
            return np.random.choice([0, 1, 2, 3, 4, 5], p=[0.1, 0.2, 0.3, 0.2, 0.1, 0.1])
        elif 30 < self.age <= 45:
            return np.random.choice([np.random.randint(2, 6), np.random.randint(6, 12)], p=[0.4, 0.6])
        elif 45 < self.age:
            return np.random.randint(10, 25)

    def fill_faith(self):
        if self.nation == 'Узбек' or self.nation == 'Узбечка':
            return np.random.choice(['Ислам', 'Христианство', 'Иудаизм', 'Атеизм'], p=[0.9, 0.06, 0.01, 0.04])
        elif self.nation == 'Русский' or self.nation == 'Русская':
            return np.random.choice(['Ислам', 'Христианство', 'Иудаизм', 'Атеизм'], p=[0.1, 0.7, 0.01, 0.19])
        elif self.nation == 'Татарин' or self.nation == 'Татарка':
            return np.random.choice(['Ислам', 'Христианство', 'Иудаизм', 'Атеизм'], p=[0.6, 0.2, 0.01, 0.19])
        elif self.nation == 'Таджик' or self.nation == 'Таджичка':
            return np.random.choice(['Ислам', 'Христианство', 'Иудаизм', 'Атеизм'], p=[0.95, 0.01, 0.01, 0.03])
        elif self.nation == 'Немец' or self.nation == 'Немка':
            return np.random.choice(['Ислам', 'Христианство', 'Иудаизм', 'Атеизм'], p=[0.1, 0.6, 0, 0.3])
        elif self.nation == 'Еврей' or self.nation == 'Еврейка':
            return np.random.choice(['Ислам', 'Христианство', 'Иудаизм', 'Атеизм'], p=[0, 0.02, 0.9, 0.08])

    def __init__(self, language_model, general_questionnaire, list_of_questionnaires):
        self.model = language_model
        self.general_questionnaire = general_questionnaire
        self.list_of_questionnaires = list_of_questionnaires
        self.gender = np.random.choice(['Женский', 'Мужской'])
        self.name = generate_name('female' if self.gender == 'Женский' else 'male')
        self.education = np.random.choice(
            ['Cреднее', 'Cреднее специальное', 'Неоконченное высшее, Бакалавр (еще учусь)',
             'Высшее, Бакалавр (уже закончил)', 'Научная степень'],
            p=[0.2, 0.2, 0.4, 0.17, 0.03])
        self.age = self.fill_age()
        self.course = self.fill_course()
        self.nation = self.fill_nation()
        self.job_exp = self.fill_job_exp()
        self.family_composition = np.random.choice(['Полная', 'Неполная'], p=[0.6, 0.4])
        self.faith = self.fill_faith()
        self.siblings_num = np.random.choice([0, 1, 2, 3, 4], p=[0.3, 0.4, 0.2, 0.09, 0.01])
        self.probable_general_questions = ['Пол', 'Возраст', 'Образование', 'Специальность, факультет', 'Курс',
                                           'Национальность', 'Опыт работы', 'Состав семьи', 'Вероисповедание',
                                           'Количество братьев и сестер']

    def fill_general_questions(self):
        self.general_questionnaire.questions = [cut_number_of_question_order(question) for question in
                                                self.general_questionnaire.questions]

    def fill_methodic(self, questionnaire, threshold=0.6):
        questionnaire.questions = [cut_number_of_question_order(question) for question in questionnaire.questions]
        perm = np.random.permutation(len(questionnaire.questions))  # чекаем тут есчо
        inv_perm = invert_permutation(perm)  # чекаем тут есчо
        questionnaire.questions = list(np.asarray(questionnaire.questions)[perm])  # чекаем тут есчо
        questionnaire.answers = list(np.asarray(questionnaire.answers)[perm])  # чекаем тут есчо
        filler = MethodicFiller(questionnaire.answer_options, questionnaire.questions, self.model)
        filler.put_answers(threshold=threshold)
        questionnaire.answers = filler.ready_answers
        questionnaire.questions = list(np.asarray(questionnaire.questions)[inv_perm])  # чекаем тут есчо
        questionnaire.answers = list(np.asarray(questionnaire.answers)[inv_perm])  # чекаем тут есчо
        return questionnaire

    def fill_survey(self):
        self.fill_general_questions()
        for questionnaire in self.list_of_questionnaires:
            questionnaire = self.fill_methodic(questionnaire)


class SampleGenerator(object):
    def __init__(self, language_model, num_of_respondents, general_questionnaire, list_of_questionnaires):
        self.model = language_model
        self.num_of_respondents = num_of_respondents
        self.general_questionnaire = general_questionnaire
        self.list_of_questionnaires = list_of_questionnaires
        self.respondents = []

    def __call__(self):
        for it in range(self.num_of_respondents):
            respondent = RespondentGenerator(self.model, self.general_questionnaire, self.list_of_questionnaires)
            respondent.fill_survey()
            self.respondents.append(respondent)
            # gFormParser.fill_scale_form(url, respondent)  # вот здесь она должна принимать респондента.
