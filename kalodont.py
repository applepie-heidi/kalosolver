import sys
import time

from algorihms import semi_eulerian_path
from graph import Graph, debug_print_graph_subsets
from solver import WordGameModel
from words import make_graph, read_words, reconstruct_words


def log(*args):
    print(*args, file=sys.stderr)


def play_kalodont(filename):
    words = read_words(filename)
    log("Total words:", len(words))

    graph = make_graph(words)
    log("Input graph:", graph.info())
    debug_print_graph_subsets(graph)

    log("Solving...")
    model = WordGameModel(graph)
    res = model.solve()

    log(f"==================\n{res}\n==================")
    log("Number of edges in MILP solution:", len(res.x))

    optimized_graph = model.optimized_graph()
    debug_print_graph_subsets(optimized_graph)

    log("Optimized graph:", optimized_graph.info())

    path = semi_eulerian_path(optimized_graph)[0]

    def names(seq):
        return [optimized_graph.name(n) for n in seq]

    log(
        f"Final path (nodes:{len(path)}, edges:{len(path)-1}):",
        names(path[:5]) + ["..."] + names(path[-5:]),
    )

    result = reconstruct_words(words, optimized_graph, path)
    log("Number of words: ", len(result))

    with open(f"best_recursive_{int(time.time())}.txt", "w") as best_file:
        for word in result:
            best_file.write(word + " ")
            print(word, end=" ")


if __name__ == "__main__":
    # play_kalodont("generirane_rijeci.txt")
    play_kalodont(sys.argv[1] if len(sys.argv) > 1 else "rijeci.txt")
