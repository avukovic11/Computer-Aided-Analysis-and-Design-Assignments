import sys
from pathlib import Path

current_path = Path(__file__).resolve()
lab2_path = current_path.parents[2] / "lab2/0035235027"
sys.path.append(str(lab2_path))

class Matrix:
    def __init__(self, rows=0, cols=0, from_file=None, data=None):
        """
        Initializes a matrix with a specified number of rows and columns, loads data from a file, or initializes with provided data.
        Input: rows (int), cols (int), from_file (str - file name, optional), data (list of lists of floats, optional).
        Output: None.
        """
        if from_file:
            self.data = self._load_from_file(from_file)
            self.rows = len(self.data)
            self.cols = len(self.data[0])
        elif data:
            self.data = data
            self.rows = len(data)
            self.cols = len(data[0])
        else:
            self.rows = rows
            self.cols = cols
            self.data = [[0.0 for _ in range(cols)] for _ in range(rows)]
        self.num_switches = 0

    def add_row(self, new_row):
        """
        Adds a new row to the matrix.
        Input: new_row (list of floats).
        Output: None.
        """
        if len(new_row) != self.cols:
            raise ValueError("The new row must have the same number of columns as the matrix.")
        self.data.append(new_row)
        self.rows += 1

    def to_point(self):
        """
        Converts the matrix to a point if it has one column.
        Output: Point.
        """
        from point import Point
        if self.cols != 1:
            raise ValueError("Matrix must have exactly one column to convert to a Point.")
        return Point([row[0] for row in self.data])

    def _load_from_file(self, file_name):
        """
        Loads matrix data from a file.
        Input: file_name (str).
        Output: matrix (list of lists of floats).
        """
        with open(file_name, 'r') as f:
            matrix = [list(map(float, line.split())) for line in f]
        return matrix

    def save_to_file(self, file_name):
        """
        Saves matrix data to a file.
        Input: file_name (str).
        Output: None.
        """
        with open(file_name, 'w') as f:
                f.write('\n'.join(' '.join(map(str, row)) for row in self.data))

    def __str__(self):
        """
        Returns a string representation of the matrix.
        Input: None.
        Output: A string showing matrix rows.
        """
        return '\n'.join(' '.join(map(str, row)) for row in self.data)

    def __getitem__(self, idx):
        """
        Returns the row at the specified index.
        Input: idx (int - row index).
        Output: A list representing the row.
        """
        return self.data[idx]

    def __setitem__(self, idx, value):
        """
        Sets the row at the specified index to the given value.
        Input: idx (int - row index), value (list of floats).
        Output: None.
        """
        self.data[idx] = float(value)

    def __eq__(self, other):
        """
        Checks if two matrices are equal.
        Input: other (Matrix).
        Output: True if matrices are equal, False otherwise.
        """
        if self.rows != other.rows or self.cols != other.cols:
            return False
        for i in range(self.rows):
            for j in range(self.cols):
                if self.data[i][j] != other.data[i][j]:
                    return False
        return True

    def __add__(self, other):
        """
        Adds two matrices of the same dimensions.
        Input: other (Matrix).
        Output: A new matrix representing the sum.
        """
        if self.rows != other.rows or self.cols != other.cols:
            self.__raise_dimensions_error(other, "addition")

        result = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                result.data[i][j] = self.data[i][j] + other.data[i][j]
        return result

    def __iadd__(self, other):
        """
        In-place addition of two matrices.
        Input: other (Matrix).
        Output: Updated matrix after addition.
        """
        if self.rows != other.rows or self.cols != other.cols:
            self.__raise_dimensions_error(other, "addition")

        for i in range(self.rows):
            for j in range(self.cols):
                self.data[i][j] += other.data[i][j]
        return self

    def __sub__(self, other):
        """
        Subtracts another matrix from this matrix.
        Input: other (Matrix).
        Output: A new matrix representing the difference.
        """
        if self.rows != other.rows or self.cols != other.cols:
            self.__raise_dimensions_error(other, "subtraction")

        result = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                result.data[i][j] = self.data[i][j] - other.data[i][j]
        return result

    def __isub__(self, other):
        """
        In-place subtraction of another matrix.
        Input: other (Matrix).
        Output: Updated matrix after subtraction.
        """
        if self.rows != other.rows or self.cols != other.cols:
            self.__raise_dimensions_error(other, "subtraction")

        for i in range(self.rows):
            for j in range(self.cols):
                self.data[i][j] -= other.data[i][j]
        return self
    
    def __truediv__(self, scalar):
        """
        Divides each element of the matrix by a scalar.
        Input: scalar (float).
        Output: A new matrix after division.
        """
        if scalar == 0:
            raise ValueError("Can't divide by zero.")
        result = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                result.data[i][j] = self.data[i][j] / scalar
        return result

    def __itruediv__(self, scalar):
        """
        In-place division of each matrix element by a scalar.
        Input: scalar (float).
        Output: Updated matrix after division.
        """
        if scalar == 0:
            raise ValueError("Can't divide by zero.")
        for i in range(self.rows):
            for j in range(self.cols):
                self.data[i][j] /= scalar
        return self
    
    def __rttuediv__(self, scalar):
        """
        Divides each element of the matrix by a scalar (reverse).
        Input: scalar (float).
        Output: A new matrix after division.
        """
        return self.__truediv__(scalar)

    def __mul__(self, scalar):
        """
        Multiplies each element of the matrix by a scalar.
        Input: scalar (float).
        Output: A new matrix after multiplication.
        """
        result = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                result.data[i][j] = self.data[i][j] * scalar
        return result
    
    def __rmul__(self, scalar):
        """
        Multiplies each element of the matrix by a scalar (reverse).
        Input: scalar (float).
        Output: A new matrix after multiplication.
        """
        return self.__mul__(scalar)
    
    def __imul__(self, scalar):
        """
        In-place multiplication of each matrix element by a scalar.
        Input: scalar (float).
        Output: Updated matrix after multiplication.
        """
        for i in range(self.rows):
            for j in range(self.cols):
                self.data[i][j] *= scalar
        return self

    def __matmul__(self, other):
        """
        Multiplies this matrix by another matrix (matrix multiplication).
        Input: other (Matrix).
        Output: A new matrix after multiplication.
        """
        if self.cols != other.rows:
            self.__raise_dimensions_error(other, "matrix multiplication")

        result = Matrix(self.rows, other.cols)
        for i in range(self.rows):
            for j in range(other.cols):
                result.data[i][j] = sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
        return result
    
    def __imatmul__(self, other):
        """
        In-place multiplication of matrix by another matrix (matrix multiplication).
        Input: other (Matrix).
        Output: A new matrix after multiplication.
        """
        if self.cols != other.rows:
            self.__raise_dimensions_error(other, "matrix multiplication")
            
        result = Matrix(self.rows, other.cols)
        for i in range(self.rows):
            for j in range(other.cols):
                result.data[i][j] = sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
        self.data = result.data
        self.rows, self.cols = result.rows, result.cols
        return self

    def __invert__(self):
        """
        Returns the transpose of the matrix.
        Input: None.
        Output: A new matrix that is the transpose.
        """
        result = Matrix(self.cols, self.rows)
        for i in range(self.rows):
            for j in range(self.cols):
                result.data[j][i] = self.data[i][j]
        return result
    
    def LU_decomposition(self, epsilon=1e-8):
        """
        Performs LU decomposition of the matrix.
        Input: epsilon (float - tolerance for zero).
        Output: None (modifies the matrix in place).
        """
        self.num_switches = 0 # LU doesn't require row switches
        n = self.rows
        for i in range(n-1):
            if abs(self.data[i][i]) < epsilon:
                raise ValueError("Can't perform LU decomposition (division by 0).")
            for j in range(i+1, n):
                self.data[j][i] /= self.data[i][i] # divide column by pivot
                for k in range(i+1, n):
                    self.data[j][k] -= self.data[j][i] * self.data[i][k] # subtract the product of the pivot row and the column
    
    def LUP_decomposition(self, epsilon=1e-8):
        """
        Performs LUP decomposition of the matrix with pivoting.
        Input: epsilon (float - tolerance for zero).
        Output: None (modifies the matrix in place, creates permutation matrix).
        """
        self.num_switches = 0
        n = self.rows
        self.P = Matrix(rows=n, cols=n) # permutation matrix
        for i in range(n):
            self.P[i][i] = 1.
        
        for i in range(n-1):
            for j in range(i+1, n): # pick pivot
                if abs(self.data[j][i]) > abs(self.data[i][i]):
                    self.num_switches += 1
                    self.P.data[i], self.P.data[j] = self.P.data[j], self.P.data[i]
                    self.data[i], self.data[j] = self.data[j], self.data[i]
                    if abs(self.data[i][i]) < epsilon: # division by 0
                        continue
            for j in range(i+1, n): # perform the same as in LU
                self.data[j][i] /= self.data[i][i]
                for k in range(i+1, n):
                    self.data[j][k] -= self.data[j][i] * self.data[i][k]
    
    def forward_supstitution(self, b):
        """
        Solves a lower triangular system using forward substitution.
        Input: b (Matrix - right-hand side).
        Output: Updated right-hand side vector after forward substitution.
        """
        if self.cols != b.rows:
            self.__raise_dimensions_error(b, "forward substitution")
        
        if hasattr(self, 'P'):
            b = self.P @ b # apply permutation matrix

        for i in range(b.rows-1):
            for j in range(i+1, b.rows):
                # no need to divide by diagonal element because L has 1s on the diagonal
                b[j][0] -= self.data[j][i] * b[i][0] # solve equation
        return b
    
    def backward_supstitution(self, b, epsilon=1e-8):
        """
        Solves an upper triangular system using backward substitution.
        Input: b (Matrix - right-hand side), epsilon (float - tolerance for zero).
        Output: Updated right-hand side vector after backward substitution.
        """
        if self.cols != b.rows:
            self.__raise_dimensions_error(b, "backward substitution")
        
        for i in range(b.rows-1, -1, -1):
            if abs(self.data[i][i]) < epsilon:
                raise ValueError("Can't perform backward substitution (division by 0).")
            b[i][0] /= self.data[i][i] # divide by diagonal element because U doesn't have 1s on the diagonal like L
            for j in range(i):
                b[j][0] -= self.data[j][i] * b[i][0] # same as forward substitution
        return b
    
    def solve(self, b, epsilon=1e-8):
        """
        Solves the linear system Ax = b using LUP decomposition.
        Input: b (Matrix - right-hand side), epsilon (float - tolerance for zero).
        Output: Solution vector x (Matrix).
        """
        y = self.forward_supstitution(b)
        x = self.backward_supstitution(y, epsilon)
        return x
    
    def get_inverse(self, epsilon=1e-8):
        """
        Computes the inverse of the matrix.
        Input: epsilon (float - tolerance for zero).
        Output: The inverse of the matrix (Matrix).
        """
        if self.rows != self.cols:
            raise ValueError("Matrix is not square.")
        
        self.LUP_decomposition(epsilon)
        n = self.rows

        I = Matrix(n, n) # identity matrix
        for i in range(n):
            I[i][i] = 1.
            
        A_inv = Matrix(n, n)
        for i in range(n):
            col = Matrix(n, 1)
            for j in range(n):
                col[j][0] = I[j][i]
            solved_col = self.solve(col, epsilon)
            for j in range(n):
                A_inv[j][i] = solved_col[j][0]
        return A_inv
    
    def get_determinant(self):
        """
        Computes the determinant of the matrix using LUP decomposition.
        Input: None.
        Output: Determinant of the matrix (float).
        """
        self.LUP_decomposition()
        det = 1 if self.num_switches % 2 == 0 else -1
        for i in range(self.rows):
            det *= self[i][i]
        return det

    def __raise_dimensions_error(self, other, operation):
        """
        Raises an error if matrix dimensions do not match for a specific operation.
        Input: other (Matrix), operation (str - operation name).
        Output: None (raises an error).
        """
        raise ValueError(f"""Matrices dimensions do not allow {operation}.
Matrix 1 dimensions: {self.rows} x {self.cols}
Matrix 2 dimensions: {other.rows} x {other.cols}""")