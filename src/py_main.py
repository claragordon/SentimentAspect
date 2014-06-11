import xml.etree.ElementTree as ET
import sys
from collections import defaultdict
import nltk
from nltk.corpus import wordnet as wn
import re
import string
from nltk.stem.porter import *
from mrs_features import *
# from stat_parser import Parser

if len(sys.argv) > 1:
    train, test = sys.argv[1], sys.argv[2]
    train_out = "mallet_files/train"
    test_out = "mallet_files/test"
    sentistength_file = open('lib/EmotionLookupTable.txt', 'r')
    # citation: http://jmlr.org/papers/volume5/lewis04a/a11-smart-stop-list/english.stop
    stoplist_file = open('lib/stoplist.txt', 'r')
    swear_file =open('lib/swearWords.txt', 'r')

else:
    train = '../data/train/laptop--train.xml'
    test = '../data/test/laptop--test.gold.xml'
    train_out = "../mallet_files/train"
    test_out = "../mallet_files/test"
    sentistength_file = open('../lib/EmotionLookupTable.txt', 'r')
    stoplist_file = open('../lib/stoplist.txt', 'r')
    swear_file =open('../lib/swearWords.txt', 'r')

#TODO


# presence/absence of but or something clever with the number of aspects and conjunctions

# number of negation terms in sentence (or window)
# number of other valence shifters (if we can find a list of them somewhere)
# improve the negation
# other kinds of expansion?


# sent_terms = defaultdict(set)
pos_terms = ''
neg_terms = ''
stopwords = set()
allowed_words = set() # words with freq above a certain threshold

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

                # get word-tokenized indices of start and end of aspect range
                start = len(nltk.word_tokenize(text.split(aspect.get('term'))[0]))
                end = start + len(nltk.word_tokenize(aspect.get('term'))) - 1

                data[text].append((aspect.get('term'), aspect.get('polarity'), start, end, aspect.get('from'), aspect.get('to')))

    return data



# load data from outside resources

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


def load_swear_words(file):
    data = file.read().strip().split("\n")
    return data

def load_stopwords(file):
    stopword_temp = set()
    for line in file:
        stopword_temp.add(line.strip())
    return stopword_temp


def threshold(train, test, threshold):
    counts = defaultdict(int)
    for sentence in train:
        words = nltk.word_tokenize(sentence.encode('utf-8'))
        for word in words:
            counts[word] += 1

    for sentence in test:
        words = nltk.word_tokenize(sentence.encode('utf-8'))
        for word in words:
            counts[word] += 1

    for word in counts:
        if counts[word] > threshold:
            allowed_words.add(word)


def count_neg(sentence):
    sentence = nltk.word_tokenize(sentence.encode('utf-8'))
    return "neg_count:"+str(len([word for word in sentence if word in neg_words]))+" "

# return the location of the aspect in the sentence (location = words away from from sentence start)
def aspect_loc(sentence, aspect):
    result = ''
    sentence = sentence.encode('utf-8')
    s_len = len(nltk.word_tokenize(sentence))

    back = s_len - aspect[3] - 1
    front = aspect[2]

    if front < 4:
        result += "first_four:1 "
    elif back < 4:
        result += "last_four:1 "
    else:
        result += "middle:1 "
    return result


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

    # pos ratios: nn/jj and vb/rb
    nn, jj, vb, rb, = 0.0, 0.0, 0.0, 0.0
    for pos in pos_counts:
        if 'NN' in pos:
            nn += pos_counts[pos]
        if 'JJ' in pos:
            jj += pos_counts[pos]
        if 'VB' in pos:
            vb += pos_counts[pos]
        if 'RB' in pos:
            rb += pos_counts[pos]

    if jj != 0:
        result = result + "nn_jj_ratio:" + str(nn/jj)+" "
    if rb != 0:
        result = result + "vb_rb_ratio:" + str(vb/rb)+" "
    return result


def valence_heuristics(sentence, intensifier):

    if intensifier:
        vocab = intensifiers
        marker = 'intensifier'
    else:
        vocab = diminishers
        marker = 'diminisher'


    activated = False
    delims = "?.,!:;"
    sequence = []
    words = nltk.word_tokenize(sentence)

    for word in words:
        # stripped = word.strip(delchars)
        word = word.lower()
        term = marker + '_' + word if (activated and not re.match(r'\W+', term)) else word #put in not_prepended if state is negative, regular if not
        sequence.append(term)

        # flip negation if another negator is encountered
        if word in vocab:
            activated = not activated

        # flip negation if a delimiter is encountered
        if any(c in word for c in delims):
            activated = False

    return ' '.join(sequence)



def negate_sequence(sentence):

    negation = False
    delims = "?.,!:;"
    negated_sequence = []
    words = nltk.word_tokenize(sentence)

    for word in words:
        # stripped = word.strip(delchars)
        stripped = word.lower()
        negated = "not_" + stripped if (negation and not re.match(r'\W+', negated)) else stripped #put in not_prepended if state is negative, regular if not
        negated_sequence.append(negated)

        # flip negation if another negator is encountered
        if any(neg in word for neg in ["not", "n't", "no"]):
            negation = not negation

        # flip negation if a delimiter is encountered
        if any(c in word for c in delims):
            negation = False


    return ' '.join(negated_sequence)

# prepend VERY
def intensify_sequence(sentence):
    sentence = sentence.encode('utf-8')
    negation = False
    delims = "?.,!:;"
    negated_sequence = []
    words = sentence.split()

    for word in words:
        # stripped = word.strip(delchars)
        stripped = word.strip(delims).lower()
        negated = "very_" + stripped if negation else stripped #put in not_prepended if state is negative, regular if not
        negated_sequence.append(negated)

        # flip negation if another negator is encountered
        if word in intensifiers:
            negation = not negation

        # flip negation if a delimiter is encountered
        if any(c in word for c in delims):
            negation = False

    result = ''
    for word in negated_sequence:
        result = result+word+":1 "
    return result

# prepend BARELY
def diminish_sequence(sentence):
    sentence = sentence.encode('utf-8')
    negation = False
    delims = "?.,!:;"
    negated_sequence = []
    words = sentence.split()

    for word in words:
        # stripped = word.strip(delchars)
        stripped = word.strip(delims).lower()
        negated = "barely_" + stripped if negation else stripped #put in not_prepended if state is negative, regular if not
        negated_sequence.append(negated)

        # flip negation if another negator is encountered
        if word in diminishers:
            negation = not negation

        # flip negation if a delimiter is encountered
        if any(c in word for c in delims):
            negation = False

    result = ''
    for word in negated_sequence:
        result = result+word+":1 "

    return result




def sentistrength_expansion(term):

    if re.match(pos_terms, term):
        return "POS"
    elif re.match(neg_terms, term):
        return "NEG"
    else:
        return term





def char_grams(sentence, aspect, n, backoff=False, stopword=False, POS=False, aspect_replace=False, threshold=False):
    sentence = sentence.encode('utf-8')
    sentence = sentence.replace(" ", '@')
    toks = list(sentence)
    return assemble_ngrams(toks, n, stopword, threshold)

def pos_grams(sentence, aspect, n, backoff=False, stopword=False, POS=False, aspect_replace=False, threshold=False):
    sentence = sentence.encode('utf-8')
    sentence = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(sentence)
    toks = [item[1] for item in tagged]
    return assemble_ngrams(toks, n, backoff, stopword)

def stem_sentence(sentence):
    stemmer = PorterStemmer()
    # sentence = sentence.encode('utf-8')
    result = ''
    for word in nltk.word_tokenize(sentence):
        result += stemmer.stem(word) + " "
    return result

def assemble_ngrams(toks, n, stopword, threshold):

    results = ''
    counts = defaultdict(int)


    for i in range (0, len(toks) - n + 1):
        n_gram = toks[i]
        for j in range(1, n):

            n_gram += '_' + toks[i+j]

        counts[n_gram] += 1

    for item in counts:
        count = counts[item]
        if not threshold or (threshold and item in allowed_words):
            if not stopword or (stopword and not item in stoplist):
                # remove punc-only tokens
                #     if not re.match(r'\W+', item):
                results += item.lower() + ':' + str(count) + ' '

    return results

def ngrams(sentence, aspect, n, backoff=False, stopword=False,
                POS=False, aspect_replace=False, threshold=False, distance=False, window=0):


    if aspect_replace:
        sentence = string.replace(sentence, aspect[0], 'ASPECT')


    toks = nltk.word_tokenize(sentence.encode('utf-8'))

    if backoff:
        for i in range (0, len(toks)):
            toks[i] = sentistrength_expansion(toks[i])

    if POS:
        pos_tagged = nltk.pos_tag(toks)
        for i in range (0, len(toks)):
            toks[i] = toks[i] + '_' + pos_tagged[i][1]

    if distance:
        len_asp = len(nltk.word_tokenize(aspect[0]))
        i = aspect[2] - 1
        j = aspect[3] + 1
        counter = 1
        while i > -1 or j < len(toks):
            if i > -1:
                toks[i] = toks[i] + '_' + str(counter)
            if j < len(toks):
                toks[j] = toks[j] + '_' + str(counter)
            i -= 1
            j += 1
            counter += 1


    if window > 0:
        toks = ngrams_window(toks, aspect, window, distance)

    return assemble_ngrams(toks, n, stopword, threshold)


def ngrams_window(toks, aspect, window, distance):



    asp_start = aspect[2]
    asp_end = aspect[3]
    len_asp = asp_end - asp_start + 1
    left_idx = asp_start - window
    right_idx = asp_end + window
    if left_idx < 0:
        left_idx = 0
    if right_idx > len(toks):
        right_idx = len(toks)

    slice = toks[left_idx:right_idx + 1]

    return slice

# this now returns a tuple of the result and also a set of all synonyms
def wordnet_expansion(sentence):

    results = ''
    text = nltk.word_tokenize(sentence.encode("utf-8"))
    seen = set()
    pos = nltk.pos_tag(text)
    for tup in pos:
        # print tup
        if tup[1] in ['JJ']:
            if len(wn.synsets(tup[0])) > 0:
                syn = wn.synsets(tup[0]) #first synset for adjective
                for lemma in syn:
                    if lemma.name.split(".")[0] not in seen:
                        # print str(lemma.name.split(".")[0])
                        results += lemma.name.split(".")[0]+":"+'1 '
                        seen.add(lemma.name.split(".")[0])
    return (results, seen)

def aspect_feat(aspect):
    result = 'aspect=' + '_'.join(aspect[0].encode('utf-8').split()) + ' '
    return result


def post_expansion_backoff(sentence):
    result = ''
    terms = wordnet_expansion(sentence)[1]
    counts = defaultdict(int)
    for term in terms:
        counts[sentistrength_expansion(term)] += 1
        # result += sentistrength_expansion(term)+":1 "
    for k in counts:
        result += k+":"+str(counts[k])+" "
    return result

def swear_count(sentence):
    sentence = nltk.word_tokenize(sentence.encode('utf-8'))
    return "swear_count:"+str(len([word for word in sentence if word in swear_words]))+" "

def swear_near(sentence, aspect):
    sentence = sentence.encode('utf-8')
    aspect = aspect[0].encode('utf-8').split()[0]

    front = sentence.split(aspect)[0].split()[-3:]
    back = sentence.split(aspect)[1].split()[:3]

    if any(word for word in front if word in swear_words):
        return "swear_near:1 "
    elif any(word for word in back if word in swear_words):
        return "swear_near:1 "
    else:
        return "swear_near:0 "


def other_aspects(sentence, all_aspects, aspect):

    results = ''


    for asp_candidate in all_aspects:
        if not asp_candidate[0] == aspect[0]:
            results += aspect[0] + '_' + str(abs(int(asp_candidate[2]) - int(aspect[2]))) + ' '

    return results.encode('utf-8')






# aspect_tuple = (text, polarity, from, to)
def process_file(dict, out_file):

    counter = 0

    for sentence in dict:
        # print sentence.encode("utf-8")
        for aspect in dict[sentence]:
            out_file.write('Aspect' + str(counter) + ' ' + aspect[1].encode('utf-8')+" ") # write label

            # # INDIVIDUAL FEATURE TESTS
            #
            # 1
            # out_file.write(ngrams(sentence, aspect, 1))
            #
            # 2
            # out_file.write(ngrams(sentence, aspect, 2))
            #
            # 3
            #
            # out_file.write(ngrams(sentence, aspect, 3))
            #
            #
            # 4
            # out_file.write(ngrams(sentence, aspect, 1, POS=True))
            #
            # 5
            # out_file.write(ngrams(sentence, aspect, 2, POS=True))
            #
            # 6
            # out_file.write(ngrams(sentence, aspect, 1, backoff=True))
            #
            # # 7
            # out_file.write(ngrams(sentence, aspect, 2, backoff=True))x
            #
            # 8
            # out_file.write(ngrams(sentence, aspect, 2, aspect_replace=True))
            #
            # 9
            # out_file.write(ngrams(sentence, aspect, 1, threshold=True))
            #
            # 10
            # out_file.write(ngrams(sentence, aspect, 1, distance=True))
            #
            # 11
            # stemmed = stem_sentence(sentence)
            # out_file.write(ngrams(stemmed, aspect, 1))
            #
            # 12
            # stemmed = stem_sentence(sentence)
            # out_file.write(ngrams(stemmed, aspect, 2))
            #
            # 13
            # out_file.write(pos_grams(sentence, aspect, 2))
            #
            # 14
            # out_file.write(char_grams(sentence, aspect, 4))
            #
            # 15
            # out_file.write(char_grams(sentence, aspect, 5))
            #
            # 16
            # out_file.write(char_grams(sentence, aspect, 6))
            #
            # 17
            # negated = negate_sequence(sentence)
            # out_file.write(ngrams(negated, aspect, 1))
            #
            # 18
            # negated = negate_sequence(sentence)
            # out_file.write(ngrams(negated, aspect, 2))
            #
            # # 19
            # intense = valence_heuristics(sentence, True)
            # out_file.write(ngrams(intense, aspect, 1))
            #
            # # 20
            # intense = valence_heuristics(sentence, True)
            # out_file.write(ngrams(intense, aspect, 2))
            #
            # # 21
            # dimin = valence_heuristics(sentence, False)
            # out_file.write(ngrams(dimin, aspect, 1))
            #
            # # 22
            # dimin = valence_heuristics(sentence, False)
            # out_file.write(ngrams(dimin, aspect, 2))
            #
            # #23
            # out_file.write(ngrams(sentence, aspect, 1, window=5))
            #
            # #24
            # out_file.write(ngrams(sentence, aspect, 2, window=5))
            #
            # #25
            # out_file.write(ngrams(sentence, aspect, 3, window=5))
            #
            #
            # #26
            # out_file.write(ngrams(sentence, aspect, 1, window=7))
            #
            # #27
            # out_file.write(ngrams(sentence, aspect, 2, window=7))
            #
            # #28
            # out_file.write(ngrams(sentence, aspect, 3, window=7))
            #
            # 29
            # out_file.write(swear_near(sentence, aspect))
            #
            # #30
            # out_file.write(swear_count(sentence))
            #
            # #31
            # out_file.write(aspect_feat(aspect))
            #
            # #32
            # out_file.write(sentence_stats(sentence))
            #
            # #33
            # out_file.write(wordnet_expansion(sentence)[0])
            #
            # #34
            # out_file.write(post_expansion_backoff(sentence))
            #
            # # WINDOW TESTS
            #
            # 35
            # out_file.write(ngrams(sentence, aspect, 1, window=3))
            #
            # 36
            # out_file.write(ngrams(sentence, aspect, 1, window=4))
            #
            # 37
            # out_file.write(ngrams(sentence, aspect, 1, window=6))
            #
            # 38
            # out_file.write(ngrams(sentence, aspect, 1, window=8))
            # # write every bigram from the sentence
            # out_file.write(ngrams_dumb(sentence, aspect, 2))

            #39
            # stemmed = stem_sentence(sentence)
            # out_file.write(ngrams(stemmed, aspect, 1, window=7))

            #40
            # negated = negate_sequence(sentence)
            # out_file.write(ngrams(negated, aspect, 1, window=7))

            #41
            # intense = valence_heuristics(sentence, True)
            # out_file.write(ngrams(intense, aspect, 1, window=7))

            #42
            # dimin = valence_heuristics(sentence, False)
            # out_file.write(ngrams(dimin, aspect, 1, window=7))

            #43
            # out_file.write(ngrams(sentence, aspect, 1, window=7, distance=True))

            #44
            # out_file.write(ngrams(sentence, aspect, 1, window=7, POS=True))

            #45
            # stemmed = stem_sentence(sentence)
            # out_file.write(ngrams(stemmed, aspect, 1, window=7))
            #
            # negated = negate_sequence(sentence)
            # out_file.write(ngrams(negated, aspect, 1, window=7))
            #
            #
            # intense = valence_heuristics(sentence, True)
            # out_file.write(ngrams(intense, aspect, 1, window=7))
            #
            #
            # dimin = valence_heuristics(sentence, False)
            # out_file.write(ngrams(dimin, aspect, 1, window=7))
            #
            #
            # out_file.write(ngrams(sentence, aspect, 1, window=7, distance=True))
            #
            # out_file.write(ngrams(sentence, aspect, 1, window=7, POS=True))

            #46
            # out_file.write(aspect_loc(sentence, aspect))

            #47
            # out_file.write(swear_near(sentence, aspect))
            # out_file.write(sentence_stats(sentence))
            # out_file.write(aspect_loc(sentence, aspect))
            # out_file.write(aspect_feat(aspect))

            #48
            # stemmed = stem_sentence(sentence)
            # out_file.write(ngrams(stemmed, aspect, 1, window=7, distance=True))

            #49
            # stemmed = stem_sentence(sentence)
            # out_file.write(ngrams(stemmed, aspect, 1, window=7))
            # out_file.write(ngrams(sentence, aspect, 1, POS=True))

            #50
            # stemmed = stem_sentence(sentence)
            # intense = valence_heuristics(stemmed, True)
            # dimin = valence_heuristics(intense, False)
            # # print ngrams(dimin, aspect, 1, window=7)
            # out_file.write(ngrams(dimin, aspect, 1, window=7))

            #51
            # stemmed = stem_sentence(sentence)
            # intense = valence_heuristics(stemmed, True)
            # dimin = valence_heuristics(intense, False)
            # # print ngrams(dimin, aspect, 1, window=7)
            # out_file.write(ngrams(dimin, aspect, 1, window=7, distance=True))


            #52
            # stemmed = stem_sentence(sentence)
            # out_file.write(ngrams(stemmed, aspect, 1, window=7))
            # out_file.write(swear_near(sentence, aspect))
            # out_file.write(sentence_stats(sentence))
            # out_file.write(aspect_loc(sentence, aspect))
            # out_file.write(aspect_feat(aspect))

            #53
            # stemmed = stem_sentence(sentence)
            # out_file.write(ngrams(stemmed, aspect, 1, window=7))
            # out_file.write(aspect_feat(aspect))
            # # write position of aspect in sentence
            # out_file.write(aspect_loc(sentence, aspect))


            counter += 1


            out_file.write("\n")

# main



pos_terms, neg_terms = load_sentistrength(sentistength_file)
stoplist = load_stopwords(stoplist_file)
neg_words = ["no", "not", "can't", "cannot", "never", "won't", "shouldn't", "don't", "nothing", "non", "isn't", "aint", "doesn't", "couldn't", "shouldn't", "without", "minus", "sans", "nor", "neither", "nought"]
intensifiers = ["so", "very", "super", "extremely", "uber", "so many", "unbelievably", "ridiculously", "really", "so much", "high", "highly", "absolutely", "pretty", "totally", "completely", ]
diminishers = ["little", "barely", "hardly", "not even", "only", "partially", "somewhat", "kind of", "kinda", "a bit", "a little"]
swear_words = load_swear_words(swear_file)


train = read_data(train)
test = read_data(test)

train_out = open(train_out, 'w')
test_out = open(test_out, 'w')

threshold(train, test, 5)

process_file(train, train_out)
process_file(test, test_out)
