def output_dic_withtf(input_dic, filepath):
    """
    writes index into txt file
    :param input_dic: dictionary with key that are string and values that are floats, lists tuples
    :param filepath: filename of output
    """
    with open(filepath, 'w') as f:
        for key, value in input_dic.items():
            f.write(key + ' ')
            f.write(str(value[0]))
            f.write(' ')
            for docid, tf in value[1:]:
                f.write(docid)
                f.write(' ')
                f.write(str(tf))
                f.write(' ')
            f.write('\n')
    f.close()


def output_dic(input_dic, filepath):
    """
    writes index into txt file
    :param input_dic: dictionary with key that are string and values that are lists of strings
    :param filepath: filename of output
    """
    with open(filepath, 'w') as f:
        for key, value in input_dic.items():
            f.write(key + ' ')
            for docid in value:
                f.write(docid)
                f.write(' ')
            f.write('\n')
    f.close()


def output_docindex(input_dic, filepath):
    """
    writes items from a dictionary into a file
    :param input_dic: dictionary with key that are string and value that is an integer
    :param filepath: filename of output
    :return:
    """
    with open(filepath, 'w') as f:
        for key, value in input_dic.items():
            f.write(str(key) + ' ')
            f.write(str(value))
            f.write('\n')
    f.close()


def read_index(filepath):
    """
    extracts index with tf and idf as a dictionary from a txt file
    :param filepath: filepath of index
    """
    index = {}
    try:
        with open(filepath) as file:
            line = file.readline()
            split_line = line.split(sep=' ')
            if split_line:
                postings_list = [split_line[1]]
                for i in range(2, len(split_line[2:-1]) + 2, 2):
                    # print([split_line[i], split_line[i+1]])
                    postings_list.append((split_line[i], split_line[i + 1]))
                # print(postings_list)
                index[split_line[0]] = postings_list
            while line:
                line = file.readline()
                split_line = line.split(sep=' ')
                if split_line != ['']:
                    postings_list = [split_line[1]]
                    for i in range(2, len(split_line[2:-1]) + 2, 2):
                        postings_list.append((split_line[i], split_line[i + 1]))
                    index[split_line[0]] = postings_list
        file.close()
        return index
    except FileNotFoundError:
        print('No index found at given filepath.')
        return {}


read_index('index.txt')


def read_index_doc(filepath):
    """
    extracts doc index as a dictionary from a txt file
    :param filepath: filepath of index
    """
    index = {}
    try:
        with open(filepath) as file:
            line = file.readline()
            split_line = line.split(sep=' ')
            if split_line:
                index[split_line[0]] = float(split_line[1][:-1])
            while line:
                line = file.readline()
                split_line = line.split(sep=' ')
                if split_line != ['']:
                    index[split_line[0]] = float(split_line[1][:-1])
        file.close()
        # print(index)
        return index
    except FileNotFoundError:
        print('No index found at given filepath.')
        return {}


def save_query_results(result, filepath):
    """
    saves given list of results in txt
    """
    with open(filepath, 'w') as f:
        for docid in result:
            f.write(str(docid) + ' ')
        f.write('\n')
    f.close()


def save_subcorpus(result, filepath):
    """
    saves subcorpus in filepath
    """
    with open(filepath, 'w') as f:
        for token in result:
            f.write(str(token) + '\n')
    f.close()
