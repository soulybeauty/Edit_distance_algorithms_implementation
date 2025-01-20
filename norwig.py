import re
from collections import Counter
import textdistance
import os
from nltk import word_tokenize
import itertools
import pandas as pd
from memory_profiler import profile
from jellyfish import jaro_similarity
from utils import get_plain_vocabluary

# filtering words from text
def words(text): return re.findall(r'\w+', text.lower())

#word frequency dictionary 
WORDS = Counter(words(open(r'words.txt', encoding='utf-8').read()))

#calculate word frequential probability 
def P(word, N=sum(WORDS.values())):
    return WORDS[word] / N

#function which takes sentence and returns corrected versions as dictionary type ex: slm --> salam;
def correction(sentence):
    words = word_tokenize(sentence)
    suggestions = []
    for index in range(len(words)):
        word = words[index]
        if word != words[-1]:
            merger = word + words[index+1]
            suggestions.append({"probability" : round(P(merger),9), "from": [word,words[index+1]], "to":merger, "cost" :1})
        first,second = candidates(word)["1"], candidates(word)["2"]
        first_prob = sorted(first, key=P)[:3]
        second_prob = sorted(second, key=P)[:3]
        for c in [(1, first_prob), (2, second_prob)]:
            
            for valid in c[1]:
                if c != word:
                    suggestions.append({"probability" : round(P(valid),9), "from":word, "to":valid, "cost" :1 if c[0]==1 else 2 })
    return suggestions

#takes word as input and returns potential corrections for 1 and 2 edit distance;
def candidates(word):
    first = known(edits1(word), word)
    second = known(edits2(word), word)
    return {"1":first, "2":second}

# filters corrections if word is in vocabulary;
def known(words, word): 
    return set(w for w in words if w in WORDS and (w != word)) #or (w!=word and w.lower() == word.lower()

# calculates corrections for 1 edit distance
def edits1(word):
    letters    = 'ABCÇDEƏFGĞHXIİJKQLMNOÖPRSŞTUÜVYZ'.lower()
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    # print("darag" in inserts)
    return set(deletes + transposes + replaces + inserts)

# calculates corrections for 2 edit distance
def edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1))
