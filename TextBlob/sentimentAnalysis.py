#!/usr/bin/env python
# coding=utf-8

import sys,os
import numpy as np
from numpy import *
import jieba
import math
import jieba.analyse
import os
from os import path
from textblob import TextBlob

import csv

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

def write_to_csv( dict1, dict2, file_name):
    with open(file_name, 'w', newline='', encoding="utf8") as csvfile:
        fieldnames = ['Complexity_level', 'text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # writer = csv.DictWriter(csvfile)
        keys = dict1.keys()
        writer.writeheader()
        for k in keys:
            # writer.writerow({'Complexity_level': dict1[k], 'text': dict2[k] })
            writer.writerow({'text': dict2[k], 'Complexity_level': dict1[k]})

def read_from_csv(file_name):
    with open(file_name, mode='r', encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1

            text_with_dup_dict[line_count] = row["text"]
            line_count += 1
            if row["text"] in text_dict.values():
                continue
            else:
                testimonial = TextBlob(row["text"])
                polarity_dict[line_count] = testimonial.sentiment.polarity
                subjectivity_dict[line_count] = testimonial.sentiment.subjectivity
                text_dict[line_count] = row["text"]
                complexity_dict[line_count]=row["Complexity_level"]


def read_from_file(file_name):
    with open(file_name,"r", encoding='utf-8') as fp:
        words = fp.read()
    return words

if __name__ == "__main__":
    d = os.getcwd()
   # textPath = path.join(d, 'Train_KF_T.csv')
    textPath = path.join(d, 'Train_all_types.csv')
    read_from_csv(textPath)

    polarity_dict = {k: v for k, v in sorted(polarity_dict.items(), key=lambda item: item[1], reverse=True)}
    subjectivity_dict = {k: v for k, v in sorted(subjectivity_dict.items(), key=lambda item: item[1], reverse=True)}

    print('---------------------TOP 50------------------------')
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

    print('---------------------Train_all_types.csv------------------------')
    print(f'Processed {len(text_dict)} lines.')
    print(f'Processed {len(text_with_dup_dict)} lines with dups.')
    write_to_csv( text_dict, complexity_dict, 'Train_all_types_no_dup.csv')

    polarity_dict.clear()
    subjectivity_dict.clear()
    text_dict.clear()
    complexity_dict.clear()
    text_with_dup_dict.clear()
    textPath = path.join(d, 'Train_KF_T.csv')
    read_from_csv(textPath)

    print('---------------------Train_KF_T.csv------------------------')
    print(f'Processed {len(text_dict)} lines.')
    print(f'Processed {len(text_with_dup_dict)} lines with dups.')
    write_to_csv( text_dict, complexity_dict, 'Train_KF_T_no_dup.csv')

    polarity_dict.clear()
    subjectivity_dict.clear()
    text_dict.clear()
    complexity_dict.clear()
    text_with_dup_dict.clear()
    textPath = path.join(d, 'Train_KF_X.csv')
    read_from_csv(textPath)

    print('---------------------Train_KF_X.csv------------------------')
    print(f'Processed {len(text_dict)} lines.')
    print(f'Processed {len(text_with_dup_dict)} lines with dups.')
    write_to_csv( text_dict, complexity_dict, 'Train_KF_X_no_dup.csv')

    polarity_dict.clear()
    subjectivity_dict.clear()
    text_dict.clear()
    complexity_dict.clear()
    text_with_dup_dict.clear()
    textPath = path.join(d, 'Train_KF2.csv')
    read_from_csv(textPath)

    print('---------------------Train_KF2.csv------------------------')
    print(f'Processed {len(text_dict)} lines.')
    print(f'Processed {len(text_with_dup_dict)} lines with dups.')
    write_to_csv( text_dict, complexity_dict, 'Train_KF2_no_dup.csv')

    polarity_dict.clear()
    subjectivity_dict.clear()
    text_dict.clear()
    complexity_dict.clear()
    text_with_dup_dict.clear()
    textPath = path.join(d, 'Train_question.csv')
    read_from_csv(textPath)

    print('---------------------Train_question.csv------------------------')
    print(f'Processed {len(text_dict)} lines.')
    print(f'Processed {len(text_with_dup_dict)} lines with dups.')
    write_to_csv( text_dict, complexity_dict, 'Train_question_no_dup.csv')

    polarity_dict.clear()
    subjectivity_dict.clear()
    text_dict.clear()
    complexity_dict.clear()
    text_with_dup_dict.clear()
    textPath = path.join(d, 'Train_resource.csv')
    read_from_csv(textPath)

    print('---------------------Train_resource.csv------------------------')
    print(f'Processed {len(text_dict)} lines.')
    print(f'Processed {len(text_with_dup_dict)} lines with dups.')
    write_to_csv( text_dict, complexity_dict, 'Train_resource_no_dup.csv')

# classifier: https://textblob.readthedocs.io/en/latest/classifiers.html
# sentiment analyzers: https://textblob.readthedocs.io/en/latest/advanced_usage.html#sentiment-analyzers
# API overview: https://textblob.readthedocs.io/en/latest/index.html
