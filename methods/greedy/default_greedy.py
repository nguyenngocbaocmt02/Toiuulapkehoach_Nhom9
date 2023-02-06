class Greedy:
    def __init__(self, time_limit):
        self.time_limit = time_limit

    def greedy_mtsp(self, num_workers, num_customers, cost):
        # Initialize the solution with a random starting city for each vehicle
        current_customer = [0 for _ in range(num_workers)]
        unvisited_customers = set(range(1, num_customers+1))
        routes = [[] for _ in range(num_workers)]
        for v in range(num_workers):
            routes[v].append(current_customer[v])

        # Iterate over all unvisited cities and add them to the tour of the vehicle with the closest current city
        while unvisited_customers:
            closest_customer = None
            closest_cost = float("inf")
            closest_worker = None
            for customer in unvisited_customers:
                for v in range(num_workers):
                    distance = cost[current_customer[v]][customer]
                    if distance < closest_cost:
                        closest_customer = customer
                        closest_cost = distance
                        closest_worker = v
            routes[closest_worker].append(closest_customer)
            current_customer[closest_worker] = closest_customer
            unvisited_customers.remove(closest_customer)
        for route in routes:
            route.append(0)
        return routes

    def solve(self, instance):
        data = instance.data
        cost = data['distance_matrix']
        num_workers = data['K']
        num_customers = len(cost[0]) - 1
        return self.greedy_mtsp(num_workers, num_customers, cost), [], []