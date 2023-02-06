from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

class CP:
    def __init__(self):
        pass

    def print_solution(self, manager, routing, solution):
        #print(f'Objective: {solution.ObjectiveValue()}')
        max_route_distance = 0
        for vehicle_id in range(self.K):
            index = routing.Start(vehicle_id)
            plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
            route_distance = 0
            while not routing.IsEnd(index):
                plan_output += ' {} -> '.format(manager.IndexToNode(index))
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(
                    previous_index, index, vehicle_id)
            #plan_output += '{}\n'.format(manager.IndexToNode(index))
            #plan_output += 'Distance of the route: {}m\n'.format(route_distance)
            #print(plan_output)
            max_route_distance = max(route_distance, max_route_distance)
        return max_route_distance



    def solve(self, instance):
        self.distance_matrix = instance.data["distance_matrix"]
        self.K = instance.data["K"]

        manager = pywrapcp.RoutingIndexManager(len(self.distance_matrix),K,0),

        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return self.distance_matrix[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        dimension_name = 'Distance'
        routing.AddDimension(
            transit_callback_index,
            0,  # no slack
            3000,  # vehicle maximum travel distance
            True,  # start cumul to zero
            dimension_name)
        distance_dimension = routing.GetDimensionOrDie(dimension_name)
        distance_dimension.SetGlobalSpanCostCoefficient(100)

        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        # Solve the problem.
        solution = routing.SolveWithParameters(search_parameters)

        # Print solution on console.
        if solution:
            return self.print_solution(self, manager, routing, solution)
        else:
            print('No solution found !')
