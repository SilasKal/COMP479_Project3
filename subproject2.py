from helper_functions import read_index_doc, read_index, save_query_results


# import heapq # not necessary because of change in design


def single_query_processor(term, index_filename):
    """
    returns the list of documentsID in which the single term can be found in
    :param term: single term
    :param index_filename: filename of index which should be used for the query
    :return: list of documentIDs in which the term can be found in
    """
    index = read_index(index_filename)
    result = []
    if term in index.keys():
        for (document, _) in index[term][1:]:
            result.append(document)
        print(len(result), 'documents contain the term \'' + term + '\':', result)
        return result
    else:
        print('No document contains the term \'' + term + '\'.')
        return ''


def or_query_processor(terms, index_filename):
    """
    returns the list of documentsID in which the at least one of the terms can be found in ordered by how many of the
    terms the document contains
    :param terms: list of terms
    :param index_filename: filename of index which should be
    used for the query
    :return: list of documentIDs in which the term can be found in
    """
    index = read_index(index_filename)
    result = []
    dict_how_many = {}
    for term in terms:
        if term in index.keys():
            for (document, _) in index[term][1:]:
                result.append(document)
                if document in dict_how_many:
                    dict_how_many[document].append(term)
                else:
                    dict_how_many[document] = [term]
    for key, value in dict_how_many.items():
        dict_how_many[key] = len(set(value))
    result = list(set(result))
    result.sort(key=lambda k: (dict_how_many[k], -int(k)), reverse=True)
    if result:
        print(len(result), 'documents contain at least one of the terms ' + str(terms) + ': ' + str(result))
        return result
    else:
        print('No document contains at least one of the terms ' + str(terms) + '.')
        return ''


def and_query_processor(terms, index_filename):
    """
    returns the list of documentsID in which all terms can be found in ordered by documentID
    :param terms: list of terms
    :param index_filename: filename of index which should be used for the query
    :return: list of documentIDs in which the term can be found in
    """
    index = read_index(index_filename)
    postings_lists = []
    for term in terms:
        curr_postings_list = []
        if term in index.keys():
            for (document, _) in index[term][1:]:
                curr_postings_list.append(document)
        postings_lists.append(set(curr_postings_list))
    result = postings_lists[0].intersection(*postings_lists)
    result = list(result)
    result.sort(key=int)
    if result:
        print(len(result), 'documents contain the terms ' + str(terms) + ': ' + str(result))
        return result
    else:
        print('No document contains the terms ' + str(terms) + '.')
        return ''


def tf(term, document, index):
    """
    returns tf of term in given document and index
    """
    for (docid, termf) in index[term][1:]:
        if docid == document:
            return int(termf)
    return 0


def bm25query(terms, index_filename, index_doc_filename):
    """
    returns top 10 ranked documents based on BM25 formula
    :param terms: list of terms in the query
    :param index_filename: filename of index which should be used for the query
    :param index_doc_filename: filename of index where the length of the documents is stored
    :return: list of top10 documentIDs order by BM25
    """
    index = read_index(index_filename)
    index_doc = read_index_doc(index_doc_filename)
    k1 = 1.25
    b = 0.8
    lav = index_doc['lav']
    document_list = list(index_doc.keys())[:-1]
    result = []
    for document in document_list:
        ld = index_doc[document]
        score = 0
        for term in terms:
            if term in index.keys():
                idf_term = float(index[term][0])
                tf_term = float(tf(term, document, index))
                try:
                    score += idf_term * ((tf_term * (k1 + 1)) / (tf_term + k1 * ((1 - b) + b * (ld / lav))))
                except ZeroDivisionError:
                    pass
        result.append((document, score))
        # heapq.heappush(h, (-score, document)) # design change used heap before to only return top 10 results
        # since it is required to return the whole ranked list of documents using a heap does not make any sense
    # result = []
    # for i in range(10):
    #     result.append(heapq.heappop(h))
    # print('Top 10 documents for your query ' + ':' + str(result).)
    result.sort(key=lambda x: x[1], reverse=True)
    ranked_docs = [docid for (docid, score) in result]
    print('Ranked List of documents according to BM25: ', str(ranked_docs))
    return ranked_docs


def get_query_input():
    """
    implements query search in console
    """
    print('started query processor')
    user_input = input(
        'Type 1 for BM25 ranked retrieval, 2 for an AND query, 3 for an OR query, 4 for a single keyword query, '
        't for the test queries and stop for ending the query. \n')
    while user_input not in ['1', '2', '3', '4', 'stop', 't']:
        print('You mistyped. Try again. ')
        user_input = input(
            'Type 1 for BM25 ranked retrieval, 2 for an AND query, 3 for an OR query, 4 for a single keyword query, '
            't for the test queries and stop for ending the query. \n')
    else:
        if user_input == 'stop':
            pass
        elif user_input == 't':
            test_queries()
            get_query_input()
        else:
            user_input2 = input('Enter the term/terms you want to search for. ')
            terms = user_input2.split()
            terms = [token for token in terms if
                     any(charac.isalnum() for charac in token) and token != '']  # TODO check if it makes sense
            if user_input == '1':
                bm25query(terms, 'index.txt', 'index_doc.txt')
                get_query_input()
            elif user_input == '2':
                and_query_processor(terms, 'index.txt')
                get_query_input()
            elif user_input == '3':
                or_query_processor(terms, 'index.txt')
                get_query_input()
            elif user_input == '4':
                if len(terms) == 1:
                    single_query_processor(terms[0], 'index.txt')
                else:
                    print('Please enter just one single term. ')
                get_query_input()


def test_queries():
    for idx, terms in enumerate([['Democrats’', 'welfare', 'and', 'healthcare', 'reform', 'policies'],
                                 ['Drug', 'company', 'bankruptcies'], ['George', 'Bush']]):
        print(terms)
        save_query_results(bm25query(terms, 'index.txt', 'index_doc.txt'), 'bm25_test_' + str(idx) + '.txt')
        save_query_results(and_query_processor(terms, 'index.txt'), 'AND_test_' + str(idx) + '.txt')
        save_query_results(or_query_processor(terms, 'index.txt'), 'OR_test_' + str(idx) + '.txt')
    save_query_results(single_query_processor('article', 'index.txt'), 'singlekeyword_sample_query.txt')
    save_query_results(bm25query(['average', 'net', 'profits'], 'index.txt', 'index_doc.txt'), 'bm25_sample_query.txt')
    save_query_results(and_query_processor(['San', 'Francisco'], 'index.txt'), 'AND_sample_query.txt')
    save_query_results(or_query_processor(['Czech', 'Republic', 'Luxembourg'], 'index.txt'), 'OR_sample_query.txt')

# print(bmi25query(['average', 'net', 'profits'], 'index.txt', 'index_doc.txt'))
# or_query_processor(['Showers', 'test_word'], 'index.txt')
# or_query_processor(['Czech', 'Republic', 'Luxembourg'], 'index.txt')
