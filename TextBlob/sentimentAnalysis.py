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
csv.register_dialect("comma", delimiter=",")

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


text_dict_EE = Dict()
text_dict_E = Dict()
text_dict_F = Dict()
text_dict_EF = Dict()

complexity_dictEE = Dict()
complexity_dictE = Dict()
complexity_dictEF = Dict()
complexity_dictF = Dict()

def write_to_hashes_csv(dict1, dict2, file_name):
    with open(file_name, 'w', newline='', encoding="utf8") as csvfile:
        # fieldnames = ['Complexity_level', 'text']
        writer = csv.writer(csvfile, dialect="hashes")
        keys = dict1.keys()
        for k in keys:
            writer.writerow((dict2[k], dict1[k]))

def write_to_comma_csv(dict1, dict2, file_name):
    with open(file_name, 'w', newline='', encoding="utf8") as csvfile:
        # fieldnames = ['Complexity_level', 'text']
        writer = csv.writer(csvfile, dialect="comma")
        keys = dict1.keys()
        for k in keys:
            writer.writerow((dict1[k], dict2[k]))


def write_four_types_to_csv(dict1, dict2, file_name):
    with open(file_name, 'w', newline='', encoding="utf8") as csvfile:
        # fieldnames = ['Complexity_level', 'text']
        writer = csv.writer(csvfile, dialect="comma")
        keys = dict1.keys()
        for k in keys:
            writer.writerow((dict1[k], dict2[k]))

def clean_text(text):
    '''Make text lowercase, remove text in square brackets, remove punctuation and remove words containing numbers.'''
    text = text.lower()
    text = re.sub(r'!"#%&(),:;<=>@]_`}~', '', text) # *+/

    # text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    # text = re.sub(r'\w*\d\w*', '', text)
    # text = re.sub(r'http\S+', 'urllink', text, flags=re.S)

    # remove http/https, punctuation, and remove space at the beginning and the end
    text = text.replace('https', '').replace('http', '').replace('/', ' ')\
        .replace('<', ' ').replace('>', ' ').replace(';', ' ').replace(':', ' ').replace('(', ' ')\
        .replace(')', ' ').replace('www', '')\
        .replace('!', ' ').replace('?', ' ').replace('.', ' ').replace(',', ' ')\
        .replace('[','').replace(']','').replace('-','')\
        .replace('$', ' ').replace('\n', '').replace('\t', '').replace('\r','')

    #print('before strip():' + text)

    text = (" ".join(text.split())).strip()
    #print('after strip():' + text)
    # split text without spaces into list of words and concatenate string in a list to a single string
    # text = ' '.join(wn.split(text))

    # spell check


    return text

def read_four_types_from_csv(file_name):
    with open(file_name, mode='r', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:

            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
                continue

            tmp = clean_text(row[1])

            text_with_dup_dict[line_count] = tmp
            line_count += 1

            if tmp in text_dict_EE.values() or tmp in text_dict_E.values() or tmp in text_dict_EF.values() or tmp in text_dict_F.values():
                print('line_count: ' + str(line_count) + ' complexity_level: ' + row[0]  + ' text: ' + tmp)
                continue
            elif row[0] == 'L-EE':
                text_dict_EE[line_count] = tmp
                complexity_dictEE[line_count] = row[0]
            elif row[0] == 'L-EF':
                text_dict_EF[line_count] = tmp
                complexity_dictEF[line_count] = row[0]
            elif row[0] == 'L-E':
                text_dict_E[line_count] = tmp
                complexity_dictE[line_count] = row[0]
            elif row[0] == 'L-F':
                text_dict_F[line_count] = tmp
                complexity_dictF[line_count] = row[0]

def process_four_csv_file(file_name):
    d = os.getcwd()
    text_dict_E.clear()
    text_dict_EE.clear()
    text_dict_F.clear()
    text_dict_EF.clear()

    complexity_dictEE.clear()
    complexity_dictE.clear()
    complexity_dictEF.clear()
    complexity_dictF.clear()

    complexity_dict.clear()
    text_with_dup_dict.clear()
    textPath = path.join(d, file_name)
    read_four_types_from_csv(textPath)

    print(f'---------------------{file_name}------------------------')
    print(f'Processed text_dict_E {len(text_dict_E)} lines without dups.')
    print(f'Processed text_dict_EE {len(text_dict_EE)} lines without dups.')
    print(f'Processed text_dict_EF {len(text_dict_EF)} lines without dups.')
    print(f'Processed text_dict_F {len(text_dict_F)} lines without dups.')
    print(f'Processed {len(text_with_dup_dict)} lines with dups.')
    new_file_name1 = 'EF_clean.csv'
    new_file_name2 = 'F_clean.csv'
    new_file_name3 = 'E_clean.csv'
    new_file_name4 = 'EE_clean.csv'
    write_four_types_to_csv( complexity_dictEF, text_dict_EF, new_file_name1)
    write_four_types_to_csv( complexity_dictF, text_dict_F, new_file_name2)
    write_four_types_to_csv( complexity_dictE, text_dict_E, new_file_name3)
    write_four_types_to_csv( complexity_dictEE, text_dict_EE, new_file_name4)

def read_from_csv(file_name):
    with open(file_name, mode='r', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:

            if line_count == 0:
                # print(f'Column names are {", ".join(row)}')
                line_count += 1
                continue

            tmp = clean_text(row[1])

            text_with_dup_dict[line_count] = tmp
            line_count += 1

            # list out keys and values separately

            if tmp in text_dict.values():

                key_list = list(text_dict.keys())
                val_list = list(text_dict.values())
                val_index = val_list.index(tmp)
                print('existing complexity_dict: ' + complexity_dict[key_list[val_index]] + ' text: ' + text_dict[key_list[val_index]])
                print('duplicate complexity_level: ' + row[0] + ' text: ' + tmp)
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

def process_csv_file(file_name):
    d = os.getcwd()
    text_dict.clear()
    complexity_dict.clear()
    text_with_dup_dict.clear()
    textPath = path.join(d, file_name)
    read_from_csv(textPath)

    print(f'---------------------{file_name}------------------------')
    print(f'Processed {len(text_dict)} lines without dups.')
    print(f'Processed {len(text_with_dup_dict)} lines with dups.')
    new_file_name = str(file_name).split('.')[0]+'_hashes.csv'
    write_to_hashes_csv( complexity_dict, text_dict, new_file_name)
    new_file_name = str(file_name).split('.')[0]+'_comma.csv'
    write_to_comma_csv( complexity_dict, text_dict, new_file_name)

if __name__ == "__main__":
    d = os.getcwd()
   # textPath = path.join(d, 'Train_KF_T.csv')
    # textPath = path.join(d, 'Train_all_types_hashes.csv')
    '''
    process_csv_file('Train_KF_T copy.csv')
    # process_four_csv_file('light_data_v01.csv')
    process_csv_file('Train_KF_all_types copy.csv')
    '''

    process_csv_file('Train_all_types.csv')
    process_csv_file('Train_KF_T.csv')
    process_csv_file('Train_KF_X.csv')
    process_csv_file('Train_KF2.csv')
    process_csv_file('Train_question.csv')
    process_csv_file('Train_resource.csv')

    # process_csv_file('light_data_v01.csv')


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


# classifier: https://textblob.readthedocs.io/en/latest/classifiers.html
# sentiment analyzers: https://textblob.readthedocs.io/en/latest/advanced_usage.html#sentiment-analyzers
# API overview: https://textblob.readthedocs.io/en/latest/index.html
