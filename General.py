import numpy as np
from scipy.special import softmax

N = 10
# Number of Samples

C = [[0 for i in range(N + 1)] for i in range(N + 1)]
xpoly = []
mxpoly = []
def Pre():
    for i in range(0, N + 1):
        C[i][0] = 1
        for j in range(1, i + 1):
            C[i][j] = C[i - 1][j - 1] + C[i - 1][j]

    xp = np.poly1d([1, 0])
    xpoly.append(np.poly1d([1]))
    for i in range(1, N + 1):
        xpoly.append(np.polymul(xp, xpoly[i - 1]))

    mxp = np.poly1d([-1, 1])
    mxpoly.append(np.poly1d([1]))
    for i in range(1, N + 1):
        mxpoly.append(np.polymul(mxp, mxpoly[i - 1]))
    # print(mxpoly[N])

def pdf(N, i):
    #Return the p.d.f. of the i-th order statistics
    res = np.polymul(xpoly[i - 1], mxpoly[N - i])
    res = np.polymul(res, np.poly1d([N * C[N - 1][i - 1]]))
    return res

eps = 1e-8

def mini(ALGx):
    f = ALGx
    mini = min(np.polyval(f, 0), np.polyval(f, 1))

    df = np.polyder(f)
    x = np.roots(df)
    for v in x:
        if (v.imag < eps):
            if(v.real < 0):
                continue
            if(v.real > 1):
                continue
            mini = min(mini, np.polyval(f, v.real))

    return mini

def Ratio(a):
#Solve the inner optimization problem 
#when the order statistics choose the $i$th order statistics w.p. a[i]
    f = np.poly1d([0])
    for i in range(N):
        f = np.polyadd(f, np.polymul(np.poly1d([a[i]]), pdf(N, i + 1)))

    If1 = np.polyint(np.polymul(f, np.poly1d([1, 0])))
    If1 = np.polysub(If1, np.poly1d(np.polyval(If1, 0)))

    ALGx = np.poly1d([-1, 1])
    ALGx = np.polyadd(ALGx, If1)
    # print(ALGx)

    return mini(ALGx)

Pre()

