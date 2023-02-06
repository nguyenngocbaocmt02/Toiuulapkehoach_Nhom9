class CIGreedy:
    def __init__(self, time_limit):
        self.time_limit = time_limit
        

    def cheapest_insertion(self, num_workers, num_customers, cost_matrix):
        routes = [[0] for _ in range(num_workers)]
        unvisited_customers = set(range(1, num_customers + 1))
        current_customer = [0 for _ in range(num_workers)]
        while unvisited_customers:
            cheapest_customer = None
            cheapest_cost = float("inf")
            for v in range(num_workers):
                for city in unvisited_customers:
                    cost = cost_matrix[current_customer[v]][city]
                    if cost < cheapest_cost:
                        cheapest_customer = city
                        cheapest_cost = cost
                        cheapest_worker = v
            routes[cheapest_worker].append(cheapest_customer)
            current_customer[cheapest_worker] = cheapest_customer
            unvisited_customers.remove(cheapest_customer)
            for route in routes:
                route.append(0)
        return routes

    def solve(self, instance):
        data = instance.data
        cost = data['distance_matrix']
        num_workers = data['K']
        num_customers = len(cost[0]) - 1
        return self.cheapest_insertion(num_workers, num_customers, cost),[],[]

    