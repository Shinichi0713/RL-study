# 方策反復
import matplotlib.pyplot as plt
import numpy as np
import agent, environment


def policy_iteration():
    env = environment.Environment()
    agent_instance = agent.Agent(env)
    iteration = 0

    # 学習の経過を保存するリスト
    pi_history = []

    while True:
        iteration += 1
        value_function = agent_instance.evaluate_pi()
        is_pi_stable = agent_instance.improve_pi()

        # deep copyで保存
        pi_history.append(np.copy(agent_instance.pi))

        print(f"Iteration {iteration}:")
        print("Value function:", value_function)
        print("pi =", agent_instance.pi)
        if is_pi_stable:
            break

    print("\n最適方策:", agent_instance.pi)
    print("最適状態価値:", agent_instance.value_function)
    return pi_history, agent_instance.pi


def visualize_policy_1d(pi):
    # pi: shape = (num_states, num_actions)
    # 0:←, 1:→, 0.5:・

    # 各状態の最善行動を取得
    best_actions = np.argmax(pi, axis=1)
    # もし確率が0.5なら・にする
    symbols = []
    for i in range(pi.shape[0]):
        if np.allclose(pi[i, 0], 0.5) and np.allclose(pi[i, 1], 0.5):
            symbols.append("・")
        elif best_actions[i] == 0:
            symbols.append("←")
        elif best_actions[i] == 1:
            symbols.append("→")
        else:
            symbols.append("?")
    statuses = np.arange(pi.shape[0]) + 1
    fig, ax = plt.subplots(figsize=(8, 2))
    ax.set_xlim(0.5, pi.shape[0]+0.5)
    ax.set_ylim(-1, 1)
    ax.set_xticks(statuses)
    ax.set_yticks([])

    for i, symbol in enumerate(symbols):
        if symbol == "←":
            # 左向き矢印
            ax.arrow(i+0.2+1, 0, -0.4, 0, head_width=0.2, head_length=0.15, fc='b', ec='b')
        elif symbol == "→":
            # 右向き矢印
            ax.arrow(i-0.2+1, 0, 0.4, 0, head_width=0.2, head_length=0.15, fc='r', ec='r')
        elif symbol == "・":
            ax.plot(i, 0, "ko", markersize=12)
        else:
            ax.text(i, 0, symbol, fontsize=20, ha='center', va='center')

    ax.set_xlabel("status")
    ax.set_title("best policy with pi-iteration")
    plt.tight_layout()
    plt.show()

# --- 実行 ---
if __name__ == "__main__":
    pi_history, pi = policy_iteration()

    visualize_policy_1d(pi)

