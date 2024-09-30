'''
This is the module you'll submit to the autograder.

There are several function definitions, here, that raise RuntimeErrors.  You should replace
each "raise RuntimeError" line with a line that performs the function specified in the
function's docstring.

For implementation of this MP, You may use numpy (though it's not needed). You may not 
use other non-standard modules (including nltk). Some modules that might be helpful are 
already imported for you.
'''

import math
from collections import defaultdict, Counter
from math import log
import numpy as np

# define your epsilon for laplace smoothing here

def baseline(train, test):
    '''
    Implementation for the baseline tagger.
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words, use utils.strip_tags to remove tags from data)
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    flatwords=[element[0] for sublist in train for element in sublist]
    flattag=[element[1] for sublist in train for element in sublist]
    tags = []
    words = []
    for i in range(len(flattag)):
        if flattag[i] not in tags:
            tags.append(flattag[i])

        if flatwords[i] not in words:
            words.append(flatwords[i])
           
        

            
            
    a = dict()
    for word in words:
        a[word] = dict()
        for tag in tags:
            a[word][tag] = 0;
    for word, tag in zip(flatwords, flattag):
        #print(word, tag)
        a[word][tag] += 1
    most_seen_tag = max(set(flattag), key = flattag.count)
    result = test.copy()

    for i in range(len(result)):
        for j in range(len(result[i])):
            if result[i][j] in a.keys():
                dic = a.get(result[i][j])
                #print(dic)
                sorted_dic = dict(sorted(dic.items(), key = lambda x:x[1], reverse = True))
                #print(sorted_dic)
                tag = list(sorted_dic.items())[0]
                #print(tag)
                result[i][j] = (result[i][j], tag[0])
            else:
                result[i][j] = (result[i][j], most_seen_tag)
                
    return result


def viterbi(train, test):
    '''
    Implementation for the viterbi tagger.
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences with tags on the words
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''


    smoothness = 1e-5

    prior = 0.99
    
    tag_word = dict()
    for i in range(len(train)):
        for word, tag in train[i]:
            if tag not in tag_word:
                tag_word[tag] = dict()
            if word not in tag_word[tag]:
                tag_word[tag][word] = 0
            tag_word[tag][word] += 1

   
    tag_tag = dict()
    for i in range(len(train)):
        for j in range(len(train[i])-1):
            tag1 = train[i][j][1]
            tag2 = train[i][j+1][1]
            if tag1 not in tag_tag:
                tag_tag[tag1] = dict()
            if tag2 not in tag_tag[tag1]:
                tag_tag[tag1][tag2] = 0
            tag_tag[tag1][tag2] += 1



            
    for tag in tag_word.keys():
        count = sum(tag_word[tag].values()) + smoothness * len(tag_word[tag].values()) + smoothness
        for word in tag_word[tag].keys():
            tag_word[tag][word] = (smoothness + tag_word[tag][word]) / count
        tag_word[tag]["OOV"] = smoothness / count
      
    for tag1, val in tag_tag.items():
        count = sum(tag_tag[tag1].values()) + smoothness * len(tag_tag[tag1].values()) + smoothness
        for tag2 in tag_tag[tag1].keys():
            tag_tag[tag1][tag2] = (smoothness + tag_tag[tag1][tag2]) / count
        tag_tag[tag1]["OOV"] = smoothness / count

    


    result = []
    for test_case in test:
        root = [dict()]
        dic = [dict()]
        len_tag_word = len(tag_word.keys())
        for tag in tag_word:
            if tag == 'START':
                dic[0][tag] = np.log(prior)
            else:
                dic[0][tag] = np.log((1-prior)/len_tag_word)
                

        
        for i in range(len(test_case) - 1):           
            root.append(dict())
            dic.append(dict())
            
            
        #print('a: ', a)
        
        #print(dic)
        
        for i in range(1, len(test_case)):
            for tag1 in tag_word:
                prob = -999999999
                the_tag = 'None'
                for tag2 in tag_tag:
                    #print(dic[i-1])
                    p = dic[i - 1][tag2]
                    if tag1 in tag_tag[tag2] and test_case[i] in tag_word[tag1]:
                        p += log(tag_tag[tag2][tag1])
                        p += log(tag_word[tag1][test_case[i]])
                    elif tag1 in tag_tag[tag2] and test_case[i] not in tag_word[tag1]:
                        p += log(tag_tag[tag2][tag1])
                        p += log(tag_word[tag1]["OOV"])
                    elif tag1 not in tag_tag[tag2] and test_case[i] in tag_word[tag1]:
                        p += log(tag_tag[tag2]["OOV"])
                        p += log(tag_word[tag1][test_case[i]])
                    elif tag1 not in tag_tag[tag2] and test_case[i] not in tag_word[tag1]:
                        p += log(tag_tag[tag2]["OOV"])
                        p += log(tag_word[tag1]["OOV"])
                    
                    
                    if p > prob:
                        
                        the_tag = tag2
                        
                    prob = max(prob, p)
                   
                        
                        
                        
                dic[i][tag1] = prob
                root[i][tag1] = the_tag

                
        end = "END"
        tags = [end]
        for i in range(len(test_case)-1, 0, -1):
            end = root[i][end]
            tags.append(end)
#         count = len(sentence)
#         while count != 1:
#             end = root[i-1][end]
#             tags.append(end)
#             count -= 1
        #print(tags)
        tags.reverse()
        #print(tags)

        
        l = []
        for w, t in zip(test_case, tags):
            l.append((w, t))
        result.append(l)

    return result
                               
                               
                               
                               


def viterbi_ec(train, test):
    '''
    Implementation for the improved viterbi tagger.
    input:  training data (list of sentences, with tags on the words). E.g.,  [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
            test data (list of sentences, no tags on the words). E.g.,  [[word1, word2], [word3, word4]]
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    raise NotImplementedError("You need to write this part!")



