import gurobipy as gp
from gurobipy import GRB

# Create a new model
m = gp.Model("bilinear")


def softtime(model, where):
    if where == GRB.Callback.MIP:
        # runtime = model.cbGet(GRB.Callback.RUNTIME)
        objbst = model.cbGet(GRB.Callback.MIP_OBJBST)
        objbnd = model.cbGet(GRB.Callback.MIP_OBJBND)
        gap = abs((objbst - objbnd) / objbst)

        if objbst < 0 or objbnd >= 0.00001:
            model.terminate()


r = 0.65

from math import *

n = 50
block = 1.0 / (n**2)
p = [float(i / 20.0) for i in range(n)]
w = [0 for i in range(n)]
for i in range(n - 10):
	p[i] = float(i / 10.0) 

for i in range(10):
	w[i] += sqrt(i) * 5 + 10.3

for i in range(10, 20):
	w[i] += 22

for i in range(20, 30):
	w[i] += 9.5

for i in range(20, n - 10):
	w[i] += 3

for i in range(n - 10, n):
	p[i] = float(((i - (n - 10)) / 5.0)) + (n - 10) / 10.0 + 0.2
	w[i] = (n - i) 

w[0] = w[n - 1] = 0

p[n - 1] = 1000.0

s = 0
for x in w:
    s += x

for i in range(n):
	w[i] = w[i] / s

s = 0
for x in w:
    s += x
if abs(s - 1) >= 0.0001:
    exit()
print(p)
print(w)
Q = [[0.0 for i in range(n)] for j in range(n)]
C = [[[0.0 for i in range(n)] for j in range(n)] for k in range(n)]

for k in range(n):
    for i in range(k):
        for j in range(k + 1, n):
            C[k][i][j] = p[j] - p[i]

for i in range(n):
    for j in range(n):
        Q[i][j] = max(p[i], p[j])

# Create variables

s = [m.addVar(lb = 0.0, ub = 2.0, name = "s" + str(i)) for i in range(n)]
b = [m.addVar(lb = 0.0, ub = 10.0, name = "b" + str(i)) for i in range(n)]

def setObj():
	expr = gp.QuadExpr()

	for k in range(n):
		expr += s[k] * p[k]

	for k in range(n):
		for i in range(n):
			for j in range(n):
				if C[k][i][j] != 0:
					if (i >=k or j <= k):
						print("Error")
						exit(0)
					expr += C[k][i][j] * s[i] * b[j] * w[k]
			
	for i in range(n):
		for j in range(n):
			expr -= r * s[i] * b[j] * Q[i][j]
	m.setObjective(expr, GRB.MINIMIZE)


setObj()


expr = gp.LinExpr()
for i in range(n):
    expr += s[i]

m.addLConstr(expr >= 1, "SumS1")
m.addLConstr(expr <= 1.001, "SumS2")


expr = gp.LinExpr()
for i in range(n - 1):
    expr += b[i]

m.addLConstr(expr <= 1, "SumB1")

expr = gp.LinExpr()
for i in range(n):
	expr += b[i]
m.addLConstr(expr >= 1, "SumB2")


expr = gp.LinExpr()
for i in range(n):
    expr += s[i] * p[i]
m.addLConstr(expr == 1, "Normalization")


try:
    m.optimize()
except gp.GurobiError:
    print("Optimize failed due to non-convexity")

# Solve bilinear model
m.Params.NonConvex = 2
m.optimize(softtime)

m.printAttr('x')
