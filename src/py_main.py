import xml.etree.ElementTree as ET
import sys
from collections import defaultdict
import nltk
from nltk.corpus import wordnet as wn

if len(sys.argv) > 1:
    train, test = sys.argv[1], sys.argv[2]
    train_out = "mallet_files/train"
    test_out = "mallet_files/test"
else:
    train = '../data/train/laptop--train.xml'
    test = '../data/test/laptop--test.gold.xml'
    train_out = "../mallet_files/train"
    test_out = "../mallet_files/test"




# def n_gram_window(sentence, start, end, n):
#
#
#






def n_grams_dumb(sentence, n):
    
    results = ''
    counts = defaultdict(int)
    
    toks = nltk.word_tokenize(sentence.encode('utf-8'))
    
    for i in range (0, len(toks) - n):
        n_gram = toks[i]
        for j in range(1, n):
            n_gram += '_' + toks[i+j]
            
        counts[n_gram] += 1

    for item in counts:
        results += item + ':' + str(counts[item]) + ' ' 
        
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

            # print aspect[0].encode("utf-8")


            # expanding by adding synonyms of adjectives
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
                                out_file.write(lemma.name.split(".")[0]+":"+'1 ')
                                seen.add(lemma.name.split(".")[0])

            # write every unigram from the sentence
            out_file.write(n_grams_dumb(sentence, 1))
            

            counter += 1

            out_file.write("\n")

# main


train = read_data(train)
test = read_data(test)

train_out = open(train_out, 'w')
test_out = open(test_out, 'w')

process_file(train, train_out)
process_file(test, test_out)
