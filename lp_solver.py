from graph import graph_model
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

    # index = np.array([i for i in range(edges_num)])
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
    print('LP has ', lp.num_col_, ' columns', lp.num_row_, ' rows and ', num_nz, ' nonzeros')

    print("OOO", dir(h.getOptions()))
    h.changeObjectiveSense(highspy.ObjSense.kMaximize)
    h.run()

    solution = h.getSolution()
    basis = h.getBasis()
    info = h.getInfo()
    model_status = h.getModelStatus()
    print('Model status = ', h.modelStatusToString(model_status))
    print()
    print('Optimal objective = ', info.objective_function_value)
    print('Iteration count = ', info.simplex_iteration_count)
    print('Primal solution status = ', h.solutionStatusToString(info.primal_solution_status))
    print('Dual solution status = ', h.solutionStatusToString(info.dual_solution_status))
    print('Basis validity = ', h.basisValidityToString(info.basis_validity))

    print(solution.col_value)


if __name__ == '__main__':
    simple_graph = [
        [1, 2, 3, 4],
        [2, 3, 4, 5],
        [1, 1, 3, 4, 5],
        [4, 4, 5],
        [2, 2, 2, 2, 5],
        []
    ]
    model = graph_model(simple_graph)
    lp_model(model)
