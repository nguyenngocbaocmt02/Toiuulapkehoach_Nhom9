from methods.greedy.ortools_greedy import OrtoolsMTSP
from utils.instance import Instance
from methods.ga.ga import GA

instance = Instance("")
instance.create_example_data()

ga_model = GA(pop_size=200, num_generations=500, mutation_probability=0.2, local_search_prob=0.4, keep_rate=0.1)
best_routes, best_fitness = ga_model.solve(instance)
print("Best routes: ", best_routes)
print("Best distance: ", best_fitness)
print("Check distance:", instance.obj_func(best_routes))
