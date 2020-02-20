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

def read_from_csv(file_name):
    with open(file_name, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            #print(f'\t line count: {line_count} \t classification: {row["Complexity_level"]} \t text: {row["text"]}.')
            testimonial = TextBlob(row["text"])
            #print(f'\t line count: {line_count} \t polarity: {testimonial.sentiment.polarity} \t subjectivity: {testimonial.sentiment.subjectivity}.')
            polarity_dict[line_count] = testimonial.sentiment.polarity
            subjectivity_dict[line_count] = testimonial.sentiment.subjectivity
            line_count += 1
        print(f'Processed {len(polarity_dict)} lines.')

def read_from_file(file_name):
    with open(file_name,"r", encoding='utf-8') as fp:
        words = fp.read()
    return words

if __name__ == "__main__":
    d = os.getcwd()
    textPath = path.join(d, 'Train_KF_T.csv')
    read_from_csv(textPath)

    polarity_dict = {k: v for k, v in sorted(polarity_dict.items(), key=lambda item: item[1], reverse=True)}
    subjectivity_dict = {k: v for k, v in sorted(subjectivity_dict.items(), key=lambda item: item[1], reverse=True)}

    line_count = 0
    for k, v in polarity_dict.items():
        if line_count < 20:
            print('\t line count: %s \t --- \t polarity: %s' % (k, v))
        else:
            break
        line_count += 1

    line_count = 0
    for k, v in subjectivity_dict.items():
        if line_count < 20:
            print('\t line count: %s \t --- \t subjectivity: %s' % (k, v))
        else:
            break
        line_count += 1
    # print(words)

# classifier: https://textblob.readthedocs.io/en/latest/classifiers.html
# sentiment analyzers: https://textblob.readthedocs.io/en/latest/advanced_usage.html#sentiment-analyzers
# API overview: https://textblob.readthedocs.io/en/latest/index.html
