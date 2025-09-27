import matplotlib.pyplot as plt 
import numpy as np
from scipy.integrate import quad

# Визначення функції та межі інтегрування
def f(x):
    return x ** 2

a = 0  # Нижня межа
b = 2  # Верхня межа

# Створення діапазону значень для x
x = np.linspace(0, 2, 400)
y = f(x)

# Створення графіка
fig, ax = plt.subplots()

# Малювання функції
ax.plot(x, y, 'r', linewidth=2)

# Заповнення області під кривою
ix = np.linspace(a, b)
iy = f(ix)
ax.fill_between(ix, iy, color='gray', alpha=0.3)

# Налаштування графіка
ax.set_xlim([x[0], x[-1]])
ax.set_ylim([0, max(y) + 0.1])
ax.set_xlabel('x')
ax.set_ylabel('f(x)')

# Додавання меж інтегрування та назви графіка
ax.axvline(x=a, color='gray', linestyle='--')
ax.axvline(x=b, color='gray', linestyle='--')
ax.set_title('Графік інтегрування f(x) = x^2 від ' + str(a) + ' до ' + str(b))
plt.grid()
plt.show()

# --- Обчислення інтегралу анадітично---
analytical = (b**3 - a**3) / 3

# --- Обчислення інтегралу методом Монте-Карло---
N = 100_000  # кількість випадкових точок
x_rand = np.random.uniform(a, b, N)
y_rand = f(x_rand)

monte_carlo = (b - a) * np.mean(y_rand)

# --- Обчислення інтегралу методом quad з SciPy---
quad_result, error = quad(f, a, b)

# --- Вивід результатів ---
print(f"Аналітичний інтеграл     = {analytical:.6f}")
print(f"Метод Монте-Карло (N={N}) = {monte_carlo:.6f}")
print(f"Quad з SciPy              = {quad_result:.6f}, похибка ~ {error:.2e}")

# --- Висновок ---
diff_mc = abs(monte_carlo - analytical)
diff_quad = abs(quad_result - analytical)
print(f"\nВідхилення Монте-Карло від аналітичного: {diff_mc:.6f}")
print(f"Відхилення quad від аналітичного:       {diff_quad:.6f}")