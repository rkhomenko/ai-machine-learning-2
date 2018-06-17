import numpy as np, json
from nltk import stem, tokenize, corpus

with open('good_comments_shuffle.json', 'r') as good_file:
    good = json.load(good_file)['comments']
with open('bad_comments_shuffle.json', 'r') as bad_file:
    bad = json.load(bad_file)['comments']

vocabulary_index = 0
vocabulary = {}

def tokenize_comment(comment, voc, voc_index):
    tokenizer = tokenize.RegexpTokenizer(r'\w+')
    stemmer = stem.SnowballStemmer('russian')
    result = []
    for sent in tokenize.sent_tokenize(comment):
        filtered = [word for word in tokenizer.tokenize(sent) \
                if word not in corpus.stopwords.words('russian')]
        stemmed = [stemmer.stem(word) for word in filtered]
        for word in stemmed:
            if voc.get(word) == None:
                voc[word] = voc_index
                voc_index += 1
        result += stemmed
    return voc_index, result

good_stemmed = []
bad_stemmed = []

for comment in good:
    vocabulary_index, stemmed = tokenize_comment(comment, vocabulary, vocabulary_index)
    good_stemmed.append(stemmed)

for comment in bad:
    vocabulart_index, stemmed = tokenize_comment(comment, vocabulary, vocabulary_index)
    bad_stemmed.append(stemmed)

def make_word_bags(comments, voc):
    result = []
    count = 1
    for comment in comments:
        print('Comment', count, 'from', len(comments))
        count += 1
        arr = {}
        for word in comment:
            index = voc.get(word)
            if arr.get(index) == None:
                arr[index] = 1
            else:
                arr[index] += 1
        result.append(arr)
    return result

good_bags = make_word_bags(good_stemmed, vocabulary)
bad_bags = make_word_bags(bad_stemmed, vocabulary)

with open('good_bags.json', 'w') as out_file:
    json.dump({'lenght': len(vocabulary), 'bags': good_bags}, out_file, indent=4)

with open('bad_bags.json', 'w') as out_file:
    json.dump({'lenght': len(vocabulary), 'bags': bad_bags}, out_file, indent=4)
