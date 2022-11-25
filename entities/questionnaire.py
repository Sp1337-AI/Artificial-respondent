class Question(object):
    """One block containing a question and answer options."""

    def __init__(self, question_string="", answer_options=[], description_string="", is_required=True):
        self.question_string = question_string
        self.answer_options = answer_options
        self.description_string = description_string
        self.is_required = is_required

    def __str__(self):
        s = ""
        s += "===\n" + self.question_string
        if self.is_required:
            s += " *"
        s += self.description_string + '\n'
        s += "---" + '\n'
        for option in self.answer_options:
            s += option + '\n'
        s += '\n'
        return s


class QuestionnaireHolder(object):
    """One instance of the questionnaire. 
    It can consist of several pages. Each page is represented by a questionnaire - methodology."""

    def __init__(self):
        self.name = ""
        self.questionnaires = []

    def add_methodology(self, questionnaire):
        self.questionnaires.append(questionnaire)

    def __str__(self):
        s = ""
        for questionnaire in self.questionnaires:
            s += "Questionnaire:\n"
            s += str(questionnaire)
        return s


class QuestionnaireBase(object):
    """Questionnaire with all questions and types of answers"""

    def __init__(self):
        """Constructor"""
        self.questions = []
        self.other_questions = []
        self.answers = []

    def add_main_question(self, question):
        self.questions.append(question)

    def add_supportive_question(self, question):
        self.other_questions.append(question)

    def add_answer(self, answer):
        self.answers.append(answer)

    def __str__(self):
        s = ""
        for question in self.questions:
            s += str(question)
        return s
