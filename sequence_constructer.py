import copy


def extract_shortest_circuits(graph):
    graph_copy = copy.deepcopy(graph)
    curr = graph_copy[0]
    curr_i = 0
    trail = [0]
    circuits = []
    x = 0
    while curr:
        if len(curr) == 1 and curr[0][1] == 1:
            curr_i = curr[0][0]
            curr = graph_copy[curr_i]
            trail.append(curr_i)
        else:
            circuit = bfs(graph_copy, curr_i)
            if circuit:
                for i in range(len(circuit)):
                    v = circuit[i]
                    if i < len(circuit) - 1:
                        w = circuit[i + 1]
                    else:
                        w = circuit[0]
                    for j in range(len(graph_copy[v])):
                        node = graph_copy[v][j][0]
                        cost = graph_copy[v][j][1]
                        if node == w:
                            if cost > 1:
                                graph_copy[v][j] = (w, cost - 1)
                            else:
                                del graph_copy[v][j]
                            break
                circuits.append(circuit)
    return trail, circuits


def bfs(graph, node):
    visited = [node]
    queue = [node]

    prev = {}

    while queue:
        n = queue.pop(0)

        for neighbour, _weight in graph[n]:
            if neighbour == node:
                circuit = [n]
                while n != node:
                    n = prev[n]
                    circuit.append(n)
                circuit.reverse()
                return circuit
            if neighbour not in visited:
                prev[neighbour] = n
                visited.append(neighbour)
                queue.append(neighbour)
    return []


def construct_sequence(trail, circuits):
    circuits_first_el = [c[0] for c in circuits]
    sequence = []
    for node in trail:
        while True:
            try:
                i = circuits_first_el.index(node)
                circuits_first_el[i] = -1
                sequence.extend(circuits[i])
            except ValueError:
                break
        sequence.append(node)
    return sequence


if __name__ == "__main__":
    g = [
        [(3, 1.0)],
        [(3, 1.0)],
        [(1, 1.0), (4, 1.0), (5, 1.0)],
        [(2, 3.0)],
        [(3, 1.0)],
        [(6, 1.0)],
        [],
    ]
    trail, circuits = extract_shortest_circuits(g)
    seq = construct_sequence(trail, circuits)
    print("seq:")
    print(seq)
