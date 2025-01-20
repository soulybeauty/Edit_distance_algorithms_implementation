from nltk import word_tokenize
import itertools
from norwig import P
from utils import get_plain_vocabluary

# Calculate the Levenshtein distance between two strings
def levenshtein_distance(s1, s2):
    # Initialize the dimensions of the input strings
    m = len(s1)
    n = len(s2)

    # Base cases
    if m == 0:
        return n
    if n == 0:
        return m

    # Calculate the cost based on the last characters of the strings
    if s1[m-1] == s2[n-1]:
        cost = 0
    else:
        cost = 1

    # Recursive calls with deletion, insertion, and substitution operations
    return min(
        levenshtein_distance(s1[:m-1], s2) + 1,
        levenshtein_distance(s1, s2[:n-1]) + 1,
        levenshtein_distance(s1[:m-1], s2[:n-1]) + cost
    )

# Check if a word has a suffix by comparing it with a list of suffixes
def check_suffix(word):
    with open('suffixes.txt', "r", encoding='utf-8') as f:
        suffixes = f.read().split('\n')
        if word in suffixes:
            return True
        else:
            return False

# Perform spelling correction on a given sentence
def spelling_correction(sentence):
    splittedsentence = word_tokenize(sentence)
    suggestions = []
    merges = []
    vocwords = list(itertools.chain.from_iterable([get_plain_vocabluary()]))
    for i in range(len(splittedsentence) -1 ):
        merge = splittedsentence[i] + splittedsentence[i+1]
        merges.append(merge)
    special_words = []
    final = splittedsentence
    for i, word in enumerate(final):
        if word.isdigit() or word.isdecimal():
            try:
                special_words.append(final[i+1])
            except:
                continue
        if not word.isdigit():
            if word in special_words:
                if check_suffix(word):
                    suggestions.append({"from":f"{word}, {final[i-1]}", "to": final[i-1]+'-'+word, "probability":1, "cost":1})
                    for vocword in set(vocwords):
                        if vocword == word:
                            continue
                        levdistances.append((levenshtein_distance(word, vocword), vocword, round(P(word),9)))
                    values = sorted(levdistances)[:10]
                    for v in values:
                        if check_suffix(v[1]):
                            suggestions.append({"from":word, "to": value[1], "probability":value[2], "cost":value[0]})
                    continue
            levdistances = []
            for vocword in set(vocwords):
                if vocword == word:
                    continue
                levdistances.append((levenshtein_distance(word, vocword), vocword, round(P(word),9)))
            values = sorted(levdistances)
            for value in values:
                suggestions.append({"from":word, "to": value[1], "probability":value[2], "cost":value[0]})
    return suggestions

# Test cases
# print(spelling_correction("salam necesen"))
# print(spelling_correction("işiq otagima"))
# vocab = get_plain_vocabluary();
# assert 'otağıma' in vocab, "not";
# assert 'işıq' in vocab, "not";
# assert 'düşdü' in vocab, "not";
