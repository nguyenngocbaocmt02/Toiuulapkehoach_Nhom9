from methods.greedy.ortools_greedy import OrtoolsMTSP
from utils.instance import Instance
from methods.ga.ga import GA
from methods.tabu_search.tabu_search import TabuSearch
instance = Instance("")
instance.create_example_data()

ga_model = GA(pop_size=200, num_generations=200, mutation_probability=0.2, local_search_prob=0, keep_rate=0.1)
best_routes, best_fitness = ga_model.solve(instance)
#tabu_model = TabuSearch(tabu_list_length= 7 * len(instance.data["distance_matrix"]), max_iterations=1000, n_neighbors=10, intensification_factor=1.0, local_search_prob=0.4)
#best_routes, best_fitness = tabu_model.solve(instance)
print("Best routes: ", best_routes)
print("Best distance: ", best_fitness)
print("Check distance:", instance.obj_func(best_routes))
