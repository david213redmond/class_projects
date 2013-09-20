from pylab import *
from newton import solve

def g1(x):
    return x * cos(pi*x)

def g2(x):
    return 1 - .6*x**2

def g1g2(x):
    f = g1(x) - g2(x)
    fp = cos(pi*x) - x*pi*sin(pi*x) +  1.2*x
    return f, fp

##calculating the 4 zeros from the 4 initial guesses.
x_guesses = [-2.2,-1.6,-0.77,1.43]
zeros = []
for x0 in x_guesses:
    x, i = solve(g1g2, x0, False)
    zeros.append(x)
    print "With initial guess x0 = %22.15e," %x0
    print "      solve returns x = %22.15e after %i iterations" %(x,i)
    print

##plot the results
x = linspace(-5,5,500)
figure(1)
clf()
plot(x,g1(x))
plot(x,g2(x))
for i in range(4):
    plot(zeros[i],g1(zeros[i]),'ko')
savefig('intersections.png')



