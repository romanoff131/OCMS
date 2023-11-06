import numpy as np
import matplotlib.pyplot as plt
import math

a = [0.3, 0.2, -0.1, 4.2, -2, 1.5, 0]
b = [0.1, 0.2, 0.3, 4, -2.2, 1.6, 0.1]

fig, (ax1, ax2) = plt.subplots(2, 1) # Создание первого подграфика
ax1.plot(a)
ax1.set(title='График a', xlabel='Индекс элемента', ylabel='Значение')

ax2.plot(b)
ax2.set(title='График b', xlabel='Индекс элемента', ylabel='Значение')

plt.show()

def Corr1(a, b):
    p = np.sum(a * b)
    return p

def Corr2(a, b):
    p = np.sum(a * b) / (np.sqrt(np.sum(a**2)) * np.sqrt(np.sum(b**2)))
    return p

ab = Corr1(a, b)
print(f"{ab:.0f}")