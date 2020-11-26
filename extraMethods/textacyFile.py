from __future__ import unicode_literals
import spacy
import en_core_web_sm
import textacy
import os
import re
nlp = en_core_web_sm.load()


def findTxts(path):
    result = list()
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.txt'):
                result.append(file)
    return result


pattern = [{'POS': 'VERB', 'OP': '?'},
           {'POS': 'ADV', 'OP': '*'},
           {'OP': '*'},  # additional wildcard - match any text in between
           {'POS': 'VERB', 'OP': '+'}]
for txtFile in findTxts('TextFiles'):
    filePath = open('TextFiles/' + txtFile, 'r', encoding='utf-8')
    text = filePath.read()
    doc = textacy.make_spacy_doc(text, lang='en_core_web_sm')
    lists = textacy.extract.matches(doc, pattern)
    for list in lists:
        print(list.text)
