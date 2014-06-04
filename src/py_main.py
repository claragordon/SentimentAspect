import xml.etree.ElementTree as ET
import sys
from collections import defaultdict
import nltk
from nltk.corpus import wordnet as wn
import re
import string
from stat_parser import Parser

if len(sys.argv) > 1:
    train, test = sys.argv[1], sys.argv[2]
    train_out = "mallet_files/train"
    test_out = "mallet_files/test"
    sentistength_file = open('lib/EmotionLookupTable.txt', 'r')
    # citation: http://jmlr.org/papers/volume5/lewis04a/a11-smart-stop-list/english.stop
    stoplist_file = open('lib/stoplist.txt', 'r')

else:
    train = '../data/train/laptop--train.xml'
    test = '../data/test/laptop--test.gold.xml'
    train_out = "../mallet_files/train"
    test_out = "../mallet_files/test"
    sentistength_file = open('../lib/EmotionLookupTable.txt', 'r')
    stoplist_file = open('../lib/stoplist.txt', 'r')



# sent_terms = defaultdict(set)
pos_terms = ''
neg_terms = ''
stopwords = set()




# return the location of the aspect in the sentence (location = words away from from)
def aspect_loc(sentence, aspect):
    sentence = sentence.encode('utf-8')
    aspect = aspect[0].encode('utf-8')
    return len(sentence.split(aspect)[0].split())


# return the closest adjective (distance = words away), also return the polarity of that adj
# returns a tuple of (distance to closest adj, (word, POS))
def closest_adj(sentence, aspect):
    loc = aspect_loc(sentence, aspect)
    sentence = nltk.word_tokenize(sentence.encode('utf-8'))
    aspect = aspect[0].encode('utf-8')
    pos = nltk.pos_tag(sentence)
    min = (999, '')
    for word in pos:
        if word[1] in ['JJ']:
            distance = abs(loc - sentence.index(word[0]))
            if distance < min:
                min[0], min[1] = distance, word
    return min

# return various stats, like number of words, number of POS, number of capital letters, number of punctuation marks
def sentence_stats(sentence):
    sentence = sentence.encode('utf-8')
    result = "length:"+str(len(nltk.word_tokenize(sentence)))+" " # number of tokens in sentence+

    # counts for each POS
    pos_counts = defaultdict(int)
    pos = nltk.pos_tag(nltk.word_tokenize(sentence))
    # print pos
    for tagged_word in pos:
        pos_counts[tagged_word[1]] += 1
        # print tagged_word[0], tagged_word[1], pos_counts[tagged_word[1]]
    for k in pos_counts:
        result = result + k+"_count:"+str(pos_counts[k])+" "
    # print result

    result = result + "cap_count:"+str(len([c for c in sentence if c.isupper()]))+" " # number of capital letters in sentence

    result = result + "punc_count:"+str(len([c for c in sentence if c in string.punctuation]))+" " # number of punctuation marks in sentence

    return result

def pos_grams():
    return




# prepend NOT
def negate():
    return

def negate_sequence(sentence):
    sentence = sentence.encode('utf-8')
    negation = False
    delims = "?.,!:;"
    negated_sequence = []
    words = sentence.split()

    for word in words:
        # stripped = word.strip(delchars)
        stripped = word.strip(delims).lower()
        negated = "not_" + stripped if negation else stripped #put in not_prepended if state is negative, regular if not
        negated_sequence.append(negated)

        # flip negation if another negator is encountered
        if any(neg in word for neg in ["not", "n't", "no"]):
            negation = not negation

        # flip negation if a delimiter is encountered
        if any(c in word for c in delims):
            negation = False

    result = ''
    for word in negated_sequence:
        result = result+word+":1 "

    return result

# prepend VERY or BARELY, can't find a list of these, don't want to build one, acl wiki is down at the moment
def valence_shifters():
    return

def load_sentistrength(file):
    pos_terms = ''
    neg_terms = ''


    for line in file:
        split = line.split('\t')
        term = split[0].replace('*', '\w*')
        if int(split[1]) > 0:
            pos_terms += term + '|'
            #sent_terms['pos'].add(term)
        else:
            neg_terms += term + '|'
            # sent_terms['neg'].add(term)


    return pos_terms[:-1], neg_terms[:-1]


def load_stopwords(file):

    stopword_temp = set()
    for line in file:
        stopword_temp.add(line.strip())
    return stopword_temp


def sentistrength_expansion(term):

    if re.match(pos_terms, term):
        return "POS"
    elif re.match(neg_terms, term):
        return "NEG"
    else:
        return term


def assemble_ngrams(toks, n, backoff, stopword, POS, aspect_replace):

    results = ''
    counts = defaultdict(int)

    for i in range (0, len(toks)):
        toks[i] = sentistrength_expansion(toks[i])

    for i in range (0, len(toks) - n):
        n_gram = toks[i]
        for j in range(1, n):
            n_gram += '_' + toks[i+j]

        counts[n_gram] += 1

    for item in counts:
        count = counts[item]
        if not stopword or (stopword and not item in stoplist):
            # remove punc-only tokens
            if not re.match(r'\W+', item):
                results += item.lower() + ':' + str(count) + ' '

    return results


def ngrams_dumb(sentence, aspect, n, backoff=False, stopword=False, POS=False, aspect_replace=False):

    toks = []

    if aspect_replace:
        sentence = string.replace(sentence, aspect[0], 'ASPECT')

    if POS:
        pos_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))
        for item in pos_tagged:
            toks.append(item[0] + '_' + item[1])
    else:
        toks = nltk.word_tokenize(sentence.encode('utf-8'))
    return assemble_ngrams(toks, n, backoff, stopword, POS, aspect_replace)


def ngrams_window(sentence, aspect, start, end, n, window, backoff=False, stopword=False, POS=False, aspect_replace=False, distance=False):

    # pos_mappings = {}
    # if POS:
    #     pos_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))
    #     for item in pos_tagged:
    #         pos_mappings[item[0].lower] = item[1]



    first_half = nltk.word_tokenize(sentence[:start])
    second_half = nltk.word_tokenize(sentence[end:])

    if distance:
        counter = 1
        for i in range (len(first_half) - 1, -1, -1):
            first_half[i] = first_half[i] + '_' + str(counter)
            counter +=1
        counter = 1
        for i in range(0, len(second_half)):
            second_half[i] = second_half[i] + '_' + str(counter)
            counter += 1


    if len(first_half) > window:
        first_half = first_half[len(first_half) - window:]

    if len(second_half) > window:
        second_half = second_half[:len(second_half) - window + 1]

    first_half = ['before_' + k for k in assemble_ngrams(first_half, n, backoff, stopword, POS, aspect_replace).split()]
    second_half = ['after_' + k for k in assemble_ngrams(second_half, n, backoff, stopword, POS, aspect_replace).split()]

    return ' '.join(first_half) + ' ' + ' '.join(second_half)


def wordnet_expansion(sentence):

    results = ''

    text = nltk.word_tokenize(sentence.encode("utf-8"))
    seen = set()
    pos = nltk.pos_tag(text)
    for tup in pos:
        # print tup
        if tup[1] in ['JJ', 'RB']: # or adv?
            if len(wn.synsets(tup[0])) > 0:
                syn = wn.synsets(tup[0]) #first synset for adjective
                for lemma in syn:
                    if lemma.name.split(".")[0] not in seen:
                        # print str(lemma.name.split(".")[0])
                        results += lemma.name.split(".")[0]+":"+'1 '
                        seen.add(lemma.name.split(".")[0])

    return results



# takes a file name and returns a dict of text -> list of aspect tuples
def read_data(data_file):

    data = defaultdict(list)

    xml = ET.parse(data_file)
    root = xml.getroot()

    for sentence in root.iter('sentence'):
        text = sentence.find('text').text
        aspects = sentence.find('aspectTerms').findall('aspectTerm')
        if aspects != None:
            for aspect in aspects:
                data[text].append((aspect.get('term'), aspect.get('polarity'), aspect.get('from'), aspect.get('to')))

    return data

# aspect_tuple = (text, polarity, from, to)
def process_file(dict, out_file):
    
    counter = 0

    for sentence in dict:
        # print sentence.encode("utf-8")
        for aspect in dict[sentence]:
            out_file.write('Aspect' + str(counter) + ' ' + aspect[1].encode('utf-8')+" ") # write label

            # expanding by adding synonyms of adjectives
            out_file.write(wordnet_expansion(sentence))

            # write every unigram from the sentence
            out_file.write(ngrams_dumb(sentence, 1, False))

            # write every bigram from the sentence
            out_file.write(ngrams_dumb(sentence, 2, False))

            # write window ngrams
            out_file.write(ngrams_window(sentence, aspect, int(aspect[2]), int(aspect[3]), 1, 7, False))

            # write sentence stats
            out_file.write(sentence_stats(sentence))

            # DUMB NGRAMS

            # write every unigram from the sentence
            # out_file.write(ngrams_dumb(sentence, aspect, 1))
            #
            # #write every unigram from the sentence, stopword removal
            # out_file.write(ngrams_dumb(sentence, aspect, 1, stopword=True))
            #
            # #write every unigram from the sentence, sentiment backoff
            # out_file.write(ngrams_dumb(sentence, aspect, 1, backoff=True))
            #
            # #write every unigram from the sentence, sentiment backoff and stopword removal
            # out_file.write(ngrams_dumb(sentence, aspect, 1, backoff=True, stopword=True))
            #
            # # write every bigram from the sentence
            # out_file.write(ngrams_dumb(sentence, aspect, 2))


            # write every unigram from the sentence
            # out_file.write(ngrams_dumb(sentence, aspect, 1, backoff=True))
            # out_file.write(ngrams_dumb(sentence, aspect, 2, backoff=True))
            # out_file.write(ngrams_dumb(sentence, aspect, 3, backoff=True))

            # WINDOW NGRAMS

            out_file.write(ngrams_window(sentence, aspect, int(aspect[2]), int(aspect[3]), 1, 20, distance=True))

            # write window ngrams
            #out_file.write(ngrams_window(sentence, aspect, int(aspect[2]), int(aspect[3]), 1, 5))

            # write window unigrams, stopword removal
            # out_file.write(ngrams_window(sentence, aspect, int(aspect[2]), int(aspect[3]), 1, 7, stopword=True))

            # write window unigrams, sentiment backoff
            #out_file.write(ngrams_window(sentence, aspect, int(aspect[2]), int(aspect[3]), 1, 7, backoff=True))

            # # write window unigrams, sentiment backoff
            # out_file.write(ngrams_window(sentence, aspect, int(aspect[2]), int(aspect[3]), 1, 7, backoff=True, stopword=True ))


            # # expanding by adding synonyms of adjectives
            #out_file.write(wordnet_expansion(sentence))


            #
            # # write sentence stats
            # out_file.write(sentence_stats(sentence))
            #
            # # negation hueristics
            # out_file.write(negate_sequence(sentence))
            #
            # # write position of aspect in sentence
            # out_file.write("distance:"+str(aspect_loc(sentence, aspect))+" ")
            #

            counter += 1

            out_file.write("\n")

# main


pos_terms, neg_terms = load_sentistrength(sentistength_file)
stoplist = load_stopwords(stoplist_file)

train = read_data(train)
test = read_data(test)

train_out = open(train_out, 'w')
test_out = open(test_out, 'w')

process_file(train, train_out)
process_file(test, test_out)
