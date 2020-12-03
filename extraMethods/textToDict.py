import re
import os
from collections import Counter
import csv
import time


def reg_tokenize(regFilter, text):
    text = text.lower()
    text = re.sub(r"[^A-Za-z—\-\'\’ ]", ' ', text)
    text = re.sub(r"\s+", ' ', text)
    words = regFilter.findall(text)
    return words


def findTxts(path):
    result = list()
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.txt'):
                result.append(file)
    return result


if __name__ == "__main__":
    mainStartTime = time.time()
    WORD = re.compile(r'[A-Za-z—\-\'\’]*')
    token_list = list()
    for txtFile in findTxts('TextFiles'):
        filePath = open('TextFiles/' + txtFile, 'r', encoding='utf-8')
        text = filePath.read()
        tokens = reg_tokenize(WORD, text)
        token_list.extend(tokens)
    count = Counter(token_list)
    with open("Counts/WordFreqDict.csv", "w+", newline="", encoding='utf-8') as csv_file:
        csv_file.write("%s,%s\n" % ('word', 'count'))
        for key, value in count.most_common():
            csv_file.write("%s, %s\n" % (key, value))
    print("--- %s seconds --- for all" %
          (time.time() - mainStartTime))
