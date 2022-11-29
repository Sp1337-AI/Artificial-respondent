from entities import questionnaire as q


def load_questions_from_txt(path, encoding="utf8") -> q.QuestionnaireHolder:
    with open(path, 'r', encoding=encoding) as f:
        lines = f.read().splitlines()
    questionnaire = q.QuestionnaireBase()
    for line in lines:
        questionnaire.add_main_question(line)
    holder = q.QuestionnaireHolder()
    holder.add_methodology(questionnaire)
    return holder
