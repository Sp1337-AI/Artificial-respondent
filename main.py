import googleFormsInterface as gFormParser
import questionnaire as q
from mimesis import Person
from mimesis.locales import Locale
from mimesis.enums import Gender
import numpy as np
import random
from model import LanguageModel
from answer_fill import MethodicFiller
url = "https://docs.google.com/forms/d/e/1FAIpQLSdSs4dNhMFKDAp3xEu-VgS8yJ9UbSGf_K7F1Bk8VA3l61xTlw/viewform"

questionnaire = gFormParser.parse_scale_form(url)
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


model = LanguageModel()
for i in range(1):
    print('respondent number:', i+1)
    questionnaire.name = generate_name(np.random.choice(['female', 'male'], p=[0.5, 0.5]))
    print('questionaire.name =', questionnaire.name)
    questionnaire.questions = [cut_number_of_question_order(question) for question in questionnaire.questions]
    filler = MethodicFiller(questionnaire.answer_options, questionnaire.questions, model)
    filler.put_answers(threshold=0.6)
    questionnaire.answers = filler.ready_answers
    print("answers =", questionnaire.answers)
    print()
    #gFormParser.fill_scale_form(url, questionnaire)

