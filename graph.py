

class Graph:
    def __init__(self, *, file=None, filename=None):
        self.graph = [dict()]
        self.vertices = ["s"]
        self.edges_num = 0
        self.max_kalodont = []
        self.best_filename = ""
        self.data_filename = ""
        self.current_filename = ""
        if (file and filename) or (not file and not filename):
            raise Exception("Must specify exactly file or filename")

        vertices_dict = {"s": 0}
        vertex_i = 1
        with Autofile(file, filename) as f:
            for word in f:
                word = word.strip().lower()
                if True:  # not word.startswith("ka"):
                    prefix = word[:2]
                    suffix = word[-2:]

                    if prefix not in vertices_dict:
                        self.vertices.append(prefix)
                        vertices_dict[prefix] = vertex_i
                        self.graph.append(dict())
                        self.graph[0][vertex_i] = 1
                        self.edges_num += 1
                        vertex_i += 1
                    if suffix not in vertices_dict:
                        self.vertices.append(suffix)
                        vertices_dict[suffix] = vertex_i
                        self.graph.append(dict())
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
        self.graph.append(dict())

        if 1:
            self.graph[vertices_dict["nt"]][vertex_i] = 1
            self.edges_num += 1
        else:
            for i in range(1, len(self.graph) - 1):
                self.graph[i][vertex_i] = 1
                self.edges_num += 1
                
        # turn graph into list of lists
        self.graph = [list(row.items()) for row in self.graph]

        print("Number of edges", self.edges_num)

    def create_graph_model(self):
        row_num = len(self.graph)
        graph_model = [[0 for _ in range(self.edges_num)] for _ in range(row_num)]
        costs = []
        variables = []
        loop_variables = []
        element_i = 0
        loop_element_i = self.edges_num
        loop_costs = []
        for out_row_i in range(row_num):
            for in_row_i, cost in self.graph[out_row_i]:
                if out_row_i != in_row_i:
                    graph_model[out_row_i][element_i] = -1
                    graph_model[in_row_i][element_i] = 1
                    costs.append(cost)
                    variables.append((out_row_i, in_row_i))
                    element_i += 1
                else:
                    for i in range(row_num):
                        graph_model[i].append(0)
                    graph_model[out_row_i][element_i] = -1
                    graph_model[in_row_i][loop_element_i] = 1
                    costs.append(cost)
                    loop_costs.append(cost)
                    variables.append((out_row_i, in_row_i))
                    loop_variables.append((out_row_i, in_row_i))
                    element_i += 1
                    loop_element_i += 1
        costs.extend(loop_costs)
        variables.extend(loop_variables)
        return graph_model, costs, variables

    def create_optimized_graph(self, lp_solution, variables):
        optimized_graph = [[] for _ in range(len(self.graph))]
        solution_i = 0
        set_nodes = set()
        for i, x in enumerate(lp_solution):
            if x > 0:
                xi0, xi1 = variables[i]
                if xi0 == xi1:
                    if xi0 not in set_nodes:
                        optimized_graph[xi0].append((xi1, x))
                        set_nodes.add(xi0)
                else:
                    optimized_graph[xi0].append((xi1, x))
        '''for row in self.graph:
            optimized_row = []
            for node, cost in row:
                x_i = lp_solution[solution_i]
                if x_i > 0:
                    optimized_row.append((node, x_i))
                solution_i += 1
            optimized_graph.append(optimized_row)'''
        return optimized_graph


def debug_print_optimized_graph_info(optimized_graph):
    remaining = list(range(len(optimized_graph)))
    counts = {}
    while remaining:
        node = remaining[0]

        # Follow the node (DFS)
        stack = [node]
        visited = []
        total_cost = 0
        while stack:
            n = stack.pop()
            if n not in visited:
                visited.append(n)
                remaining.remove(n)
                for next_n, cost in optimized_graph[n]:
                    stack.append(next_n)
                    total_cost += cost
        old = counts.get(len(visited), (0, 0))
        counts[len(visited)] = old[0] + 1, old[1] + total_cost
    for num_nodes, (graph_cnt, total_cost) in counts.items():
        print(f"- Found {graph_cnt:3} graph(s) with {num_nodes:3} nodes and total cost {total_cost}")


class Autofile:
    def __init__(self, file, filename):
        self.file = file
        self.filename = filename

    def __enter__(self):
        if not self.file:
            self.file = open(self.filename, "r")
        return self.file

    def __exit__(self, *args):
        if self.filename:
            self.file.close()
