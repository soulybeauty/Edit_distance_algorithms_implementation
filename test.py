from damerau_levenshtein import spelling_correction as sp1
from levenshtein_distance import spelling_correction as sp2
from norwig import correction as sp3
from weighted_edit_distance import spelling_correction as sp4

# Test cases
easy_unit_tests = [(["işig"], "işıq"), (["dünəkni"],"dünənki"), (["mənm"], "mənim"), (["sehra"], "səhra"), (["günəşh"], "günəş"), (["salm"], "salam"), (["düny"], "dünya"), (['layihə'], "lahiyə"), (["sagollaşmaq"],"sağollaşmaq")]
hard_unit_tests = [(["isig"], "işıq"), (["darg"], ["daraq", "dar"]), (["yorlu"], "yorul"), (["alşıq"], "alqış"), ([""], ""), (), (), (), (), ()]
edge_unit_tests = [("ishıq", "işıq"), ("82ci", "82-ci"), ("ev de", "evde"), ("ali", "Ali"), ("get gel", "get-gəl"), ("hergun", "her gun"), ("iki-2", "iki-iki")]

# Function to transpose adjacent characters in a word
def wordTransposer(word):
    chars = list(word)
    outs = []
    l = len(chars)
    for i in range(l-2):
        r = chars[i+1] + chars[i] + "".join(chars[i+1:])
        outs.append(r)
    return outs

# Function to create one-character misspellings of a word
def wordOneCharMisspell(word):
    import random
    letters = list('ABCÇDEƏFGĞHXIİJKQLMNOÖPRSŞTUÜVYZ '.lower())
    chars = list(word)
    outs = []
    l = len(chars)
    for i in range(l):
        r = "".join(chars[:i]) + random.choice(letters) + "".join(chars[i+1:])
        outs.append(r)
    return outs

# Function to delete one character from a word
def wordOneCharDelete(word):
    chars = list(word)
    outs = []
    l = len(chars)
    for i in range(l):
        r = "".join(chars[:i]) + "".join(chars[i+1:])
        outs.append(r)
    return outs

# Spelling correction models and their names
spellers = [sp1, sp2, sp3, sp4]
names = ["optimized", "basic", "norwig", "weighted"]
models = list(zip(spellers, names))

# Function to perform unit testing on a speller using word packs
def unit_tester(speller, word_pack):
    spellerName = speller[1]
    speller = speller[0]
    count = 0
    outs = []
    print("Process start:.")
    print(word_pack)
    for wordp in word_pack:
        print(wordp)
        if wordp:
            for word_test in wordp[0]:
                result = speller(word_test)
                print(result)
                for r in result:
                    outs.append(r['to'])
                if wordp[1] in outs:
                    print(wordp[1])
                    print(outs)
                    count += 1
    return spellerName + "-->" + f"{round(100*count/len(word_pack), 3)} accurate"

# Perform unit testing on different models with different word packs
for speller in models:
    print(unit_tester(speller, hard_unit_tests))
