import googleFormsInterface as gFormParser
import questionnaire as q
from model import LanguageModel

url = "https://docs.google.com/forms/d/e/1FAIpQLSfqoOW5xa4qBb5jMczGmoyBlkwD4Qg70ti-Yo2xrcXNolvZFQ/viewform"

questionnaire = gFormParser.parse_multipaged_form(url)
print(questionnaire)

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
