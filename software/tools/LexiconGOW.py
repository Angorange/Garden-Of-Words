# Angorange 2019
# Quick and Dirty script to generate lexicon in the needed format

# trim_lexicon : keeps only words within a given range length
# group_by_anagrams : groups words by exact anagrams (same length, same letters)
# group_by_included_anagrams : group words by included anagrams (same letters, but can be shorter words)

from itertools import chain, combinations
import pickle

# Opens text file src_name containing one word per line
# and writes in dst_name the ones containing between min_letter and max_letter

def trim_lexicon(src_name, dst_name, min_letter, max_letter):

    print("Generate: " + dst_name)
    print("Keep only word from " + str(min_letter) + " letters to " + str(max_letter) + " letters")

    srcFile = open(src_name, "r")
    allLines = srcFile.readlines()
    srcFile.close()

    dstFile = open(dst_name, "w")

    stats = [0] * (max_letter + 1)
    total = 0

    for line in allLines:
        word_length = len(line) - 1 # removing return line character '\n'
        
        if word_length >= min_letter and word_length <= max_letter:
            stats[word_length] += 1
            total += 1
            dstFile.write(line)

    dstFile.close()

    print("Total word: " +str(total))

    for index in range (min_letter, max_letter + 1):
        print(str(index) + " letters words: " + str(stats[index]))



def hash(word): 
    result = "" 

    return result.join(sorted(word))

# Open text file src_name containing one word per line
# groups word by anagrams in a dict (same letters, same length)
# save the dict to dst_name


def group_by_anagrams(src_name, dst_name):

    print("Generate: " + dst_name)

    srcFile = open(src_name, "r")
    allLines = srcFile.readlines()
    srcFile.close()

    d = dict()

    for line in allLines:
        word = line.strip()
        key = hash(word)

        if key not in d: 
            d[key] = [] # Creates the entry if it does not exist yet
        d[key].append(word)
    
    dstFile = open(dst_name,"wb")
    pickle.dump(d, dstFile, pickle.HIGHEST_PROTOCOL)
    dstFile.close()


    max_friends = 0

    stats = [0] * 100

    for i, (k, v) in enumerate(d.items()):
        anagram_count = len(v)

        if anagram_count < len(stats):
            stats[anagram_count] += 1
        elif (anagram_count > max_friends):
            max_friends += anagram_count

    print("Number of entry : " + str(len(d)))

    for index in range (len(stats)):
        if stats[index] != 0:
            print("Entry with " + str(index) + " anagrams: " + str(stats[index]))
    
    if max_friends != 0:
        print ("!!! Need to increment stats to: " + str(max_friends) + " !!!")


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

    result = (hash(r) for r in result)

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


def group_by_included_anagrams(anagrams_src_filename, dst_filename):

    print("Generate: " + dst_filename)

    srcFile = open(anagrams_src_filename, "rb")
    anagrams_dic = pickle.load(srcFile)
    srcFile.close()

    included_anagrams_dic = dict()

    for key in anagrams_dic.keys():
        included_anagrams_dic[key] = find_included_anagrams(key, anagrams_dic)


    dstFile = open(dst_filename, "wb")
    pickle.dump(included_anagrams_dic, dstFile, pickle.HIGHEST_PROTOCOL)
    dstFile.close()

    max_friends = 0

    stats = [0] * 100

    for i, (k, v) in enumerate(included_anagrams_dic.items()):
        anagram_count = len(v)

        if anagram_count < len(stats):
            stats[anagram_count] += 1
        elif (anagram_count > max_friends):
            max_friends += anagram_count

    print("Number of entry : " + str(len(included_anagrams_dic)))

    for index in range (len(stats)):
        if stats[index] != 0:
            print("Entry with " + str(index) + " anagrams: " + str(stats[index]))
    
    if max_friends != 0:
        print ("!!! Need to increment stats to: " + str(max_friends) + " !!!")




def create_JDM_files():
    minLength = 3
    maxLength = 7

    path = "../../data/"
    all_words_file = path + "lexique_fr.txt"
    words_3_7_file = path + "lexicon_fr_3_7.txt"
    anagrams_dict_file = path + "anagrams_fr_3_7.bin"
    included_anagrams_dict_file = path + "included_anagrams_fr_3_7.bin"

    # Generates "lexicon_fr_3_7.txt" from file "lexique_fr.txt" generated by wouf's script
    # It keeps only words having between 3 and 7 letters (included)
    trim_lexicon(all_words_file, words_3_7_file, minLength, maxLength)
    print("-----")

    # Groups words by anagrams (words with same length and same letters)
    group_by_anagrams(words_3_7_file, anagrams_dict_file)
    print("-----")

    # Groups words by "included" anagrams (words using the same letters or subsets of letters)
    group_by_included_anagrams(anagrams_dict_file, included_anagrams_dict_file)

def test_find_anagrams(letters):

    included_anagrams_dict_file = "included_anagrams_fr_3_7.bin"
    
    src_file = open(included_anagrams_dict_file, "rb")
    anagram_dic = pickle.load(src_file)
    src_file.close()

    key = hash(letters)

    print(letters + ":" + str(sorted(anagram_dic[key])))


create_JDM_files()
# test_find_anagrams("MIELDN")