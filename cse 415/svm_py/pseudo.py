##svm_smo.py
from scipy import *

class sparse_vector:
    def _init_(self):
        id=[]
        val=[]

#sparse dot product
def sparse_dot_prod(vec1,vec2):
    p1 = 0, p2 = 0, dot = 0
    while p1<num1 && p2<num2:
        a1 = id1[p1], a2 = id2[p2]
        if a1 == a2:
            dot+= val1[p1] *val2[p2]
            p1++, p2++
        elif a1 > a2:
            p2++
        else:
            p1++



target = []#desired output vector
point = []#training point matrix

def trainKernel():

def takeStep(i1,i2):
    if i1==i2: return 0
    alph1 = lagrange multiplier for i1
    y1 = target[i1]
    E1 = SVM output on point[i1] - y1 #check in error cache
    s = y1*y2
    Compute L,H
    if L == H:
        return 0
    #training kernel.
    k11 = kernel(point[i1], point[i1])
    k12 = kernel(point[i1], point[i2])
    k22 = kernel(point[i2], point[i2])
    eta = 2*k12-k11-k22
    if eta < 0:
        a2 = alph2 - y2*(E1-E2)/eta
        if a2 < L: a2 = L
        elif a2> H: a2 = H
    else:
        Lobj =#objective function at a2=L
        Hobj =#objective function at a2=H
        if Lobj > Hobj + eps:
            a2 = L
        elif Lobj < Hobj-eps:
            a2 = H
        else:
            a2 = alpha2

    if abs(a2-alph2) < eps*(a2+alpha2+eps):
        return 0
    a1 = alph1 + s*(alph2 - a2)
    #update threshold to reflect change in Lagrange multipliers
    #update weight vector to reflect change in a1 & a2, if linear SVM.
    #update error cache using new Lagrange multipliers
    #store a1 in the alpha array.
    #store a2 in the alpha array.
    return 1

def examineExample(i2):
    y2 = target[i2]
    alph2 = #lagrange multiplier for i2
    E2 = #SVM output on point[i2] - y2(check in error cache)
    r2 = E2*y2
    if (r2 < -tol && alph2 < C) || (r2 > tol && alph2 >0):
        if number of non-zero > 1 and non-C alpha>1:
            i1 = result of second choice heuristic
            if takeStep(i1,i2):
                return 1
        #loop over all non-zero and non-C alpha, starting at random point.
        loop:
            i1 = identity of current alpha
            if takeStep(i1,i2):
                return 1
        end
        #loop over all possible i1,starting at a random point.
        loop:
            i1 = loop variable
            if takeStep(i1,i2):
                return 1
    return 0


#main

#initialize alpha array to all zero
alph_array = [0]*m
#initialize threshold to zero.
numChanged = 0
examineAll = 1
while numChanged > 0 | examineAll:
    numChanged = 0
    if examineAll:
        #loop I over all training examples
        loop:
            numChanged += examineExample(I)
        end
    else:
        #loop I over examples where alpha is not 0 & not C.
        loop:
            numChanged += examineExample(I)
        end
    if examineAll == 1:
        examineAll = 0
    else if numChanged == 0:
        examineAll = 1

        
                
                
    
    
