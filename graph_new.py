from collections import OrderedDict

from word_grouper import parse_groups


class Graph:
    def __init__(self, dictionary_filename):
        self.graph = [OrderedDict()]
        self.vertices = ["s"]
        self.edges_num = 0
        self.groups = parse_groups(dictionary_filename)
        self.max_kalodont = []
        self.best_filename = ""
        self.data_filename = ""
        self.current_filename = ""

        vertices_dict = {"s": 0}
        vertex_i = 1
        with open(dictionary_filename, "r") as words_f:
            lines = words_f.readlines()
            for word in lines:
                word = word[:-1]
                if True: #not word.startswith("ka"):
                    prefix = word[:2]
                    suffix = word[-2:]

                    if prefix not in vertices_dict:
                        self.vertices.append(prefix)
                        vertices_dict[prefix] = vertex_i
                        self.graph.append(OrderedDict())
                        self.graph[0][vertex_i] = 1
                        self.edges_num += 1
                        vertex_i += 1
                    if suffix not in vertices_dict:
                        self.vertices.append(suffix)
                        vertices_dict[suffix] = vertex_i
                        self.graph.append(OrderedDict())
                        self.graph[0][vertex_i] = 1
                        self.edges_num += 1
                        vertex_i += 1
                    out_vertex = vertices_dict.get(prefix)
                    in_vertex = vertices_dict.get(suffix)
                    get = self.graph[out_vertex].get(in_vertex, 0)
                    self.graph[out_vertex][in_vertex] = get + 1
                    if not get:
                        self.edges_num += 1

        self.vertices.append("t")
        self.graph.append(OrderedDict())

        if 0:
            self.graph[vertices_dict["nt"]][vertex_i] = 1
            self.edges_num += 1
        else:
            for i in range(1, len(self.graph)-1):
                self.graph[i][vertex_i] = 1
                self.edges_num += 1
        print("Number of edges", self.edges_num)

    def create_graph_model(self):
        row_num = len(self.graph)
        graph_model = [[0 for _ in range(self.edges_num)] for _ in range(row_num)]
        costs = []
        element_i = 0
        for out_row_i in range(row_num):
            for in_row_i, cost in self.graph[out_row_i].items():
                graph_model[out_row_i][element_i] = -1
                graph_model[in_row_i][element_i] = 1
                costs.append(cost)
                element_i += 1

        return graph_model, costs

    def create_optimized_graph(self, lp_solution):
        optimized_graph = []
        solution_i = 0
        for row in self.graph:
            optimized_row = []
            for vertex, cost in row.items():
                solution_el = lp_solution[solution_i]
                if solution_el > 0:
                    optimized_row.append((vertex, solution_el))
                solution_i += 1
            optimized_graph.append(optimized_row)

        return optimized_graph
