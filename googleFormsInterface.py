import gforms.elements
from gforms import Form
from gforms.elements import Short, Value, Radio, Paragraph, Scale

import questionnaire as q


def parse_multipage_form(url) -> q.QuestionnaireHolder:
    form = Form()
    form.load(url)
    multipage_questionnaire = q.QuestionnaireHolder()
    for page in form.pages:
        questionnaire = parse_form(page)
        multipage_questionnaire.add_methodology(questionnaire)
    return multipage_questionnaire


def parse_form(page) -> q.QuestionnaireBase:
    questionnaire = q.QuestionnaireBase()
    for element in page.elements:
        new_question = q.Question()
        if element.description is not None:
            new_question.description_string = element.description
        new_question.question_string = element.name
        new_question.is_required = element.required
        answer_options = []
        if hasattr(element, 'options'):
            for option in element.options:
                if option.value is not None:
                    answer_options.append(option.value)
        new_question.answer_options = answer_options
        questionnaire.add_main_question(new_question)
    return questionnaire


def fill_multipage_form(url, questionnaire_holder: q.QuestionnaireHolder):
    form = Form()
    form.load(url)

    def form_filler(element, page_index, element_index):
        return questionnaire_holder.questionnaires[page_index].answers[element_index]

    form.fill(form_filler)
    form.submit()
