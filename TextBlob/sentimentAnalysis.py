#!/usr/bin/env python
# coding=utf-8

from numpy import *
import os
from os import path
from textblob import TextBlob

import csv
import re, string
import wordninja as wn

csv.register_dialect("hashes", delimiter="#")

class Dict(dict):
    def __missing__(self, key):
        return 0

# global variable
# https://docs.python.org/3/library/stdtypes.html#dict
polarity_dict = Dict()
subjectivity_dict = Dict()
text_dict = Dict()
complexity_dict = Dict()
text_with_dup_dict = Dict()

def write_to_csv(dict1, dict2, file_name):
    with open(file_name, 'w', newline='', encoding="utf8") as csvfile:
        # fieldnames = ['Complexity_level', 'text']
        writer = csv.writer(csvfile, dialect="hashes")
        keys = dict1.keys()
        for k in keys:
            writer.writerow((dict2[k].replace('"', '').replace('[', '').replace(']', '').replace('-', ' '), dict1[k]))

def clean_text(text):
    '''Make text lowercase, remove text in square brackets, remove punctuation and remove words containing numbers.'''
    text = text.lower()
    text = re.sub(r'!"#%&(),:;<=>@]_`}~', '', text) # *+/
    # text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    # text = re.sub(r'\w*\d\w*', '', text)
    # text = re.sub(r'http\S+', 'urllink', text, flags=re.S)

    text = text.replace('https', '').replace('http', '').replace('/', ' ')\
        .replace('<', ' ').replace('>', ' ').replace(';', ' ').replace(':', ' ').replace('(', ' ').replace(')', ' ')\
        .replace('!', ' ').replace('?', ' ').replace('.', ' ').replace(',', ' ')

    # split text without spaces into list of words and concatenate string in a list to a single string
    text = ' '.join(wn.split(text))

    # spell check


    return text

def read_from_csv(file_name):
    with open(file_name, mode='r', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:

            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1

            tmp = clean_text(row[1])
            text_with_dup_dict[line_count] = tmp
            line_count += 1

            if tmp in text_dict.values():
                print('line_count: ' + str(line_count) + ' text: ' + tmp)
                continue
            else:

                text_dict[line_count] = tmp
                complexity_dict[line_count] = row[0]


                testimonial = TextBlob(tmp)
                polarity_dict[line_count] = testimonial.sentiment.polarity
                subjectivity_dict[line_count] = testimonial.sentiment.subjectivity

def read_from_file(file_name):
    with open(file_name,"r", encoding='utf-8') as fp:
        words = fp.read()
    return words

if __name__ == "__main__":
    d = os.getcwd()
   # textPath = path.join(d, 'Train_KF_T.csv')
    # textPath = path.join(d, 'Train_all_types_hashes.csv')
    textPath = path.join(d, 'Train_all_types.csv')  # path.join(d, 'Train_all_types.csv')
    read_from_csv(textPath)

    print('---------------------Train_all_types.csv------------------------')
    print(f'Processed {len(text_dict)} lines without dups.')
    print(f'Processed {len(text_with_dup_dict)} lines with dups.')
    write_to_csv( complexity_dict, text_dict, 'Train_all_types_clean.csv')

    '''
    polarity_dict = {k: v for k, v in sorted(polarity_dict.items(), key=lambda item: item[1], reverse=True)}
    subjectivity_dict = {k: v for k, v in sorted(subjectivity_dict.items(), key=lambda item: item[1], reverse=True)}

    print('---------------------TOP 50------------------------')

    print(f'Processed polarity_dict: {len(polarity_dict)} lines with dups.')
    line_count = 0
    for k, v in polarity_dict.items():
        if line_count < 50:
            print('\t line count: %s \t --- \t polarity: %s --- \t subjectivity: %s --- \t text: %s' % (k, v, subjectivity_dict[k], text_dict[k]))
            #print('\t line count: %s \t --- \t polarity: %s' % (k, v))
        else:
            continue
        line_count += 1

    print('---------------------TOP 50------------------------')
    line_count = 0
    for k, v in subjectivity_dict.items():
        if line_count < 50:
            print('\t line count: %s \t --- \t polarity: %s --- \t subjectivity: %s --- \t text: %s' % (k, polarity_dict[k], v, text_dict[k]))
            #print('\t line count: %s \t --- \t subjectivity: %s' % (k, v))
        else:
            continue
        line_count += 1

    print('---------------------------------------------')

    polarity_dict = {k: v for k, v in sorted(polarity_dict.items(), key=lambda item: item[1])}
    subjectivity_dict = {k: v for k, v in sorted(subjectivity_dict.items(), key=lambda item: item[1])}

    print('---------------------BOTTOM 50------------------------')
    line_count = 0
    for k, v in polarity_dict.items():
        if v != 0.0 and line_count < 50:
            print('\t line count: %s \t --- \t polarity: %s --- \t subjectivity: %s --- \t text: %s' % (k, v, subjectivity_dict[k], text_dict[k]))
            line_count += 1
            #print('\t line count: %s \t --- \t polarity: %s' % (k, v))
        else:
            continue

    print('---------------------BOTTOM 50------------------------')
    line_count = 0
    for k, v in subjectivity_dict.items():
        if v != 0.0 and line_count < 50:
            print('\t line count: %s \t --- \t polarity: %s --- \t subjectivity: %s --- \t text: %s' % (k, polarity_dict[k], v, text_dict[k]))
            line_count += 1
            #print('\t line count: %s \t --- \t subjectivity: %s' % (k, v))
        else:
            continue

    polarity_dict.clear()
    subjectivity_dict.clear()
    '''
    text_dict.clear()
    complexity_dict.clear()
    text_with_dup_dict.clear()
    textPath = path.join(d, 'Train_KF_T.csv')
    read_from_csv(textPath)

    print('---------------------Train_KF_T.csv------------------------')
    print(f'Processed {len(text_dict)} lines without dups.')
    print(f'Processed {len(text_with_dup_dict)} lines with dups.')
    write_to_csv( complexity_dict, text_dict, 'Train_KF_T_clean.csv')

    polarity_dict.clear()
    subjectivity_dict.clear()
    text_dict.clear()
    complexity_dict.clear()
    text_with_dup_dict.clear()
    textPath = path.join(d, 'Train_KF_X.csv')
    read_from_csv(textPath)

    print('---------------------Train_KF_X.csv------------------------')
    print(f'Processed {len(text_dict)} lines without dups.')
    print(f'Processed {len(text_with_dup_dict)} lines with dups.')
    write_to_csv( complexity_dict, text_dict, 'Train_KF_X_clean.csv')

    polarity_dict.clear()
    subjectivity_dict.clear()
    text_dict.clear()
    complexity_dict.clear()
    text_with_dup_dict.clear()
    textPath = path.join(d, 'Train_KF2.csv')
    read_from_csv(textPath)

    print('---------------------Train_KF2.csv------------------------')
    print(f'Processed {len(text_dict)} lines without dups.')
    print(f'Processed {len(text_with_dup_dict)} lines with dups.')
    write_to_csv( complexity_dict, text_dict, 'Train_KF2_clean.csv')

    polarity_dict.clear()
    subjectivity_dict.clear()
    text_dict.clear()
    complexity_dict.clear()
    text_with_dup_dict.clear()
    textPath = path.join(d, 'Train_question.csv')
    read_from_csv(textPath)

    print('---------------------Train_question.csv------------------------')
    print(f'Processed {len(text_dict)} lines without dups.')
    print(f'Processed {len(text_with_dup_dict)} lines with dups.')
    write_to_csv( complexity_dict, text_dict, 'Train_question_clean.csv')

    polarity_dict.clear()
    subjectivity_dict.clear()
    text_dict.clear()
    complexity_dict.clear()
    text_with_dup_dict.clear()
    textPath = path.join(d, 'Train_resource.csv')
    read_from_csv(textPath)

    print('---------------------Train_resource.csv------------------------')
    print(f'Processed {len(text_dict)} lines without dups.')
    print(f'Processed {len(text_with_dup_dict)} lines with dups.')
    write_to_csv( complexity_dict, text_dict, 'Train_resource_clean.csv')

# classifier: https://textblob.readthedocs.io/en/latest/classifiers.html
# sentiment analyzers: https://textblob.readthedocs.io/en/latest/advanced_usage.html#sentiment-analyzers
# API overview: https://textblob.readthedocs.io/en/latest/index.html
