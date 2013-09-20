
"""
Demonstration module for quadratic interpolation.
Update this docstring to describe your code.
Modified by: ** your name here **
"""


import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import solve

def quad_interp(xi,yi):
    """
    Quadratic interpolation.  Compute the coefficients of the polynomial
    interpolating the points (xi[i],yi[i]) for i = 0,1,2.
    Returns c, an array containing the coefficients of
      p(x) = c[0] + c[1]*x + c[2]*x**2.

    """

    # check inputs and print error message if not valid:

    error_message = "xi and yi should have type numpy.ndarray"
    assert (type(xi) is np.ndarray) and (type(yi) is np.ndarray), error_message

    error_message = "xi and yi should have length 3"
    assert len(xi)==3 and len(yi)==3, error_message

    # Set up linear system to interpolate through data points:
    A = np.zeros((3,3))
    for i in range(0,3):
	for j in range(0,3):
		A[i,j] = pow(xi[i],j)
    b = yi
    c = solve(A,b)
    ### Fill in this part to compute c ###

    return c

def cubic_interp(xi,yi):
    """
    Cubic interpolation.  Compute the coefficients of the polynomial
    interpolating the points (xi[i],yi[i]) for i = 0,1,2.

    Returns c, an array containing the coefficients of
      p(x) = c[0] + c[1]*x + c[2]*x**2 + c[3]*x**3.

    """

    # check inputs and print error message if not valid:

    error_message = "xi and yi should have type numpy.ndarray"
    assert (type(xi) is np.ndarray) and (type(yi) is np.ndarray), error_message

    error_message = "xi and yi should have length 4"
    assert len(xi)==4 and len(yi)==4, error_message

    # Set up linear system to interpolate through data points:
    A = np.zeros((4,4))
    for i in range(0,4):
        for j in range(0,4):
                A[i,j] = pow(xi[i],j)
    b = yi
    c = solve(A,b)
    ### Fill in this part to compute c ###

    return c


def plot_quad(xi,yi):
    c = quad_interp(xi,yi)
    x = np.linspace(xi.min()-1, xi.max() + 1,1000)
    y = c[0] + c[1]*x + c[2]*x**2

    plt.figure(1)       # open plot figure window
    plt.clf()           # clear figure
    plt.plot(x,y,'b-')  # connect points with a blue line

    # Add data points  (polynomial should go through these points!)
    plt.plot(xi,yi,'ro')   # plot as red circles
    plt.ylim(-2,8)         # set limits in y for plot

    plt.title("Data points and interpolating polynomial")

    plt.savefig('hw2b.png')   # save figure as .png file

def plot_cubic(xi,yi):
    c = cubic_interp(xi,yi)
    x = np.linspace(xi.min()-1, xi.max() + 1,1000)
    y = c[0] + c[1]*x + c[2]*x**2 + c[3]*x**3

    plt.figure(1)       # open plot figure window
    plt.clf()           # clear figure
    plt.plot(x,y,'b-')  # connect points with a blue line

    # Add data points  (polynomial should go through these points!)
    plt.plot(xi,yi,'ro')   # plot as red circles
    plt.ylim(-2,8)         # set limits in y for plot

    plt.title("Data points and interpolating polynomial")

    plt.savefig('cubic.png')   # save figure as .png file


def test_quad1():
    """
    Test code, no return value or exception if test runs properly.
    """
    xi = np.array([-1.,  0.,  2.])
    yi = np.array([ 1., -1.,  7.])
    c = quad_interp(xi,yi)
    c_true = np.array([-1.,  0.,  2.])
    print "c =      ", c
    print "c_true = ", c_true
    # test that all elements have small error:
    assert np.allclose(c, c_true), \
        "Incorrect result, c = %s, Expected: c = %s" % (c,c_true)

def test_quad2():
    """
    Test code, no return value or exception if test runs properly.
    """
    xi = np.array([-1.,  2.,  5.])
    yi = np.array([ 1., -4.,  7.])
    test_quad(xi,yi)
    xi = np.array([1.,  3.,  5.])
    yi = np.array([ 2., -1.,  7.])
    test_quad(xi,yi)
    xi = np.array([5.,  1.,  2.])
    yi = np.array([ 3., -4.,  7.])
    test_quad(xi,yi)

def test_quad(xi,yi):
    c = quad_interp(xi,yi)
    A = np.vstack([np.ones(3),xi,xi**2]).T
    b = yi
    c_true = solve(A,b)
    print "c =      ", c
    print "c_true = ", c_true
    # test that all elements have small error:
    assert np.allclose(c, c_true), \
        "Incorrect result, c = %s, Expected: c = %s" % (c,c_true)

def test_cubic1():
    """
    Test code, no return value or exception if test runs properly.
    """
    xi = np.array([-1.,  2.,  5. ,1])
    yi = np.array([ 1., -4.,  7. , 5])
    test_cubic(xi,yi)

def test_cubic(xi,yi):
    c = cubic_interp(xi,yi)
    A = np.vstack([np.ones(4),xi,xi**2,xi**3]).T
    b = yi
    c_true = solve(A,b)
    print "c =      ", c
    print "c_true = ", c_true
    # test that all elements have small error:
    assert np.allclose(c, c_true), \
        "Incorrect result, c = %s, Expected: c = %s" % (c,c_true)


        
if __name__=="__main__":
    # "main program"
    # the code below is executed only if the module is executed at the command line,
    #    $ python demo2.py
    # or run from within Python, e.g. in IPython with
    #    In[ ]:  run demo2
    # not if the module is imported.
    print "Running test..."
    test_quad1()
    test_quad2()
    test_cubic1()


