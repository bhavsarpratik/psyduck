import os
import re

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from unidecode import unidecode

def get_text_from_html_file(file_path):
    return BeautifulSoup(open(file_path, mode='rt', encoding='utf-8'), 'html.parser').get_text()


def remove_numbers(val):
    m = re.findall(r'([A-Za-z]\w+)', val, flags=re.I)
    return ' '.join(m)


def remove_months(val):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December', 'Jan', 'Feb', 'Mar', 'Apr', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    regex_string = r'' + '|'.join(months)
    return re.sub(regex_string, 'month', val, flags=re.I)


def remove_small_words(val):
    m = re.findall(r'[a-zA-Z]{3,}', val, flags=re.I)
    return ' '.join(m)


def replace_numbers(x, replace_with='num'):
    return re.sub(r'[0-9\,]+', replace_with, x)


def remove_brackets_and_newline(x):
    return re.sub(r'[\n()]+', ' ', x)


def remove_roman_from_datapoints_1(val):
    val = str(val).strip()
    val = val.strip()
    match_char = re.search(r'\(\w\)', val[:7])
    match_digit = re.search(r'\d', val[:3])
    match_2_char = re.search(r'\(\w\w\)', val[:7])
    match_3_char = re.search(r'\(\w\w\w\)', val[:7])
    match_2_digit = re.search(r'\d\d', val[:3])

    if match_char is not None:
        val = " ".join(val.split(match_char.group())[1:]).strip()
    elif match_digit is not None:
        val = " ".join(val.split(match_digit.group())[1:]).strip()
    elif match_2_char is not None:
        val = " ".join(val.split(match_2_char.group())[1:]).strip()
    elif match_3_char is not None:
        val = " ".join(val.split(match_3_char.group())[1:]).strip()
    elif match_2_digit is not None:
        val = " ".join(val.split(match_2_digit.group())[1:]).strip()
    elif val[:7].find('.') != -1:
        val = " ".join(val.split('.')[1:]).strip()
    if val[:7].find(')') != -1:
        val = " ".join(val.split(')')[1:]).strip()
    if val.lower() == '[total]':
        val = 'Total'
    return val


def remove_roman_from_datapoints_2(val):
    val = str(val).strip()
    match_char_1 = re.search(r'\{\w\}', val[:7])
    match_char_2 = re.search(r'\(\w\}', val[:7])
    match_s_patt = re.search(r'\(\w\b', val[:7])

    match_s_1 = re.search(r'\w\}', val[:5])

    if match_char_1 is not None:
        val = " ".join(val.split(match_char_1.group())[1:]).strip()
    elif match_char_2 is not None:
        val = " ".join(val.split(match_char_2.group())[1:]).strip()
    elif match_s_patt is not None:
        val_list = val.split(match_s_patt.group())
        if len(val_list[0]) <= 3:
            val = " ".join(val.split(match_s_patt.group())[1:]).strip()
        else:
            val = val[1:]
    elif match_s_1 is not None:
        val = " ".join(val.split(match_s_1.group())[1:]).strip()

    val_list = val.split(" ")
    if len(val_list[0]) == 1 or val_list[0].lower() in ['ii', 'iii', 'iv', 'vi', 'vii', 'viii', 'ix']:
        val = " ".join(val_list[1:]).strip()
    if match_s_1 is not None:
        val = " ".join(val.split(match_s_1.group())[1:]).strip()
    return val

def remove_roman_numbers(val):
    regex_string = r"\b(\(*)(?=[MDCLXVI])M{0,3}(?:D|D?C{1,3}|C[DM])?(?:L|L?X{1,3}|X[LC])?(?:V|V?I{1,3}|I[VX])?(\)*)\b"
    return re.sub(regex_string, '', val, flags=re.I)

def truncate_text(x, max_len):
    return x[:max_len] if len(x) > max_len else x


def unicode_to_ASCII(val):
    """For converting special characters to ASCII."""
    return unidecode(val)


def remove_roman_numbers_sentence(sent):
    regex_string = "^(\(*)(?=[MDCLXVI])M{0,3}(?:D|D?C{1,3}|C[DM])?(?:L|L?X{1,3}|X[LC])?(?:V|V?I{1,3}|I[VX])?(\)*)$"
    processed=[]
    for token in sent.split():
            processed.append(re.sub(regex_string, '', token, flags=re.I))
    sent=" ".join(processed)
    return sent


def text_cleaner(x):
    """Text processor for preparation, train and predict."""
    for pp in [unicode_to_ASCII, remove_numbers, remove_months, remove_small_words, remove_roman_numbers, remove_brackets_and_newline]:
        x = pp(x)
    return x.lower()


def remove_char(x, pos=4):
    return x[:pos] + x[(pos + 1):]


def replace_char(x, pos=4, replace_char='z'):
    return x[:pos] + replace_char + x[(pos + 1):]


def remove_simple_roman_numbers(val):
    for sym in ['(ii)', '(iii)', '(iv)', '(vi)', '(vii)', '(viii)', '(ix)']:
        val=val.replace(sym,"")
    return val

def remove_newline(x):
    return re.sub(r'[\n]+', ' ', x)

def process_parenthesis(inputstring):
    char1 = "("
    char2 = ")"
    substrings = []
    intstart = 0
    strlength = len(inputstring)
    continueloop = 1
    if (inputstring.__contains__(char1) and inputstring.__contains__(char2)):
        while (intstart < strlength and continueloop == 1):
            intindex1 = inputstring.find(char1, intstart)
            if (intindex1 != -1):
                intindex1 = intindex1 + len(char1)
                intindex2 = inputstring.find(char2, intindex1)
                if (intindex2 != -1):
                    subsequence = inputstring[intindex1:intindex2]
                    substrings.append(subsequence)
                    intstart = intindex2 + len(char2)
                else:
                    continueloop = 0
            else:
                continueloop = 0
    else:
        return inputstring

    for word in substrings:
        if (len(word) < 2):
            start = inputstring.index(word) - 1
            stop = start + len(word) + 1
            if len(inputstring) > stop:
                inputstring = inputstring[0: start:] + inputstring[stop + 1::]

    return inputstring.strip() 
