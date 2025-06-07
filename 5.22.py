#智能仓储机器人路径优化系统
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from collections import defaultdict

X_train = np.array([
    [1, 2], [2, 3], [3, 4], [5, 6], [7, 8],
    [10, 10], [9, 9], [8, 8], [7, 7], [6, 6]
])
y_train = np.array([0, 0, 0, 1, 1, 1, 1, 1, 1, 1])  # 0:正常，1:异常

clf = RandomForestClassifier()
clf.fit(X_train, y_train)

plt.figure(figsize=(8, 6))
for label in np.unique(y_train):
    plt.scatter(X_train[y_train == label, 0], X_train[y_train == label, 1], label=f'Label {label}')
plt.title("Supervised Learning: Anomaly Detection Training Data")
plt.legend()
plt.grid(True)
plt.show()

task_points = np.array([
    [1, 2], [2, 3], [3, 4],
    [6, 6], [7, 7], [8, 8],
    [1, 9], [2, 8], [3, 7], [4, 6]
])

kmeans = KMeans(n_clusters=3)
kmeans.fit(task_points)
labels = kmeans.labels_

plt.figure(figsize=(8, 6))
for i in range(3):
    plt.scatter(task_points[labels == i, 0], task_points[labels == i, 1], label=f'Cluster {i}')
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=200, c='black', marker='X', label='Centroids')
plt.title("Unsupervised Learning: Task Points Clustering")
plt.legend()
plt.grid(True)
plt.show()

grid_size = 10
env = np.zeros((grid_size, grid_size))

for x in range(grid_size):
    for y in range(grid_size):
        if clf.predict([[x, y]])[0] == 1:
            env[x][y] = -1  # -1表示障碍

start = (0, 0)
end = (9, 9)
env[start] = 0
env[end] = 0

actions = {
    0: (-1, 0),  # 上
    1: (1, 0),   # 下
    2: (0, -1),  # 左
    3: (0, 1)    # 右
}

q_table = defaultdict(lambda: np.zeros(4))
alpha = 0.1     # 学习率
gamma = 0.9     # 折扣因子
epsilon = 0.1   # 探索率
episodes = 1000

for episode in range(episodes):
    state = start
    done = False
    while not done:
        if np.random.uniform() < epsilon:
            action = np.random.choice(4)
        else:
            action = np.argmax(q_table[state])

        next_state = tuple(np.array(state) + actions[action])

        if next_state[0] < 0 or next_state[0] >= grid_size or next_state[1] < 0 or next_state[1] >= grid_size:
            reward = -10
            done = False
        elif env[next_state] == -1:
            reward = -10
            done = False
        elif next_state == end:
            reward = 100
            done = True
        else:
            reward = -1
            done = False

        q_table[state][action] += alpha * (
            reward + gamma * np.max(q_table[next_state]) - q_table[state][action]
        )

        state = next_state

path = []
state = start
path.append(state)
while state != end:
    action = np.argmax(q_table[state])
    state = tuple(np.array(state) + actions[action])
    path.append(state)

path = np.array(path)
plt.figure(figsize=(8, 8))
plt.imshow(env, cmap='gray')
plt.plot(path[:, 1], path[:, 0], 'r.-', markersize=10)
plt.plot(start[1], start[0], 'go', label='Start')
plt.plot(end[1], end[0], 'bo', label='End')
plt.title("Reinforcement Learning: Robot Path Planning")
plt.legend()
plt.grid(True)
plt.xticks(range(grid_size))
plt.yticks(range(grid_size))
plt.show()

print("强化学习路径规划完成，路径如下图所示")
