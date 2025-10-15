import sys
from pathlib import Path

current_path = Path(__file__).resolve()
lab1_path = current_path.parents[2] / "lab1/0035235027"
sys.path.append(str(lab1_path))
lab2_path = current_path.parents[2] / "lab2/0035235027"
sys.path.append(str(lab2_path))

from matrix import Matrix
from point import Point
from lab2_utils import golden_section_search
from functions import *

def gradient_descent(f, x0, e=1e-6, use_golden_section=True, max_iter=10000):
    x = x0.copy()
    best_f_value = f(x.copy())
    no_improvement_count = 0
    grad = f.gradient(x.copy()).to_point()
    for i in range(max_iter):
        if use_golden_section:
            lambda_ = golden_section_search(lambda l: f.f_lambda(x, grad, l), 0)
        else:
            lambda_ = -1.
        x += lambda_ * grad
        grad = f.gradient(x.copy()).to_point()

        if best_f_value <= f(x):
            no_improvement_count += 1
            if no_improvement_count == 10:
                print("Error: Goal function value hasn't decreased for 10 iterations (algorithm diverged).")
                break
        else:
            best_f_value = f(x.copy())
            no_improvement_count = 0

        if grad.euclidean_norm() < e:
            break

    return x

def newton_raphson(f, x0, e=1e-6, use_golden_section=True, max_iter=10000):
    x = x0.copy()
    best_f_value = f(x.copy())
    no_improvement_count = 0
    for i in range(max_iter):
        grad = f.gradient(x.copy())
        hessian = f.hessian(x.copy())
        hessian.LUP_decomposition()
        delta_x = -1 * hessian.solve(grad).to_point()
        if use_golden_section:
            lambda_ = golden_section_search(lambda l: f.f_lambda(x, delta_x, l), 0)
        else:
            lambda_ = 1.
        
        x += lambda_ * delta_x

        if best_f_value <= f(x):
            no_improvement_count += 1
            if no_improvement_count == 10:
                print("Error: Goal function value hasn't decreased for 10 iterations (algorithm diverged).")
                break
        else:
            best_f_value = f(x.copy())
            no_improvement_count = 0

        if delta_x.euclidean_norm() < e:
            break

    return x

def gauss_newton(f, x0, e=1e-6, use_golden_section=True, max_iter=10000):
    x = x0.copy()
    best_f_value = f(x.copy())
    no_improvement_count = 0
    for i in range(max_iter):
        jacobian = f.jacobian(x.copy())
        G = f.g(x.copy())
        if jacobian.rows != jacobian.cols:
            A = ~jacobian @ jacobian
            g = ~jacobian @ G
        else:
            A = jacobian
            g = G
        A.LUP_decomposition()
        delta_x = -1 * A.solve(g).to_point()
        if use_golden_section:
            lambda_ = golden_section_search(lambda l: f.f_lambda(x, delta_x, l), 0)
        else:
            lambda_ = 1.
        
        x += lambda_ * delta_x

        if best_f_value <= f(x):
            no_improvement_count += 1
            if no_improvement_count == 10:
                print("Error: Goal function value hasn't decreased for 10 iterations (algorithm diverged).")
                break
        else:
            best_f_value = f(x.copy())
            no_improvement_count = 0

        if delta_x.euclidean_norm() < e:
            break
    return x