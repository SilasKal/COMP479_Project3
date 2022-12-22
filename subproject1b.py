from math import log

import nltk

from helper_functions import output_dic_withtf, output_docindex
from module1 import read_extract


def extend_index(file_path_idx, file_path_doc):
    """
    creates an index with the following structure term->idf, [(docID, tf), ..] and an index where the length of every
    document is stored
    :param file_path_idx: filename of output file for index
    :param file_path_doc: filename of ouput file for docindex
    :return: created index, created docindex
    """
    index = {}
    num_articles = 0
    index_document = {}
    sum_len_articles = 0
    for i in range(22):
        if i < 10:
            dict_000 = read_extract('reuters21578/reut2-00' + str(i) + '.sgm')
        else:
            dict_000 = read_extract('reuters21578/reut2-0' + str(i) + '.sgm')
        print('document ' + str(i))
        for article in dict_000.keys():
            curr_article = dict_000[article]
            num_articles += 1
            tokens = nltk.word_tokenize(curr_article)
            tokens = [token for token in tokens if any(charac.isalnum() for charac in token) and token != '']
            len_article = len(tokens)
            index_document[article] = len_article
            sum_len_articles += len_article
            tf_dic = {}
            for token in tokens:
                if token in tf_dic.keys():
                    tf_dic[token] += 1
                else:
                    tf_dic[token] = 1
            for term, tf in tf_dic.items():
                if term in index.keys():
                    index[term].append((article, tf))
                else:
                    index[term] = [(article, tf)]
    for key in index:
        index[key].insert(0, round(log(num_articles / len(index[key])), 2))  # calculate idf and insert into index
    len_avg_articles = round(sum_len_articles / num_articles, 2)
    index_document['lav'] = len_avg_articles
    output_docindex(index_document, file_path_doc)
    output_dic_withtf(index, file_path_idx)
    return index, index_document
