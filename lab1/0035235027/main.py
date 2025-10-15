from matrix import Matrix

def compare_matrices(directory):
    """
    Compares two matrices loaded from the same file to check for equality.
    Input: directory (str) - path to the directory containing the matrix file.
    Output: Prints the comparison results of matrix equality.
    """
    A = Matrix(from_file=directory+'task1.txt')
    B = Matrix(from_file=directory+'task1.txt')
    print("Matrix A (and B):\n", A)
    print("A==B:", A == B)

    n = 30.57638536459
    B = B * n / n
    print(f"\nMatrix B multiplied and divided by {n}:\n", B)
    print("A==B:", A == B)

def print_system_of_linear_equations(directory):
    """
    Loads and prints the system of linear equations represented by matrix A and vector b.
    Input: directory (str) - path to the directory containing 'A.txt' and 'b.txt'.
    Output: Prints matrix A and vector b in the form of Ax = b.
    """
    A = Matrix(from_file=directory+'A.txt')
    b = Matrix(from_file=directory+'b.txt')
    print("Ax = b")
    print("Matrix A:\n", A)
    print("Matrix b:\n", b)

def solve_system_of_linear_equations(directory, epsilon=1e-8):
    """
    Solves a system of linear equations using LU and LUP decomposition.
    Input: directory (str) - path to the directory containing 'A.txt' and 'b.txt'.
           epsilon (float, optional) - tolerance for numerical stability (default is 1e-8).
    Output: Prints the solution of the system if successful or an error message.
    """
    A = Matrix(from_file=directory+'A.txt')
    b = Matrix(from_file=directory+'b.txt')
    print_system_of_linear_equations(directory)
    print("")

    try:
        A.LU_decomposition(epsilon)
        x = A.solve(b, epsilon=epsilon)
        print("LU solution for x:\n", x)
    except ValueError as e:
        print(f"An error occurred in LU decomposition solution for x: {e}")

    A = Matrix(from_file=directory+'A.txt')
    b = Matrix(from_file=directory+'b.txt')
    
    try:
        A.LUP_decomposition(epsilon)
        x = A.solve(b, epsilon=epsilon)
        print("LUP solution for x:\n", x)
    except ValueError as e:
        print(f"An error occurred in LUP decomposition solution for x: {e}")

def print_inverse(directory):
    """
    Loads a matrix from a file and prints its inverse.
    Input: directory (str) - path to the directory containing 'A.txt'.
    Output: Prints the inverse of matrix A or an error message if it does not exist.
    """
    A = Matrix(from_file=directory+'A.txt')
    print("Matrix A:\n", A)
    print("")
    try:
        print("Inverse of A:\n", A.get_inverse())
    except ValueError as e:
        print(f"An error occurred in getting inverse of A: {e}")

def print_determinant(directory):
    """
    Loads a matrix from a file and prints its determinant.
    Input: directory (str) - path to the directory containing 'A.txt'.
    Output: Prints the determinant of matrix A or an error message if it cannot be computed.
    """
    A = Matrix(from_file=directory+'A.txt')
    print("Matrix A:\n", A)
    print("")
    try:
        print("Determinant of A:", A.get_determinant())
    except ValueError as e:
        print(f"An error occurred in getting determinant of A: {e}")

def __main__():
    """
    Executes a series of tasks including matrix comparison, solving systems of linear equations,
    finding matrix inverses, and computing determinants.
    Input: None.
    Output: Prints the results of each task, with separators between tasks.
    """
    print(f"TASK 1:")
    compare_matrices("tasks/task1/")
    print("------------------------------------------------")

    for i in range(2, 7):
        print(f"TASK {i}:")
        directory = f"tasks/task{i}/"
        epsilon = 1e-6 if i == 6 else 1e-8
        solve_system_of_linear_equations(directory, epsilon)
        print("------------------------------------------------")

    for i in range(7, 9):
        print(f"TASK {i}:")
        directory = f"tasks/task{i}/"
        print_inverse(directory)
        print("------------------------------------------------")

    for i in range(9, 11):
        print(f"TASK {i}:")
        directory = f"tasks/task{i}/"
        print_determinant(directory)
        print("------------------------------------------------")

if __name__ == "__main__":
    __main__()