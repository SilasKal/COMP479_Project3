from subproject1a import spimi_inspired, naive_indexer, preprocess
from subproject1b import extend_index
from subproject2 import get_query_input

for i in [10000, 100000, 500000]:
    doc_index = preprocess(i)
    print('The SPIMI-inspired indexer is', naive_indexer(
doc_index,'index_naive' + str(i) + '.txt')[0] - spimi_inspired(doc_index, 'index_spimi' + str(i) + '.txt')[0],
'seconds faster than the naive indexer (' + str(i) + ' tokens).')
extend_index('index.txt', 'index_doc.txt')
get_query_input()
