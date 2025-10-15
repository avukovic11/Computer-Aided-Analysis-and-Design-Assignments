from abc import ABC, abstractmethod
import math

from matrix import Matrix

class AbstractFunction(ABC):
    def __init__(self):
        self.num_goal_function_calls = 0
        self.num_gradient_calls = 0
        self.num_hessian_calls = 0
        self.num_jacobian_calls = 0

    @abstractmethod
    def __call__(self, x):
        pass

    @abstractmethod
    def gradient(self, x):
        pass

    @abstractmethod
    def hessian(self, x):
        pass

    def reset_counters(self):
        self.num_goal_function_calls = 0
        self.num_gradient_calls = 0
        self.num_hessian_calls = 0
        self.num_jacobian_calls = 0

    def f_lambda(self, x, grad, lambda_):
        return self(x + lambda_ * grad)

class Function1(AbstractFunction):
    def __call__(self, x):
        self.num_goal_function_calls += 1
        return 100 * (x[1] - x[0]**2)**2 + (1 - x[0])**2

    def gradient(self, x):
        self.num_gradient_calls += 1
        return Matrix(data=[[-400 * x[0] * (x[1] - x[0]**2) - 2 * (1 - x[0])], [200 * (x[1] - x[0]**2)]])

    def hessian(self, x):
        self.num_hessian_calls += 1
        return Matrix(data=[[1200 * x[0]**2 - 400 * x[1] + 2, -400 * x[0]], [-400 * x[0], 200]])
    
    def g(self, x):
        return Matrix(data=[[10 * (x[1] - x[0]**2)], [1 - x[0]]])
    
    def jacobian(self, x):
        self.num_jacobian_calls += 1
        return Matrix(data=[[-20 * x[0], 10], [-1, 0]])

class Function2(AbstractFunction):
    def __call__(self, x):
        self.num_goal_function_calls += 1
        return (x[0] - 4)**2 + 4 * (x[1] - 2)**2

    def gradient(self, x):
        self.num_gradient_calls += 1
        return Matrix(data=[[2 * (x[0] - 4)], [8 * (x[1] - 2)]])

    def hessian(self, x):
        self.num_hessian_calls += 1
        return Matrix(data=[[2, 0], [0, 8]])

class Function3(AbstractFunction):
    def __call__(self, x):
        self.num_goal_function_calls += 1
        return (x[0] - 2)**2 + (x[1] + 3)**2

    def gradient(self, x):
        self.num_gradient_calls += 1
        return Matrix(data=[[2 * (x[0] - 2)], [2 * (x[1] + 3)]])

    def hessian(self, x):
        self.num_hessian_calls += 1
        return Matrix(data=[[2, 0], [0, 2]])

class Function4(AbstractFunction):
    def __call__(self, x):
        self.num_goal_function_calls += 1
        return 0.25 * x[0]**4 - x[0]**2 + 2 * x[0] + (x[1] - 1)**2

    def gradient(self, x):
        self.num_gradient_calls += 1
        return Matrix(data=[[x[0]**3 - 2 * x[0] + 2], [2 * (x[1] - 1)]])

    def hessian(self, x):
        self.num_hessian_calls += 1
        return Matrix(data=[[3 * x[0]**2 - 2, 0], [0, 2]])
    
class Function_Task5(AbstractFunction):
    def __call__(self, x):
        self.num_goal_function_calls += 1
        return (x[0]**2 + x[1]**2 - 1)**2 + (x[1] - x[0]**2)**2
    
    def gradient(self, x):
        pass

    def hessian(self, x):
        pass

    def g(self, x):
        return Matrix(data=[[x[0]**2 + x[1]**2 - 1], [x[1] - x[0]**2]])
    
    def jacobian(self, x):
        self.num_jacobian_calls += 1
        return Matrix(data=[[2 * x[0], 2 * x[1]], [-2 * x[0], 1]])
    
class Function_Task6(AbstractFunction):
    def __init__(self, measurements):
        super().__init__()
        self.measurements = measurements

    def __call__(self, x):
        self.num_goal_function_calls += 1
        return sum([(x[0] * math.exp(x[1] * t) + x[2] - y)**2 for t, y in self.measurements])
    
    def gradient(self, x, t):
        pass

    def hessian(self, x, t):
        pass

    def g(self, x):
        residuals = []
        for t, y in self.measurements:
            residuals.append([x[0] * math.exp(x[1] * t) + x[2] - y])
        return Matrix(data=residuals)
    
    def jacobian(self, x):
        self.num_jacobian_calls += 1
        jacobian = []
        for t, y in self.measurements:
            grad_x1 = math.exp(x[1] * t)
            grad_x2 = x[0] * t * math.exp(x[1] * t)
            grad_x3 = 1
            jacobian.append([grad_x1, grad_x2, grad_x3])
        return Matrix(data=jacobian)