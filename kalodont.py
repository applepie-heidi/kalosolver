import time

import lp_solver
import graph
import sequence_constructor


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
            word = word.strip().lower()  # .replace("-", "")
            if word:
                tokens.add(word[:2])
                tokens.add(word[-2:])
    print("total tokens", len(tokens))


if __name__ == '__main__':
    filename = "generirane_rijeci.txt"
    filename = "rijeci.txt"
    count_tokens(filename)
    word_graph = graph.Graph(filename=filename)
    print("total nodes", len(word_graph.vertices))
    print("total edges before", total_edge_cost(word_graph.graph))
    print("total edges before without s and t", total_edge_cost(word_graph.graph)[1] - len(word_graph.graph[0]) * 2)

    word_graph_model, costs, variables = word_graph.create_graph_model()

    solution = lp_solver.solve_scipy_model(word_graph_model, costs)

    for s in solution:
        if abs(float(int(s)) - s) != 0.0:
            print("NON INTEGER", s)
            raise Exception()

    word_optimized_graph = word_graph.create_optimized_graph(solution, variables)
    #graph.debug_print_optimized_graph_info(word_optimized_graph)
    print("total edges after", total_edge_cost(word_optimized_graph))

    trail, circuits = sequence_constructor.extract_shortest_circuits(word_optimized_graph)
    print("trail nodes count: ", len(trail))
    c_count = sum(len(c) for c in circuits)
    print("circuit nodes count:", sum(len(c) for c in circuits))
    print("extracted edges count:", len(trail) + c_count - 1)

    sequence = sequence_constructor.construct_sequence(trail, circuits)
    print(sequence[-10:])
    print("Final sequence:", len(sequence) - 1)
    print(word_graph.vertices[sequence[-3]], word_graph.vertices[sequence[-2]])
