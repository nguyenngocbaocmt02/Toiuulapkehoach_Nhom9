import random
import numpy as np
import copy
import time

class TabuSearch:
    def __init__(self, tabu_list_length, n_neighbors, intensification_factor, local_search_prob, max_iterations, time_limit):
        self.tabu_list_length = tabu_list_length
        self.max_iterations = max_iterations
        self.n_neighbors = n_neighbors
        self.intensification_factor = intensification_factor
        self.local_search_prob = local_search_prob
        self.time_limit = time_limit
        
    def decode(self, individual, N):
        routes = []
        tmp = []
        for i in range(len(individual)):
            if individual[i] >= N:
                routes.append([0] + copy.deepcopy(tmp) + [0])
                tmp = []
            else:
                tmp.append(individual[i])
        routes.append([0] + copy.deepcopy(tmp) + [0])
        return routes
    
    def encode(self, routes):
        individual = []
        num_cities = 0
        for route in routes:
            num_cities += (len(route) - 2)
        for i, route in enumerate(routes):
            for pos in route[1:-1]:
                individual.append(pos)
            if i != len(routes) -1 :
                individual.append(i + 1 + num_cities)
        return individual

    def cost_route(self, distance_matrix, route):
        tmp = 0
        for i in range(0, len(route) - 1):
            tmp += distance_matrix[route[i]][route[i+1]]
        return tmp

    def fitness_function_individual(self, individual, distance_matrix):
        routes = self.decode(individual, len(distance_matrix))
        fitness = -float("inf")
        for route in routes:
            fitness = max(self.cost_route(distance_matrix, route), fitness)
        return fitness

    def generate_neighborhood(self, current_individual, distance_matrix, n_neighbors):
        neighborhood = []
        for i in range(len(current_individual) - 1):
            for j in range(i + 2, len(current_individual) - 1):
                new_individual = current_individual[:]
                new_individual[i + 1:j + 1] = reversed(new_individual[i + 1:j + 1])
                neighborhood.append(new_individual)      
        random.shuffle(neighborhood)    
        return neighborhood[:n_neighbors]

    def two_opt(self, distance_matrix, individual):
        routes = self.decode(individual, len(distance_matrix))
        for stt, route in enumerate(routes):
            for i in range(1, len(route) - 1):
                for j in range(i+1, len(route) - 1):
                    new_route = np.copy(route)
                    new_route[i:j+1] = route[j:i-1:-1]
                    new_cost = self.cost_route(distance_matrix, new_route)
                    current_cost = self.cost_route(distance_matrix, route)
                    if new_cost < current_cost:
                        routes[stt] = new_route
        return self.encode(routes)

    def local_search_2(self, distance_matrix, individual):
        routes = self.decode(individual, len(distance_matrix))
        improve = True
        max_stt, max_cost = None, -float("inf")
        min_stt, min_cost = None, float("inf")
        for stt, route in enumerate(routes):
            tmp = self.cost_route(distance_matrix, route)
            if tmp > max_cost:
                max_cost = tmp
                max_stt = stt
            if tmp < min_cost:
                min_cost = tmp
                min_stt = stt

        length = max_cost
        
        if min_stt != max_stt:
            new_routes = self.decode(individual, len(distance_matrix))
            new_routes[max_stt], new_routes[min_stt], new_length = self.optimize_routes(distance_matrix, new_routes[max_stt], new_routes[min_stt])
            if new_length < length:
                return self.encode(new_routes)     
               
        for i in range(len(routes)):
            if i == max_stt:
                continue
            new_routes = self.decode(individual, len(distance_matrix))
            new_routes[max_stt], new_routes[i], new_length = self.optimize_routes(distance_matrix, new_routes[max_stt], new_routes[i])
            if new_length < length:
                return self.encode(new_routes)
        return individual

    def optimize_routes(self, distance_matrix, route1, route2):
        max_length = max(self.cost_route(distance_matrix, route1), self.cost_route(distance_matrix, route2))
        res_route1 = copy.deepcopy(route1[:])
        res_route2 = copy.deepcopy(route2[:])
        for i in range(1, len(route1)-1):
            for j in range(1, len(route2)-1):
                new_route1 = route1[:]
                new_route2 = route2[:]
                new_route2.insert(j, new_route1.pop(i))
                new_length = max(self.cost_route(distance_matrix, new_route1), self.cost_route(distance_matrix, new_route2))
                if new_length < max_length:
                    res_route1 = new_route1
                    res_route2 = new_route2
                    max_length = new_length
        return res_route1, res_route2, max_length

    def solve(self, instance):
        distance_matrix = instance.data["distance_matrix"]
        K = instance.data["K"]
        individual_len = len(distance_matrix)
        gen_len = len(distance_matrix) + K - 2
        n_neighbors = np.copy(self.n_neighbors)
        begin_t = time.time()
        current_individual = [_ for _ in range(1, gen_len + 1)]
        random.shuffle(current_individual)
        tabu_list = []
        best_individual = current_individual
        best_cost = self.fitness_function_individual(current_individual, distance_matrix)
        log1 = []
        log2 = [1e9 for i in range(10)]
        for iteration in range(self.max_iterations):
            if iteration % 10 == 0:
                log1.append(best_cost)
            for i in range(len(log2)):
                if log2[i] != 1e9:
                    continue
                else:
                    if (time.time() - begin_t>= self.time_limit / 10.0 * i):
                        log2[i] = best_cost
            if time.time() - begin_t >= self.time_limit:
                log2[-1] = best_cost
                break 

            neighborhood = self.generate_neighborhood(current_individual, distance_matrix, n_neighbors)
            for i in range(len(neighborhood)):
                if random.uniform(0, 1) < self.local_search_prob:
                    neighborhood[i] = self.local_search_2(distance_matrix, neighborhood[i])
                    neighborhood[i] = self.two_opt(distance_matrix, neighborhood[i])
            best_neighbor = neighborhood[0]
            best_neighbor_cost = self.fitness_function_individual(best_neighbor, distance_matrix)
            for neighbor in neighborhood:
                cost = self.fitness_function_individual(neighbor, distance_matrix)
                if cost < best_neighbor_cost and neighbor not in tabu_list:
                    best_neighbor = neighbor
                    best_neighbor_cost = cost
            if best_neighbor_cost < best_cost:
                best_individual = best_neighbor
                best_cost = best_neighbor_cost
                n_neighbors = int(n_neighbors * self.intensification_factor)
            else:
                n_neighbors = int(n_neighbors / self.intensification_factor)
            if len(tabu_list) == self.tabu_list_length:
                tabu_list.pop(0)
            tabu_list.append(best_neighbor)
            current_individual = best_neighbor

        return self.decode(best_individual, len(distance_matrix)), log1, log2

