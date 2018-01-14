from collections import Counter, defaultdict
import re

LINE_RE = re.compile('(\w+)\(word\) = ([0-9.]+|True|False)')

def solve_file(fname, data):
    """Solve a file as best we can.
    :returns: List of words that match based on functions we have.
    """
    #print(fname)
    words = None
    for line in open(fname):
        fn, val = parse(line)
        #print((fn, val))
        #print()
        if fn not in data:
            continue  # unknown functions
        try:
            if words is None:
                words = set(data[fn][val])
            else:
                words &= set(data[fn][val])
        except KeyError:
            import pdb; pdb.set_trace()
    return words


def parse(line):
    """Get (fn, val) from a line"""
    #print(line.strip())
    return LINE_RE.search(line).groups()


def parse_words():
    """Calculate all scores of all words and save it to a dict.
    # To save it to a file:
    >>> json.dump(data, open('./data.json', 'w'), indent=4, sort_keys=True)
    :returns: Dict of {function_name: {score: [words]}}
    """
    functions = {'units': units,
                 'typewriter': typewriter,
                 'scrabble': scrabble,
                 'elements': elements}
    data = defaultdict(lambda: defaultdict(list))
    for word in open('./words.txt'):
        word = word[:-1]
        for name, fn in functions.items():
            score = str(fn(word))
            data[name][score].append(word)
    output = {}
    for fn, scores in data.items():
        output[fn] = {}
        for score, words in scores.items():
            output[fn][score] = words
    return output

def units(word):
    """Units - length of word"""
    return len(word)

tw_ltrs = 'qwertyuiop'
def typewriter(word):
    """Typewriter - number of letters from top row of keyboard"""
    c = Counter(word)
    return sum(c[l] for l in tw_ltrs)


SCORES = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
          "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
          "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
          "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
          "x": 8, "z": 10}
def scrabble(word):
    """Scrabble - get the scrabble score of a word"""
    print "::{}".format(word)
    return sum(SCORES[l] for l in word)

atomic_numbers = { "h": 1, "he": 2, "li": 3, "be": 4, "b": 5, "c": 6, "n": 7,
"o": 8, "f": 9, "ne": 10, "na": 11, "mg": 12, "al": 13, "si": 14, "p": 15, "s":
16, "cl": 17, "ar": 18, "k": 19, "ca": 20, "sc": 21, "ti": 22, "v": 23, "cr":
24, "mn": 25, "fe": 26, "co": 27, "ni": 28, "cu": 29, "zn": 30, "ga": 31, "ge":
32, "as": 33, "se": 34, "br": 35, "kr": 36, "rb": 37, "sr": 38, "y": 39, "zr":
40, "nb": 41, "mo": 42, "tc": 43, "ru": 44, "rh": 45, "pd": 46, "ag": 47, "cd":
48, "in": 49, "sn": 50, "sb": 51, "te": 52, "i": 53, "xe": 54, "cs": 55, "ba":
56, "la": 57, "ce": 58, "pr": 59, "nd": 60, "pm": 61, "sm": 62, "eu": 63, "gd":
64, "tb": 65, "dy": 66, "ho": 67, "er": 68, "tm": 69, "yb": 70, "lu": 71, "hf":
72, "ta": 73, "w": 74, "re": 75, "os": 76, "ir": 77, "pt": 78, "au": 79, "hg":
80, "tl": 81, "pb": 82, "bi": 83, "po": 84, "at": 85, "rn": 86, "fr": 87, "ra":
88, "ac": 89, "th": 90, "pa": 91, "u": 92, "np": 93, "pu": 94, "am": 95, "cm":
96, "bk": 97, "cf": 98, "es": 99, "fm": 100, "md": 101, "no": 102, "lr": 103,
"rf": 104, "db": 105, "sg": 106, "bh": 107, "hs": 108, "mt": 109, "ds": 110,
"rg": 111, "cn": 112, "nh": 113, "fl": 114, "mc": 115, "lv": 116, "ts": 117,
"og": 118 }

def elements(w):
    totals = []
    for i,l in enumerate(w):
        if atomic_numbers.get(l):
            totals.append(atomic_numbers.get(l))
        if len(w) > i+1 and atomic_numbers.get("{}{}".format(l,w[i+1])):
            totals.append(atomic_numbers.get("{}{}".format(l, w[i+1])))
    return sum([ a for a in totals if a != None ])
