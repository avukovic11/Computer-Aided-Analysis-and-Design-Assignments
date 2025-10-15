from functions import *
from lab3_utils import gradient_descent, newton_raphson, gauss_newton

def print_results(starting_point, optimal_point, f, algorithm):
    print("Starting point:", starting_point)
    print("Minimum:", optimal_point)
    print("Function value at minimum:", f(optimal_point))
    print("Number of goal function calls:", f.num_goal_function_calls - 1) # -1 because I call f in the line above
    if algorithm in ["Gradient Descent", "Newton-Raphson"]:
        print("Number of gradient calls:", f.num_gradient_calls)
    if algorithm == "Newton-Raphson":
        print("Number of hessian calls:", f.num_hessian_calls)
    if algorithm == "Gauss-Newton":
        print("Number of jacobian calls:", f.num_jacobian_calls)
    print("--------------------------------------------------")

def task1():
    print("TASK 1: f3 + GRADIENT DESCENT WITHOUT AND WITH GOLDEN SECTION")
    f3 = Function3()
    print("WITHOUT GOLDEN SECTION:")
    optimal_point = gradient_descent(f3, Point([0, 0]), use_golden_section=False)
    print_results(Point([0, 0]), optimal_point, f3, algorithm="Gradient Descent")

    f3.reset_counters()
    print("WITH GOLDEN SECTION:")
    optimal_point = gradient_descent(f3, Point([0, 0]), use_golden_section=True)
    print_results(Point([0, 0]), optimal_point, f3, algorithm="Gradient Descent")

def task2():
    # Newton-Raphson doesn't find the minimum of f2 in the first iteration because 
    # the default precision (1e-6) is too small
    # if we set it to 1e-5, it will find the minimum in the first iteration for f2?
    print("TASK 2: GRADIENT DESCENT VS NEWTON-RAPHSON METHOD FOR f1 AND f2")
    functions = [Function1(), Function2()]
    for i, f in enumerate(functions):
        print("Function", i+1)
        print("GRADIENT DESCENT:")
        f.reset_counters()
        optimal_point = gradient_descent(f, Point([-1.9, 2]) if i == 0 else Point([0.1, 0.3]), use_golden_section=True)
        print_results(Point([-1.9, 2]) if i == 0 else Point([0.1, 0.3]), optimal_point, f, algorithm="Gradient Descent")
        print("NEWTON-RAPHSON:")
        f.reset_counters()
        optimal_point = newton_raphson(f, Point([-1.9, 2]) if i == 0 else Point([0.1, 0.3]), use_golden_section=True)
        print_results(Point([-1.9, 2]) if i == 0 else Point([0.1, 0.3]), optimal_point, f, algorithm="Newton-Raphson")

def task3():
    print("TASK 3: f4 + NEWTON-RAPHSON METHOD WITHOUT AND WITH GOLDEN SECTION")
    f4 = Function4()
    starting_points = [Point([3, 3]), Point([1, 2])]
    for i, starting_point in enumerate(starting_points):
        f4.reset_counters()
        optimal_point = newton_raphson(f4, starting_point, use_golden_section=False)
        print("WITHOUT GOLDEN SECTION:")
        print_results(starting_point, optimal_point, f4, algorithm="Newton-Raphson")

        f4.reset_counters()
        optimal_point = newton_raphson(f4, starting_point, use_golden_section=True)
        print("WITH GOLDEN SECTION:")
        print_results(starting_point, optimal_point, f4, algorithm="Newton-Raphson")

def task4():
    print("TASK 4: f1 + GAUSS-NEWTON WITHOUT AND WITH GOLDEN SECTION")
    f1 = Function1()
    staring_point = Point([-1.9, 2])

    print("WITHOUT GOLDEN SECTION:")
    optimal_point = gauss_newton(f1, staring_point, use_golden_section=False)
    print_results(staring_point, optimal_point, f1, algorithm="Gauss-Newton")

    print("WITH GOLDEN SECTION:")
    f1.reset_counters()
    optimal_point = gauss_newton(f1, staring_point, use_golden_section=True)
    print_results(staring_point, optimal_point, f1, algorithm="Gauss-Newton")

def task5():
    print("TASK 5: f_task5 + GAUSS-NEWTON METHOD WITH GOLDEN SECTION")
    starting_points = [Point([-2, 2]), Point([2, 2]), Point([2, -2])]
    f = Function_Task5()
    for starting_point in starting_points:
        optimal_point = gauss_newton(f, starting_point, use_golden_section=True)
        print_results(starting_point, optimal_point, f, "Gauss-Newton")
        f.reset_counters()

def task6():
    print("TASK 6: f_task6 + GAUSS-NEWTON METHOD WITH GOLDEN SECTION")
    measurements = [(1, 3), (2, 4), (3, 4), (5, 5), (6, 6), (7, 8)]
    f = Function_Task6(measurements)
    starting_point = Point([1, 1, 1])

    optimal_point = gauss_newton(f, starting_point, use_golden_section=True)
    print_results(starting_point, optimal_point, f, "Gauss-Newton")

def main():
    tasks = [task1, task2, task3, task4, task5, task6]
    # tasks = [task2]
    for task in tasks:
        task()
        print("==================================================")
        print()

if __name__ == "__main__":
    main()