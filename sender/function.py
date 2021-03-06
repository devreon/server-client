import math
import numpy as np

def f(x, y, t):
    return (math.sin(x * x + y * y) /(x * x+0.1 + y * y+0.1)) +t


def calculate(X, Y, Z, t):
    for i in np.arange(len(X)):
        for j in np.arange(len(Y)):
            Z[i][j] = f(X[i], Y[j], t)
            round(Z[i][j], 8)


