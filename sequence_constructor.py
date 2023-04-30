import copy


def extract_shortest_circuits(graph):
    graph_copy = copy.deepcopy(graph)
    curr = graph_copy[0]  # [(3,1), (4,123)] aka [(node,cost), ...]
    curr_i = 0
    trail = [0]
    circuits = []
    while curr:
        out_edges_num = len(curr)
        if out_edges_num == 1: # and curr[0][1] == 1:
            curr_i = curr[0][0]
            curr = graph_copy[curr_i]
            trail.append(curr_i)
        else:
            print(f"{curr_i} = {curr}")
            circuit = bfs(graph_copy, curr_i)
            if circuit:
                for i, v in enumerate(circuit):
                    if i < len(circuit) - 1:
                        next_v = circuit[i + 1]
                    else:
                        next_v = circuit[0]
                    edges = graph_copy[v]
                    for v_i, (node, cost) in enumerate(edges):
                        if node == next_v:
                            if cost > 1:
                                edges[v_i] = (next_v, cost - 1)
                            else:
                                del edges[v_i]
                            break
                circuits.append(circuit)
            else:
                print("IT happened---------------------------------", curr_i)
                trail.append(curr_i)

                break
    print([r for r in graph_copy if r])
    return trail, circuits


def bfs(graph, node):
    visited = [node]
    queue = [node]

    prev = {}

    while queue:
        print(f"queue = {queue}")
        n = queue.pop(0)
        print(f"graph[{n}] = {graph[n]}")
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
