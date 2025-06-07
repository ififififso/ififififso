#强化学习-网格世界，使用值迭代（Value Iteration）来求解最优策略。
import numpy as np

grid_size = 4
num_states = grid_size * grid_size
num_actions = 4
actions = {'UP': 0, 'DOWN': 1, 'LEFT': 2, 'RIGHT': 3}
gamma = 1.0
theta = 1e-8

def next_state(s, a):
    row, col = divmod(s, grid_size)
    if a == actions['UP']:
        row = max(row - 1, 0)
    elif a == actions['DOWN']:
        row = min(row + 1, grid_size - 1)
    elif a == actions['LEFT']:
        col = max(col - 1, 0)
    elif a == actions['RIGHT']:
        col = min(col + 1, grid_size - 1)
    return row * grid_size + col

def is_terminal(s):
    return s == 0 or s == (grid_size * grid_size - 1)

V = np.zeros(num_states)

while True:
    delta = 0
    for s in range(num_states):
        if is_terminal(s):
            continue
        v = V[s]
        max_q = -np.inf
        for a in range(num_actions):
            s_prime = next_state(s, a)
            reward = 0 if is_terminal(s_prime) else -1
            q = reward + gamma * V[s_prime]
            max_q = max(max_q, q)
        V[s] = max_q
        delta = max(delta, abs(v - V[s]))
    if delta < theta:
        break

policy = np.zeros((num_states), dtype=int)
for s in range(num_states):
    if is_terminal(s):
        policy[s] = -1
        continue
    best_action = None
    max_q = -np.inf
    for a in range(num_actions):
        s_prime = next_state(s, a)
        reward = 0 if is_terminal(s_prime) else -1
        q = reward + gamma * V[s_prime]
        if q > max_q:
            max_q = q
            best_action = a
    policy[s] = best_action

def print_policy(policy):
    action_names = ['↑', '↓', '←', '→']
    for i in range(grid_size):
        for j in range(grid_size):
            s = i * grid_size + j
            if is_terminal(s):
                print(" T ", end="")
            else:
                print(f"{action_names[policy[s]]} ", end="")
        print()

print("Optimal Value Function:")
print(V.reshape(grid_size, grid_size))

print("\nOptimal Policy:")
print_policy(policy)
