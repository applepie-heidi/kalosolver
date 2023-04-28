import highspy
import numpy as np


def create_lp_model(model, costs):
    edges_num = len(model[0])

    h = highspy.Highs()

    for i in range(edges_num):
        h.addVar(0, costs[i])

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

    h.changeObjectiveSense(highspy.ObjSense.kMaximize)

    return h


def solve_lp_model(model):
    model.run()
    solution = model.getSolution()

    return solution.col_value
