import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP
NP -> N | N P NP | AdjP NP | NP Conj NP | NP VP | Det NP VP | NP Adv VP | NP Adv | NP Conj VP
VP -> V | V Det NP | V P Det NP | V Det AdjP NP | V P NP | VP Adv | VP Adv Conj VP | VP NP
AdjP -> Adj
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    words = nltk.word_tokenize(sentence)
    n = len(words)
    i = 0
    while i < n:
        words[i] = words[i].lower()
        remove = 1
        for j in range(len(words[i])):
            if words[i][j].isalpha():
                remove = 0
        if remove == 1:
            words.remove(words[i])
            i -= 1
            n -= 1
        i += 1
    print(words)
    return words
    #raise NotImplementedError


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    #print(tree)
    #for i in tree:
    #    print(i, i.label())
    #tree.draw()
    print("-------------------------\n\n\n")
    for i in tree.subtrees():
        print(i)
    print("\n\n\n-------------------------")
    list = []
    for i in tree.subtrees():
        add = 1
        print(f"In I {i.label()}")
        for j in i.subtrees():
            print(f"In J {j.label()}")
            print(i.__eq__(j))
            if j.label() == "NP" and not i.__eq__(j):
                add = 0
        if add == 1 and i.label() == "NP":
            list.append(i)
    print(list)
    #raise NotImplementedError


if __name__ == "__main__":
    main()
