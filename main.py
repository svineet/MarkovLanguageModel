import random
from itertools import tee
from purify import get_file_word_data
from collections import defaultdict


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


visited = defaultdict(lambda: False)
def make_graph():
    """
        Make adjacency list for
        Markov Chain graph
        with Graph edges containing
        frequency of occurence of that pair.
    """
    adj = defaultdict(lambda: defaultdict(int))
    word_list = get_file_word_data("data/caesar.txt", 4)
    for line in word_list:
        for word1, word2 in pairwise(line):
            visited[word1] = False
            visited[word2] = False
            if (word2.endswith(".")):
                adj[word1][word2[:-1:]] += 1
                adj[word2]["$$$"] = 1
                # Ender word.
                pass
            else:
                adj[word1][word2] += 1

    print("Graph done.")
    return adj


def traverse_graph(adj, seed):
    """
        Traverse Markov Chain keeping
        Probability in mind.
        Returns a list of words traversed.
    """
    if (seed == "$$$"): return ["."]

    tot = 0
    for (nx, prob) in adj[seed].items():
        if (visited[nx] is True): continue
        tot += prob

    choice = random.uniform(0, tot)
    acc = 0
    for (nx, prob) in adj[seed].items():
        if (visited[nx] is True): continue
        if (acc <= choice and choice <= acc+prob):
            visited[nx] = True
            return [nx]+traverse_graph(adj, nx)
        acc += prob

    return ["."]

if __name__ == '__main__':
    adj = make_graph()
    seed = input()
    while (seed != "stfu"):
        print(" ".join([seed]+traverse_graph(adj, seed)))
        for (key, val) in visited.items():
            visited[key] = False
        seed = input()
    print("kthxbai hope you enjoyed the disappointing progrem xd gci winur 2017")
