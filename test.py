from methods.greedy.ortools_greedy import OrtoolsMTSP
from utils.instance import Instance

solver = OrtoolsMTSP()
instance = Instance("")
instance.create_example_data()

print(solver.solve(instance))