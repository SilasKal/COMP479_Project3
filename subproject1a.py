import nltk
from module1 import read_extract
from helper_functions import output_dic, save_subcorpus
import time


def preprocess(limit_tokens=10000):
    """
    creates sub corpus stored in a dictionary with NEWID of article as a key and list of tokens as the value
    :param limit_tokens: limit of the numbers of tokens in the subcorpus
    :return: dictionary containing NEWID and list of tokens
    """
    counter_terms = 0
    document_dic = {}
    for i in range(22):
        if i < 10:
            dict_000 = read_extract('reuters21578/reut2-00' + str(i) + '.sgm')
        else:
            dict_000 = read_extract('reuters21578/reut2-0' + str(i) + '.sgm')
        for article in dict_000.keys():
            curr_tokens = nltk.word_tokenize(dict_000[article])
            curr_tokens = [token for token in curr_tokens if any(charac.isalnum() for charac in token) and token != '']
            counter_terms += len(curr_tokens)
            document_dic[article] = curr_tokens
            if counter_terms >= limit_tokens:
                diff = limit_tokens - (counter_terms - len(curr_tokens))
                document_dic[article] = curr_tokens[:diff]
                # for document, tokens in document_dic.items():
                #     save_subcorpus(tokens, document+'.txt') # save subcorpus
                return document_dic


def spimi_inspired(document_dic, filepath):
    """
    spimi inspired procedure of creating an index based on dictionary with NEWID and list of tokens
    :return: time taken, created index
    """
    start = time.time()
    index = {}
    for article, tokens in document_dic.items():
        for token in tokens:
            if token in index.keys():
                index[token].add(article)
            else:
                index[token] = {article}
    output_dic(index, filepath)
    end = time.time()
    return end - start, index


def naive_indexer(document_dic, file_path):
    """
    naive indexer, creates list of term-docid pairs and then calls function to create index based on that list
    :param document_dic: subcorpus stored in dic
    :param file_path: filename output file
    :return: time taken, created index
    """
    start = time.time()
    F = []
    for article, tokens in document_dic.items():
        for token in tokens:
            F.append((token, article))
    F_filtered = sorted(list(set(F)), key=lambda x: (x[0], int(x[1])))  # sort and remove duplicates
    index = create_index(F_filtered)
    output_dic(index, file_path)
    end = time.time()
    return end - start, index


def create_index(F):
    """
    creates index from list F
    :param F: sorted and filtered list F
    :return: index
    """
    index = {}
    for element in F:
        if element[0] in index.keys():
            old_postings_list = index[element[0]]
            if isinstance(old_postings_list, int):
                index[element[0]] = [old_postings_list]
            index[element[0]].append(element[1])  # update postings list
        else:
            index[element[0]] = [element[1]]  # add term and postings list
    return index
