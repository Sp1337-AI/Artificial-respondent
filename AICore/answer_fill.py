import numpy as np
from sklearn.metrics.pairwise import cosine_similarity



class MethodicFiller(object):

    def __init__(self, list_of_variants, questions, cur_model):
        self.model = cur_model
        self.list_of_variants = list_of_variants
        self.num_of_variants = len(list_of_variants)
        self.questions = questions
        self.questions_length = len(questions)
        self.ready_answers = [None] * self.questions_length

    def put_first(self):
        self.num_of_variants = len(self.list_of_variants)
        self.list_of_variants = np.asarray(self.list_of_variants)
        ans = None
        if self.num_of_variants == 2:
            ans = np.random.choice(self.list_of_variants, p=[0.5, 0.5])
        elif self.num_of_variants == 3:
            ans = np.random.choice(self.list_of_variants, p=[0.45, 0.1, 0.45])
        elif self.num_of_variants == 4:
            ans = np.random.choice(self.list_of_variants, p=[0.2, 0.3, 0.3, 0.2])
        elif self.num_of_variants == 5:
            ans = np.random.choice(self.list_of_variants, p=[0.2, 0.28, 0.04, 0.28, 0.2])
        elif self.num_of_variants == 6:
            ans = np.random.choice(self.list_of_variants, p=[0.14, 0.16, 0.2, 0.2, 0.16, 0.14])
        elif self.num_of_variants == 7:
            ans = np.random.choice(self.list_of_variants, p=[0.14, 0.16, 0.19, 0.02, 0.19, 0.16, 0.14])
        return ans

    def fill_prob_list(self, previous_index, cur_similarity):
        prob = np.zeros(self.num_of_variants)

        if cur_similarity >= 0.93:
            prob[previous_index] = 1.0
            return prob

        if self.num_of_variants == 2:
            prob[previous_index], prob[previous_index - 1] = 0.9, 0.1
            return prob

        if self.num_of_variants == 3:
            if previous_index == 2:
                prob[1], prob[2] = 0.2, 0.8
            elif previous_index == 0:
                prob[0], prob[1] = 0.8, 0.2
            else:
                prob[0], prob[1], prob[2] = 0.15, 0.7, 0.15
            return prob

        if self.num_of_variants == 4:
            if previous_index == 0:
                prob[0], prob[1] = 0.7, 0.3
            elif previous_index == 1:
                prob[0], prob[1], prob[2] = 0.3, 0.6, 0.1
            elif previous_index == 2:
                prob[1], prob[2], prob[3] = 0.1, 0.6, 0.3
            else:
                prob[2], prob[3] = 0.3, 0.7
            return prob

        if self.num_of_variants == 5:
            if previous_index == 0:
                prob[0], prob[1] = 0.7, 0.3
            elif previous_index == 1:
                prob[0], prob[1], prob[2] = 0.25, 0.7, 0.05
            elif previous_index == 2:
                prob[1], prob[2], prob[3] = 0.15, 0.7, 0.15
            elif previous_index == 3:
                prob[2], prob[3], prob[4] = 0.05, 0.7, 0.25
            elif previous_index == 4:
                prob[3], prob[4] = 0.3, 0.7
            return prob

        if self.num_of_variants == 6:
            if previous_index == 0:
                prob[0], prob[1], prob[2] = 0.6, 0.3, 0.1
            elif previous_index == 1:
                prob[0], prob[1], prob[2] = 0.2, 0.6, 0.2
            elif previous_index == 2:
                prob[0], prob[1], prob[2], prob[3] = 0.1, 0.25, 0.6, 0.05
            elif previous_index == 3:
                prob[2], prob[3], prob[4], prob[5] = 0.05, 0.6, 0.25, 0.1
            elif previous_index == 4:
                prob[3], prob[4], prob[5] = 0.2, 0.6, 0.2
            elif previous_index == 5:
                prob[3], prob[4], prob[5] = 0.1, 0.3, 0.6
            return prob

        if self.num_of_variants == 7:
            if previous_index == 0:
                prob[0], prob[1], prob[2] = 0.6, 0.3, 0.1
            elif previous_index == 1:
                prob[0], prob[1], prob[2] = 0.2, 0.6, 0.2
            elif previous_index == 2:
                prob[0], prob[1], prob[2], prob[3] = 0.12, 0.25, 0.6, 0.03
            elif previous_index == 3:
                prob[1], prob[2], prob[3], prob[4], prob[5] = 0.03, 0.12, 0.7, 0.12, 0.03
            elif previous_index == 4:
                prob[3], prob[4], prob[5], prob[6] = 0.03, 0.6, 0.25, 0.12
            elif previous_index == 5:
                prob[4], prob[5], prob[6] = 0.2, 0.6, 0.2
            elif previous_index == 6:
                prob[4], prob[5], prob[6] = 0.1, 0.3, 0.6
            return prob

    def put_according_prev(self, previous, cur_similarity):
        previous_index = list(self.list_of_variants).index(previous)
        self.num_of_variants = len(self.list_of_variants)
        assert previous_index < self.num_of_variants, "Index must be in range of possible answers"
        self.list_of_variants = np.asarray(self.list_of_variants)
        prob = self.fill_prob_list(previous_index, cur_similarity)
        ans = np.random.choice(self.list_of_variants, p=prob)
        return ans

    def put_answers(self, threshold):
        encoded_questions = self.model(self.questions)
        print('min value for questions', encoded_questions.min())
        similarities = cosine_similarity(encoded_questions.cpu(), encoded_questions.cpu())
        for i in range(self.questions_length):
            #print(f'similarities[{i}] =', len(similarities[i][similarities[i] > threshold]))
            print('min sim:', similarities[i].min())
            if self.ready_answers[i] is None:
                self.ready_answers[i] = self.put_first()
                for j, similarity in enumerate(similarities[i]):
                    if similarity > threshold and self.ready_answers[j] is not None and i != j:
                        self.ready_answers[j] = self.put_according_prev(self.ready_answers[i], similarity)

list_of_variants = ['Точно нет', 'Частично нет', 'Не знаю', 'Частично да', 'Точно да']

questions = [
    'Мне легче что-либо сделать самому, чем объяснить другому.',
    'Мне интересно составлять компьютерные программы.',
    'Я люблю читать книги.',
    'Мне нравится живопись, скульптура, архитектура.',
    'Даже в отлаженном деле я стараюсь что-то улучшить.',
    'Я лучше понимаю, если мне объясняют на предметах или рисунках.',
    'Я люблю играть в шахматы.',
    'Я легко излагаю свои мысли как в устной, так и в письменной форме.',
    'Когда я читаю книгу, я четко вижу ее героев и описываемые события.',
    'Я предпочитаю самостоятельно планировать свою работу.',
    'Мне нравится все делать своими руками.',
    'В детстве я создавал (а) свой шифр для переписки с друзьями.',
    'Я придаю большое значение сказанному слову.',
    'Знакомые мелодии вызывают у меня в голове определенные картины.',
    'Разнообразные увлечения делают жизнь человека богаче и ярче.',
    'При решении задачи мне легче идти методом проб и ошибок.',
    'Мне интересно разбираться в природе физических явлений.',
    'Мне интересна работа ведущего теле-радиопрограмм, журналиста.',
    'Мне легко представить предмет или животное, которых нет в природе.',
    'Мне больше нравится процесс деятельности, чем сам результат.',
    'Мне нравилось в детстве собирать конструктор из деталей, лего.',
    'Я предпочитаю точные науки (математику, физику).',
    'Меня восхищает точность и глубина некоторых стихов.',
    'Знакомый запах вызывает в моей памяти прошлые события.',
    'Я не хотел (а) бы подчинять свою жизнь определенной системе.',
    'Когда я слышу музыку, мне хочется танцевать.',
    'Я понимаю красоту математических формул.',
    'Мне легко говорить перед любой аудиторией.',
    'Я люблю посещать выставки, спектакли, концерты.',
    'Я сомневаюсь даже в том, что для других очевидно.',
    'Я люблю заниматься рукоделием, что-то мастерить.',
    'Мне интересно было бы расшифровать древние тайнописи.',
    'Я легко усваиваю грамматические конструкции языка.',
    'Я согласен с Ф.М. Достоевским, что красота спасет мир.',
    'Не люблю ходить одним и тем же путем.',
    'Истинно только то, что можно потрогать руками.',
    'Я легко запоминаю формулы, символы, условные обозначения.',
    'Друзья любят слушать, когда я им что-то рассказываю.',
    'Я легко могу представить в образах содержание рассказа или фильма.',
    'Я не могу успокоиться, пока не доведу свою работу до совершенства.',
]


# print('ready answers after:', filler.ready_answers)
