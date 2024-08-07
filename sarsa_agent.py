import numpy as np
import matplotlib.pyplot as plt
from grid_world import standard_grid
from constants import ACTION_SPACE
import utils


class SARSA:
    def __init__(self, grid, gamma=0.9, alpha=0.1):
        """
        Initializes the SARSA agent.

        Args:
            grid (Grid): The grid environment.
            gamma (float, optional): Discount factor. Default is 0.9.
            alpha (float, optional): Learning rate. Default is 0.1.
        """
        self.grid = grid
        self.gamma = gamma
        self.alpha = alpha
        self.q = {}
        self.update_counts = {}
        self.initialize_q()
        self.policy = {}

    def initialize_q(self):
        """
        Initializes the Q-values for all state-action pairs to zero.
        """
        states = self.grid.all_states()
        for s in states:
            self.q[s] = {}
            for a in ACTION_SPACE:
                self.q[s][a] = 0

    def epsilon_greedy(self, s, eps=0.1):
        """
        Chooses an action using the epsilon-greedy policy.

        Args:
            s (tuple): The current state.
            eps (float, optional): The probability of choosing a random action. Default is 0.1.

        Returns:
            str: The chosen action.
        """
        if s in list(self.grid.rewards.keys()):
            print("visited a final state")
            return np.random.choice(ACTION_SPACE)
        if np.random.random() < eps:
            return np.random.choice(list(self.grid.actions[s]))
        else:
            return utils.max_dict(self.q[s])[0]

    def train(self, episodes=10000, max_steps=50, epsilon=0.1):
        """
        Trains the SARSA agent.

        Args:
            episodes (int, optional): Number of episodes to train. Default is 10000.
            max_steps (int, optional): Maximum steps per episode. Default is 50.
            epsilon (float, optional): The probability of choosing a random action. Default is 0.1.

        Returns:
            list: Reward per episode.
            dict: The Q-values.
        """
        reward_per_episode = []
        for it in range(episodes):
            if it % 2000 == 0:
                print("it:", it)
            s = self.grid.reset()
            self.grid.policeman.reset_police()
            a = self.epsilon_greedy(s, eps=epsilon)
            episode_reward = 0
            step = 0
            while not self.grid.game_over() and step < max_steps:
                self.grid.policeman.move()
                step += 1
                r = self.grid.move(a, self.q)
                s2 = self.grid.current_state()
                episode_reward += r
                a2 = self.epsilon_greedy(s2, eps=epsilon)
                self.q[s][a] = self.q[s][a] + self.alpha * (r + self.gamma * self.q[s2][a2] - self.q[s][a])
                self.update_counts[s] = self.update_counts.get(s, 0) + 1
                s = s2
                a = a2
            reward_per_episode.append(episode_reward)
        final_reward_per_episode = []
        for i in range(0, len(reward_per_episode), 10):
            final_reward_per_episode.append(sum(reward_per_episode[i:i + 9]) // 10)
        return final_reward_per_episode, self.q

    def extract_policy_and_values(self):
        """
        Extracts the policy and state values from the Q-values.

        Returns:
            dict: The policy.
            dict: The state values.
        """
        policy = {}
        V = {}
        for s in self.grid.actions.keys():
            a, max_q = utils.max_dict(self.q[s])
            policy[s] = a
            V[s] = max_q
        self.policy = policy.copy()
        return policy, V


def main(game_info):
    """
    Main function to set up the grid and train the SARSA agent.

    Args:
        game_info (dict): Dictionary containing game configuration.

    Returns:
        dict: Updated game configuration with trained policy and Q-values.
    """
    grid = standard_grid(n=game_info['grid_size'], rewards=game_info['rewards'], slippery=game_info['slippery'],
                         walls=game_info['walls'], coins=game_info['coins'], lever=game_info['lever'],
                         reward_per_coin=game_info['reward_per_coins'], walls_to_remove=game_info['walls_to_remove'])

    sarsa = SARSA(grid, gamma=game_info['gamma'], alpha=game_info['alpha'])
    rewards, q = sarsa.train(episodes=game_info['training_phase'], max_steps=game_info['max_steps_per_episode'],
                             epsilon=game_info['epsilon'])
    plt.plot(rewards)
    plt.title("Reward per Episode")
    plt.show()
    policy, V = sarsa.extract_policy_and_values()
    print("Values:")
    utils.print_values(V, grid)
    print("Policy:")
    utils.print_policy(policy, grid)
    game_info['policy'] = policy
    game_info['q'] = q
    return game_info
