import numpy as np
import matplotlib.pyplot as plt
from grid_world import standard_grid, ACTION_SPACE
import utils


class SARSA:
    def __init__(self, grid, gamma=0.9, alpha=0.1):
        self.grid = grid
        self.gamma = gamma
        self.alpha = alpha
        self.q = {}
        self.update_counts = {}
        self.initialize_q()

    def initialize_q(self):
        states = self.grid.all_states()
        for s in states:
            self.q[s] = {}
            for a in ACTION_SPACE:
                self.q[s][a] = 0

    def epsilon_greedy(self, s, eps=0.1):
        if np.random.random() < eps:
            return np.random.choice(ACTION_SPACE)
        else:
            return utils.max_dict(self.q[s])[0]

    def slippery(self, s):
        if np.random.random() < 0.5:
            return utils.max_dict(self.q[s])[0]
        else:
            return np.random.choice(list(self.q[s].keys()))

    def second_best(self, s, a):
        action_space = []
        for item in s.keys():
            if item != a:
                action_space.append(item)
            else:
                continue
        new_action = np.random.choice(action_space)
        return new_action, s[new_action]

    def run(self, episodes=10000, max_steps=50, epsilon=0.1):
        reward_per_episode = []
        for it in range(episodes):
            if it % 2000 == 0:
                print("it:", it)
            s = self.grid.reset()
            a = self.epsilon_greedy(s, eps=epsilon)
            self.grid.policeman.reset_police()
            episode_reward = 0
            step = 0
            while not self.grid.game_over() and step < max_steps:
                step += 1
                self.grid.policeman.move()
                r = self.grid.move(a)
                if self.grid.current_state() == self.grid.policeman.get_pos():
                    self.grid.undo_move(a)
                    new_action, second_best_q = self.second_best(self.q[s], a)
                    r = self.grid.move(new_action)
                    s2 = self.grid.current_state()
                    episode_reward += r
                    a2 = self.epsilon_greedy(s2, eps=epsilon)
                    if s2 in self.grid.slippery:
                        a2 = self.slippery(s2)
                    self.q[s][new_action] = self.q[s][new_action] + self.alpha * (r + self.gamma * self.q[s2][a2] - self.q[s][new_action])
                    self.update_counts[s] = self.update_counts.get(s, 0) + 1
                    s = s2
                    a = a2
                else:
                    s2 = self.grid.current_state()
                    episode_reward += r
                    a2 = self.epsilon_greedy(s2, eps=epsilon)
                    if s2 in self.grid.slippery:
                        a2 = self.slippery(s2)
                    self.q[s][a] = self.q[s][a] + self.alpha * (r + self.gamma * self.q[s2][a2] - self.q[s][a])
                    self.update_counts[s] = self.update_counts.get(s, 0) + 1
                    s = s2
                    a = a2
            reward_per_episode.append(episode_reward)
        return reward_per_episode

    def extract_policy_and_values(self):
        policy = {}
        V = {}
        for s in self.grid.actions.keys():
            a, max_q = utils.max_dict(self.q[s])
            policy[s] = a
            V[s] = max_q
        return policy, V


def main(game_info):
    grid = standard_grid(n=game_info['grid_size'], rewards=game_info['rewards'], slippery=game_info['slippery'])
    sarsa = SARSA(grid, gamma=game_info['gamma'], alpha=game_info['alpha'])
    rewards = sarsa.run(episodes=game_info['training_phase'], max_steps=game_info['max_steps_per_episode'], epsilon=game_info['epsilon'])
    plt.plot(rewards)
    plt.title("Reward per Episode")
    plt.show()
    policy, V = sarsa.extract_policy_and_values()
    print("Values:")
    utils.print_values(V, grid)
    print("Policy:")
    utils.print_policy(policy, grid)
    game_info['policy'] = policy
    return game_info
