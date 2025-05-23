__練習問題__
以下のように5×5の迷路を使います。

Q学習またはSARSAを使って「スタートからゴールまで最短経路を学習するプログラム」を作成してください。

```
maze = [
    ['S', '.', '.', '#', '.'],
    ['.', '#', '.', '#', '.'],
    ['.', '#', '.', '.', '.'],
    ['.', '.', '#', '#', '.'],
    ['#', '.', '.', 'G', '.']
]
S: スタート
G: ゴール
#: 壁（通れない）
.: 通れるマス
```

## 構成

1. 環境
   迷路、リワードする、状態を返す、壁は通さない
2. エージェント
   行動選択する、行動価値を更新する
3. 訓練コード
   エージェントを訓練する


```python
    def update(self, s_idx, a, r, s_next_idx, a_next, done):
        # Q(λ)更新
        td_error = r + self.gamma * np.max(self.q[s_next_idx]) * (not done) - self.q[s_idx, a]
        self.e[s_idx, a] += 1  # eligibility traceを増加

        # 全状態・全行動について一括更新
        self.q += self.alpha * td_error * self.e
        # eligibility trace減衰
        self.e *= self.gamma * self.lam

        if done:
            self.e *= 0  # 終了時はtraceリセット
```

更新式

```math
\delta(\lambda) = r + \gamma
```

![1748130301143](image/problem/1748130301143.png)


TD誤差を実装する場合

```python
import numpy as np

def td_lambda_update(V, states, rewards, alpha, gamma, lambd):
    """
    TD(λ) の更新を行う関数
    V: 状態価値を保持する辞書
    states: 状態のリスト
    rewards: 報酬のリスト
    alpha: 学習率
    gamma: 割引率
    lambd: λの値
    """
    eligibility_trace = {s: 0 for s in V.keys()}
    for t in range(len(states) - 1):
        state = states[t]
        next_state = states[t + 1]
        reward = rewards[t]
        td_error = reward + gamma * V[next_state] - V[state]
      
        eligibility_trace[state] += 1
      
        # 各状態の価値を更新
        for s in V.keys():
            V[s] += alpha * td_error * eligibility_trace[s]
            eligibility_trace[s] *= gamma * lambd

    return V

# サンプルデータ
states = ['A', 'B', 'C', 'D']
rewards = [1, 0, -1, 2]
V = {state: 0.0 for state in states}
alpha = 0.1
gamma = 0.9
lambd = 0.8

# 実行
updated_V = td_lambda_update(V, states, rewards, alpha, gamma, lambd)
print(updated_V)

```


### Q:適合度トレースはどのような動作をすることになるでしょうか？

適合度トレース（エリジビリティトレース、eligibility trace）は、強化学習のTD(λ)アルゴリズムで使われる仕組みです。このコードでは、各状態-行動ペアごとに「どれだけ最近そのペアが訪れたか」を記録し、TD誤差（学習信号）をどの程度反映させるかを調整します。

### 動作の概要

* 行動を選択・実行するたびに、その状態-行動ペアの適合度トレース値を1だけ増やします（`self.set_eligibility_trace(state, action, ... + 1)`）。
* すべての状態-行動ペアについて、価値関数の更新時に「TD誤差 × 適合度トレース値」を掛けて重み付けします。
* 各エピソードのステップごとに、適合度トレース値は `γλ`倍されて減衰していきます（`self.get_eligibility_trace(*sa) * self.gamma * self.lambd`）。
* エピソードが終了したら、すべての適合度トレースをリセットします。

### まとめ

適合度トレースは「過去に訪れた状態-行動ペア」にもTD誤差を分配し、より効率的に学習できるようにするための仕組みです。最近訪れたペアほど大きく、古いものほど小さく重み付けされます。
