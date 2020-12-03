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
    #"POS:ADP POS:DET:? POS:ADJ:? POS:NOUN:+"
    pattern = [{'POS': 'DET', 'OP': '?'},
               {'POS': 'ADJ', 'OP': '*'},
               {'POS': 'NOUN', 'OP': '+'}]
    matcher = Matcher(nlp.vocab)
    matcher.add("Verb phrase", None, pattern)
    count = list()
    txtFile = ["Due to the highly volatile and competitive nature of the industries in which the Company competes, the Company must continually introduce new products, services and technologies, enhance existing products and services, and effectively stimulate customer demand for new and upgraded products."]
    text = txtFile[0]
    doc = nlp(text)
    spans = [doc[start:end] for _, start, end in matcher(doc)]
    count.extend(spans)
    df = pd.DataFrame({'NP': count})
    df['count'] = 1
    df.to_csv(
        'Counts/TestSpacyNP.csv', index=False)
    df = pd.read_csv('Counts/TestSpacyNP.csv', header=0)
    dfAgg = df.groupby(['NP']).sum()
    dfAgg.reset_index().sort_values(by='count', ascending=False).to_csv(
        'Counts/TextSpacyNPWordFreqDict.csv', index=False)
    print("--- %s seconds --- for all" %
          (time.time() - mainStartTime))
