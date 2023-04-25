import highspy
import numpy as np

h = highspy.Highs()

lower = 0
upper = 1
cost = 1

for i in range(21):
    h.addVar(lower, upper)

for i in range(21):
    h.changeColCost(i, cost)
num_nz = 4
index = np.array([13, 14, 15, 16])
value = np.array([1, 1, 1, 1])
h.addRow(1, 1, num_nz, index, value)

num_nz = 5
index = np.array([0, 1, 2, 3, 4, 13, 17])
value = np.array([-1, -1, -1, 1, 1, 1, -1])
h.addRow(0, 0, num_nz, index, value)

num_nz = 8
index = np.array([0, 3, 4, 5, 6, 9, 10, 11, 12, 14, 18])
value = np.array([1, -1, -1, -1, -1, 1, 1, 1, 1, 1, -1])
h.addRow(0, 0, num_nz, index, value)

num_nz = 4
index = np.array([1, 5, 7, 8, 15, 19])
value = np.array([1, 1, -1, -1, 1, -1])
h.addRow(0, 0, num_nz, index, value)

num_nz = 7
index = np.array([2, 6, 7, 8, 9, 10, 11, 12, 16, 20])
value = np.array([1, 1, 1, 1, -1, -1, -1, -1, 1, -1])
h.addRow(0, 0, num_nz, index, value)

num_nz = 4
index = np.array([17, 18, 19, 20])
value = np.array([1, 1, 1, 1])
h.addRow(1, 1, num_nz, index, value)

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
