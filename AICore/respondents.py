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
        pass

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
        self.age = None
        self.course = None

    def fill_general_questions(self):
        pass

    def fill_methodic(self, questionnaire, threshold=0.6):
        questionnaire.questions = [cut_number_of_question_order(question) for question in questionnaire.questions]
        # тут надо еще перемешать вопросы и обратно их поставить в порядке
        filler = MethodicFiller(questionnaire.answer_options, questionnaire.questions, self.model)
        filler.put_answers(threshold=threshold)
        questionnaire.answers = filler.ready_answers
        return questionnaire

    def fill_survey(self):
        self.fill_general_questions()
        for questionnaire in self.list_of_questionnaires:
            questionnaire = self.fill_methodic(questionnaire)


class GeneratorTolpi(object):
    def __init__(self, language_model, razmer_tolpi, general_questionnaire, list_of_questionnaires):
        self.model = language_model
        self.razmer_tolpi = razmer_tolpi
        self.general_questionnaire = general_questionnaire
        self.list_of_questionnaires = list_of_questionnaires

    def tolpu_v_boy(self, url):
        for it in range(self.razmer_tolpi):
            respondent = RespondentGenerator(self.model, self.general_questionnaire, self.list_of_questionnaires)
            respondent.fill_survey()
            gFormParser.fill_scale_form(url, respondent)  # вот здесь она должна принимать респондента.
