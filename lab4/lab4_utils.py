from functions import *
from point import Point
from lab2_utils import hooke_jeeves
import random
import math

def satisfies_inequality_constraints(point, constraints):
    return all(constraint(point) > 0 for constraint in constraints)

def box_method(f, x0, implicit_constraints, x_lower, x_upper, alpha=1.3, epsilon=1e-6, max_iter=10000):
    dim = x0.dim
    for i in range(dim):
        if x0[i] < x_lower[i] or x0[i] > x_upper[i]:
            raise ValueError("Initial point does not satisfy explicit constraints")
    if not satisfies_inequality_constraints(x0, implicit_constraints):
        raise ValueError("Initial point does not satisfy implicit constraints")

    points = [x0.copy()]
    xc = x0.copy()

    for _ in range(2 * dim):
        x_new = Point([random.uniform(x_lower[i], x_upper[i]) for i in range(dim)])
        while not satisfies_inequality_constraints(x_new, implicit_constraints):
            x_new = (x_new + xc) / 2 # move point towards centroid
        points.append(x_new)
        points.sort(key=f)
        xc = sum(points[:-1], start=Point([0] * dim)) / (len(points) - 1)

    cnt = 0
    for _ in range(max_iter):
        points.sort(key=f)
        x_h = points[-1]
        x_h2 = points[-2]

        xc = sum(points[:-1], start=Point([0] * dim)) / (len(points) - 1)
        xr = (1 + alpha) * xc - alpha * x_h

        # check constraints
        for i in range(dim):
            if xr[i] < x_lower[i]:
                xr[i] = x_lower[i]
            elif xr[i] > x_upper[i]:
                xr[i] = x_upper[i]

        while not satisfies_inequality_constraints(xr, implicit_constraints):
            xr = (xr + xc) / 2

        if f(xr) > f(x_h2):
            xr = (xr + xc) / 2 # move point towards centroid

        points[-1] = xr # update worst point

        x_l_prev = points[0]
        x_l = min(points, key=f)

        if f(x_l) >= f(x_l_prev):
            cnt += 1
            if cnt == 100:
                print("Divergence")
                break
        else:
            cnt = 0

        # found this in script https://www.fer.unizg.hr/_download/repository/book[1].pdf
        # algorithm 6.3
        if math.sqrt(0.5 * sum((f(x_i) - f(xc))**2 for x_i in points)) < epsilon:
            break

    return x_l

def inner_point_method(x0, inequality_constraints, max_iter=10000):
    def G(x):
        return sum(-constraint(x) for constraint in inequality_constraints if constraint(x) < 0)
    
    x = x0.copy()
    for _ in range(max_iter):
        x = hooke_jeeves(G, x)
        if satisfies_inequality_constraints(x, inequality_constraints):
            return x
    return ValueError("Inner point method did not converge")

def transformation_method(f, x0, inequality_constraints, equality_constraints, t=1, epsilon=1e-6, max_iter=10000):
    def transformed_function(x):
        penalty = 0
        for constraint in inequality_constraints:
            if constraint(x) <= 0:
                return float('inf')
            else:
                penalty -= 1/t * math.log(constraint(x))
        for constraint in equality_constraints:
            penalty += t * constraint(x)**2
        
        return f(x) + penalty

    if not satisfies_inequality_constraints(x0, inequality_constraints):
        print("Initial point does not satisfy inequality constraints.")
        print("Applying inner point method...")
        x0 = inner_point_method(x0, inequality_constraints)
        print("Initial point after inner point method:", x0)
    x = x0.copy()
    cnt = 0
    for _ in range(max_iter):
        x_old = x.copy()
        x = hooke_jeeves(transformed_function, x)
        t *= 10

        if abs(f(x) - f(x_old)) < epsilon: # convergence
            break
        if f(x) >= f(x_old): # divergence
            cnt += 1
            if cnt == 100:
                print("Divergence")
                break
        else:
            cnt = 0

    return x