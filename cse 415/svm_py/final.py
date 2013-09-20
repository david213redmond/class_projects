import math
import random
K_matrix = []
omegaX = []                    
X = []
y = []
E = []
a = []
b = 0
n = 0
C = 1                                       #constant, weight for loss function. KKT boundary.
Tol = 0.0001                                #tolerance.                                          
rho = 100                                   #kernel width 
epsilon = pow(10,-3)			    #KKT condition is fulfilled within epsilon.

def classify(omegaX,b):
    global n
    global y
    results = []
    for i in range(0,n):
        f = omegaX[i]-b
        results.append(f*y[i])
    return results

#Storing a Kernel matrix lookup table for fast future access.
#n: how many data examples are there.
def create_K_matrix(n):
    global K_matrix
    global X
    K_matrix = [[1]*n]*n
    for i in range(0,n):
        for j in range(0,n):
            K_matrix[i][j] = kernel(X[i],X[j])

def dot_product(x1,x2):
    if len(x1) == len(x2):
        dot = 0
        for i in range(0,len(x1)):
            dot+=x1[i]*x2[i]
        return dot
    else:
        "There's an error when doing dot product of: "+ x1 +" and "+ x2
            
def init_alphas(n):
    global a
    global C
    for i in range(0,n):
        a.append(random.random()*C) #random initialization of a, a in [0,C]

def init_error_cache(n):
    global E
    global X
    global y
    global a
    global b
    global K_matrix
    omegaX = [0]*n
    E = []
    for k in range(0,n):
        for i in range(0,n):
            omegaX[k] += a[i]*y[i]*K_matrix[i][k]
    for i in range(0,n):
        f = omegaX[i] - b
        error = f - y[i]
        E.append(error)

def kernel(X1,X2):
    global rho
    norm_square = dot_product(X1,X1) - 2*dot_product(X1,X2) + dot_product(X2,X2)
    return math.exp(-0.5 * norm_square/pow(rho,2))

def update_obj(n):
    global a
    global y
    global K_matrix
    tempSum = 0
    W = 0
    for i in range(0,n):
        for j in range(0,n):
            tempSum= tempSum + y[i]*y[j]*a[i]*a[j]*K_matrix[i][j]
        W= W + a[i]
    W = W - 0.5 * tempSum
    return W

def update_omegaX():
    global n
    global X
    global y
    global a
    global K_matrix
    global omegaX
    omegaX = [0]*n
    for k in range(0,n):
        for i in range(0,n):
            omegaX[k] += a[i]*y[i]*K_matrix[i][k]

def takeStep(i1, i2):
    global a
    global b
    global y
    global epsilon
    global K_matrix
    global n
    global omegaX
    if i1 == i2:
        return 0
    a1old = a[i1]; a2old = a[i2]
    a1 = 0; a2 = 0
    y1 = y[i1] ; y2 = y[i2]
    bold = b
    update_omegaX()
    f1 = omegaX[i1] -b ; f2 = omegaX[i2] -b
    E1 = f1 - y1 ; E2 = f2 - y2
    s = y1*y2
    L = 0 ; H=0;
    if s == -1:
        L = max(0, a2old - a1old)
        H = min(C, C + a2old - a1old)
    else:
        L = max(0, a1old + a2old - C)
        H = min(C, a1old + a2old)
    if L==H:
        return 0
    k11 = K_matrix[i1][i1]
    k12 = K_matrix[i1][i2]
    k22 = K_matrix[i2][i2]
    eta = 2 * k12 - k11 - k22
    if eta < 0:
        a2 = a2old - y2*(E1-E2)/eta
        if a2 < L:
            a2 = L
        if a2 > H: 
            a2 = H
    else:
        c1 = eta/2
        c2 = y2 * (E1-E2) - eta * a2old
        Lobj = c1 * L * L + c2 * L
        Hobj = c1 * H * H + c2 * H
        if Lobj > Hobj + epsilon:
            a2 = L
        elif Lobj < Hobj - epsilon:
            a2 = H
        else:
            a2 = a2old
    if a2 < 1e-8:
        a2 = 0
    elif a2 > C-1e-8:
       a2 = C
    if abs(a2 - a2old) < epsilon * (a2 + a2old + epsilon):
        return 0
    a1 = a1old + s*(a2old - a2)
    b1 = E1 + y1 * (a1 - a1old) * k11 + y2 * (a2 - a2old) * k12 + bold
    b2 = E1 + y1 * (a1 - a1old) * k12 + y2 * (a2 - a2old) * k22 + bold
    if a1 > 0 and a1 < C:
        b = b2
    else:
        if a2 > 0 and a2 < C:
            b = b1
        else:
            b = (b1 + b2) / 2
    #update error cache.
    for k in range(0,n):
        f = omegaX[k] - b
        E[k] = f - y[k]
    E[i1] = 0
    E[i2] = 0
    a[i1] = a1
    a[i2] = a2
    update_omegaX()
    return 1

def examineExample(i1):
    global y
    global C
    global Tol
    global n
    global b
    global omegaX
    y1 = y[i1]
    a1old = a[i1]
    E1 = 0
    #correctly iterating through the whole alphas array.
    if a1old >0 and a1old<C:
        E1 = E[i1]
    else:
        f = omegaX[i1] -b
        E1 = f-y1
    r1 = E1 * y1
    
    
    if (r1 < -Tol and a1old < C) or(r1 > Tol and a1old > 0):
        a_index = 0
        a_nonBound = []
        #count the alphas that is non-zero or non-C.
        for alpha in a:
            if (alpha != 0 or alpha !=C): a_nonBound.append(a_index)
            a_index += 1
        if len(a_nonBound) > 0:
            #using norm of error difference as step size is the second choice heuristic.
            step_max = 0
            i2 = -1
            for k in range(0,n):
                E2 = E[k]
                step_size = abs(E1 - E2)
                if step_size > step_max:
                    i2 = k
            #print('2nd heuristic chose: '+str(i2))
            if i2 >= 0:
                if takeStep(i1,i2):
                    #print('after using 2nd heuristic to check')
                    return 1
        #loop over all non-zero and non-C alpha, starting at random point
        while len(a_nonBound) > 0:
            index = math.floor(random.random() * len(a_nonBound))
            i2 = a_nonBound[index]
            a_nonBound.remove(i2)
            if takeStep(i1,i2):
                return 1
        #loop over all possible i2, starting at a random point
        temp_a = a[:]
        while len(temp_a) > 0:
            i2 = math.floor(random.random() * len(temp_a))
            temp_a.remove(temp_a[i2])
            if takeStep(i1,i2):
                return 1
    return 0

##main
def svm_main(data_pos, data_neg):
    global X
    global a
    global n
    global y
    global C
    #initializations
    X = data_pos + data_neg
    y = [1]*len(data_pos) + [-1]*len(data_neg)
    n = len(X)
    create_K_matrix(n)
    init_alphas(n)
    init_error_cache(n)
    b = 0
    #save raw parameters before training
    b_raw = b
    update_omegaX()
    omegaX_raw = omegaX[:]
    numChanged = 0
    examineAll = 1
    #first choice heuristic to choose i1.
    while numChanged > 0 or examineAll:
        numChanged = 0
        if examineAll:
            for i in range(0,n):
                numChanged += examineExample(i)
            #print('one run of all examples')
        else:
            a_nonBoundI = []
            for i in range(0,n):
                if a[i] != 0 and a[i] != C:
                    a_nonBoundI.append(i)
            for i in a_nonBoundI:
                # alphas are not changing.
                numChanged += examineExample(i)
            #print('one round of non-bound examples')
        if examineAll:
            examineAll = 0
        elif numChanged == 0:
            examineAll = 1
##        print(numChanged)
##        print(a)
##        print('W--->' + str(update_obj(n)))
    #results printing
    print('error after training:')
    print(E)
    print("--------------------------------------------------")
    print('original class labels:')
    print(y)
    print('trained results:')
    print(classify(omegaX,b))

d1 = [[500*random.random()]] * 6
d2 = [[100*random.random()]] * 10
svm_main(d1,d2)













