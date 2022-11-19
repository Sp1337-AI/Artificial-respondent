import googleFormsInterface as gFormParser
import questionnaire as q
from mimesis import Person
from mimesis.locales import Locale
from mimesis.enums import Gender
import numpy as np
import random
from model import LanguageModel
from answer_fill import MethodicFiller

url = "https://docs.google.com/forms/d/e/1FAIpQLSfQ_-joZ_Cj2_Igm0hgYaeKleHzNH89ff5ofH0Xoq6UoTzOyQ/viewform"

questionnaire = gFormParser.parse_multipaged_form(url)
print(questionnaire)


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

    def __init__(self, language_model, general_questionnaire, list_of_questionnaires):
        self.model = language_model
        self.general_questionnaire = general_questionnaire
        self.list_of_questionnaires = list_of_questionnaires
        self.name = generate_name(np.random.choice(['female', 'male'], p=[0.5, 0.5]))

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

    def tolpu_v_boy(self):
        for it in range(self.razmer_tolpi):
            respondent = RespondentGenerator(self.model, self.general_questionnaire, self.list_of_questionnaires)
            respondent.fill_survey()
            gFormParser.fill_scale_form(url, respondent) #вот здесь она должна принимать респондента.

'''

questions = [
    'Когда я над чем-нибудь работаю, я не могу расслабиться, пока не доведу это до совершенства',

    'Я никогда не задаюсь целью добиться совершенства в том, над чем работаю',
    'Мне не особенно нужно быть совершенным',
    'Мне не обязательно быть лучшим во всем, чем я занимаюсь',
    'Я не ставлю перед собой больших, труднодостижимых целей',

    'Одна из моих целей - быть совершенным во всем, что я делаю',
    'Я стремлюсь быть лучшим во всем, что я делаю',
    'Мне крайне неприятно обнаруживать ошибки в своей работе',
    'Я всегда должен работать в полную силу',

    'Я способен с лёгкостью описать свои чувства',
    'Легко могу развеселить самую скучную компанию',
    'Желание побыть одному зависит у меня от обстоятельств и настроения',
    'Мне нравятся неожиданности',
]

from sklearn.metrics.pairwise import cosine_similarity

model = LanguageModel()

encoded_questions = model(questions)
similarities = cosine_similarity(encoded_questions.cpu(), encoded_questions.cpu())
for i in range(len(similarities)):
    print(similarities[i])

'''
