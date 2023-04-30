import io

import lp_solver as lps
import graph as g
import sequence_constructor as seq
from kalodont import total_edge_cost
import random


def make_random_dictionary():
    syllables = ["aa", "ee", "ii", "oo", "uu", "ae", "ai", "ao", "au", "ea"]
    rand_syllables_num = random.randint(2, len(syllables))
    rand_syllables = random.sample(syllables, rand_syllables_num)
    rand_syllables.append("nt")

    # create random number of random words starting and ending with random syllables from rand_syllables
    # they must not start with "nt"
    rand_words_num = random.randint(2, 20)
    rand_words = [random.choice(rand_syllables) + "00" + "nt"]
    for i in range(rand_words_num):
        rand_word = random.choice(rand_syllables)
        while rand_word.startswith("nt"):
            rand_word = random.choice(rand_syllables)
        rand_word += str(i) + random.choice(rand_syllables)
        rand_words.append(rand_word)

    return "\n".join(rand_words)


def run_algo():
    dictionary = make_random_dictionary()
    word_graph = g.Graph(file=io.StringIO(dictionary))
    word_graph_model, costs, variables = word_graph.create_graph_model()

    solution = lps.solve_scipy_model(word_graph_model, costs)

    word_optimized_graph = word_graph.create_optimized_graph(solution, variables)
    expected = total_edge_cost(word_optimized_graph)[1]
    trail, circuits = seq.extract_shortest_circuits(word_optimized_graph)
    c_count = sum(len(c) for c in circuits)
    extracted = len(trail) + c_count - 1
    return dictionary, expected, extracted


def main():
    while True:
        dictionary, expected, extracted = run_algo()
        if expected != extracted:
            print("expected", expected)
            print("extracted", extracted)
            print(dictionary)
            break


if __name__ == '__main__':
    main()
