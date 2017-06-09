#!/usr/bin/env python3
import numpy as np

np.set_printoptions(suppress=True, linewidth=300)

#the last n-1 rows are considered to be <=, the 0th is our optimization
constraint_matrix = np.array(
    [[13.0, 23.0, 0.0],
     [5.0, 15.0, 480.0],
     [4.0, 4.0, 160.0],
     [35.0, 20.0, 1190.0]]
    )

final_col = constraint_matrix[:, -1]
constraint_matrix = constraint_matrix[:, :-1]

#add in our slack variables
for i, _ in enumerate(constraint_matrix):
    tmp = []
    for _ in range(i):
        tmp.append(0)
    tmp.append(-1 if i == 0 else 1)
    for _ in range(len(constraint_matrix)-i-1):
        tmp.append(0)
    constraint_matrix = np.append(constraint_matrix, np.array([tmp]).T, axis=1)
#print(final_col)
constraint_matrix = np.concatenate((constraint_matrix, np.array([final_col]).T), axis=1)

def findPivot():
    pvCol = -1
    for i in range(len(constraint_matrix[0])-1):
        if constraint_matrix[0][i] > 0:
            pvCol = i
            break
    if pvCol == -1:
        return -1, -1
    tmpMin = constraint_matrix[1][-1]/constraint_matrix[1][pvCol]
    pvRow = 1
    for i in range(1, len(constraint_matrix)):
        ratio = constraint_matrix[i][-1]/constraint_matrix[i][pvCol]
        if ratio < tmpMin:
            pvRow = i
            tmpMin = ratio
    return pvRow, pvCol

def performPivot(row, col):
    print("Pivoting on %d, %d"%(row, col))
    #let c be a row resulting from solving for M[r][c]
    c = constraint_matrix[row]
    constraint_matrix[row] *= 1/c[col]
    c = (1/c[col])*c
    c *= [-1 for _ in range(1, len(c))] + [1]
    c[col] = -1
    print(c)
    for i, _ in enumerate(constraint_matrix):
        if i == row:
            continue
        constraint_matrix[i] += constraint_matrix[i][col]*c

print(constraint_matrix)
r, c = findPivot()
while r != -1 and c != -1:
    performPivot(r, c)
    r, c = findPivot()
    print(constraint_matrix)
