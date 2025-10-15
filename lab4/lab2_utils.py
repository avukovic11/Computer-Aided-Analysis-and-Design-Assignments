from point import Point

def find_unimodal_interval(f, start_point, step=1, return_num_iterations=False):
    left = start_point - step
    right = start_point + step
    middle = start_point
    num_iterations = 0
    f_left = f(left)
    f_middle = f(middle)
    f_right = f(right)
    num_iterations += 3
    
    if f_middle < f_left and f_middle < f_right:
        if return_num_iterations:
            return left, right, num_iterations
        return left, right
    
    elif f_middle > f_left:
        while f_middle > f_left:
            right = middle
            middle = left
            left = middle - step
            f_middle = f_left
            f_left = f(left)
            num_iterations += 1
            step *= 2
        if return_num_iterations:
            return left, right, num_iterations
        return left, right    
    else:
        while f_middle > f_right:
            left = middle
            middle = right
            right = middle + step
            f_middle = f_right
            f_right = f(right)
            num_iterations += 1
            step *= 2
        if return_num_iterations:
            return left, right, num_iterations
        return left, right

# always returns float because it only works for single variable functions
def golden_section_search(f, start_point=None, a=None, b=None, step=1, e=1e-6, print_steps=False, return_num_iterations=False):
    k = (5**0.5 - 1) / 2
    if a is None and b is None:
        if start_point is None:
            raise ValueError("You must provide either start_point or a and b")
        if isinstance(start_point, Point):
            if start_point.dim > 1:
                raise ValueError("This function only works for single variable functions")
            start_point = start_point[0]
        if not return_num_iterations:
            a, b = find_unimodal_interval(f, start_point, step, return_num_iterations=return_num_iterations)
        else:
            a, b, num_iter = find_unimodal_interval(f, start_point, step, return_num_iterations=return_num_iterations)
            
    c = b - k * (b - a)
    d = a + k * (b - a)
    fc = f(c)
    fd = f(d)
    if return_num_iterations:
        num_iterations = num_iter + 2
    else:
        num_iterations = 2  
    cnt = 1
    while (b - a) >= e:
        if print_steps:
            print(f"STEP {cnt}:")
            print(f"a: {a}\nb: {b}\nc: {c}\nd: {d}\nf(a): {f(a)}\nf(b):{f(b)}\nf(c): {fc}\nf(d): {fd}")        
            print("-----------------------------------")
        cnt += 1
        if fc < fd:
            b = d
            d = c
            c = b - k * (b - a)
            fd = fc
            fc = f(c)
            num_iterations += 1
        else:
            a = c
            c = d
            d = a + k * (b - a)
            fc = fd
            fd = f(d)
            num_iterations += 1 

    if return_num_iterations:
        return (a+b)/2, num_iterations
    return (a+b)/2

def scale_dimensions(vector, n):
    if len(vector) > 1 and len(vector) != n:
        raise ValueError(f"The length of {vector} must be equal to the number of dimensions of x0 ({n})")
    if len(vector) == 1 and n > 1:
        vector = vector * n
    return vector

# returns float if x0 is a single variable, otherwise returns list
def coordinate_search(f, x0, e=[1e-6], max_iter=1000, return_num_iterations=False):
    x = x0
    n = x.dim
    e = scale_dimensions(e, n)
    num_iterations = 0
    
    for i in range(max_iter):
        x_prev = x.copy()
        
        for j in range(n):
            def line_goal_function(lambda_):
                x_temp = x.copy()
                x_temp[j] += lambda_ # * 1 because we are working with perpendicular lines
                return f(x_temp)
            
            if not return_num_iterations:
                lambda_opt = golden_section_search(line_goal_function, start_point=x_prev[j], return_num_iterations=return_num_iterations)
            else:
                lambda_opt, num_iter = golden_section_search(line_goal_function, start_point=x_prev[j], return_num_iterations=return_num_iterations)
                num_iterations += num_iter
            x[j] += lambda_opt

        if all(abs(x[k] - x_prev[k]) <= e[k] for k in range(n)):
            break
    
    if return_num_iterations:
        return x, num_iterations
    return x

def explore(f, xp, delta_x, return_num_iterations=False):
    num_iterations = 0
    x = xp.copy()
    for i in range(x.dim):
        P = f(x)
        x[i] += delta_x[i]
        N = f(x)
        num_iterations += 2
        if N > P:
            x[i] -= 2 * delta_x[i]
            N = f(x)
            num_iterations += 1
            if N > P:
                x[i] += delta_x[i]

    if not return_num_iterations:
        return x
    return x, num_iterations

def hooke_jeeves(f, x0, e=[1e-6], delta_x=[0.5], max_iter=1000, return_num_iterations=False, print_steps=False):
    num_iterations = 0
    x = x0
    xp = x.copy()
    xb = x.copy()
    n = x.dim
    e = scale_dimensions(e, n)
    delta_x = scale_dimensions(delta_x, n)

    for i in range(max_iter):
        if not return_num_iterations:
            xn = explore(f, xp, delta_x, return_num_iterations=return_num_iterations)
        else:
            xn, num_iter = explore(f, xp, delta_x, return_num_iterations=return_num_iterations)
            num_iterations += num_iter
        if print_steps:
            print(f"STEP {i+1}:")
            print(f"xb: {xb}\nf(xb): {f(xb)}")
            print(f"xp: {xp}\nf(xp): {f(xp)}")
            print(f"xn: {xn}\nf(xn): {f(xn)}")
            print("-----------------------------------")
        if f(xn) < f(xb):
            num_iterations += 2
            xp = Point([2 * xn[i] - xb[i] for i in range(xn.dim)])
            xb = xn.copy()
        else:
            delta_x = [delta_x[i] / 2 for i in range(n)]
            xp = xb.copy()

        if all(delta_x[i] <= e[i] for i in range(n)):
            break

    if return_num_iterations:
        return xb, num_iterations
    return xb

def generate_initial_simplex(x0, step):
    simplex = [x0]
    for i in range(x0.dim):
        new_point = x0.copy()
        new_point[i] += step
        simplex.append(new_point)
    return simplex

def nelder_mead(f, x0, step=1, alpha=1, beta=0.5, gamma=2, sigma=0.5, e=1e-6, max_iter=1000, return_num_iterations=False, print_steps=False):
    num_iterations = 0
    x = generate_initial_simplex(x0, step)

    for i in range(max_iter):
        x = sorted(x, key=lambda p: f(p))  # sort points by function value
        num_iterations += len(x)
        l = 0  # best
        h = -1  # worst
        xc = Point([(sum(p[j] for p in x) - x[h][j]) / (len(x) - 1) for j in range(x[h].dim)]) # centroid
        if print_steps:
            print(f"STEP {i+1}:")
            print(f"Centroid: {xc}")
            print("f(Optimum): ", f(x[l]))
            print("-----------------------------------")
        xr = (1 + alpha) * xc - alpha * x[h] # reflection
        if f(xr) < f(x[l]):
            num_iterations += 2
            xe = (1 - gamma) * xc + gamma * xr # expansion
            if f(xe) < f(x[l]):
                num_iterations += 2
                x[h] = xe
            else:
                x[h] = xr
        elif f(xr) > f(x[-2]):
            num_iterations += 2
            if f(xr) < f(x[h]):
                num_iterations += 2
                x[h] = xr
            xk = (1 - beta) * xc + beta * x[h] # contraction
            if f(xk) < f(x[h]):
                num_iterations += 2
                x[h] = xk
            else:
                x = [sigma * (p + x[l]) for p in x] # move towards x[l]
        else:
            x[h] = xr

        # i don't know which condition to use for stopping the algorithm
        f_values = [f(p) for p in x]
        mean_f = sum(f_values) / len(f_values)
        variance_f = sum((fv - mean_f) ** 2 for fv in f_values) / len(f_values)
        std_f = variance_f ** 0.5
        if std_f < e:
            break

    if return_num_iterations:
        return x[l], num_iterations
    return x[l]