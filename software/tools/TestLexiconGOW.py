from itertools import chain, combinations
import pickle
import sys

def hash_word(word): 
    result = "" 

    return result.join(sorted(word))

# From the itertools page : https://docs.python.org/3/library/itertools.html#itertools-recipes
# Generates all combinations possible

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

# Uses powerset to generate all combinations
# Hashes each element of the combinations
# Removes duplicate
# Returns the list

def generate_combinations(key):

    result = powerset(key)
    result = (hash_word(r) for r in result)

    # Removing duplicates
    result = dict.fromkeys(result)

    return result


def find_included_anagrams(key, anagrams_dic):
    
    combinations = generate_combinations(key)

    result = list()

    for combination_key in combinations:
        if combination_key in anagrams_dic:
            result = result + anagrams_dic[combination_key]

    # Removing duplicates
    result = list(dict.fromkeys(result))

    return result


def test_find_anagrams2(letters):

    path = "../../data/"
    anagrams_dict_file = "anagrams_fr_3_7.bin"
    
    src_file = open(path + anagrams_dict_file, "rb")
    anagram_dic = pickle.load(src_file)
    src_file.close()

    key = hash_word(letters)

    res = find_included_anagrams(key, anagram_dic)

    if len(res) == 0:
        print ("No anagrams found for:", letters)
    else:
        print ("Anagrams for", letters, ":", len(res))

        for i in reversed(range(1, len(letters) + 1)):
            res2 = sorted([word for word in res if len(word) == i])

            if len(res2) != 0:
                print (i, "letters (", len(res2), "):", res2)


if len(sys.argv) != 2:
    print ("Needs anagram letters as an input (capital letters): python TestLexiconGOW.py ABCDEFG")
else:
    test_find_anagrams(sys.argv[1])
