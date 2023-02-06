import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from methods.ortools_greedy.ortools_greedy import OrtoolsGreedy
from utils.instance import Instance
from methods.ga.ga import GA
from methods.tabu_search.tabu_search import TabuSearch
from methods.greedy.default_greedy import Greedy
from methods.local_search.local_search import LocalSearch
from methods.brute_force.brute_force import BruteForce
from methods.ortools_lp.ortools_lp import LP
from methods.ortools_cp.ortools_cp import CP
import csv

def return_model(name, instance, time_limit):
    if method == "ga_local_search":
        model = model = GA(pop_size=200, num_generations=1000, mutation_probability=0.2, local_search_prob=0.4, keep_rate=0.1, time_limit=time_limit)
    if method == "ga":
        model = model = GA(pop_size=200, num_generations=1000, mutation_probability=0.2, local_search_prob=0, keep_rate=0.1, time_limit=time_limit)   
    if method == "tabu_local_search":
        model = TabuSearch(tabu_list_length= 7 * len(instance.data["distance_matrix"]), max_iterations=10000, n_neighbors=10, intensification_factor=1.0, local_search_prob=0.4, time_limit=time_limit)
    if method == "tabu":
        model = TabuSearch(tabu_list_length= 7 * len(instance.data["distance_matrix"]), max_iterations=10000, n_neighbors=10, intensification_factor=1.0, local_search_prob=0, time_limit=time_limit)
    if method == "local_search":
        model = LocalSearch(pop_size=100, num_generations=1000, time_limit=time_limit)
    if method == "ortools_greedy":
        model = OrtoolsGreedy(time_limit=time_limit)
    if method == "greedy":
        model = Greedy(time_limit=time_limit)
    if method == "lp":
        model = LP(time_limit)
    if method == "cp":
        model = CP(time_limit)
    if method == "brute_force":
        model = BruteForce(time_limit)
    return model

if __name__ == "__main__":
    method = sys.argv[1]
    dataset_folder_path = sys.argv[2]
    result_folder_path = sys.argv[3]
    time_limit = 15
    model = None
    
    result = []
    log1 = []
    log2 = []
    files = []
    for file in os.listdir(dataset_folder_path):
        input_file = os.path.join(dataset_folder_path, file)
        output_res_file = os.path.join(result_folder_path, method, "result.csv")
        output_log_file1 = os.path.join(result_folder_path, method, "log1.csv")
        output_log_file2 = os.path.join(result_folder_path, method, "log2.csv")
        
        instance = Instance(input_file)
        model = return_model(method, instance, time_limit)
        routes, l1, l2 = model.solve(instance)
        ttt = 1e9
        for i in range(len(l2)):
            ttt = min(ttt, l2[i])
            l2[i] = ttt
        if type(routes) == "list":
            res = instance.obj_func(routes)[1]
        else:
            res = routes

        files.append(file)
        result.append(res)
        log1.append(l1)
        log2.append(l2)
        
        os.makedirs(os.path.dirname(output_log_file1), exist_ok=True)
        os.makedirs(os.path.dirname(output_log_file2), exist_ok=True)
        os.makedirs(os.path.dirname(output_res_file), exist_ok=True)
        header = ["instance", method]
        with open(output_res_file, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            # write the header
            writer.writerow(header)
            # write the data
            for i in range(len(files)):
                data = [files[i], result[i]]
                writer.writerow(data)
        
        header = files
        with open(output_log_file1, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            # write the header
            writer.writerow(header)
            # write the data
            ite = 0
            while True:
                flag = True
                data = []
                for tmp in log1:
                    if ite >= len(tmp):
                        data.append("")
                    else:
                        data.append(tmp[ite])
                        flag = False
                writer.writerow(data)
                ite += 1
                if flag:
                    break

        header = files
        with open(output_log_file2, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            # write the header
            writer.writerow(header)
            # write the data
            ite = 0
            while True:
                flag = True
                data = []
                for tmp in log2:
                    if ite >= len(tmp):
                        data.append("")
                    else:
                        data.append(tmp[ite])
                        flag = False
                writer.writerow(data)
                if flag:
                    break       
                ite += 1     

                
