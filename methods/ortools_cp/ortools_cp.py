from ortools.linear_solver import pywraplp
class CP:
    def __init__(self, time_limit):
        self.time_limit = time_limit

    def solve(self, instance):
        K = instance.data['K']
        distance = instance.data['distance_matrix']
        n = len(distance)
        L = n - K
        M = 9999
        solver = pywraplp.Solver.CreateSolver('SCIP')
        
    # Decision Variables

        u = {}
        for i in range(1,n):
            u[i] = solver.IntVar(1, L, "u[%i]" % i)
    
        x = {}
        for i in range(n):
            for j in range(n):
                x[i, j] = solver.IntVar(0, 1, "x[%i, %i]" % (i, j))

        s = {}
        for i in range(n):
            s[i] = solver.IntVar(1, M, "u[%i]" % i)
        
        solver.Minimize(solver.Sum([distance[i][j] * x[i, j] for j in range(n) for i in range(n)]) + s[0])
        
    # Constraints


        # (1) and (2) 

        solver.Add(solver.Sum(x[0, i] for i in range(1, n)) == K)
        solver.Add(solver.Sum(x[i, 0] for i in range(1, n)) == K)
    
        # (3) and (4)

        for i in range(1,n):
            solver.Add(solver.Sum(x[i, j] for j in range(n) if i!=j) == 1)
    
        for i in range(1,n):
            solver.Add(solver.Sum(x[j, i] for j in range(n) if i!=j) == 1)

        # (4) and (5) prevent sub tours.

        for i in range(1, n):
            for j in range(1, n):
                if i != j:
                    solver.Add(u[i] - u[j] + L * x[i, j] <= L - 1)
        # (6)
        for i in range(1, n):
            for j in range(n):
                if i != j:
                    solver.Add(s[j] - s[i] >= distance[i][j] - M * (1 - x[i, j]))
        # (7)
        for j in range(1, n):
            solver.Add(s[j] >= distance[0][j] * x[0, j])
        # Solve()
        solver.set_time_limit(self.time_limit * 1000)
        status = solver.Solve()

        if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
            s  = []
            for i in range(n):
                tmp = []
                for j in range(n):
                    tmp.append(x[i, j].solution_value())
                s.append(tmp)
            #print("visiting rank:", end= " ")
            #for i in range(1,n):
            #    print(u[i].solution_value(), end= "   ")
            #print("")
            return self.result(s, distance), [], []
                
        else:
            return None, [], []
            
    def result(self, x, d):
        n = len(x)
        results = []

        # for i in range(n):
        #     for j in range(n):
        #         print(x[i][j], end= "   ")
        #     print("")

        def found_column(i, sum):
            for j in range(n):
                if x[i][j] == 1:
                    if j == 0 : return sum + d[i][j]
                    else: return found_column(j, sum + d[i][j])

        for i in range(n):
            if x[0][i] == 1:
                sum_tmp = d[0][i]
                results.append(found_column(i, sum_tmp))

        return max(results)
        
