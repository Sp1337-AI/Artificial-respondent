class QuestionnaireHolder(object):
    """One instance of the questionnaire. 
    It can consist of several pages. Each page is represented by a questionnaire - methodology."""

    def __init__(self):
        self.name = ""
        self.questionnaires = []


    def add_methodic(self, questionnaire):
        self.questionnaires.append(questionnaire)

    def __str__(self):
        s = ""
        for questionnaire in self.questionnaires:
            s += str(questionnaire)
        return s


class QuestionnaireBase(object):
    """Questionnaire with all questions and types of answers"""

    # questions = []
    # other_questions = []
    # answers = []

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


class QuestionnaireOptionsInterval(QuestionnaireBase):
    """Questionnaire with option """

    def __init__(self, low, high):
        """Constructor"""
        super().__init__()
        self.answer_options = []
        self.low = low
        self.high = high

    def add_answer_option(self, option_name):
        self.answer_options.append(option_name)

    def set_low(self, low):
        self.low = low

    def set_high(self, high):
        self.high = high

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


class QuestionnaireGeneralQuestions(QuestionnaireBase):
    """Questionnaire for general questions such as name, sex, age, etc.
    Now holding all questions
     """

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.answer_options = []

    def __str__(self):
        s = ""
        for question in self.questions:
            s += question + "\n"
        s += "===\n"
        s += "Answers: \n"
        for answer in self.answers:
            for answer_option in answer:
                s += answer_option + ", "
            s += "\n"
        return s
