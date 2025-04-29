import sys

def is_querry_simple(query : str) :
    bad_words = None
    split_query = query.split()

    with open("bad_words.txt") as file:
        bad_words = file.read().split()
    if len(split_query) > 5 :
        return False
    for bad_word in  bad_words :
        for words in split_query :
            if bad_word in words.lower() :
                return True
    return False

def main() :
    print(is_querry_simple(sys.argv[1]))

if __name__ == "__main__" :
    main()