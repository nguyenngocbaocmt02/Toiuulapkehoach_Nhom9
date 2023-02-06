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


def create_input(N, K, limited_time=100, limited_dis=100):
    random.seed(0)
    filename = 'N' + str(N) + '_' + 'K' + str(K)
    with open(os.path.join("data", filename), 'w') as file:
        matrix = generate_random_distance_symmetric_matrix(N + 1, limited_dis)
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

Ns = [5, 10, 20, 50, 100, 200, 300, 400, 500] + [6, 7, 8, 9]
Ks = [int(y/20)+1 if y>20 else 2 for y in Ns] + [2, 2, 2, 2]
for i in range(len(Ns)):
    create_input(Ns[i], Ks[i])



