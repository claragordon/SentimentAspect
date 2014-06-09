
import nltk
import subprocess
import os
import sys
from collections import defaultdict
import xml.etree.ElementTree as ET


def read_data(data_file):

    data = defaultdict(list)

    xml = ET.parse(data_file)
    root = xml.getroot()

    for sentence in root.iter('sentence'):
        text = sentence.find('text').text # need to get sentence id
        id = sentence.get('id')
        aspects = sentence.find('aspectTerms').findall('aspectTerm')
        if aspects != None:
            for aspect in aspects:
                data[(text, id)].append((aspect.get('term'), aspect.get('polarity'), aspect.get('from'), aspect.get('to')))

    return data

# if len(sys.argv) > 1:
#     data_dir = sys.argv[1]
#     location = sys.argv[2] # this is the location of ace
# else:
data_dir = "../data/train/"
location = "/Users/jaredkramer/PycharmProjects/SentimentAspect/src/ace-0.9.17/"

# main

with open("ABSA_MRS", 'w') as out_file:
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    for file in os.listdir(data_dir):
        out_file.write("<file: "+file+">\n")
        in_data = read_data(data_dir + file)
        for sentence_tup in in_data:
            sentence = sentence_tup[0].encode('utf-8')
            id = sentence_tup[1]
            out_file.write(" ".join([sentence, id, "\n"]))
            p1 = None
            p2 = None

            try:
                # print "".join([location, "ace"])
                # print "".join([location, "erg.dat"])
                p1 = subprocess.Popen(["echo", '"'+sentence+'"'], stdout=subprocess.PIPE)
                p2 = subprocess.Popen(["".join([location, "ace"]), "-g", "".join([location, "erg.dat"]), '-r root_formal root_informal root_frag root_inffrag', "-1T"], stdin=p1.stdout, stdout=subprocess.PIPE)
            except:
                print "failed"
                continue
            mrs = p2.communicate()
            out_file.write(mrs[0])
            out_file.write("\n")

        # print p2.communicate()



    #     out_file = open(dir+doc_num+"MRS", 'w')
    #     for i in range (0, len(results)):
    #         # if len(results) == 0:
    #         #     ## what to do here???
    #         #     out_file.write(data[i]+ '\n')
    #         #     out_file.write('\n')
    #
    #         result = results[i][0]
    #         prelim = result.split()
    #         split = result.split('\n')
    #         if len(prelim) < 2:
    #             out_file.write(data[i] + '\n')
    #             out_file.write('\n')
    #         elif prelim[0] == "SENT:":
    #             out_file.write(split[0].strip()[7:-1] + '\n')
    #             out_file.write(split[1].strip() + '\n')
    #         else:
    #             out_file.write(split[0].strip()[7:-1] + '\n')
    #             out_file.write('\n')
    #     out_file.close()
    #

