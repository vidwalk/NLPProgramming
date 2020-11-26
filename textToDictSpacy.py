import spacy
import os
from collections import defaultdict, Counter
import csv
from spacy.tokenizer import Tokenizer
import re


def findTxts(path):
    result = list()
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.txt'):
                result.append(file)
    return result


if __name__ == "__main__":
    pos_counts = defaultdict(Counter)
    # python -m spacy download en_core_web_sm
    nlp = spacy.load("en_core_web_sm", max_length=1529140)
    tokenizer = Tokenizer(nlp.vocab)
    for txtFile in findTxts('TextFiles'):
        filePath = open('TextFiles/' + txtFile, 'r', encoding='utf-8')
        text = filePath.read()
        # text to lowercase
        text = text.lower()
        # keep only letters, -, ' and space
        text = re.sub(r"[^A-Za-z—\-\'\’ ]", ' ', text)
        # replace multiple whitespace with just one
        text = re.sub(r"\s+", ' ', text)
        # tokenize the data
        tokens = tokenizer(text)
        for token in tokens:
            #
            pos_counts[token.pos][token.orth] += 1
        # 'w' open for writing '+' open a disk file for updating (reading and writing)
    with open("Counts/SpacyWordFreqDict.csv", mode="w+", newline="", encoding='utf-8') as csv_file:
        # headers
        csv_file.write("%s,%s\n" % ('word', 'count'))
        for pos_id, counts in sorted(pos_counts.items()):
            for orth_id, count in counts.most_common():
                csv_file.write("%s, %d\n" %
                               (tokens.vocab.strings[orth_id], count))
