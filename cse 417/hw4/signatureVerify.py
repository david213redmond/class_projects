import numpy as np
import csv

gap_cost = 5

##return the cost value of the minimum cost alignment.
def signatureVerify(S1,S2):
    N1 = len(S1)+1
    N2 = len(S2)+1
    M = np.array([[0]*N2]*N1)
    for i in range(1,N1): M[i,0] = gap_cost*i
    for j in range(1,N2): M[0,j] = gap_cost*j
    for j in range(1,N2):
        for i in range(1,N1):
            Va = S1[i-1]
            Vb = S2[j-1]
            M[i,j] =  min((match_cost(Va,Vb) + M[i-1,j-1]),gap_cost+M[i-1,j],gap_cost+M[i,j-1])
    return M[N1-1,N2-1]


##calculate the match cost of the given two strokes.
def match_cost(v1,v2):
    if v1 == v2:
        return 0
    else:
        mode1 = v1[2]
        mode2 = v2[2]
        angle1 = int(v1[1])
        angle2 = int(v2[1])
        raw_angle_diff = abs(angle1 - angle2)
        angle_diff = 0
        if raw_angle_diff/4 >= 1:
            angle_diff = 4 - raw_angle_diff%4
        else:
            angle_diff = raw_angle_diff
        if mode1 != mode2:
            return 11
        else:
            if angle_diff == 1 and mode1 == 'u':
                return 1
            if angle_diff == 1 and mode1 == 'd':
                return 2
            if angle_diff == 2 and mode1 == 'u':
                return 2
            if angle_diff == 2 and mode1 == 'd':
                return 4
            if angle_diff > 2 and mode1 == 'u':
                return 4
            if angle_diff > 2 and mode1 == 'd':
                return 8

##main
data = []
filename = "basic.csv"
with open(filename, 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        data.append(row)

##the signatures of john hancock.
input = data[0]
val1 = signatureVerify(input,data[1])
val2 = signatureVerify(input,data[2])
val3 = signatureVerify(input,data[3])
val4 = signatureVerify(input,data[4])
val5 = signatureVerify(input,data[5])
val6 = signatureVerify(input,data[6])
print('basic examples')
print(val1) #6
print(val2) #5
print(val3) #0
print(val4) #20
print(val5) #2
print(val6) #24


data = []
filename = "John-sigs.csv"
with open(filename, 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        data.append(row)

##the signatures of john hancock.
john1 = data[0]
john2 = data[1]
john3 = data[2]

M_j1j2 = signatureVerify(john1,john2)
M_j1j3 = signatureVerify(john1,john3)

print('Advanced Examples')
print(M_j1j2)   ## M(john1, john2) = 45
print(M_j1j3)   ## M(john2, john3) = 212
