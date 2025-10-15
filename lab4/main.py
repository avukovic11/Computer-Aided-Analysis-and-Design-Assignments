from functions import *
from point import Point
from lab4_utils import box_method, transformation_method

def print_results(f, optimal_point):
    print(f"Optimal point: {optimal_point}, Optimal value: {f(optimal_point)}")
    # print(f"Number of goal function evaluations: {f.num_goal_function_calls}")

f1 = Function1()
f2 = Function2()

implicit_constraints = [
    lambda point: point[1] - point[0],
    lambda point: 2 - point[0]
]

x_lower = [-100, -100]
x_upper = [100, 100]

print("TASK 1:")
x0 = Point([-1.9, 2])
optimal_point = box_method(f1, x0, implicit_constraints, x_lower, x_upper)
print_results(f1, optimal_point)

x0 = Point([0.1, 0.3])
optimal_point = box_method(f2, x0, implicit_constraints, x_lower, x_upper)
print_results(f2, optimal_point)

f1.reset_counters()
f2.reset_counters()
print("TASK 2:")
x0 = Point([-1.9, 2])
optimal_point = transformation_method(f1, x0, implicit_constraints, [])
print_results(f1, optimal_point)

x0 = Point([0.1, 0.3])
optimal_point = transformation_method(f2, x0, implicit_constraints, [])
print_results(f2, optimal_point)

print("TASK 3:")
f4 = Function4()
inequality_constraints = [
    lambda point: 3 - point[0] - point[1],
    lambda point: 3 + 1.5 * point[0] - point[1]
]

equality_constraints = [
    lambda point: point[1] - 1
]

x0 = Point([5, 5])
optimal_point = transformation_method(f4, x0, inequality_constraints, equality_constraints)
print_results(f4, optimal_point)