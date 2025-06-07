#迁移学习-路径最优问题。
import numpy as np

n_states = 9
actions = ['left', 'right', 'up', 'down']
n_actions = len(actions)

Q = np.zeros([n_states, n_actions])

alpha = 0.1
gamma = 0.9
epsilon = 0.9

action_to_index = {'left': 0, 'right': 1, 'up': 2, 'down': 3}

def choose_action(state):
    if np.random.uniform() < epsilon:
        action = np.argmax(Q[state, :])
    else:
        action = np.random.choice(n_actions)
    return action

def update_q_table(old_state, action, reward, new_state):
    predict = Q[old_state, action]
    target = reward + gamma * np.max(Q[new_state, :])
    Q[old_state, action] += alpha * (target - predict)

def get_reward(state):
    if state == 8:
        return 100
    else:
        return -1

# 主循环
for episode in range(500):
    state = 0
    while state != 8:
        action_idx = choose_action(state)
        action = actions[action_idx]

        if action == 'right' and state not in [2, 5, 8]:
            new_state = state + 1
        elif action == 'down' and state not in [6, 7, 8]:
            new_state = state + 3
        else:
            new_state = state

        reward = get_reward(new_state)
        update_q_table(state, action_idx, reward, new_state)
        state = new_state

print("训练完成后的Q表：")
print(Q)


