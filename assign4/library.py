# -*- coding: utf-8 -*-
"""library.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EZ0QrV3f3zC8WXPaPEibTTL4kvmaH-Z3
"""

def log(x, tol=1e-6):
    n = 10000
    return n * (x**(1/n) - 1)

def factorial(x):
    prod = 1
    if x == 0:
        return 1
    else:
        for i in range(2,x+1):
            prod *= i
        return prod

def sine_term(x, i):
    term = (((-1)**i)/(factorial(2*i + 1)))*x**(2*i + 1)
    return term

def sin(x, tol=1e-6):
    summation = 0
    i = 0
    diff = sine_term(x, i)
    while abs(diff) > tol:
        summation += diff
        i += 1
        diff = sine_term(x, i)

    return summation

def cos_term(x, i):
    term = (((-1)**i)/factorial(2*i))*x**(2*i)
    return term

def cos(x, tol=1e-6):
    summation = 0
    i = 0
    diff = cos_term(x, i)
    while abs(diff) > tol:
        summation += diff
        i += 1
        diff = cos_term(x, i)

    return summation

# Checks if the guess roots bracket around the actual root
def bracket(f, a, b):
    ct = 0   # keeps track of number of iterations
    beta = 0.5 # step value
    if a > b:
        print("'a' should be less than 'b'!!!")
        exit()
    else:
        prod = f(a)*f(b)
        if prod < 0:
            return a, b
        else:
            while prod > 0:
                if abs(f(a)) < abs(f(b)):
                    a = a - beta*(b-a)
                    ct += 1
                    prod = f(a) * f(b)

                elif abs(f(a)) > abs(f(b)):
                    b = b + beta*(b-a)
                    ct += 1
                    prod = f(a) * f(b)

            if ct > 12:
                print("Try another range.")
                exit()

            return a, b

# Bisection method of finding roots
def bisection(f, a, b, tol):
    a, b = bracket(f, a, b)
    iterations = []
    root_i = []
    abs_error = []
    max_iter = 200   # maximum iterations allowed
    for i in range(max_iter):
        c = (a+b)/2
        prod = f(a) * f(c)
        if prod < 0:
            b = c
        elif prod > 0:
            a = c

        iterations.append(i)
        root_i.append(c)
        error = abs(root_i[i] - root_i[i-1])
        abs_error.append(error)

        if abs(a-b)<tol:
            return c, abs_error, iterations

# Regula Falsi method of finding roots
def regula_falsi(f, a, b, tol):
    a, b = bracket(f, a, b)
    iterations = []
    root_i = []
    abs_error = []
    max_iter = 200
    c = a  # initial guess for the root
    for i in range(max_iter):
        c_prev = c
        c = b - ((b-a)*f(b))/(f(b) - f(a))
        if f(a) * f(c) < 0:
            b = c
        elif f(a) * f(c) > 0:
            a = c

        iterations.append(i)
        root_i.append(c)
        error = abs(root_i[i] - root_i[i-1])
        abs_error.append(error)

        if abs(c - c_prev) < tol:
            return c, abs_error, iterations

# Derivation function at x = x0 with default tolerance (h-value) = 1e-6
def derivative(f, x0, tol=1e-6):
    df = (f(x0+tol) - f(x0-tol))/(2*tol)
    return df

# Double derivative of a function with default tolerance (h-value) = 1e-6
def double_derivative(f, x0, tol=1e-6):
    f1 = derivative(f, x0) + tol
    f0 = derivative(f, x0) - tol
    ddf = (f1-f0)/(2*tol)
    return ddf

# Newton-Raphson method of finding roots
def newton_raphson(f, x0, tol):
    iterations = []
    abs_error = []
    max_iter = 200
    for i in range(max_iter):
        x_prev = x0
        x0 = x0 - (f(x0)/derivative(f, x0))
        iterations.append(i)
        abs_error.append(abs(x0 - x_prev))

        if abs(x0 - x_prev)<tol:
            return x0, abs_error, iterations

def write_table(col1, col2):
    table = [[ 0 for i in range(3)] for j in range(len(col1))]
    for i in range(len(col1)):
        for j in range(3):
            table[i][:] = [col1[i], col2[i]]
    return table

def print_table(table, head1, head2):
    data = table.copy()
    col1 = [head1]   # stores first column
    col2 = [head2]   # stores second column
    for i in range(len(data)):
        col1.append(data[i][0])
        col2.append(data[i][1])

    for i in range(len(data)+1):
        print(col1[i],"|", col2[i])

def polynomial(coeffs, x):
    degree = len(coeffs) - 1

    func = 0   # polynomial function
    for i in range(len(coeffs)):
        func += coeffs[i] * x**(degree-i)

    return func
    
# Uses synthetic division
def deflation(coeffs, x0):
    new_coeffs = []
    new_coeffs.append(coeffs[0])
    for i in range(1, len(coeffs)):
        new_coeffs.append(x0*new_coeffs[i-1] + coeffs[i])

    new_coeffs.pop()    # removes the last '0' from the new set of coefficients

    return new_coeffs

def poly_derivative(coeffs, alpha, tol=1e-6):
    dv = (polynomial(coeffs, alpha+tol) - polynomial(coeffs, alpha-tol))/(2*tol)
    return dv

def poly_double_derivative(coeffs, alpha, tol=1e-6):
    ddv = (poly_derivative(coeffs, alpha+tol) - poly_derivative(coeffs, alpha-tol))/(2*tol)
    return ddv

# Computes variables in Laguerre's method
def laguerre(coeffs, alpha, tol):
    n = len(coeffs) - 1    # n is the degree of the polynomial
    max_iter = 200

    if abs(polynomial(coeffs, alpha)) < tol:
        return alpha

    else:
        for i in range(max_iter):
            G = poly_derivative(coeffs, alpha)/(polynomial(coeffs, alpha))
            H = G**2 - (poly_double_derivative(coeffs, alpha)/polynomial(coeffs, alpha))

            denom1 = (G + ((n-1)*(n*H - G**2))**0.5)
            denom2 = (G - ((n-1)*(n*H - G**2))**0.5)
            if denom1 > denom2:
                a = n/denom1

            else:
                a = n/denom2

            alpha_prev = alpha
            alpha = alpha - a

            if abs(alpha - alpha_prev) < tol:
                x0 = alpha
                return x0

# Polynomial root solver using Laguerre's method
def polynomial_solver(coeffs, alpha, tol=1e-6):
    roots = []
    index = -1  # holds index position of newly added root
    while(len(coeffs) > 1):
        roots.append(laguerre(coeffs, alpha, tol))
        index += 1
        coeffs = deflation(coeffs, roots[index])

    return roots