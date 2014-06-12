from delphin.codecs import simplemrs
from delphin.mrs import Xmrs
import xml.etree.ElementTree as ET
from collections import defaultdict
import re
import sys


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
                # start = len(nltk.word_tokenize(text.split(aspect.get('term'))[0]))
                # end = start + len(nltk.word_tokenize(aspect.get('term'))) - 1

                data[text].append((aspect.get('term'), aspect.get('polarity'), sentence.get('id')))

    return data


# def read_mrs(data_file):
#
#     lines = open(data_file, 'r').readlines()
#     for i in range(0, len(lines)):





class MRS_Feature_Extractor():


    IGNORE = ['udef_q_rel', 'proper_q_rel', 'named_rel', 'pron_rel', 'pronoun_q_rel']
    mrses = {}





    def __init__(self, data, mrs_file, data_file, out_file, pos_words, neg_words):

        self.pos_words = pos_words
        self.neg_words = neg_words
        self.out_file = open(out_file, 'w')




        # populate mrs hash
        counter = 0
        lines = open(mrs_file, 'r').readlines()
        while not counter >= len(lines):
            line = lines[counter]
            split = line.strip().split(' ')
            id = int(split[len(split) - 1])
            test = lines[counter + 1].split()
            if test[0] == 'SENT:':
                counter += 2
                if counter < len(lines):
                    mrs = lines[counter]
                    self.mrses[id] = mrs
                    counter += 4
            else:
                counter += 5

        for sentence in data:
            for aspect in data[sentence]:
                self.process_mrs(sentence, aspect)



    def process_mrs(self, sentence, aspect):

        id = int(aspect[2])
        if id in self.mrses:
            mrs = self.mrses[id]
            self.features = defaultdict(int)

            self.out_file.write(str(id) + ' "' + aspect[0] + '" ')

            try:
                m = simplemrs.loads(mrs)
                # m = simplemrs.deserialize(mrs) # read in a line of MRS


                for ep_obj in m.select_eps(): # get EPs

                    ep1 = str(ep_obj.pred)

                    if not ep1 in self.IGNORE:

                        ep1_replacement = self.get_replacement(ep1, pos_words, neg_words)

                        for arg in ep_obj.args:

                            to_crawl = []
                            to_crawl.append(arg.value)

                            argname = arg.argname

                            argvalue = str(arg.value)
                            if argvalue[0] == 'h':
                                # print('handle var ' + argvalue + ' ' + ep1)
                                hc = m.get_hcons(arg.value)
                                if hc is not None:
                                    lo = hc.lo
                                    # print('qeqed ' + str(lo))
                                    to_crawl.append(lo)
                                    # print (str(to_crawl))
                            for var in to_crawl:

                                share_label = m.select_eps(None, None, var, None)

                                for ep2_obj in m.select_eps(None, var, None, None) + share_label:

                                    ep2 = str(ep2_obj.pred)
                                    ep2_replacement = self.get_replacement(ep2, file)


                                    # triples
                                    self.add_triples(ep1, ep2, ep1_replacement, ep2_replacement, argname)

                for feat in self.features:
                    self.out_file.write(feat + ' ' + str(self.features[feat]) + ' ')

                self.out_file.write('\n')

            except:
                sys.stderr.write('PROBLEM MRS: ' + sentence + ' ' + mrs)
                self.out_file.write('\n')


    def add_triples(self, ep1, ep2, ep1_replacement, ep2_replacement, argname):


        if not ep2 is ep1:

            # @1: no replacement
            self.features[ep1 + '&' + argname + '&' + ep2] += 1

            # # @2: first pred replacement
            # if not ep1_replacement == None:
            #     self.features[ep1_replacement + '&' + argname + '&' + ep2] += 1
            #
            # # @3: second pred replacement
            # if not ep2_replacement == None:
            #     self.features[ep1 + '&' + argname + '&' + ep2_replacement] +=1

            # # @4: both
            # if not ep1_replacement == None and not ep2_replacement == None:
            #     self.features[ep1_replacement + '&' + argname + '&' + ep2_replacement] += 1
            #
            #  # @5: both preds open-class r-preds
            # if ep1.startswith('"') and ep2.startswith('"'):
            #     self.features[ep1 + '&' + argname + '&' + ep2] += 1



    def get_replacement(pred, file, pos_terms, neg_terms):


        if pred.startswith('"'):
            split = pred.split('_')
            word = split[1]
            try:
                remove = split[3]
                pred = pred.replace(remove, '')
            except:
                sys.stderr.write(str(sys.exc_info()[0]) +' ' + str(sys.exc_info()[1]) + ' ' + str(sys.exc_info()[2]) + '\n')
                sys.stderr.write(pred + ' ' + file + '\n')
            if re.match(pos_terms, word):
                return "POS"
            elif re.match(neg_terms, word):
                return "NEG"
            else:
                return None


    def print_feats(self, id, aspect):

        for feat in self.features:
            self.out_file.write(feat + ':' + str(self.features[feat]) + ' ')





def load_sentistrength(file):
    pos_terms = ''
    neg_terms = ''


    for line in open(file):
        split = line.split('\t')
        term = split[0].replace('*', '\w*')
        if int(split[1]) > 0:
            pos_terms += term + '|'
            #sent_terms['pos'].add(term)
        else:
            neg_terms += term + '|'
            # sent_terms['neg'].add(term)

    return pos_terms[:-1], neg_terms[:-1]


sentistength_file = open('../lib/EmotionLookupTable.txt', 'r')
pos_words, neg_words = load_sentistrength('../lib/EmotionLookupTable.txt')


train_mrs_file = '../data/ABSA_MRS_train'
test_mrs_file = '../data/ABSA_MRS_test'
train_file = '../data/train/laptop--train.xml'
test_file = '../data/test/laptop--test.gold.xml'
train_out = "../data/mrs_feats_train"
test_out = "../data/mrs_feats_test"


train_data = read_data(train_file)
test_data = read_data(test_file)

extractor = MRS_Feature_Extractor(train_data, train_mrs_file, train_file, train_out, pos_words, neg_words)
extractor = MRS_Feature_Extractor(test_data, test_mrs_file, test_file, test_out, pos_words, neg_words)




#
# extractor.process_file(train, train_out)
# extractor.process_file(test, test_out)







