import numpy as np
from mimesis import Person
from mimesis.locales import Locale
from mimesis.enums import Gender

import AICore.model
from AICore.answer_fill import MethodicFiller
from sklearn.metrics.pairwise import cosine_similarity


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


def clean_question_string(question):
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


class Respondent(object):
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
            raise ValueError(f"Wrong education value: {self.education}")

    def fill_course(self):
        if self.education == 'Научная степень':
            return np.random.randint(1, 3)
        else:
            return np.random.randint(1, 5)

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
            return np.random.choice(['Ислам', 'Христианство', 'Иудаизм', 'Атеизм'], p=[0.9, 0.04, 0.01, 0.05])
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

    def __init__(self, general_questionnaire, list_of_questionnaires):
        self.model = AICore.model.current_model
        self.general_questionnaire = general_questionnaire
        self.list_of_questionnaires = list_of_questionnaires
        self.gender = np.random.choice(['Женский', 'Мужской'])
        self.name = generate_name('female' if self.gender == 'Женский' else 'male')
        self.education = np.random.choice(
            ['Среднее', 'Среднее специальное', 'Неоконченное высшее, Бакалавр (еще учусь)',
             'Высшее, Бакалавр (уже закончил)', 'Научная степень'],
            p=[0.2, 0.2, 0.4, 0.17, 0.03])
        self.age = self.fill_age()
        self.course = self.fill_course()
        self.nation = self.fill_nation()
        self.job_exp = self.fill_job_exp()
        self.family_composition = np.random.choice(['Полная', 'Неполная'], p=[0.6, 0.4])
        self.faith = self.fill_faith()
        self.siblings_num = np.random.choice([0, 1, 2, 3, 4], p=[0.3, 0.4, 0.2, 0.09, 0.01])
        self.speciality = None
        self.faculty = None
        self.probable_general_questions = ['Пол', 'Возраст', 'Образование', 'Специальность, факультет', 'Курс',
                                           'Национальность', 'Опыт работы', 'Состав семьи', 'Вероисповедание',
                                           'Количество братьев и сестер']

    def find_variant_in_answers(self, variant, answer_options):
        encoded_variant = self.model(str(variant))
        encoded_answer_options = self.model(answer_options)
        similarities = cosine_similarity(encoded_variant.cpu(), encoded_answer_options.cpu())
        argmax = np.argmax(similarities[0])
        return answer_options[argmax]

    def fill_general_question(self, probable_variant, question):
        if probable_variant == 'Пол':
            if question.answer_options is None:
                return self.gender
            else:
                return self.find_variant_in_answers(self.gender, question.answer_options)
        elif probable_variant == 'Возраст':
            if question.answer_options is None:
                return self.age
            else:
                return self.find_variant_in_answers(self.age, question.answer_options)
        elif probable_variant == 'Образование':
            if question.answer_options is None:
                return self.education
            else:
                return self.find_variant_in_answers(self.education, question.answer_options)
        elif probable_variant == 'Специальность':
            if question.answer_options is None:
                return self.speciality
            else:
                return self.find_variant_in_answers(self.speciality, question.answer_options)
        elif probable_variant == 'Факультет':
            if question.answer_options is None:
                return self.faculty
            else:
                return self.find_variant_in_answers(self.faculty, question.answer_options)
        elif probable_variant == 'Курс':
            if question.answer_options is None:
                return self.course
            else:
                return self.find_variant_in_answers(self.course, question.answer_options)
        elif probable_variant == 'Национальность':
            if question.answer_options is None:
                return self.nation
            else:
                return self.find_variant_in_answers(self.nation, question.answer_options)
        elif probable_variant == 'Опыт работы':
            if question.answer_options is None:
                return self.job_exp
            else:
                return self.find_variant_in_answers(self.job_exp, question.answer_options)
        elif probable_variant == 'Состав семьи':
            if question.answer_options is None:
                return self.family_composition
            else:
                return self.find_variant_in_answers(self.family_composition, question.answer_options)
        elif probable_variant == 'Вероисповедание':
            if question.answer_options is None:
                return self.faith
            else:
                return self.find_variant_in_answers(self.faith, question.answer_options)
        elif probable_variant == 'Количество братьев и сестер':
            if question.answer_options is None:
                return self.siblings_num
            else:
                return self.find_variant_in_answers(self.siblings_num, question.answer_options)

    def fill_general_questions(self):
        encoded_general_questions = self.model(self.general_questionnaire.get_all_clean_question_strings())
        encoded_probable_questions = self.model(self.probable_general_questions)
        similarities = cosine_similarity(encoded_general_questions.cpu(), encoded_probable_questions.cpu())
        for i in range(len(similarities)):
            argmax = np.argmax(similarities[i])
            probable_variant = self.probable_general_questions[argmax]
            self.general_questionnaire.answers[i] = self.fill_general_question(probable_variant,
                                                                               self.general_questionnaire.questions[i])

    def fill_methodic(self, questionnaire, threshold=0.6):
        # questionnaire.questions = [clean_question_string(question) for question in questionnaire.questions]
        cleaned_questions = questionnaire.get_all_clean_question_strings()
        #perm = np.random.permutation(len(cleaned_questions))  # чекаем тут есчо
        #inv_perm = invert_permutation(perm)  # чекаем тут есчо
        #cleaned_questions = list(np.asarray(cleaned_questions)[perm])  # чекаем тут есчо
        #questionnaire.answers = list(np.asarray(questionnaire.answers)[perm])  # чекаем тут есчо
        filler = MethodicFiller(questionnaire.questions[0].answer_options, cleaned_questions)
        filler.put_answers(threshold=threshold)
        print('filler ready answers:', filler.ready_answers)
        questionnaire.answers = filler.ready_answers
        # questionnaire.questions = list(np.asarray(questionnaire.questions)[inv_perm])  # чекаем тут есчо
        #questionnaire.answers = list(np.asarray(questionnaire.answers)[inv_perm])  # чекаем тут есчо
        return questionnaire

    def fill_survey(self, fill_general):
        if fill_general:
            self.fill_general_questions()
        #for i in range(len(self.list_of_questionnaires)):
        #    self.list_of_questionnaires[i] = self.fill_methodic(self.list_of_questionnaires[i])
        for questionnaire in self.list_of_questionnaires:
            questionnaire = self.fill_methodic(questionnaire)
            #print("in fill_survey", questionnaire.answers)


class SampleGenerator2(object):
    def __init__(self):
        self.model = AICore.model.current_model

    def get_sample(self, num_of_respondents, questionnaire_holder):
        respondents = []
        for it in range(num_of_respondents):
            respondent = Respondent(None, questionnaire_holder.list_of_questionnaires)
            respondent.fill_survey(False)
            respondents.append(respondent)
        return respondents


class SampleGenerator(object):
    def __init__(self):
        self.model = AICore.model.current_model

    def get_sample(self, num_of_respondents, holder, general_questionnaire, list_of_questionnaires):
        holders = []
        for it in range(num_of_respondents):
            respondent = Respondent(general_questionnaire, list_of_questionnaires)
            if general_questionnaire is None:
                list_of_questionnaires = holder.questionnaires
                respondent.fill_survey(False)
                holder.questionnaires = respondent.list_of_questionnaires
                print(respondent.list_of_questionnaires[0].answers)
            else:
                respondent.fill_survey(True)
                holder.questionnaires = respondent.general_questionnaire.extend(respondent.list_of_questionnaires)
            holders.append(holder)
        return holders

    def __call__(self, num_of_respondents, holder, have_general):
        if have_general:
            return self.get_sample(num_of_respondents, holder, holder.questionnaires[0], holder.questionnaires[1:])
        else:
            return self.get_sample(num_of_respondents, holder, None, holder.questionnaires)
