import time

import lp_solver_new as lps
import graph_new as g
import sequence_constructer as seq


def total_edge_cost(graph):
    edges = 0
    total = 0
    for row in graph:
        if isinstance(row, dict):
            for edge, weight in row.items():
                edges += 1
                total += weight
        else:
            for edge, weight in row:
                edges += 1
                total += weight

    return edges, total


def count_tokens(filename):
    tokens = set()
    with open(filename) as f:
        for word in f:
            word = word.strip().lower()#.replace("-", "")
            if word:
                tokens.add(word[:2])
                tokens.add(word[-2:])
    print("total tokens", len(tokens))


if __name__ == '__main__':
    count_tokens("rijeci.txt")
    word_graph = g.Graph("rijeci.txt")
    print("total nodes",len(word_graph.vertices))
    print("total edges before",total_edge_cost(word_graph.graph))
    print("total edges before without s and t", total_edge_cost(word_graph.graph)[1]-len(word_graph.graph[0])*2)

    word_graph_model, costs = word_graph.create_graph_model()

    solution = lps.solve_scipy_model(word_graph_model, costs)

    for s in solution:
        if abs(float(int(s))-s) != 0.0:
            print("NON INTEGER", s)
            raise Exception()

    word_optimized_graph = word_graph.create_optimized_graph(solution)
    print("total edges after", total_edge_cost(word_optimized_graph))

    trail, circuits = seq.extract_shortest_circuits(word_optimized_graph)
    sequence = seq.construct_sequence(trail, circuits)
    print(sequence[-10:])
    print(len(sequence))
    print(word_graph.vertices[sequence[-3]], word_graph.vertices[sequence[-2]])

