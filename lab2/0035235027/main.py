import math
import random
from tabulate import tabulate
from point import Point
from lab2_utils import golden_section_search, coordinate_search, hooke_jeeves, nelder_mead

def f_task1(x):
    if isinstance(x, Point):
        return (x[0]-3)**2
    return (x-3)**2

def f1(x):
    return 100 * (x[1] - x[0]**2)**2 + (1 - x[0])**2

def f2(x):
    return (x[0] - 4)**2 + 4 * (x[1] - 2)**2

def f3(x):
    return sum((x[i] - i)**2 for i in range(x.dim))

def f4(x):
    return abs((x[0] - x[1]) * (x[0] + x[1])) + (x[0]**2 + x[1]**2)**0.5

def f6(x):
    return 0.5 + (math.sin((sum(xi**2 for xi in x))**0.5) - 0.5) / (1 + 0.001 * sum(xi**2 for xi in x))**2

function_starting_points = {
    # f_task1: Point([10]),
    f1: Point([-1.9, 2]),
    f2: Point([0.1, 0.3]),
    f3: Point([0, 0, 0, 0, 0]),
    f4: Point([5.1, 1.1]),
    # f6: Point([0, 0, 0, 0, 0])
}

print("TASK 1:")
results = []
for start_point in [10, 100, 1000]:
    start_point = Point([start_point])
    for algorithm in [golden_section_search, coordinate_search, hooke_jeeves, nelder_mead]:
        sp = start_point.copy() # because start_point is modified in the loop
        result, num_iterations = algorithm(f_task1, sp, return_num_iterations=True)
        results.append([start_point, algorithm.__name__, num_iterations, result, f_task1(result)])
headers = ["Starting Point", "Algorithm", "Iterations", "Optimum", "f(Optimum)"]
print(tabulate(results, headers=headers, tablefmt="grid"))

print("TASK 2:")
results = []
for f, start_point in function_starting_points.items():
    for algorithm in [nelder_mead, hooke_jeeves, coordinate_search]:
        sp = start_point.copy() # because start_point is modified in the loop
        result, num_iterations = algorithm(f, start_point, return_num_iterations=True)
        results.append([f.__name__, algorithm.__name__, num_iterations, result, f(result)])
headers = ["Function", "Algorithm", "Iterations", "Optimum", "f(Optimum)"]
print(tabulate(results, headers=headers, tablefmt="grid"))

print("TASK 3:")
results = []
for algorithm in [nelder_mead, hooke_jeeves]:
    result, num_iterations = algorithm(f4, Point([5, 5]), return_num_iterations=True)
    results.append([algorithm.__name__, num_iterations, result, f4(result)])
headers = ["Algorithm", "Iterations", "Optimum", "f(Optimum)"]
print(tabulate(results, headers=headers, tablefmt="grid"))

print("TASK 4:")
starting_points = [Point([0.5, 0.5]), Point([20, 20])]
step_sizes = range(1, 21)
results = []
for start_point in starting_points:
    for step in step_sizes:
        sp = start_point.copy()
        result, num_iterations = nelder_mead(f1, sp, step=step, return_num_iterations=True)
        results.append([start_point, step, num_iterations, result, f1(result)])
headers = ["Starting Point", "Step Size", "Iterations", "Optimum", "f(Optimum)"]
print(tabulate([results[0], results[19], results[20], results[-1]], headers=headers, tablefmt="grid"))

print("TASK 5:")
num_trials = 100
success_count = 0
results = []
for i in range(num_trials):
    start_point = Point([random.uniform(-50, 50) for _ in range(2)])
    result = nelder_mead(f6, start_point)
    if abs(f6(result)) < 1e-4:
        success_count += 1
probability = success_count / num_trials
print(f"Probability of finding the global optimum: {probability:.2f}")