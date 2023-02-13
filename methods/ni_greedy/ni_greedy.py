def all_indexes_of_min(arr):
    min_value = min(arr)
    return [index for index, value in enumerate(arr) if value == min_value]

class NIGreedy:
    def __init__(self, time_limit):
        self.time_limit = time_limit

    def nearest_insertion(self, num_workers, num_customers, cost_matrix):
        current_customer = [0 for _ in range(num_workers)]
        unvisited_customers = set(range(1, num_customers + 1))
        routes = [[0] for _ in range(num_workers)]

        current_total_doing_time = [0 for _ in range(num_workers)]
        selected_workers = all_indexes_of_min(current_total_doing_time)
        while unvisited_customers:
            print("routes: ", routes)
            print("unvisited customers: ", unvisited_customers)
            print("current_customer: ", current_customer)
            print("current total doing time: ", current_total_doing_time)
            print("selected workers: ", selected_workers)
            # 1. Saving sum of doing time
            # 2. Select the workers having minimum time
            # 3. Find the customer for these workers that the route is min.
            # 4. Update sum of doing time for worker who just do, "current_customer", "routes" and "unvisited_customers".

            closest_customer = None
            closest_cost = float("inf")
            closest_worker = None
            for customer in unvisited_customers:
                for v in selected_workers:
                    distance = cost_matrix[current_customer[v]][customer]
                    if distance < closest_cost:
                        closest_customer = customer
                        closest_cost = distance
                        closest_worker = v
            routes[closest_worker].append(closest_customer)
            current_customer[closest_worker] = closest_customer
            unvisited_customers.remove(closest_customer)

            current_total_doing_time[closest_worker] += closest_cost
            selected_workers = all_indexes_of_min(current_total_doing_time)
        for route in routes:
            route.append(0)
        return routes

    def solve(self, instance):
        data = instance.data
        cost = data['distance_matrix']
        num_workers = data['K']
        num_customers = len(cost[0]) - 1
        return self.nearest_insertion(num_workers, num_customers, cost), [], []
