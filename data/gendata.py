import random
import os
def generate_random_working_time(N, limited_time):
    matrix = []
    for i in range(N):
        matrix.append(random.randint(0, limited_time))
    return matrix
def generate_random_distance_symmetric_matrix(k, limited_dis):
    matrix = []
    for i in range(k):
        row = []
        for j in range(k):
            if i == j:
                row.append(0)
            elif i > j:
                row.append(matrix[j][i])
            else:
                row.append(random.randint(0, limited_dis))
        matrix.append(row)
    return matrix

N = int(input("Enter the value of N: "))
K = int(input("Enter the value of K: "))

pre_limited_time = 3600
pre_limited_dis = 5000
pre_filename = 'N' + str(N) + '_' + 'K' + str(K)

input_limited_time = input("Enter the value of limited working time: ")
input_limited_dis = input("Enter the value of limited distance: ")
input_filename = input("Enter the value of output filename: ")

limited_time = int(input_limited_time) if input_limited_time != "" else pre_limited_time
limited_dis = int(input_limited_dis) if input_limited_dis != "" else pre_limited_dis
filename = input_filename if input_filename != "" else pre_filename

with open(filename, 'w') as file:
    matrix = generate_random_distance_symmetric_matrix(N+1, limited_dis)
    d = generate_random_working_time(N, limited_time)
    # Write N, K in 1st line
    file.write(str(N) + " " + str(K) + "\n")

    # Write d1, d2,.. dN in 2nd line
    d_str = ' '.join(str(x) for x in d)
    file.write(d_str + '\n')

    # Write distance matrix
    for row in matrix:
        row_str = ' '.join(str(x) for x in row)
        file.write(row_str + '\n')

print("The input has been saved in the file:", filename)




