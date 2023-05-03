import numpy as np
from scipy import optimize

from graph import Graph, Node, Weight

__all__ = ["WordGameModel"]


class WordGameModel:
    def __init__(self, graph: Graph):
        node_cnt = graph.node_count()
        edge_cnt = graph.edge_count()

        self.graph = graph
        self.matrix = [[0] * edge_cnt for _ in range(node_cnt)]
        self.costs = []
        self.variables = []
        self.res = None

        # Var represents an edge.
        # This way we can later reconstruct the graph from the solution.
        def add_var(node1: Node, node2: Node, weight: Weight) -> int:
            var = len(self.variables)
            self.costs.append(weight)
            self.variables.append((node1, node2))
            return var

        # Add variables for each edge.
        # * Each variable is a number of times the edge is used.
        # * Edge comming into a node is positive, edge going out is negative.
        # * Self-loops (edges going back into the same node) are skipped and
        #   handled separately when reconstructing graph.
        # Later specified in solve():
        # * Sum of edges from node "s" must be -1 (single start word)
        # * Sum of edges into node "t" must be 1 (single end word)
        # * Sum of edges for each other node must be 0 (to achieve the desired
        #   effect of having same number of edges going in and out of each node)
        for node in graph.nodes():
            for dest, weight in graph.edges(node):
                var = add_var(node, dest, weight if node != dest else 0)
                self.matrix[node][var] = -1
                self.matrix[dest][var] = 1

        assert (
            len(self.variables) == edge_cnt
        ), f"len(self.variables)={len(self.variables)} != edge_cnt={edge_cnt}"

    def solve(self):
        edges_num = len(self.matrix[0])

        # Objective (target function to maximize)
        # Max of: f = SUM(Xi)
        objective = np.array([1] * edges_num)

        # Specify that all Xi are of type 1=integer
        integrality = np.array([1] * edges_num)

        # Specify bounds (constraints) for each Xi:   Li <= Xi <= Ui
        bounds = optimize.Bounds(lb=np.array([0] * edges_num), ub=np.array(self.costs))

        # Constraints
        cons_s = optimize.LinearConstraint(self.matrix[0], -1, -1)
        cons_i = optimize.LinearConstraint(self.matrix[1:-1], 0, 0)
        cons_t = optimize.LinearConstraint(self.matrix[-1], 1, 1)
        constraints = [cons_s, cons_i, cons_t]

        # Negate objective => find MAX
        self.res = optimize.milp(
            c=-objective,
            constraints=constraints,
            integrality=integrality,
            bounds=bounds,
        )
        return self.res

    def optimized_graph(self) -> Graph:
        graph = Graph()

        # Add edges from MILP solution.
        # Each positive solution means that the edge is used that many times.
        for i, (node1, node2) in enumerate(self.variables):
            weight = self.res.x[i]
            if weight > 0:
                new_node1 = graph.add_node(self.graph.name(node1))
                new_node2 = graph.add_node(self.graph.name(node2))
                graph.add_edge(new_node1, new_node2, weight)

        # Add self-loops from original graph
        for node in self.graph.nodes():
            for n2, weight in self.graph.edges(node):
                if n2 == node:
                    # Only add self-loops that mention nodes from the solution.
                    new_node = graph.node(self.graph.name(node))
                    if new_node:
                        graph.add_edge(new_node, new_node, weight)

        return graph
