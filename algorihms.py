from typing import Tuple

from graph import Graph

__all__ = ["semi_eulerian_path"]


def semi_eulerian_path(graph: Graph) -> Tuple:
    s = graph.node("s")
    t = graph.node("t")

    trail = []
    visited_edges = {}
    stack = [(s, iter(graph.edges(s)))]
    while stack:
        node, edges = stack[-1]
        try:
            next_node, weight = next(edges)
            remaining_weight = visited_edges.setdefault((node, next_node), weight)
            if remaining_weight > 0:
                visited_edges[(node, next_node)] -= 1
                stack.append((next_node, iter(graph.edges(next_node))))
                trail.append((node, next_node))
        except StopIteration:
            stack.pop()

    # Trail like this ...
    # [ (s, aa), (aa, bb), (bb, cc), (cc, dd), (dd, aa), (aa, t),
    #   (aa, aa),
    #   (cc, ee), (ee, ff), (ff, gg), (gg, cc),
    #   (ee, ee) ]

    # ... turn into segments like this:
    # [ [s, aa, bb, cc, dd, aa, t],
    #   [aa],
    #   [cc, ee, ff, gg],
    #   [ee] ]
    segments = []

    def add_segment(seg):
        # Main segment (ending with "t") is not a loop, add entire segment
        if seg[-1] == t:
            segments.append(seg)
        # Otherwise, add all but the last node (because it's a loop)
        else:
            assert seg[0] == seg[-1]
            segments.append(seg[:-1])

    segment = [s]
    for n1, n2 in trail:
        # Add a node if it continues the chain
        if n1 == segment[-1]:
            segment.append(n2)
        # End of the chain
        else:
            add_segment(segment)
            segment = [n1, n2]
    add_segment(segment)

    # Combine segments into final path:
    path = segments[0]
    for segment in segments[1:]:
        index = path.index(segment[0])
        path = path[:index] + segment + path[index:]

    return path, trail, segments
