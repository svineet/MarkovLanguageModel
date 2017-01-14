import random
from time import time
from collections import defaultdict

STARTCHAR = "<s>"
ENDCHAR = "</s>"

def generate_ngrams():
    bigram = defaultdict(int)
    # Stores bigram -> occurences
    trigram = defaultdict(int)
    # Stores trigram -> occurences
    vocab = set()
    brown = open("data/browncorpus.txt", "r")
    for line in brown:
        line_words = line.split()
        if len(line_words) < 3:
            continue

        for (i, word) in enumerate(line_words):
            vocab.add(word)
            if i == 0:
                bigram[(STARTCHAR, word)] += 1
                trigram[(STARTCHAR, STARTCHAR, word)] += 1
            elif i == 1:
                bigram[(line_words[i-1], word)] += 1
                trigram[(STARTCHAR, line_words[i-1], word)] += 1
            else:
                bigram[(line_words[i-1], word)] += 1
                trigram[(line_words[i-2], line_words[i-1], word)] += 1

        bigram[(line_words[-1], ENDCHAR)] += 1
        trigram[(line_words[-2], line_words[-1], ENDCHAR)] += 1
        trigram[(line_words[-1], ENDCHAR, ENDCHAR)] += 1

    return (bigram, trigram, vocab)


def main(bigram, trigram, vocab):
    print(len(vocab))

def dfs(word1, word2, word3, bigram, trigram, vocab):
    print (word3, sep=" ", end=" ", flush=True)
    if (word3 == ENDCHAR): return ["."]

    # if (word1 == STARTCHAR and word2 == STARTCHAR):
    #     triple = (STARTCHAR, STARTCHAR, word2)
    #     for (i, word) in enumerate(vocab):
    #         for word_ in vocab:
    #             print (i, flush=True)
    #             if trigram[(word, word_, word3)] > trigram[triple]:
    #                 triple = (word, word_, word3)
    #     word1, word2, word3 = triple
    #     print (triple)

    if (word1 == STARTCHAR and word2 == STARTCHAR):
        for word in vocab:
            if (bigram[word, word3] > 0):
                word2 = word

    sm = 0
    for word in vocab:
        occ = trigram[(word2, word3, word)]
        if (occ == 0):
            continue
        else:
            sm += occ

    choice = int(random.uniform(0, sm))
    acc = 0
    for word in vocab:
        occ = trigram[(word2, word3, word)]
        if (occ == 0): continue
        if acc <= choice and choice <= acc+occ:
            return [word3]+dfs(word2, word3, word, bigram, trigram, vocab)
        acc += occ

    if (sm == 0): return []

if __name__ == '__main__':
    print ("This uses the trigram model on "
           "the brown corpus to generate random "
           "sentences.")
    t = time()
    bigram, trigram, vocab = generate_ngrams()
    print(time()-t)

    random.seed(time())
    main(bigram, trigram, vocab)
    s = input()
    while (s != "stfu"):
        if (s not in vocab):
            print("no pls change idk.")
        else:
            dfs(STARTCHAR, STARTCHAR, s, bigram, trigram, vocab)
            print()
        s = input()
