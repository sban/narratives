## dependencies
from allennlp.predictors.predictor import Predictor
import pandas as pd
import re


## functions

def wordcnt(text):
    return(len(text.strip().split(" ")))


def get_word(text, char):
    listOfWords = text.split(char, 1)
    if len(listOfWords) > 0:
        strValue = listOfWords[1]
    return strValue


def coref(text, model=''):
    if model == '':
        model = r'https://storage.googleapis.com/allennlp-public-models/coref-spanbert-large-2020.02.27.tar.gz'

    predictor = Predictor.from_path(model)
    prediction = predictor.predict(document=text)
    res = predictor.coref_resolved(text)
    return res


def DSG_prep(text):

    text_sent = []
     ## If text data is in a list
    if type(text) is list:
        text = ". ".join(text)

    ## Splitting the text
    text_sent = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', text)
    ## print(tmp)
    #text_sent.append(tmp)

    return text_sent


def DSG_mod(text_sent, model = ''):

    if model == '':
         model = 'https://storage.googleapis.com/allennlp-public-models/structured-prediction-srl-bert.2020.12.15.tar.gz'

    predictor = Predictor.from_path(model)

    res = []
    for i in text_sent:
        print(i)
        tree = predictor.predict(sentence= i)
        tmpA = tree ['verbs']

        for j in range(0, len(tmpA)):
            tmpB = tmpA[j]['description']
            sunits = repr(tmpB)
            sunits = pd.DataFrame(sunits.split("]"))
            V = "-" ; ARG0 = "-"; ARG1 = "-" ;  ARG2 = "-" ;  ARG3 = "-" ; ARGMM = "-" ; ARGMP = "-"; ARGMD = "-"; ARGMTMP = "-"; ARGMLOC = "-"; ARGMADV = "-"; ARGMMNR = "-"

            for h in (sunits.index):
                tmp = sunits[0][h]

                if tmp.find('V:') >= 0:
                    tmpC = get_word(tmp, 'V:')
                    V = tmpC
                if tmp.find('[ARG0:') >= 0:
                    tmpC = get_word(tmp, '0:')
                    ARG0 = tmpC
                if tmp.find('[ARG1:') >= 0:
                    tmpC = get_word(tmp, '1:')
                    ARG1 = tmpC
                if tmp.find('[ARG2:') >= 0:
                    tmpC = get_word(tmp, '2:')
                    ARG2 = tmpC
                if tmp.find('[ARG3:') >= 0:
                    tmpC = get_word(tmp, '3:')
                    ARG3 = tmpC
                if tmp.find('[ARGM-PRP:') >= 0:
                    tmpC = get_word(tmp, 'PRP:')
                    ARGMP = tmpC
                if tmp.find('[ARGM-DIR:') >= 0:
                    tmpC = get_word(tmp, 'DIR:')
                    ARGMD = tmpC
                if tmp.find('[ARGM-MOD:') >= 0:
                    tmpC = get_word(tmp, 'MOD:')
                    ARGMM = tmpC
                if tmp.find('[ARGM-TMP:') >= 0:
                    tmpC = get_word(tmp, 'TMP:')
                    ARGMTMP = tmpC
                if tmp.find('[ARGM-LOC:') >= 0:
                    tmpC = get_word(tmp, 'LOC:')
                    ARGMLOC = tmpC
                if tmp.find('[ARGM-ADV:') >= 0:
                    tmpC = get_word(tmp, 'ADV:')
                    ARGMADV = tmpC
                if tmp.find('[ARGM-MNR:') >= 0:
                    tmpC = get_word(tmp, 'MNR:')
                    ARGMMNR = tmpC

            tmpC = [V, ARG0, ARG1, ARG2, ARG3, ARGMP, ARGMD, ARGMM, ARGMTMP, ARGMLOC, ARGMADV, ARGMMNR, tmpB]
            res.append(tmpC)
    res = pd.DataFrame(res)
    res.columns = ['V', 'ARG0', 'ARG1', 'ARG2', 'ARG3', 'ARGMPRP', 'ARGMDIR', 'ARGMMOD', 'ARGMTMP', 'ARGMLOC', 'ARGMADV', 'ARGMMNR', 'txt']
    return res


def DSG_svo(input_dat, out_file = ''):

    if out_file == '':
        out_file = 'example.csv'

    res = pd.DataFrame({
        'S': "-",
        'V': input_dat['V'],
        'O': "-",
        'M': "-",
        'P': "-",
        'T': "-",
        'txt': input_dat['txt']})

    # classification order
    input_dat['codes'] = '-'

    for i in (input_dat.index):
        test_str = str(input_dat['txt'][i])
        input_dat['codes'][i] = re.findall(r'\[.*?\]', test_str)
        input_dat['codes'][i] = "".join(input_dat['codes'][i])

        ## set place
        res['P'][i] = input_dat['ARGMLOC'][i]

        # set means
        res['M'][i] = input_dat['ARGMMNR'][i]

        # set time
        res['T'][i] = input_dat['ARGMTMP'][i]

        # set modals
        if (input_dat['ARGMMOD'][i] != "-"):
            res['V'][i] = input_dat['ARGMMOD'][i] + res['V'][i]

        # set SVO
        if ((res['S'][i] == "-") & (input_dat['codes'][i][1:5] == 'ARG0') & (input_dat['ARG0'][i] != "-") & (input_dat['ARG1'][i] != "-") & (input_dat['ARG2'][i] == "-") & (input_dat['ARG3'][i] != "-")):
            res['S'][i] = input_dat['ARG0'][i]
            res['O'][i] = input_dat['ARG1'][i]
            res['M'][i] = input_dat['ARG3'][i]

        if ((res['S'][i] == "-") & (input_dat['codes'][i][1:5] == 'ARG0') & (input_dat['ARG0'][i] != "-") & (input_dat['ARG1'][i] != "-") & (input_dat['ARG2'][i] != "-") & (input_dat['ARG3'][i] == "-")):
            res['S'][i] = input_dat['ARG0'][i]
            res['O'][i] = input_dat['ARG1'][i]
            res['M'][i] = input_dat['ARG2'][i]

        if ((res['S'][i] == "-") & (input_dat['codes'][i][1:5] == 'ARG0') & (input_dat['ARG0'][i] != "-") & (input_dat['ARG1'][i] != "-") & (input_dat['ARG2'][i] == "-") & (input_dat['ARG3'][i] == "-")):
            res['S'][i] = input_dat['ARG0'][i]
            res['O'][i] = input_dat['ARG1'][i]

        if ((res['S'][i] == "-") & (input_dat['codes'][i][1:5] == 'ARG0') & (input_dat['ARG0'][i] != "-") & (input_dat['ARG1'][i] != "-") & (input_dat['ARG2'][i] == "-") & (input_dat['ARG3'][i] == "-")):
            res['S'][i] = input_dat['ARG0'][i]
            res['O'][i] = input_dat['ARG1'][i]

        if ((res['S'][i] == "-")  & (input_dat['codes'][i][1:5] == 'ARG1') & (input_dat['ARG0'][i] == "-") & (input_dat['ARG1'][i] != "-") & (input_dat['ARG2'][i] != "-") & (input_dat['ARG3'][i] == "-")):
            res['S'][i] = input_dat['ARG1'][i]
            res['O'][i] = input_dat['ARG2'][i]

        if ((res['S'][i] == "-") & (input_dat['codes'][i][1:5] == 'ARG2') & (input_dat['ARG0'][i] == "-") & (input_dat['ARG1'][i] != "-") & (input_dat['ARG2'][i] != "-") & (input_dat['ARG3'][i] == "-")):
            res['S'][i] = input_dat['ARG2'][i]
            res['O'][i] = input_dat['ARG1'][i]

        if ((res['S'][i] == "-") & (input_dat['codes'][i][1:9] == 'ARGM-TMP') & (input_dat['ARG0'][i] == "-") & (input_dat['ARG1'][i] != "-") & (input_dat['ARG2'][i] == "-") & (input_dat['ARG3'][i] == "-")):
            res['S'][i] = input_dat['ARGMTMP'][i]
            res['O'][i] = input_dat['ARG1'][i]

        if ((res['S'][i] == "-") & (input_dat['codes'][i][1:9] == 'ARGM-LOC') & (input_dat['ARG0'][i] != "-") & (input_dat['ARG1'][i] != "-") & (input_dat['ARG2'][i] == "-") & (input_dat['ARG3'][i] == "-")):
            res['S'][i] = input_dat['ARG0'][i]
            res['O'][i] = input_dat['ARG1'][i]
            res['P'][i] = input_dat['ARGMLOC'][i]

        if ((res['S'][i] == "-") & (input_dat['codes'][i][1:9] == 'ARGM-TMP') & (input_dat['ARG0'][i] != "-") & (input_dat['ARG1'][i] != "-") & (input_dat['ARG2'][i] == "-") & (input_dat['ARG3'][i] == "-")):
            res['S'][i] = input_dat['ARG0'][i]
            res['O'][i] = input_dat['ARG1'][i]
            res['T'][i] = input_dat['ARGMTMP'][i]

        if ((res['S'][i] == "-") & (input_dat['codes'][i][1:5] == 'ARG0') & (input_dat['ARG0'][i] != "-") & (input_dat['ARG1'][i] == "-") & (input_dat['ARG2'][i] == "-") & (input_dat['ARG3'][i] == "-") & (input_dat['ARGMDIR'][i] != "-")):
            res['S'][i] = input_dat['ARG0'][i]
            res['O'][i] = input_dat['ARGMDIR'][i]

        if ((res['S'][i] == "-")  & (input_dat['codes'][i][1:5] == 'ARG0') & (input_dat['ARG0'][i] != "-") & (input_dat['ARG1'][i] == "-") & (input_dat['ARG2'][i] == "-") & (input_dat['ARG3'][i] == "-") & (input_dat['ARGMPRP'][i] != "-")):
            res['S'][i] = input_dat['ARG0'][i]
            res['O'][i] = input_dat['ARGMPRP'][i]

        if ((res['S'][i] == "-")  & (input_dat['codes'][i][1:9] == 'ARGM-LOC') & (input_dat['ARG0'][i] != "-") & (input_dat['ARG1'][i] != "-") & (input_dat['ARG2'][i] == "-") & (input_dat['ARG3'][i] == "-") & (input_dat['ARGMPRP'][i] != "-")):
            res['S'][i] = input_dat['ARG1'][i]
            res['O'][i] = input_dat['ARG2'][i]

        if ((res['S'][i] == "-")  & (input_dat['codes'][i][1:5] == 'ARG0') & (input_dat['ARG0'][i] != "-") & (input_dat['ARG1'][i] == "-") & (input_dat['ARG2'][i] == "-") & (input_dat['ARG3'][i] == "-") & (input_dat['ARGMDIR'][i] == "-")):
            res['S'][i] = input_dat['ARG0'][i]

        if ((res['S'][i] == "-")  & (input_dat['codes'][i][1:5] == 'ARG1') & (input_dat['ARG0'][i] != "-") & (input_dat['ARG1'][i] != "-") & (input_dat['ARG2'][i] == "-") & (input_dat['ARG3'][i] == "-") & (input_dat['ARGMDIR'][i] == "-")):
            res['S'][i] = input_dat['ARG1'][i]
            res['O'][i] = input_dat['ARG0'][i]

        if ((res['S'][i] == "-")  & (input_dat['codes'][i][1:5] == 'ARG1') & (input_dat['ARG0'][i] == "-") & (input_dat['ARG1'][i] != "-") & (input_dat['ARG2'][i] == "-") & (input_dat['ARG3'][i] == "-") & (input_dat['ARGMDIR'][i] == "-")):
            res['S'][i] = input_dat['ARG1'][i]

        if ((res['S'][i] == "-")  & (input_dat['ARG0'][i] == "-") & (input_dat['ARG1'][i] != "-") & (input_dat['ARG2'][i] == "-") & (input_dat['ARG3'][i] == "-") & (input_dat['ARGMDIR'][i] == "-")):
            res['S'][i] = input_dat['ARG1'][i]

        if ((res['S'][i] == "-")  & (input_dat['ARG0'][i] == "-") & (input_dat['ARG1'][i] != "-") & (input_dat['ARG2'][i] != "-") & (input_dat['ARG3'][i] == "-") & (input_dat['ARGMDIR'][i] == "-")):
            res['S'][i] = input_dat['ARG1'][i]
            res['O'][i] = input_dat['ARG2'][i]


    res_out = res[res['S'] != "-"]
    res_out.to_csv(out_file, sep =';', index = False)
    return res_out

## complete
def DSG(input_dat, model='', out_file=''):

    # variables
    if out_file == '':
        out_file = 'example.csv'
    if model == '':
        model = 'https://storage.googleapis.com/allennlp-public-models/structured-prediction-srl-bert.2020.12.15.tar.gz'

    # prog
    res_prp = DSG_prep(input_dat)
    res_mod = DSG_mod(res_prp, model=model)
    res_svo = DSG_svo(res_mod, out_file = out_file)
    return res_svo
