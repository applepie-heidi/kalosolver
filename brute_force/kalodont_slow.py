import resource
import sys
import time

from word_grouper import parse_groups

resource.setrlimit(resource.RLIMIT_STACK, (2 ** 29, -1))
sys.setrecursionlimit(10 ** 6)

DEBUG_PERIOD = 2_000_000


class Node:
    def __init__(self, name, count):
        self.name = name
        self.count = count
        self.edges = []


class Graph:
    def __init__(self):
        self.head = Node("kant", 1)
        self.groups = parse_groups("../rijeci.txt")
        self.nodes = {}
        self.max_kalodont = []
        self.counter = 0
        self.started = time.time()
        self.best_filename = ""
        self.data_filename = ""
        self.current_filename = ""

        started = time.time()
        self.nodes["kant"] = self.head
        by_suffix = {}
        for group, words in self.groups.items():
            node = Node(group, len(words))
            self.nodes[group] = node
            suffix = node.name[-2:]
            by_suffix.setdefault(suffix, []).append(node)

        for node in self.nodes.values():
            prefix = node.name[:2]
            node.edges = by_suffix.get(prefix, [])
        print(f"graph creation time: {time.time() - started}s")

    def dfs(self):
        stack = [self.head]
        path = []

        while stack:
            node = stack.pop()
            if node not in path:
                path.append(node)
                for neighbour in node.edges:
                    stack.append(neighbour)

        return path

    def kalodont(self):
        self.started = time.time()
        self.best_filename = f"best_recursive_{int(self.started)}.txt"
        self.data_filename = f"data_recursive_{int(self.started)}.log"
        self.current_filename = f"current_path_recursive_{int(self.started)}.txt"
        self.recursive(self.head, [], [])
        print(f"kalodont time: {time.time() - self.started}s")

    def recursive(self, node, path, kalodont):
        self.counter += 1
        if node.count > 0:
            node.count -= 1
            path.append(node.name)
            word_list = self.groups.get(node.name)
            if word_list is not None:
                kalodont.append(word_list[node.count])
            else:
                kalodont.append("kalodont")
            if len(self.max_kalodont) < len(kalodont):
                self.max_kalodont = kalodont.copy()
                with open(self.best_filename, "w") as best_file, open(self.data_filename, "a") as data_file:
                    elapsed = time.time() - self.started
                    best_file.write(" ".join(reversed(kalodont)))
                    data_file.write(f"{len(kalodont)},{elapsed},{self.counter}\n")
                    print(f"words: {len(kalodont)} time: {elapsed}s counter: {self.counter}")

            if self.counter % DEBUG_PERIOD == 0:
                with open(self.current_filename, "w") as current_file:
                    current_file.write(str(path))
            for neighbour in node.edges:
                self.recursive(neighbour, path, kalodont)
            path.pop()
            kalodont.pop()
            node.count += 1


def main():
    graph = Graph()
    graph.kalodont()


if __name__ == '__main__':
    main()
