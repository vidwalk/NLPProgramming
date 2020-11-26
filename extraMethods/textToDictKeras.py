import os
from collections import Counter
import csv
from keras.preprocessing.text import text_to_word_sequence


def findTxts(path):
    result = list()
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.txt'):
                result.append(file)
    return result


if __name__ == "__main__":
    token_list = list()
    for txtFile in findTxts('TextFiles'):
        filePath = open('TextFiles/' + txtFile, 'r', encoding='utf-8')
        text = filePath.read()
        tokens = text_to_word_sequence(text)
        token_list.extend(tokens)
    count = Counter(token_list)
    with open("Counts/KerasWordFreqDict.csv", "w+", newline="", encoding='utf-32') as csv_file:
        csv_file.write("%s,%s\n" % ('word', 'count'))
        for key, value in count.most_common():
            csv_file.write("%s, %s\n" % (key, value))
