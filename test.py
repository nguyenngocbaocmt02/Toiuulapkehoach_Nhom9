from utils.instance import Instance
from methods.ga.ga import GA
from methods.tabu_search.tabu_search import TabuSearch
from methods.ni_greedy.ni_greedy import NIGreedy
from methods.ci_greedy.ci_greedy import CIGreedy
from methods.local_search.local_search import LocalSearch
from methods.brute_force.brute_force import BruteForce
from methods.ortools_lp.ortools_lp import LP
from methods.ortools_cp.ortools_cp import CP

instance = Instance("data/N6_K2")

#model = GA(pop_size=200, num_generations=200, mutation_probability=0.2, local_search_prob=0.4, keep_rate=0.1, time_limit=30)
#model = GA(pop_size=200, num_generations=200, mutation_probability=0.2, local_search_prob=0, keep_rate=0.1, time_limit=30)
#model = TabuSearch(tabu_list_length= 7 * len(instance.data["distance_matrix"]), max_iterations=10000, n_neighbors=10, intensification_factor=1.0, local_search_prob=0.4, time_limit=30)
#model = TabuSearch(tabu_list_length= 7 * len(instance.data["distance_matrix"]), max_iterations=10000, n_neighbors=10, intensification_factor=1.0, local_search_prob=0, time_limit=30)
#model = NIGreedy(time_limit=30)
#model = CIGreedy(time_limit=30)
#model = LocalSearch(pop_size=100, num_generations=1000, time_limit=30)
#model = BruteForce(time_limit=30)
#model = LP(time_limit=30)
#model = CP(time_limit=30)

res, log1, log2 = model.solve(instance)
print("Out: ", res)
if type(res) == list:
    res = instance.obj_func(res)
print("Check distance:", res)
