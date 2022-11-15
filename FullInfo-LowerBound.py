import gurobipy as gp
from gurobipy import GRB

# Create a new model
m = gp.Model("bilinear")


n = 16
p = [0.0, 0.1, 0.19, 0.27, 0.315, 0.355, 0.395, 0.44, 0.485, 0.535, 0.595, 0.665, 0.74, 0.875, 1.195, 1000.0]
Q = [[0.0 for i in range(n)] for j in range(n)]
C = [[[0.0 for i in range(n)] for j in range(n)] for k in range(n)]
r = 0.72

for k in range(n):
    for i in range(k):
        for j in range(k + 1, n):
            C[k][i][j] = p[j] - p[i]

for i in range(n):
    for j in range(n):
        Q[i][j] = max(p[i], p[j])

# Create variables

s = [m.addVar(lb = 0.0, ub = 2.0, name = "s" + str(i)) for i in range(n)]
b = [m.addVar(lb = 0.0, ub = 2.0, name = "b" + str(i)) for i in range(n)]


def setObj():
    obj = gp.QuadExpr()
    for i in range(n):
        for j in range(n):
            if Q[i][j] != 0:
                obj += Q[i][j]*s[i]*b[j]
    m.setObjective(obj, GRB.MAXIMIZE)


setObj()

# Add linear constraint: \sum s = \sum b 

expr = gp.LinExpr()
for i in range(n):
    expr += s[i]

m.addLConstr(expr >= 1, "SumS1")
m.addLConstr(expr <= 1.001, "SumS2")


expr = gp.LinExpr()
for i in range(n):
    expr += b[i]

m.addLConstr(expr >= 1, "SumB1")
m.addLConstr(expr <= 1.001, "SumS1")


for k in range(n):
    expr = gp.QuadExpr()
    for i in range(n):
        for j in range(n):
            if C[k][i][j] != 0:
                if (i >=k or j <= k):
                    print("Error")
                    exit(0)
                expr += C[k][i][j] * s[i] * b[j]
    
    for i in range(n):
        expr += p[i] * s[i]
    
    m.addConstr(expr <= r, "Ratio" + str(k))

try:
    m.optimize()
except gp.GurobiError:
    print("Optimize failed due to non-convexity")

# Solve bilinear model
m.Params.NonConvex = 2
m.optimize()

m.printAttr('x')
