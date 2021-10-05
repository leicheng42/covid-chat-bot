#!/usr/bin/python
# -*- coding: utf-8 -*-
# Description: 自然语言预处理
# Created: lei.cheng 2021/10/5
# Modified: lei.cheng 2021/10/5

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re
import string


def nlp_pre(text):
    """自然语言预处理"""
    """将文本中出现的字母转化为小写"""
    text = text.lower()

    """删除文本中出现的数字"""
    text = re.sub(r'\d+', '', text)

    """删除标点符号"""
    text = text.translate(str.maketrans('', '', string.punctuation))

    """删除文本前后中出现的空格"""
    text = text.strip()

    """单词符号化"""
    words = word_tokenize(text)

    """删除终止词"""
    stop_words = set(stopwords.words('english'))
    words = [i for i in words if not i in stop_words]

    """词形还原"""
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]

    return words


if __name__ == '__main__':
    text_1 = 'he and Chazz duel with all keys on the line.'
    words_1 = nlp_pre(text_1)
    print(words_1)
