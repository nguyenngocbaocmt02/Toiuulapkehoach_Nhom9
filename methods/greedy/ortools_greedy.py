from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp 

class OrtoolsMTSP:
    def __init__(self):
        pass

    def solve(self, instance, time_limit=30):
        data = instance.data
        manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                            data['K'], data['depot'])
        routing = pywrapcp.RoutingModel(manager)
        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data['distance_matrix'][from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        dimension_name = 'Distance'
        routing.AddDimension(
            transit_callback_index,
            0,  # no slack
            int(1e10),  # vehicle maximum travel distance
            True,  # start cumul to zero
            dimension_name)
        distance_dimension = routing.GetDimensionOrDie(dimension_name)
        distance_dimension.SetGlobalSpanCostCoefficient(100)

        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.FIRST_UNBOUND_MIN_VALUE)
        #search_parameters.local_search_metaheuristic = (
        #    routing_enums_pb2.LocalSearchMetaheuristic.TABU_SEARCH)
        search_parameters.time_limit.seconds = time_limit    
        # Solve the problem.
        solution = routing.SolveWithParameters(search_parameters)

        def get_routes(solution, routing, manager):
            routes = []
            for route_nbr in range(routing.vehicles()):
                index = routing.Start(route_nbr)
                route = [manager.IndexToNode(index)]
                while not routing.IsEnd(index):
                    index = solution.Value(routing.NextVar(index))
                    route.append(manager.IndexToNode(index))
                routes.append(route)
            return routes
        return get_routes(solution, routing, manager)