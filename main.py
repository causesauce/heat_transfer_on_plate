import numpy as np
import matplotlib.pyplot as plt

# number of rows
m = 40

# number of columns
n = 40

# setting temperatures for all the sides of the plane
top = 200
bottom = 150
left = 100
right = 50

plate = np.zeros((m + 2, n + 2))
for i in range(len(plate[0])):
    plate[0][i] = top
    plate[-1][i] = bottom

for i in range(len(plate)):
    plate[i][0] = left
    plate[i][-1] = right

plate[0][0] = None
plate[0][-1] = None
plate[-1][0] = None
plate[-1][-1] = None

array_of_unknowns_indices = []
for i in range(len(plate) - 2, 0, -1):
    for j in range(1, len(plate[i]) - 1, 1):
        array_of_unknowns_indices.append((i, j))

matrix_of_unknowns = []
results_matrix = []

for i in range(len(plate) - 2, 0, -1):
    for j in range(1, len(plate[i]) - 1, 1):

        result = 0.0
        tmp_array = [0] * (len(array_of_unknowns_indices))
        list_of_used_indices = []

        # T(i+1, j)
        if plate[i + 1][j] != 0:
            result -= plate[i + 1][j]
        else:
            list_of_used_indices.append((i + 1, j))

        # -4T(i, j)
        if plate[i][j] != 0:
            result -= plate[i][j]
        else:
            list_of_used_indices.append((i, j))

        # T(i-1, j)
        if plate[i - 1][j] != 0:
            result -= plate[i - 1][j]
        else:
            list_of_used_indices.append((i - 1, j))

        # T(i, j+1)
        if plate[i][j + 1] != 0:
            result -= plate[i][j + 1]
        else:
            list_of_used_indices.append((i, j + 1))

        # T(i, j-1)
        if plate[i][j - 1] != 0:
            result -= plate[i][j - 1]
        else:
            list_of_used_indices.append((i, j - 1))

        for k in range(len(array_of_unknowns_indices)):
            for index in list_of_used_indices:
                if index == array_of_unknowns_indices[k]:

                    if (i, j) == index:
                        tmp_array[k] += -4
                    else:
                        tmp_array[k] = 1

        results_matrix.append(result)
        matrix_of_unknowns.append(tmp_array)

# for i, j in zip(matrix_of_unknowns, results_matrix):
#     print(i, j)

x = np.linalg.solve(matrix_of_unknowns, results_matrix)
print(x)

counter = 0
for i in range(len(plate) - 2, 0, -1):
    for j in range(1, len(plate[i]) - 1, 1):
        plate[i][j] = x[counter]
        counter += 1

plate[0][0] = (plate[0][1] + plate[1][0] + plate[1][1]) / 3
plate[0][-1] = (plate[0][-2] + plate[1][-1] + plate[1][-2]) / 3
plate[-1][0] = (plate[-1][1] + plate[0][-2] + plate[-2][2]) / 3
plate[-1][-1] = (plate[-2][-1] + plate[-1][-2] + plate[-2][-2]) / 3

c = plate
plt.imshow(plate, cmap='hot')
plt.colorbar()
plt.show()

# print the matrix(map) of the temperatures
for i in plate:
    print(i)

