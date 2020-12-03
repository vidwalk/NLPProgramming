import spacy
import os
from collections import defaultdict, Counter
import csv
import re
import pandas as pd
from spacy.matcher import Matcher
import time


def findTxts(path):
    result = list()
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.txt'):
                result.append(file)
    return result


if __name__ == "__main__":
    mainStartTime = time.time()
    # python -m spacy download en_core_web_sm
    nlp = spacy.load("en_core_web_sm", max_length=1529140)
    pattern = [{'POS': 'VERB', 'OP': '?'},
               {'POS': 'ADV', 'OP': '*'},
               {'POS': 'VERB', 'OP': '+'}]
    matcher = Matcher(nlp.vocab)
    matcher.add("Verb phrase", None, pattern)
    count = list()
    for txtFile in findTxts('TextFiles'):
        startTime = time.time()
        filePath = open('TextFiles/' + txtFile, 'r', encoding='utf-8')
        text = filePath.read()
        text = text.lower()
        text = re.sub(r"[^A-Za-z—\-\'\’\, ]", ' ', text)
        text = re.sub(r"\s+", ' ', text)
        doc = nlp(text)
        spans = [doc[start:end] for _, start, end in matcher(doc)]
        count.extend(spans)
        print("--- %s seconds --- for %s" %
              (time.time() - startTime, txtFile))
    df = pd.DataFrame({'VP': count})
    df['count'] = 1
    df.to_csv(
        'Counts/SpacyVP.csv', index=False)
    df = pd.read_csv('Counts/SpacyVP.csv', header=0)
    dfAgg = df.groupby(['VP']).sum()
    dfAgg.reset_index().sort_values(by='count', ascending=False).to_csv(
        'Counts/SpacyVPWordFreqDict.csv', index=False)
    print("--- %s seconds --- for all" %
          (time.time() - mainStartTime))
