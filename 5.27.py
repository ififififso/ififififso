#潮流计算-三节点
import numpy as np
from numpy.linalg import inv, norm

# 导纳矩阵 (3x3)
Ybus = np.array([
    [10 - 20j, -10 + 10j, -0 + 10j],
    [-10 + 10j, 10 - 20j, -0 + 10j],
    [-0 + 10j, -0 + 10j, 0 - 20j]
])

# 初始电压角度与幅值（弧度制）
V = np.array([1.0, 1.0, 1.0])          # 电压幅值
theta = np.array([0.0, 0.0, 0.0])      # 电压角度

# PQ/PV节点的索引（从0开始计数）
PQ_index = [1]     # 只有节点2是PQ节点
PV_index = [2]     # 节点3是PV节点

# 给定的注入功率（P+jQ）
P_specified = np.array([0, -0.6, 0.5])  # MW
Q_specified = np.array([0, -0.25, 0])   # MVar（仅PQ节点有效）

max_iter = 10
tolerance = 1e-6

for iter in range(max_iter):
    P_calculated = np.zeros(3)
    Q_calculated = np.zeros(3)

    for i in range(3):
        sum_p = 0
        sum_q = 0
        for k in range(3):
            sum_p += V[i] * V[k] * np.cos(theta[i] - theta[k]) * Ybus[i, k].real \
                     - V[i] * V[k] * np.sin(theta[i] - theta[k]) * Ybus[i, k].imag
            sum_q += -V[i] * V[k] * np.cos(theta[i] - theta[k]) * Ybus[i, k].imag \
                      - V[i] * V[k] * np.sin(theta[i] - theta[k]) * Ybus[i, k].real
        P_calculated[i] = sum_p
        Q_calculated[i] = sum_q

    # 不平衡量（Mismatch）
    delta_P = P_specified - P_calculated
    delta_Q = Q_specified - Q_calculated

    # 检查收敛性
    mismatch = np.concatenate((delta_P[PQ_index + PV_index], delta_Q[PQ_index]))
    if norm(mismatch) < tolerance:
        print(f"✅ 在第{iter+1}次迭代后收敛")
        break

    # 构造雅可比矩阵 J
    n = len(V)
    J = np.zeros((2*n - 1, 2*n - 1))  # 因为平衡节点不参与方程

    row = 0
    for i in PQ_index + PV_index:
        col = 0
        for j in PQ_index + PV_index:
            if i != j:
                # dPi/dθj
                J[row, col] = V[i]*V[j]*(Ybus[i,j].real*np.sin(theta[i]-theta[j])
                                         - Ybus[i,j].imag*np.cos(theta[i]-theta[j]))
                # dPi/dVj
                if j in PQ_index:
                    J[row, col + len(PQ_index + PV_index)] = V[i]*(Ybus[i,j].real*np.cos(theta[i]-theta[j])
                                                                    + Ybus[i,j].imag*np.sin(theta[i]-theta[j]))
            else:
                # dPi/dθi
                sum_term = 0
                for k in range(n):
                    if k != i:
                        sum_term += V[i]*V[k]*(Ybus[i,k].real*np.sin(theta[i]-theta[k])
                                               - Ybus[i,k].imag*np.cos(theta[i]-theta[k]))
                J[row, col] = -V[i]**2 * Ybus[i,i].imag - sum_term
                # dPi/dVi
                if i in PQ_index:
                    J[row, col + len(PQ_index + PV_index)] = (P_calculated[i]/V[i]) + V[i]*Ybus[i,i].real
            col += 1
        row += 1

    for i in PQ_index:
        col = 0
        for j in PQ_index + PV_index:
            if i != j:
                # dQi/dθj
                J[row, col] = -V[i]*V[j]*(Ybus[i,j].real*np.cos(theta[i]-theta[j])
                                          + Ybus[i,j].imag*np.sin(theta[i]-theta[j]))
                # dQi/dVj
                J[row, col + len(PQ_index + PV_index)] = V[i]*(Ybus[i,j].real*np.sin(theta[i]-theta[j])
                                                                - Ybus[i,j].imag*np.cos(theta[i]-theta[j]))
            else:
                # dQi/dθi
                sum_term = 0
                for k in range(n):
                    if k != i:
                        sum_term += V[i]*V[k]*(Ybus[i,k].real*np.cos(theta[i]-theta[k])
                                               + Ybus[i,k].imag*np.sin(theta[i]-theta[k]))
                J[row, col] = -V[i]**2 * Ybus[i,i].real - sum_term
                # dQi/dVi
                J[row, col + len(PQ_index + PV_index)] = (Q_calculated[i]/V[i]) - V[i]*Ybus[i,i].imag
            col += 1
        row += 1

    # 解线性方程组 Δx = J⁻¹ * mismatch
    dx = np.linalg.solve(J, mismatch)

    # 更新 θ 和 V
    x_update = 0
    for i in PQ_index + PV_index:
        theta[i] += dx[x_update]
        x_update += 1
    for i in PQ_index:
        V[i] += dx[x_update]
        x_update += 1

print("\n📊 最终电压幅值（标幺值）:")
print(V)
print("\n📊 最终电压角度（弧度）:")
print(theta)
print("\n📊 计算得到的注入有功功率（标幺值）:")
print(P_calculated)
print("\n📊 计算得到的注入无功功率（标幺值）:")
print(Q_calculated)