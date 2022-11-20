from gforms import Form
from gforms.elements import Short, Value, Radio, Paragraph, Scale

import questionnaire as q


def parse_multipaged_form(url) -> q.QuestionnaireHolder:
    form = Form()
    form.load(url)
    multipaged_questionnaire = q.QuestionnaireHolder()
    # for page in form.pages:
    # parsed_methodic = parse_scale_form(page)
    # multipaged_questionnaire.add_methodic(parsed_methodic)
    for i in range(len(form.pages)):
        if i == 0:
            parsed_methodic = parse_general_questions_form(form.pages[i])
            multipaged_questionnaire.add_methodic(parsed_methodic)
        if i == 1:
            parsed_methodic = parse_scale_form(form.pages[i])
            multipaged_questionnaire.add_methodic(parsed_methodic)
    return multipaged_questionnaire


def parse_scale_form(page) -> q.QuestionnaireOptionsInterval:
    questionnaire = None
    for element in page.elements:
        if isinstance(element, Scale):
            questionnaire = q.QuestionnaireOptionsInterval(low=element.options[0].value,
                                                           high=element.options[-1].value)
            for option in element.options:
                questionnaire.add_answer_option(option.value)
    for element in page.elements:
        if isinstance(element, Scale):
            if element.description is not None:
                questionnaire.add_main_question(element.name + ";" + element.description)
            else:
                questionnaire.add_main_question(element.name + ";")
        else:
            if element.description is not None:
                questionnaire.add_supportive_question(element.name + ";" + element.description)
            else:
                questionnaire.add_supportive_question(element.name + ";")
    return questionnaire


def parse_general_questions_form(page) -> q.QuestionnaireGeneralQuestions:
    questionnaire = q.QuestionnaireGeneralQuestions()
    for element in page.elements:
        if element.description is not None:
            questionnaire.add_main_question(element.name + ";" + element.description)
        else:
            questionnaire.add_main_question(element.name + ";")
            answer_options = []
        if hasattr(element, 'options'):
            for option in element.options:
                if option.value is not None:
                    answer_options.append(option.value)
            questionnaire.add_answer(answer_options)
        else:
            questionnaire.add_answer([""])  # if we have not answer options it returns empty string
    return questionnaire


def fill_scale_form(url, questionnaire: q.QuestionnaireOptionsInterval):
    form = Form()
    form.load(url)

    def form_filler(element, page_index, element_index):
        if isinstance(element, Paragraph):
            return questionnaire.name
        else:
            return questionnaire.answers[element_index - 1]

    form.fill(form_filler)
    form.submit()
