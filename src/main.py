"""
Date: 3/4/2020 11:55 AM
Author: Achini
"""

import pickle
import src.core.emotions.emotion_extractor as emotion_extractor
import src.utils.text_processor as text_utils
import src.core.summary.keyphrase_extractor as keyphrase_extractor
import src.core.clinical_info.clinical_info_extractor as clinical_info_extractor
import xlrd
from xlwt import *

def writeDataToExcelFile(inputData,outputFile):
    wb = Workbook()
    sheet = wb.active
    sheet.title = "Sheet1"
    sheet["A1"].value = 'key_a'
    sheet["B1"].value = 'key_b'
    j = 2
    for item in  inputData:
        sheet["A"+str(j)].value = item["key_a"]
        sheet["B"+str(j)].value = item["key_b"]


def cleanText(inpath):
    indata=xlrd.open_workbook(inpath, encoding_override='utf-8')
    book=Workbook(encoding_override='utf-8')
    outdata = book.add_sheet('sheet1')
    table = indata.sheets()[0]
    nrows = table.nrows
    ncols = table.ncols
    for i in range(1, nrows):
        alldata = table.row_values(i)
        #result = alldata[1]
        clean_text_1 = text_utils.clean_text(alldata[1])
        outdata.write(i,1, alldata[0])
        outdata.write(i,2, clean_text_1)
    outdata.save("F://projects-he//nlp-emotion-analysis-Jeloh//nlp-emotion-analysis-core//src//data//AfterClean.csv")



def load_emotion_dictionaries():
    with open('models/emotions/emotions_plutchik.pkl', 'rb') as f: ##表示情绪angry、sad
        EMOTION_MAP = pickle.load(f)
    with open('models/emotions/intensifier_vocab_v2.pkl', 'rb') as f:##表示强烈程度always、completely
        INTENSIFIER_MAP = pickle.load(f)
    with open('models/emotions/negation_vocab_v2.pkl', 'rb') as f:##表示否定shouldn't
        NEGATION_MAP = pickle.load(f)
    with open('models/clinical_info/physical.pkl', 'rb') as f:##表示身体状况词汇
        PHYSICAL = pickle.load(f)

    EMO_RESOURCES = {'EMOTIONS': EMOTION_MAP,
                     'NEGATION': NEGATION_MAP,
                     'INTENSIFIERS': INTENSIFIER_MAP,
                     'PHYSICAL': PHYSICAL}

    return EMO_RESOURCES


if __name__ == '__main__':
    EMO_RESOURCES = load_emotion_dictionaries()

    #inPath = 'coronavirus_reddit_raw_comments.csv'
    text_1 = 'The disease is not even inevitable. China and Korea have shown that the disease can be managed if everyone is taking it seriously.'
    clean_text_1 = text_utils.clean_text(text_1)

    emotion_profile, emo_seq = emotion_extractor.get_emotion_profile_per_post(clean_text_1, EMO_RESOURCES)##得到情绪信息
    clinical_info = clinical_info_extractor.get_physical_sym_profile(clean_text_1, EMO_RESOURCES)##得到身体信息
    keyphrases = keyphrase_extractor.analyze_keyphrases(clean_text_1) ##分析关键词

    print(keyphrases)
    print(clinical_info)
    print(emotion_profile)



