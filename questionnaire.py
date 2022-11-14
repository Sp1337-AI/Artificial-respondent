class QuestionnaireBase():
    """Questionnaire with all questions and types of answers"""
    questions = []
    other_questions = []
    answers = []
    name = ""

    def __init__(self):
        """Constructor"""

    def add_main_question(self, question):
        self.questions.append(question)

    def add_supportive_question(self, question):
        self.other_questions.append(question)


class QuestionnaireOptionsInterval(QuestionnaireBase):
    """Questionnaire with option """

    def __init__(self, high, low):
        """Constructor"""
        # self.questions = super.questions
        self.high = high
        self.low = low
        self.answer_options = []

    def add_answer_option(self, option_name):
        self.answer_options.append(option_name)

    def __str__(self):
        s = ""
        for question in self.questions:
            s += question + "\n"
        s += "===\n"
        for question in self.other_questions:
            s += question + "\n"
        s += "Answer options: \n"
        for answer_option in self.answer_options:
            s += answer_option + ", "
        return s
