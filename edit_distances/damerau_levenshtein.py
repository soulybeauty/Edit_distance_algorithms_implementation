from nltk import word_tokenize
import itertools
from norwig import P
from utils import get_plain_vocabluary



# Function to calculate Levenshtein distance between two strings
def Levenshtein(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]



# Function to perform spelling correction on a sentence
def spelling_correction(sentence):
    splittedsentence = word_tokenize(sentence)
    suggestions = []
    merges = []
    vocwords = list(itertools.chain.from_iterable([get_plain_vocabluary()]))

    for i in range(len(splittedsentence) - 1):
        merge = splittedsentence[i] + splittedsentence[i+1]
        merges.append(merge)

    for i, word in enumerate(splittedsentence+merges):
        if not word.isdigit():  # ignore digits
            levdistances = []
            for vocword in set(vocwords):
                if vocword == word:
                    continue
                levdistances.append((Levenshtein(word, vocword), round(P(word), 9), vocword))
            values = sorted(levdistances)[:3]
            for value in values:
                suggestions.append({"from": word, "to": value[2], "probability": value[1], "cost": value[0]})
                
    return suggestions


print(spelling_correction("işiq otaqima dusdu"))
vocab = get_plain_vocabluary()
# # assert 'otağıma' in vocab, "not";
# assert 'işıq' in vocab, "not";
# assert 'düşdü' in vocab, "not";
