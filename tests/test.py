from dataInterfaces import txtFileInterface
from AICore import respondents


def calculate_scales(respondents_array):
    results = []
    for resp in respondents_array:
        #print(resp.questionnaires[0].answers)
        SD = 0
        ST = 0
        F = 0
        V = 0
        for i in range(1, len(resp.questionnaires[0].answers) + 1):
            if i == 1:
                V += resp.questionnaires[0].answers[i - 1]
            elif i == 2:
                ST += 7 - resp.questionnaires[0].answers[i - 1]
            elif i == 3:
                SD += resp.questionnaires[0].answers[i - 1]
            elif i == 4:
                ST += resp.questionnaires[0].answers[i - 1]
            elif i == 5:
                SD += resp.questionnaires[0].answers[i - 1]
            elif i == 6:
                V += resp.questionnaires[0].answers[i - 1]
            elif i == 7:
                V += resp.questionnaires[0].answers[i - 1]
            elif i == 8:
                V += resp.questionnaires[0].answers[i - 1]
            elif i == 9:
                F += resp.questionnaires[0].answers[i - 1]
            elif i == 10:
                F += resp.questionnaires[0].answers[i - 1]
            elif i == 11:
                ST += resp.questionnaires[0].answers[i - 1]
            elif i == 12:
                ST += resp.questionnaires[0].answers[i - 1]
            elif i == 13:
                ST += resp.questionnaires[0].answers[i - 1]
            elif i == 14:
                ST += resp.questionnaires[0].answers[i - 1]
            elif i == 15:
                F += 7 - resp.questionnaires[0].answers[i - 1]
            elif i == 16:
                V += resp.questionnaires[0].answers[i - 1]
            elif i == 17:
                F += resp.questionnaires[0].answers[i - 1]
            elif i == 18:
                F += resp.questionnaires[0].answers[i - 1]
            elif i == 19:
                SD += resp.questionnaires[0].answers[i - 1]
            elif i == 20:
                V += resp.questionnaires[0].answers[i - 1]
            elif i == 21:
                ST += 7 - resp.questionnaires[0].answers[i - 1]
            elif i == 22:
                V += resp.questionnaires[0].answers[i - 1]
            elif i == 23:
                F += resp.questionnaires[0].answers[i - 1]
            elif i == 24:
                F += resp.questionnaires[0].answers[i - 1]
            elif i == 25:
                V += resp.questionnaires[0].answers[i - 1]
            elif i == 26:
                F += 7 - resp.questionnaires[0].answers[i - 1]
            elif i == 27:
                ST += resp.questionnaires[0].answers[i - 1]
            elif i == 28:
                F += resp.questionnaires[0].answers[i - 1]
            elif i == 29:
                V += resp.questionnaires[0].answers[i - 1]
            elif i == 30:
                V += resp.questionnaires[0].answers[i - 1]
            elif i == 31:
                F += resp.questionnaires[0].answers[i - 1]
            elif i == 32:
                SD += resp.questionnaires[0].answers[i - 1]
            elif i == 33:
                ST += resp.questionnaires[0].answers[i - 1]
            elif i == 34:
                ST += resp.questionnaires[0].answers[i - 1]
            elif i == 35:
                ST += resp.questionnaires[0].answers[i - 1]
            elif i == 36:
                ST += 7 - resp.questionnaires[0].answers[i - 1]
            elif i == 37:
                V += resp.questionnaires[0].answers[i - 1]
            elif i == 38:
                V += resp.questionnaires[0].answers[i - 1]
            elif i == 39:
                V += resp.questionnaires[0].answers[i - 1]
            elif i == 40:
                SD += resp.questionnaires[0].answers[i - 1]
            elif i == 41:
                ST += resp.questionnaires[0].answers[i - 1]
            elif i == 42:
                SD += resp.questionnaires[0].answers[i - 1]
            elif i == 43:
                SD += resp.questionnaires[0].answers[i - 1]
            elif i == 44:
                SD += resp.questionnaires[0].answers[i - 1]
            elif i == 45:
                ST += resp.questionnaires[0].answers[i - 1]
            elif i == 46:
                F += resp.questionnaires[0].answers[i - 1]
        P = SD + ST
        E = F + V
        G = P + E
        results.append({'name': resp.name, 'SD': SD, 'ST': ST, 'F': F, 'V': V, 'P': P, 'E': E, 'G': G})
    return results


holder = txtFileInterface.load_questions_from_txt("../dataInterfaces/Экзистенциализм.txt")
#print(holder)
sg = respondents.SampleGenerator()
respondent_holders = sg(10, holder, have_general=False)
results = calculate_scales(respondent_holders)
print(results)
