from nltk import word_tokenize
import itertools
from norwig import P
from utils import get_plain_vocabluary

def cost(source, target, insertion_weight=1, deletion_weight=1, substitution_weight=1):
    if source == target:
        return 0

    n = len(source)
    m = len(target)

    # Initialize the distance matrix
    D = [[0] * (m + 1) for i in range(n + 1)]

    # Initialize the first row and column of the distance matrix
    for i in range(1, n + 1):
        D[i][0] = i * deletion_weight

    for j in range(1, m + 1):
        D[0][j] = j * insertion_weight

    # Compute the edit distance using dynamic programming
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost_of_substitution = substitution_weight
            if source[i-1] == target[j-1]:
                cost_of_substitution = 0

            D[i][j] = min(D[i-1][j] + deletion_weight,
                          D[i][j-1] + insertion_weight,
                          D[i-1][j-1] + cost_of_substitution)
    return D[n][m]

def cost2(source, target, insertion_weight=1, deletion_weight=1, substitution_weight=1, transpose_weight=1):
    if source == target:
        return 0

    n = len(source)
    m = len(target)

    # Initialize the distance matrix
    D = [[0] * (m + 1) for i in range(n + 1)]

    # Initialize the first row and column of the distance matrix
    for i in range(1, n + 1):
        D[i][0] = i * deletion_weight

    for j in range(1, m + 1):
        D[0][j] = j * insertion_weight

    # Compute the edit distance using dynamic programming
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost_of_substitution = substitution_weight
            if source[i-1] == target[j-1]:
                cost_of_substitution = 0

            D[i][j] = min(D[i-1][j] + deletion_weight,
                          D[i][j-1] + insertion_weight,
                          D[i-1][j-1] + cost_of_substitution)

            # Check for transposition
            if i > 1 and j > 1 and source[i-1] == target[j-2] and source[i-2] == target[j-1]:
                D[i][j] = min(D[i][j], D[i-2][j-2] + transpose_weight)

    return D[n][m]
# function which takes sentence and weights per operation as input and returns corrections as dictionary type 
def spelling_correction(sentence, d=1, r=1, s=1, t=1):
    splittedsentence = word_tokenize(sentence)
    merges = []
    for i in range(len(splittedsentence) -1 ):
        merge = splittedsentence[i] + splittedsentence[i+1]
        merges.append(merge)
    suggestions = []
    vocwords = list(itertools.chain.from_iterable([get_plain_vocabluary()]))
    for i,word in enumerate(splittedsentence+merges):
        if (not word.isdigit()): # ignore digits
            levdistances = []
            for vocword in set(vocwords):
                if (len(vocword)-len(word)) > 3:
                    continue
                levdistances.append((cost2(word, vocword, insertion_weight=s, deletion_weight=d, substitution_weight=r, transpose_weight=t),P(vocword),vocword))
            
            values = sorted(levdistances)[:3]

            for value in values:
                print(values)
                suggestions.append({"from":word, "to": value[2], "probability":value[1], "cost":value[0]})
    return suggestions


# print(cost2("yorlu", "yorul", 1, 1, 1, 0.6))
# print(cost("otagima", "İtaliya", 1,8,9))
# insert, delete, substitute