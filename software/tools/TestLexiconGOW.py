import pickle
import sys

def hash_word(word): 
    result = "" 

    return result.join(sorted(word))

def test_find_anagrams(letters):

    path = "../../data/"
    included_anagrams_dict_file = path + "included_anagrams_fr_3_7.bin"

    
    src_file = open(included_anagrams_dict_file, "rb")
    anagram_dic = pickle.load(src_file)
    src_file.close()

    key = hash_word(letters)

    if key not in anagram_dic:
        print ("No anagrams found for:", letters)
    else:
        print ("Anagrams for", letters, ":", len(anagram_dic[key]))

        for i in reversed(range(1, len(letters) + 1)):
            res = sorted([word for word in anagram_dic[key] if len(word) == i])

            if len(res) > 1:
                print (i, "letters (", len(res), "):", res)
        



if len(sys.argv) != 2:
    print ("Needs anagram letters as an input (capital letters): python TestLexiconGOW.py ABCDEFG")
else:
    test_find_anagrams(sys.argv[1])
