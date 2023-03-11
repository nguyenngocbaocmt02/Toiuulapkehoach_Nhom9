from ortools.linear_solver import pywraplp

def solve_lp(N, K, d, t):
    solver = pywraplp.Solver('MaintenanceScheduling', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

    # binary variable x_ij = 1 if employee j travels to customer i, 0 otherwise
    x = {}
    for i in range(N):
        for j in range(K):
            x[i, j] = solver.IntVar(0, 1, f'x_{i}_{j}')

    # continuous variable t_j representing the total working time of employee j
    y = [solver.NumVar(0, solver.infinity(), f't_{j}') for j in range(K)]

    # constraints
    for i in range(N):
        solver.Add(solver.Sum([x[i, j] for j in range(K)]) == 1)
    
    for j in range(K):
        solver.Add(y[j] == solver.Sum([(t[i][0] + d[i]) * x[i, j] for i in range(N)]))

    # objective function
    solver.Minimize(solver.Max(y) - solver.Min(y))

    # solve the problem
    solver.Solve()

    # print results
    for j in range(K):
        print(f'Employee {j + 1} total working time: {y[j].solution_value()}')

N = 4
K = 2
d = [3, 2, 4, 5]
t = [
    [0, 1, 2, 3, 4],
    [1, 0, 3, 1, 1],
    [2, 3, 0, 2, 2],
    [3, 1, 2, 0, 1],
    [4, 1, 2, 1, 0],
]

solve_lp(N, K, d, t)