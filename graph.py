simple_graph = [
    [1, 2, 3, 4],
    [2, 3, 4, 5],
    [1, 1, 3, 4, 5],
    [4, 4, 5],
    [2, 2, 2, 2, 5],
    []
]

simple_graph_bundled = [
    [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1)],
    [(2, 1), (3, 1), (4, 1), (5, 1), (6, 1)],
    [(1, 2), (3, 1), (4, 1), (6, 1)],
    [(4, 2), (6, 1)],
    [(2, 4), (6, 1)],
    [(6, 1)],
    []
]


def read_simple_graph(filename):
    return simple_graph


def read_simple_graph_bundled(filename):
    return simple_graph_bundled


def graph_model(graph):
    col_num = 0
    row_num = len(graph)
    for edges in graph:
        col_num += len(edges)

    model = [[0 for _ in range(col_num)] for _ in range(row_num)]
    element_i = 0
    for out_row_i in range(row_num):
        for in_row_i in graph[out_row_i]:
            model[out_row_i][element_i] = -1
            model[in_row_i][element_i] = 1
            element_i += 1

    return model


def graph_model_bundled(graph):
    col_num = 0
    row_num = len(graph)
    for edges in graph:
        col_num += len(edges)

    model = [[0 for _ in range(col_num)] for _ in range(row_num)]
    costs = []
    element_i = 0
    for out_row_i in range(row_num):
        for in_row_i, cost in graph[out_row_i]:
            model[out_row_i][element_i] = -1
            model[in_row_i][element_i] = 1
            costs.append(cost)
            element_i += 1

    return model, costs


def print_model(model, graph):
    print(end="  ")
    for i in range(len(graph)):
        for j in graph[i]:
            print(f"{i}-{j}".rjust(4), end="")
    print()
    for row_i in range(len(model)):
        print(f"{row_i}", end=" ")
        for element in model[row_i]:
            print(repr(element).rjust(4), end="")
        print()


if __name__ == '__main__':
    model = graph_model(simple_graph)
    print_model(model, simple_graph)
