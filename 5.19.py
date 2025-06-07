#强化学习-使用Q-learning 求解 GridWorld（网格世界）问题。
import numpy as np
import random

GRID_SIZE = 4
NUM_STATES = GRID_SIZE * GRID_SIZE
NUM_ACTIONS = 4

ACTIONS = {
    0: (-1, 0),
    1: (1, 0),
    2: (0, -1),
    3: (0, 1)
}

EPISODES = 500
ALPHA = 0.1
GAMMA = 0.9
EPSILON = 0.1

Q = np.zeros((GRID_SIZE, GRID_SIZE, NUM_ACTIONS))

def get_reward(state):
    if state == (3, 3):
        return 10
    else:
        return -1

def is_terminal(state):
    return state == (3, 3)

def choose_action(state, q_values, epsilon=EPSILON):
    if random.uniform(0, 1) < epsilon:
        return random.randint(0, NUM_ACTIONS - 1)
    else:
        return np.argmax(q_values[state])

def next_state(current_state, action):
    x, y = current_state
    dx, dy = ACTIONS[action]
    new_x = max(0, min(GRID_SIZE - 1, x + dx))
    new_y = max(0, min(GRID_SIZE - 1, y + dy))
    return (new_x, new_y)

for episode in range(EPISODES):
    state = (0, 0)
    while not is_terminal(state):
        action = choose_action(state, Q)
        next_st = next_state(state, action)
        reward = get_reward(next_st)

        Q[state][action] += ALPHA * (
            reward + GAMMA * np.max(Q[next_st]) - Q[state][action]
        )
        state = next_st

print("Q-table after training:")
print(Q)

print("\nLearned Policy:")
policy = np.full((GRID_SIZE, GRID_SIZE), ' ')
policy[3, 3] = 'G'
state = (0, 0)
step = 0
while not is_terminal(state) and step < 20:
    best_action = np.argmax(Q[state])
    policy[state] = ['↑', '↓', '←', '→'][best_action]
    state = next_state(state, best_action)
    step += 1

for row in policy:
    print(' '.join(row))
