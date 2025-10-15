import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt

# Zadani podaci (t, y)
t = np.array([1, 2, 3, 5, 6, 7])
y = np.array([3, 4, 4, 5, 6, 8])

# Model funkcija: M(x, t) = x1 * exp(x2 * t) + x3
def model(x, t):
    return x[0] * np.exp(x[1] * t) + x[2]

# Rezidualna funkcija za optimizaciju
def residuals(x, t, y):
    return model(x, t) - y

# Početne vrijednosti parametara x1, x2, x3
x0 = [1, 1, 1]

# Gauss-Newton optimizacija koristeći least_squares
result = least_squares(residuals, x0, args=(t, y))
x_opt = result.x

# Ispis optimiziranih parametara
print(f"Optimizirani parametri: x1={x_opt[0]:.4f}, x2={x_opt[1]:.4f}, x3={x_opt[2]:.4f}")

# Crtanje rezultata
t_fine = np.linspace(min(t), max(t), 100)
y_model = model(x_opt, t_fine)

plt.scatter(t, y, color='red', label='Zadane točke')
plt.plot(t_fine, y_model, label='Prilagođeni model', color='blue')
plt.xlabel('t')
plt.ylabel('y')
plt.title('Optimizirani model u (t, y) ravnini')
plt.legend()
plt.grid()
plt.show()
