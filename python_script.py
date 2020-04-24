# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np
import math
import mosek
import cvxpy as cp
import matplotlib.pyplot as plt
import time
import sys

names = locals()


# %%
#parameter

K=int(sys.argv[1])
M=int(sys.argv[2])

n_anchor = int(sys.argv[3])
n_sensor = int(sys.argv[4])
# K = 15
# M = 100
# n_anchor = 25
# n_sensor = 25


# %%
print('K: '+str(K))
print('M: '+str(M))
print('n_anchor: '+str(n_anchor))
print('n_sensor: '+str(n_sensor))


# %%
old_data = True
if old_data:
    anchors = pd.read_excel('old_data/a0.xls', usecols = range(26), header=0, nrows=n_anchor) 
    sensors = pd.read_excel('old_data/y0.xls', usecols = range(26), header=0, nrows=n_sensor)
    dist = pd.read_excel('old_data/dist0.xls', usecols = range(n_sensor), header=0, nrows=n_anchor)
    sensor = sensors.values
    anchor = anchors.values
    distance = dist.values
else:
    anchors = pd.read_excel('a0.xls', usecols = range(26), header=None, nrows=n_anchor) 
    sensors = pd.read_excel('y0.xls', usecols = range(26), header=None, nrows=n_sensor)
    dist = pd.read_excel('dist0.xls', usecols = range(n_sensor), header=None, nrows=n_anchor)
    sensor = sensors.values
    anchor = anchors.values
    distance = dist.values



# %%
J = len(sensor[:,1])
I = len(anchor[:,1])

# %% [markdown]
# add variable $\hat{y_{j}}$

# %%
for j in range(J):
    exec('hat_y_{} = cp.Variable(2)'.format(j))
    

# %% [markdown]
# add variable $\lambda_{ij}$

# %%
for i in range(I):
    for j in range(J):
        exec('lam_{}_{} = cp.Variable(2)'.format(i, j))
        
# add variable v
v = cp.Variable((I,J))


# %%
x = cp.Variable(I, boolean=True)
mu = cp.Variable((I,J))
T = cp.Variable((I,J))


# %%
constraints = []

constraints.append(cp.sum(x) == K)

for i in range(I):
    for j in range(J):
        constraints.append(cp.norm(names.get('lam_{}_{}'.format(i,j))) <= mu[i][j])
        
constraints.append(v >= 0)

for i in range(I):
    for j in range(J):
        constraints.append(1 - distance[i][j]*mu[i][j] - v[i][j] == 0)

for j in range(J):
    sum_i_lam_ij = 0
    for i in range(I):
        sum_i_lam_ij += names.get('lam_{}_{}'.format(i,j))
    constraints.append(sum_i_lam_ij == 0)
    

for i in range(I):
    for j in range(J):
        constraints.append(cp.norm(anchor[i,:] - names.get('hat_y_{}'.format(j))) <=            distance[i][j]*(1 + T[i][j]) + M*(1-x[i]))


rhs = 0
for i in range(I):
    for j in range(J):
        rhs -= anchor[i,:]*names.get('lam_{}_{}'.format(i,j)) + distance[i][j]*mu[i][j]
constraints.append(cp.sum(T) == rhs)
        
for i in range(I):
    for j in range(J):
        constraints.append(mu[i][j] <= 100000*x[i])
        
constraints.append(T >= 0)
        
        
obj_exp = 0
for j in range(J):
    obj_exp += cp.norm(names.get('hat_y_' + str(j)) - sensor[j,:])
    


# %%
t_start = round(time.time())
obj = cp.Minimize(obj_exp)
prob = cp.Problem(obj, constraints)
prob.solve(solver=cp.MOSEK, verbose=True)
t_end = round(time.time())



if prob.status not in ["infeasible", "unbounded"]:
    # Otherwise, problem.value is inf or -inf, respectively.
    print("Optimal value: %s" % prob.value)

    violation = max([np.max(x.violation()) for x in constraints])
    print('max constraint violation: '+str(max([np.max(x.violation()) for x in constraints])))



    np.savetxt(X=x.value, fname='result/t{} x result_K{} M{} n_anchor{} n_sensor{} duration{} violation{}.txt'.format(t_start, K, M, n_anchor, n_sensor, t_end - t_start, violation))

    hat_y_value = np.zeros((J,2))
    for j in range(J):
        hat_y_value[j,:] = names.get('hat_y_{}'.format(j)).value

    np.savetxt(X=hat_y_value, fname='result/t{} hat_y result_K{} M{} n_anchor{} n_sensor{} duration{} violation{}.txt'.format(t_start, K, M, n_anchor, n_sensor, t_end - t_start, violation))




    plt.figure(figsize=(10,10))
    plt.scatter(x=anchor[:,0], y=anchor[:,1])
    plt.scatter(x=sensor[:,0], y=sensor[:,1],c='k',s=150)

    for i in range(I):
        for j in range(J):
            plt.scatter(x=names.get('hat_y_{}'.format(j)).value[0],
                        y=names.get('hat_y_{}'.format(j)).value[1],c='r')
    plt.savefig('result/t{} figure result_K{} M{} n_anchor{} n_sensor{} duration{} violation{}.pdf'.format(t_start, K, M, n_anchor, n_sensor, t_end - t_start, violation))



else:
    print("Problem status:"+prob.status)
    

 


# %%
# assert np.sum(x.value) == K

# for i in range(I):
#     for j in range(J):
#         assert np.linalg.norm(names.get('lam_{}_{}'.format(i,j)).value) - mu.value[i][j] <= 1e-6
        
        
# assert (v.value >= 0).all

# for i in range(I):
#     for j in range(J):
#         assert abs(1 - distance[i][j]*mu.value[i][j] - v.value[i][j]) < 10e-6
        
# for j in range(J):
#     sum_i_lam_ij_value = 0
#     for i in range(I):
#         sum_i_lam_ij_value += names.get('lam_{}_{}'.format(i,j)).value
#     assert (sum_i_lam_ij_value == 0).all
    
# for i in range(I):
#     for j in range(J):
#         assert np.linalg.norm(anchor[i,:] - names.get('hat_y_{}'.format(j)).value) <=\
#             distance[i][j]*(1+T.value[i][j]) + M*(1-x.value[i]) + 1e-6

        
# for i in range(I):
#     for j in range(J):
#         assert mu.value[i][j] <= 100000*x.value[i] + 1e-7
        

# rhs_value = 0
# for i in range(I):
#     for j in range(J):
#         rhs_value -= anchor[i,:].dot(names.get('lam_{}_{}'.format(i,j)).value) + distance[i][j]*mu.value[i][j]

# assert abs(np.sum(T.value) - rhs_value) < 1e-6
        

