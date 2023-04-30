import numpy as np
from scipy import optimize


def solve_scipy_model(model, costs):
    edges_num = len(model[0])

    # Objective (target function to maximize)
    # Max of: f = SUM(Xi)
    objective = np.array([1] * edges_num)

    # Specify that all Xi are of type 1=integer
    integrality = np.array([1] * edges_num)

    # Specify bounds (constraints) for each Xi:   Li <= Xi <= Ui
    bounds = optimize.Bounds(
        lb=np.array([0] * edges_num),
        ub=np.array(costs)
    )

    # Constraints
    cons_s = optimize.LinearConstraint(model[0], -1, -1)
    cons_i = optimize.LinearConstraint(model[1:-1], 0, 0)
    cons_t = optimize.LinearConstraint(model[-1], 1, 1)
    constraints = [cons_s, cons_i, cons_t]

    # Negate objective => find MAX
    res = optimize.milp(c=-objective, constraints=constraints, integrality=integrality, bounds=bounds)
    print("==================")
    print(res)
    print("==================")
    return res.x
