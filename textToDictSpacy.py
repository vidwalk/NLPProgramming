import spacy
import os
from collections import defaultdict, Counter
import csv


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
    nlp = spacy.load("en_core_web_sm", disable=[
                     'parser', 'tagger', 'ner', 'entity_ruler'], max_length=1529140)
    for txtFile in findTxts('TextFiles'):
        filePath = open('TextFiles/' + txtFile, 'r', encoding='utf-8')
        text = filePath.read()
        doc = nlp(text)
        for token in doc:
            pos_counts[token.pos][token.orth] += 1
    with open("Counts/SpacyWordFreqDict.csv", "w+", newline="", encoding='utf-32') as csv_file:
        csv_file.write("%s, %s\n" % ('word', 'count'))
        for pos_id, counts in sorted(pos_counts.items()):
            pos = doc.vocab.strings[pos_id]
            for orth_id, count in counts.most_common():
                csv_file.write("%s, %d\n" %
                               (doc.vocab.strings[orth_id], count))
