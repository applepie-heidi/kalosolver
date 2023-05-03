import sys
from typing import List, Optional, Tuple, Union

Name = Union[str, int]
Node = int
Weight = int
Edge = Tuple[Node, Weight]
Edges = List[Edge]

__all__ = ["Graph", "Node", "Edge", "Edges", "Name", "Weight"]


class Graph:
    def __init__(self):
        self._name_to_node = {}  # node names are mapped to node numbers
        self._nodes = []  # node names are stored in a list
        self._edges = []  # individual node's edges are stored in a dict

    def add_node(self, name: Name) -> Node:
        node: Node = self._name_to_node.get(name)
        if node is None:
            node = len(self._nodes)
            self._nodes.append(name)
            self._edges.append({})
            self._name_to_node[name] = node
        return node

    def add_edge(self, node1: Node, node2: Node, delta_weight: int = 1) -> Edge:
        edges = self._edges[node1]
        edges[node2] = edges.get(node2, 0) + delta_weight
        return (node2, delta_weight)

    def name(self, node: Node) -> Name:
        return self._nodes[node]

    def node(self, name: Name) -> Optional[Node]:
        return self._name_to_node.get(name)

    def nodes(self) -> List[Node]:
        return range(len(self._nodes))

    def edges(self, node: Node) -> Edges:
        return self._edges[node].items()

    def node_count(self) -> int:
        return len(self._nodes)

    def edge_count(self) -> int:
        return sum(len(edges) for edges in self._edges)

    def modify_edge(self, node1: Node, node2: Node, delta_weight: int) -> Edge:
        n, weight = self.add_edge(node1, node2, delta_weight)
        if weight == 0:
            del self._edges[node1][node2]
        return (n, weight)

    def edge(self, node1: Node, node2: Node) -> Edge:
        return (node2, self._edges[node1].get(node2, 0))

    def info(self):
        edges = 0
        total = 0
        for node in self.nodes():
            for _edge, weight in self.edges(node):
                edges += 1
                total += weight
        return {"nodes": self.node_count(), "edges": edges, "weighted edges": total}


def debug_print_graph_subsets(graph: Graph):
    remaining = list(graph.nodes())
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
                for next_n, weight in graph.edges(n):
                    stack.append(next_n)
                    total_cost += weight

        old = counts.get(len(visited), (0, 0))
        counts[len(visited)] = old[0] + 1, old[1] + total_cost

    for num_nodes, (graph_cnt, total_cost) in counts.items():
        print(
            f"- Found {graph_cnt:3} graph(s) with {num_nodes:3} nodes "
            f"and total cost {total_cost}",
            file=sys.stderr,
        )
