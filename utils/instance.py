class Instance:
    def __init__(self, file_path):
        # Read data from a file_path and create self.data like the example data in create_example_data() method 
        self.file_path = file_path
        path = self.file_path
        self.data = {}
        self.data['depot'] = 0
        with open(path, 'r') as file:
            lines = file.readlines()
            self.data['N'], self.data['K'] = [int(x) for x in lines[0].split()]
            self.data['working_time'] = [int(x) for x in lines[1].split()]
            self.data['working_time'].insert(0,0)
            self.data['distance_matrix'] = []
            for line in lines[2:]:
                row = [int(x) for x in line.split()]
                self.data['distance_matrix'].append(row)
            for i in range(self.data['N']+1):
                for j in range(self.data['N']+1):
                    if i != j:
                        self.data['distance_matrix'][i][j] += self.data['working_time'][j]             
    
    def create_example_data(self):
        """Stores the data for the problem, same as in ortools"""
        self.data = {}
        self.data['distance_matrix'] = [
            [
                0, 548, 776, 696, 582, 274, 502, 194, 308, 194, 536, 502, 388, 354,
                468, 776, 662
            ],
            [
                548, 0, 684, 308, 194, 502, 730, 354, 696, 742, 1084, 594, 480, 674,
                1016, 868, 1210
            ],
            [
                776, 684, 0, 992, 878, 502, 274, 810, 468, 742, 400, 1278, 1164,
                1130, 788, 1552, 754
            ],
            [
                696, 308, 992, 0, 114, 650, 878, 502, 844, 890, 1232, 514, 628, 822,
                1164, 560, 1358
            ],
            [
                582, 194, 878, 114, 0, 536, 764, 388, 730, 776, 1118, 400, 514, 708,
                1050, 674, 1244
            ],
            [
                274, 502, 502, 650, 536, 0, 228, 308, 194, 240, 582, 776, 662, 628,
                514, 1050, 708
            ],
            [
                502, 730, 274, 878, 764, 228, 0, 536, 194, 468, 354, 1004, 890, 856,
                514, 1278, 480
            ],
            [
                194, 354, 810, 502, 388, 308, 536, 0, 342, 388, 730, 468, 354, 320,
                662, 742, 856
            ],
            [
                308, 696, 468, 844, 730, 194, 194, 342, 0, 274, 388, 810, 696, 662,
                320, 1084, 514
            ],
            [
                194, 742, 742, 890, 776, 240, 468, 388, 274, 0, 342, 536, 422, 388,
                274, 810, 468
            ],
            [
                536, 1084, 400, 1232, 1118, 582, 354, 730, 388, 342, 0, 878, 764,
                730, 388, 1152, 354
            ],
            [
                502, 594, 1278, 514, 400, 776, 1004, 468, 810, 536, 878, 0, 114,
                308, 650, 274, 844
            ],
            [
                388, 480, 1164, 628, 514, 662, 890, 354, 696, 422, 764, 114, 0, 194,
                536, 388, 730
            ],
            [
                354, 674, 1130, 822, 708, 628, 856, 320, 662, 388, 730, 308, 194, 0,
                342, 422, 536
            ],
            [
                468, 1016, 788, 1164, 1050, 514, 514, 662, 320, 274, 388, 650, 536,
                342, 0, 764, 194
            ],
            [
                776, 868, 1552, 560, 674, 1050, 1278, 742, 1084, 810, 1152, 274,
                388, 422, 764, 0, 798
            ],
            [
                662, 1210, 754, 1358, 1244, 708, 480, 856, 514, 468, 354, 844, 730,
                536, 194, 798, 0
            ],
        ]
        self.data['K'] = 4
        self.data['depot'] = 0
        return self.data

    def obj_func(self, routes):
        visited  = [False for i in range(len(self.data["distance_matrix"]))]
        obj_val = - float("inf")
        route_cost = []
        for route in routes:
            tmp = 0
            if route[0] != self.data['depot'] or route[-1] != self.data['depot']:
                return False, float("inf"), []
            for i, cus in enumerate(route):
                visited[cus] = True
                tmp += self.data["distance_matrix"][route[i-1]][route[i]]
            tmp -= self.data["distance_matrix"][route[-1]][route[0]]
            obj_val = max(obj_val, tmp)
            route_cost.append(tmp)
        for i in visited:
            if i:
                continue
            else:
                return False, float("inf"), []
        return True, obj_val, route_cost
