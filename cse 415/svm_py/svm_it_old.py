import math
import random
K_matrix = []
omegaTx = []                    
X = []
y = []
a = []
b = 0
n = 0
C = 1                                       #constant, weight for loss function. KKT boundary.
TOL = 0.0001                                #tolerance.                                          
rho = 100                                   #kernel width 
epsilon = pow(10,-3)			    #KKT condition is fulfilled within epsilon.
def class_results():
    global omegaTx
    results = []
    for term in omegaTx:
        f = term - b
        results.append(f)
    return results

def dot_product(x1,x2):
    if len(x1) == len(x2):
        dot = 0
        for i in range(0,len(x1)):
            dot+=x1[i]*x2[i]
        return dot
    else:
        "There's an error when doing dot product of: "+ x1 +" and "+ x2

def vector_e_add(x1,x2):
    if len(x1) == len(x2):
        result = [0]*len(x1)
        for i in range(0,len(result)):
            result=x1[i]+x2[i]
        return result
    else:
        "There's an error when doing dot product of: "+x1+" and "+x2	

def vector_enlarge(x,m):
    for i in range(0,len(x)):
        x[i] = x[i] * m
    return x
	
def kernel(x1,x2):
    global rho
    norm_square = dot_product(x1,x1) - 2*dot_product(x1,x2) + dot_product(x2,x2)
    return math.exp(-0.5 * norm_square/pow(rho,2))

# def hyperplane():

#Storing a Kernel matrix lookup table for fast future access.
#n: how many data examples are there.
def create_K_matrix(n):
    global K_matrix
    K_matrix = [[1]*n]*n
    for i in range(0,n):
        for j in range(0,n):
            K_matrix[i][j] = kernel(X[i],X[j])
#n: how many data examples are there.
def update_omegaTx(n):
    global omegaTx
    omegaTx = [0]*n  
    for k in range(0,n):
        for i in range(0,n):
            omegaTx[k] = omegaTx[k] + a[i] * y[i] * K_matrix[i][k]
def init_alphas(n):
    global a
    global C
    for i in range(0,n):
        a.append(random.random()*C) #alpha's                            #random initialization of a, a in [0,C]
def update_W(n):
    tempSum = 0
    W = 0
    for i in range(0,n):
        for j in range(0,n):
            tempSum= tempSum + y[i]*y[j]*a[i]*a[j]*K_matrix[i][j]
        W= W + a[i]
    W = W - 0.5 * tempSum
    return W
        
def svm_main(data_zero, data_one):
    global K_matrix
    global omegaTx
    global epsilon
    global X
    global y
    global a
    global b
    global C
    global TOL
    X = data_zero + data_one
    X_dim = len(X[0])
    n = len(X)                                     #length of data.
    y = [-1]*len(data_zero)+[1]*len(data_one)
    #W is the objective function
    #initializations.
    init_alphas(n)
    create_K_matrix(n)
    update_omegaTx(n)
    Wold = update_W(n)
	
    #Selections of a's and b's
    #------------------------------------------------------------
    while True:	
        n1 = 0                                      #indices for the two locations.
        #n1 is chosen to be the first to violate the KKT condition.
        #using the first heuristic to choose a1.
        while n1 < n:
            f = omegaTx[n1] - b
            if (y[n1]*f < 1+epsilon and y[n1]*f > 1-epsilon) and a[n1] >= C and a[n1]<= 0:
                print(str(a[n1]) + ' breaks constraint 1 index: ' + str(n1))
                break
            if y[n1]*f > 1 and (a[n1]< -epsilon or a[n1] > epsilon):
                print(str(a[n1]) + ' breaks constraint 2 index: ' + str(n1))
                break
            if y[n1]*f < 1 and (a[n1] < C-epsilon  or a[n1] > C+epsilon):
                print(str(a[n1]) + ' breaks constraint 3 index: ' + str(n1))
                break
            n1 = n1 + 1
        #n2 is chosen by having the maximum |E1 - E2|
        E1 = 0
        E2 = 0
        maxDiff = 0	                            #maximum |E1 - E2|
        E1 = omegaTx[n1] - b - y[n1]	        #Error of choosing n1.
        for i in range(0,n):
            tempError = omegaTx[i] - b - y[i]
            if abs(E1 - tempError) > maxDiff:
                maxDiff = abs(E1 - tempError)
                n2 = i
                E2 = tempError
        #updates
        a1old = a[n1]
        a2old = a[n2]
        #a2 must satisfy the constraints.
        S = y[n1] * y[n2]
        if S == -1:
            L = max(0,a2old - a1old)
            H = min(C,C - a1old + a2old)
        else:
            L = max(0,a1old + a2old - C)
            H = min(C,a1old + a2old)
        #calculate new a2
        eta = 2*K_matrix[n1][n2] - K_matrix[n1][n1] - K_matrix[n2][n2]
        if eta < 0:
            a2new = a2old - y[n2] *(E1 - E2) / eta
            if a2new > H:
                a2new = H
            if a2new < L:
                a2new = L
        else:
            c1 = eta/2
            c2 = y[n2] * (E1-E2)- eta * a2old
            Lobj = c1 * L * L + c2 * L
            Hobj = c1 * H * H + c2 * H
            if Lobj > Hobj + epsilon:
                a2new = L
            elif Lobj < Hobj - epsilon:
                a2new = H
            else:
                a2new = a2old
        if a2new < 1e-8:
            a[n2] = 0
        elif a2new > C-1e-8:
            a[n2] = C
        else:
            a[n2] = a2new
            
        if abs(a2new - a2old) >= epsilon*(a2new + a2old + epsilon):
            #calculate new a1
            a[n1] = a1old + S * (a2old - a2new)	    
            #calculating b1, b2
            b1 = E1 + y[n1]*(a[n1] - a1old)*K_matrix[n1][n1] + y[n2]*(a[n2] - a2old)*K_matrix[n1][n2] + b
            b2 = E2 + y[n1]*(a[n1] - a1old)*K_matrix[n1][n2] + y[n2]*(a[n2] - a2old)*K_matrix[n2][n2] + b
            #updating b:
            b = (b1 + b2)/2
            #some updates
            #can optimize.
            update_omegaTx(n)
            Wnew = update_W(n)                            #W(a) after updating a.
            
            #loop exit condition: when the Dual Problem has reached a maximum objective function value.
            print('----------------------------------------------------')
            print(a)
            #print(class_results())
            if abs(Wnew/Wold - 1 ) <= TOL:
                break
    #------------------------------------------------------------ 
    #result: original classification,     
    #------------------------------------------------------------
    for i in range(0,n):
        f = omegaTx[i] - b
        print('point ',i+1)
        if i < len(data_zero):
            print('-1')
        else:
            print(' 1')
        print('    classification function value%f      classification result:',f)
        if abs(f - 1) < 0.5:
            print('1\n')
        elif abs(f + 1) < 0.5:
            print('-1\n')
        else:
            print('classification error\n')
    
    #return hyperplane()

#main
data_zero=[]
data_one=[]
for i in range(0,5):
    data_zero += [[100 + random.random()*5,100 + random.random()*5]]
for i in range(0,5):
    data_one = [[300 + random.random()*5,300 + random.random()*5]] * 5
svm_main(data_zero, data_one)
