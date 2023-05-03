from collections import defaultdict
from typing import List

from graph import Graph, Node

__all__ = ["read_words", "make_graph", "reconstruct_words"]


def read_words(filename: str) -> List[str]:
    with open(filename) as f:
        return [word.strip().lower() for word in f if word.strip()]


def make_graph(words: List[str]) -> Graph:
    graph = Graph()

    # Start node "s"
    s = graph.add_node("s")

    # Nodes from words
    for word in words:
        node1 = graph.add_node(word[:2])
        node2 = graph.add_node(word[-2:])
        graph.add_edge(node1, node2)

    # Edge from "s" to all nodes
    for node in graph.nodes():
        if node != s:
            graph.add_edge(s, node)

    # Terminal node "t"
    t = graph.add_node("t")

    # Edge from all nodes to "t"
    for node in graph.nodes():
        if node != t and node != s:
            graph.add_edge(node, t)

    return graph


def reconstruct_words(words: List[str], graph: Graph, path: List[Node]) -> List[str]:
    word_map = defaultdict(list)
    for word in words:
        key = word[:2] + word[-2:]
        word_map[key].append(word)

    # skip s and t
    s = graph.node("s")
    t = graph.node("t")
    if path[0] == s:
        path = path[1:]
    if path[-1] == t:
        path = path[:-1]

    # make word list
    results = []
    prev = path[0]
    for node in path[1:]:
        key = graph.name(prev) + graph.name(node)
        word = word_map[key].pop()
        results.append(word)
        prev = node

    return results
