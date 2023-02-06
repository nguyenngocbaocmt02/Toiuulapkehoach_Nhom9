from methods.greedy.ortools_greedy import OrtoolsMTSP
from utils.instance import Instance
from methods.ga.ga import GA
from methods.tabu_search.tabu_search import TabuSearch
from methods.greedy.default_greedy import Greedy
from methods.local_search.local_search import LocalSearch

instance = Instance("data/N200_K11")

#model = GA(pop_size=200, num_generations=200, mutation_probability=0.2, local_search_prob=0.4, keep_rate=0.1, time_limit=600)
#model = GA(pop_size=200, num_generations=200, mutation_probability=0.2, local_search_prob=0, keep_rate=0.1, time_limit=30)
#model = TabuSearch(tabu_list_length= 7 * len(instance.data["distance_matrix"]), max_iterations=10000, n_neighbors=10, intensification_factor=1.0, local_search_prob=0.4, time_limit=150)
#model = TabuSearch(tabu_list_length= 7 * len(instance.data["distance_matrix"]), max_iterations=10000, n_neighbors=10, intensification_factor=1.0, local_search_prob=0, time_limit=10)
#model = OrtoolsMTSP()
#model = Greedy()
model = LocalSearch(pop_size=100, num_generations=1000, time_limit=30)

best_routes, log = model.solve(instance)
print("Best routes: ", best_routes)
print("Check distance:", instance.obj_func(best_routes), log)
