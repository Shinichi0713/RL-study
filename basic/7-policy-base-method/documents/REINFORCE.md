## ロス関数
REINCORCEのロス関数は強化学習においてエージェントがとった行動の確率を報酬に応じて増減する、ということを目的として設計されている。
報酬の高かった行動は今後もとりやすくし、報酬が低かった行動はとりにくくする。

## 数式的な背景

REINFORCEアルゴリズムは、方策勾配法（Policy Gradient Method）の一種です。  
エージェントの方策（policy）\(\pi_\theta(a|s)\)のパラメータ\(\theta\)を、**期待される報酬**を最大化する方向に更新します。

### 期待報酬の最大化
\[
J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta} [R(\tau)]
\]
ここで\(\tau\)はエピソード（状態・行動の列）、\(R(\tau)\)は累積報酬。

### 方策勾配定理
\[
\nabla_\theta J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta} \left[ \sum_{t} \nabla_\theta \log \pi_\theta(a_t|s_t) \cdot R_t \right]
\]
この勾配を**確率的勾配降下法**で最適化します。


はい、ご指摘の通り、理論上は全状態・全行動について期待値を取りますが、実際にはサンプリング（経験）によって近似します。  
このとき、**サンプルされた状態・行動系列**を用いて、方策勾配は次のように近似されます。

---

## 方策勾配のサンプリングによる近似式

\[
\nabla_\theta J(\theta) \approx \frac{1}{N} \sum_{i=1}^{N} \nabla_\theta \log \pi_\theta(a_i|s_i) \left( Q^{\pi_\theta}(s_i, a_i) - V^{\pi}(s_i) \right)
\]

- \(N\)：サンプル数（バッチサイズやエピソード数）
- \(s_i, a_i\)：挙動方策（実際にエージェントがたどった軌跡）から得られた状態・行動
- \(Q^{\pi_\theta}(s_i, a_i)\)：その状態・行動の行動価値
- \(V^{\pi}(s_i)\)：その状態の状態価値

---

## さらに簡単な場合（REINFORCE型）

もし \(Q^{\pi_\theta}(s_i, a_i)\) の代わりに「実際に得られた報酬（リターン）」を使う場合は：

\[
\nabla_\theta J(\theta) \approx \frac{1}{N} \sum_{i=1}^{N} \nabla_\theta \log \pi_\theta(a_i|s_i) \left( R_i - b(s_i) \right)
\]

- \(R_i\)：サンプル\(i\)で得られた累積報酬
- \(b(s_i)\)：バイアス（ベースライン、例：状態価値関数）

---

**まとめ：**  
理論上の期待値は、実際にはサンプルの平均（和）で近似します。  
このようにして方策勾配法は現実的に計算されます。

以上です。