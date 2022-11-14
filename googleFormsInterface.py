from gforms import Form
from gforms.elements import Short, Value, Radio, Paragraph, Scale

import questionnaire as q


def parse_scale_form(url) -> q.QuestionnaireOptionsInterval:
    form = Form()
    form.load(url)
    questionnaire = None
    for page in form.pages:
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


def fill_scale_form(url, questionnaire: q.QuestionnaireOptionsInterval):
    form = Form()
    form.load(url)

    def form_filler(element, page_index, element_index):
        if isinstance(element, Paragraph):
            return questionnaire.name
        else:
            return questionnaire.answers[element_index-1]

    form.fill(form_filler)
    form.submit()
