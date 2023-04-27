import graph
import highspy
import numpy as np


def lp_model(model):
    lower = 0
    upper = 1
    cost = 1
    edges_num = len(model[0])

    h = highspy.Highs()

    for i in range(edges_num):
        h.addVar(lower, upper)

    for i in range(edges_num):
        h.changeColCost(i, cost)

    for row_i in range(len(model)):
        nz_num = 0
        index = []
        value = []
        for col_i in range(len(model[row_i])):
            coef = model[row_i][col_i]
            if coef != 0:
                nz_num += 1
                index.append(col_i)
                value.append(coef)
        if row_i == 0:
            h.addRow(-1, -1, nz_num, np.array(index), np.array(value))
        elif row_i == len(model) - 1:
            h.addRow(1, 1, nz_num, np.array(index), np.array(value))
        else:
            h.addRow(0, 0, nz_num, np.array(index), np.array(value))

    lp = h.getLp()
    num_nz = h.getNumNz()
    # print('LP has ', lp.num_col_, ' columns', lp.num_row_, ' rows and ', num_nz, ' nonzeros')

    h.changeObjectiveSense(highspy.ObjSense.kMaximize)

    return h


def lp_model_bundled(model, costs):
    lower = 0
    edges_num = len(model[0])

    h = highspy.Highs()

    for i in range(edges_num):
        h.addVar(lower, costs[i])

    for i in range(edges_num):
        h.changeColCost(i, costs[i])

    for row_i in range(len(model)):
        nz_num = 0
        index = []
        value = []
        for col_i in range(len(model[row_i])):
            coef = model[row_i][col_i]
            if coef != 0:
                nz_num += 1
                index.append(col_i)
                value.append(coef)
        if row_i == 0:
            h.addRow(-1, -1, nz_num, np.array(index), np.array(value))
        elif row_i == len(model) - 1:
            h.addRow(1, 1, nz_num, np.array(index), np.array(value))
        else:
            h.addRow(0, 0, nz_num, np.array(index), np.array(value))

    lp = h.getLp()
    num_nz = h.getNumNz()
    # print('LP has ', lp.num_col_, ' columns', lp.num_row_, ' rows and ', num_nz, ' nonzeros')

    h.changeObjectiveSense(highspy.ObjSense.kMaximize)

    return h


def solve_model(h):
    h.run()
    solution = h.getSolution()

    return solution.col_value


def create_optimized_graph(solution, graph):
    optimized_graph = []
    solution_i = 0
    for row in graph:
        optimized_row = []
        for element in row:
            solution_el = solution[solution_i]
            if solution_el == 1:
                optimized_row.append(element)
            elif solution_el == 0:
                pass
            else:
                print(f"IMPOSSIBLE VALUE {solution_el}")
            solution_i += 1
        optimized_graph.append(optimized_row)

    return optimized_graph


def create_optimized_graph_bundled(solution, graph):
    optimized_graph = []
    solution_i = 0
    for row in graph:
        optimized_row = []
        for element in row:
            solution_el = solution[solution_i]
            if solution_el > 0:
                optimized_row.append((element[0], solution_el))
            elif solution_el == 0:
                pass
            else:
                print(f"IMPOSSIBLE VALUE {solution_el}")
            solution_i += 1
        optimized_graph.append(optimized_row)

    return optimized_graph


if __name__ == '__main__':
    model, costs = graph.graph_model_bundled(graph.simple_graph_bundled)
    lp_model = lp_model_bundled(model, costs)
    solution = solve_model(lp_model)
    optimized_graph = create_optimized_graph_bundled(solution, graph.simple_graph_bundled)

    for row in optimized_graph:
        print(row)
