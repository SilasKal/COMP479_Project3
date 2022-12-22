def read_extract(input_filepath):
    """
    reads in a given input file and extracts the body of all articles
    returns the body of each article paired with the article's NEWID in a dictionary
    this function is made to be used for reuters collection articles and only works for them properly
    :param input_filepath: filename of index
    """
    article_information = ''
    extract = False
    articles = []
    article_ids = []
    try:
        with open(input_filepath) as file:
            line = file.readline()
            while line:
                line = file.readline()
                if line.strip().startswith('<REUTERS'):  # extract all text after <REUTERS
                    for index, c in enumerate(line.strip()):
                        if c == 'N' and line[index:index + 6] == 'NEWID=':  # extract NEWID
                            article_ids.append(line[index + 7:-3])
                    extract = True
                if line.strip().startswith('</REUTERS>'):  # stop extracting after </REUTERS>
                    articles.append(article_information)
                    article_information = ''
                    extract = False
                if extract:
                    article_information += ' ' + line.strip()
        extract_body = False
        articles_with_body = {}
        for index_article, article in enumerate(
                articles):  # extracting the bodies from the whole information of the articles
            curr_body = ''
            for index, letter in enumerate(article):
                if letter == '<':
                    if article[index:index + 6] == '<BODY>':  # start extracting after <BODY>
                        extract_body = True
                if extract_body:
                    curr_body += letter
                    if article[index:index + 7] == '</BODY>':  # stop extracting after </BODY>
                        extract_body = False
            articles_with_body[article_ids[index_article]] = curr_body[6:-5]  # update dictionary with body and NEWID
        return articles_with_body
    except FileNotFoundError:
        print('File at that filepath does not exist. An empty output file will be created.')
        return {}
