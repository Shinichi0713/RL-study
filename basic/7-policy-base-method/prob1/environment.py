## CartPoleを用いた環境
import gym
import torch


class PoleGym:
    def __init__(self, is_train=False):
        if is_train:
            self.env = gym.make('CartPole-v1')
        else:
            self.env = gym.make('CartPole-v1', render_mode="human")
        self.states, self.actions, self.rewards = [], [], []

    def reset(self):
        self.states, self.actions, self.rewards = [], [], []
        return self.env.reset()

    def step(self, action):
        next_state, reward, terminated, truncated, info = self.env.step(action)
        return next_state, reward, terminated, truncated, info

    def render(self):
        self.env.render()

    def close(self):
        self.env.close()

    # 割引累積報酬を計算
    def compute_returns(self, gamma=0.98):
        returns = []
        R = 0
        for r in reversed(self.rewards):
            R = r + gamma * R
            returns.insert(0, R)
        returns = torch.tensor(returns, dtype=torch.float32)
        # 標準化（学習を安定化させるため）
        returns = (returns - returns.mean()) / (returns.std() + 1e-6)
        return returns

    # エピソードを1つ実行して、軌跡を記録
    def run_episode(self, policy_net, device):
        state = self.reset()[0]
        done = False
        while not done:
            state_tensor = torch.FloatTensor(state).to(device)
            probs = policy_net(state_tensor)
            dist = torch.distributions.Categorical(probs)
            action = dist.sample()
            next_state, reward, done, _, _ = self.step(action.item())
            self.rewards.append(reward)
            self.states.append(state)
            self.actions.append(action)
            state = next_state
        return self.states, self.actions, self.rewards

# def run_episode(env, policy_net, device):
    # state = env.reset()[0]
    # states, actions, rewards = [], [], []
    # done = False
    # while not done:
    #     state_tensor = torch.FloatTensor(state).to(device)
    #     probs = policy_net(state_tensor)
    #     dist = torch.distributions.Categorical(probs)
    #     action = dist.sample()
    #     next_state, reward, done, _, _ = env.step(action.item())
    #     states.append(state)
    #     actions.append(action)
    #     rewards.append(reward)
    #     state = next_state
    # return states, actions, rewards



if __name__ == "__main__":
    env = PoleGym()
    state = env.reset()
    done = False
    for i in range(20):
        action = env.env.action_space.sample()
        next_state, reward, terminated, truncated, info, q_weight = env.step(action)
        env.render()
        state = next_state
        if terminated or truncated:
            print("Episode finished after {} timesteps".format(i+1))
            break
    env.close()
