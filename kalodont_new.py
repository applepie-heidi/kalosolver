import time

import lp_solver_new as lps
import graph_new as g

if __name__ == '__main__':
    word_graph = g.Graph("male_rijeci.txt")
    print(word_graph.vertices)
    for row in word_graph.graph:
        print(row)
    word_graph_model, costs = word_graph.create_graph_model()
    word_lp_model = lps.create_lp_model(word_graph_model, costs)
    solution = lps.solve_lp_model(word_lp_model)
    t = time.time()
    word_optimized_graph = word_graph.create_optimized_graph(solution)
    print(f"time: {time.time() - t}")
    for row in word_optimized_graph:
        print(row)
