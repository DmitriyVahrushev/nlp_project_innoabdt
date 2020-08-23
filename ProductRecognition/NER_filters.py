import datetime
import re

def NER_filter_percents(tokens):
    #textn = filter_text(text)
    lsst = tokens # было textn
    ind_year = [i for i, s in enumerate(lsst) if s.isdigit()]
    # извлекаем процент вклада, если он есть
    percents = []
    for i in ind_year:
        try:
            if lsst[i + 1] == 'процент' or lsst[i + 1] == '%':
                percents = [lsst[i]]
                break
        except IndexError:
            continue
    return percents


def NER_filter_time_periods(text):
    #textn = filter_text(text)
    lsst = text # было textn

    #поиск сроков кредитов
    ind_year = [i for i,s in enumerate(lsst) if s.isdigit()]
    yearn=[]
    for i in ind_year:
        try:
            if lsst[i+1]=='год':#проверка случая на 15 лет
                if len(lsst[i])<=2:#исключаем случай до 2015 года
                    yearn = int(lsst[i])*12
                    break
            elif lsst[i+1]=='месяц':#проверка случая на 180 месяцев
                if len(lsst[i])<=3:#исключаем случай до 2015 года
                    yearn = int(lsst[i])
                    break
        except IndexError:
            continue
    return yearn


def NER_monetary_amounts(text,tokens, moneyextractor):

    #             не распознает:
    #              - кредит на 5000
    #             распознает:
    #              - кредит на 5000 рублей
    #              - кредит на сумму 5000
    #              - сроком на 15 лет (3 года)
    #              - сроком на 180 месяцев

    #поиск сумм кредитов их валюты - "кредит на сумму 5000 рублей"
    matches = moneyextractor(text)
    sum1=[]
    for match in matches:
        sum1.append([match.fact.as_json['integer'],match.fact.as_json['currency']])
    #если не нашли валюту - "кредит на сумму 5000"
    if not sum1:
        ind_year = [i for i,s in enumerate(tokens) if s.isdigit()]
        for i in ind_year:
            try:
                if tokens[i-1]=='сумма':
                    sum1 = [[int(tokens[i]),'RUB']]
                    break
            except IndexError:
                continue
    return sum1

def NER_filter_currency(tokens):
    # извлекаем валюту, если она есть
    currency = []
    for cur_type in ['рубль', 'доллар', 'евро']:
            if cur_type in tokens:
                currency = cur_type
                break
    return currency

def NER_filter_month_year(text, tokens, datesextractor):

        #             не распознает:
        #              - февраль 22
        #              - 03 22
        #             распознает:
        #              - февраль 2022
        #              - в 2022 году
        #              - в 2022, в феврале
        #              - в 22 году, в феврале
        #              - в конце года (в этом году, текущего года, в нынешнем году), в феврале
        #              - в следующем году (будущего года), в феврале
        #              - в том году (в прошлом году), в феврале
        matches = datesextractor(text)
        par1 = []

        textn = ' '.join(tokens)
        #textn = text
        months = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь',
                  'ноябрь', 'декабрь']
        month_ind = [i + 1 for i, j in enumerate(months) if j in textn]

        for match in matches:
            try:
                # случай "в феврале 2022"
                par1.append([match.fact.as_json['year'], match.fact.as_json['month']])
            except:
                # случай "в 2022 году в феврале"
                try:
                    if month_ind:
                        par1.append([match.fact.as_json['year'], month_ind[0]])
                    else:
                        par1.append([match.fact.as_json['year']])
                except KeyError:
                    par1.append([match.fact.as_json['month'], match.fact.as_json['day']])
            return par1[0]

        if not par1:
            # проверяем случай "в этом году"
            if 'этот год' in textn or 'текущий год' in textn or 'нынешний год' in textn or 'в конец год' in textn:
                if month_ind:
                    par1.append([datetime.datetime.now().year, month_ind[0]])
                else:
                    par1.append([datetime.datetime.now().year])
                return par1[0]

            # проверяем случай "в следующем году"
            if 'следующий год' in textn or 'будущий год' in textn:
                if month_ind:
                    par1.append([datetime.datetime.now().year + 1, month_ind[0]])
                else:
                    par1.append([datetime.datetime.now().year + 1])
                return par1[0]

            # проверяем случай "в прошлом году"
            if 'прошлый год' in textn or 'тот год' in textn:
                if month_ind:
                    par1.append([datetime.datetime.now().year - 1, month_ind[0]])
                else:
                    par1.append([datetime.datetime.now().year - 1])
                return par1[0]

            # проверяем случай "в 2022"
            if re.search('[1-2][0-9]{3}', textn):
                yearn = int(re.search('[1-2][0-9]{3}', text)[0])
                if month_ind:
                    par1.append([yearn, month_ind[0]])
                else:
                    par1.append([yearn])
                return par1[0]

            # проверяем случай "в 22 году"
            ind_year = [i for i, s in enumerate(tokens) if s.isdigit()]
            yearn = []
            for i in ind_year:
                try:
                    if tokens[i + 1] == 'год':
                        yearn = int('20' + tokens[i])
                        break
                except IndexError:
                    continue
            if yearn:
                if month_ind:
                    par1.append([yearn, month_ind[0]])
                else:
                    par1.append([yearn])
                return par1[0]

        return par1