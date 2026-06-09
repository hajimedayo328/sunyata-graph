"""
②の検証：無分別度 D vs 相関のただの平均 — 言い換えか、本物の新視点か
================================================================
「危機で相関が1に収束」は金融で超既知。無分別度がその"言い換え"に過ぎないなら、
D と「相関平均」は常に同じ動きをするはず。

ここでは4フェーズ（平常→危機→分裂→回復）で両者を重ねる。狙いは「分裂」局面：
  危機(全員連動)と分裂(2ブロック化)は『相関の量』が似ていても『構造』が違う。
  - 相関平均：両者を区別できない（量しか見ない）
  - 無分別度：区別できる（構造＝誰と誰が同じ立場か、を見る）
ここでズレれば、無分別度は相関平均が見逃す『市場の分裂構造』を捉える＝本物の新視点。
"""
import os
import numpy as np
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
matplotlib.rcParams["font.family"] = "Yu Gothic"
matplotlib.rcParams["axes.unicode_minus"] = False

OUT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "docs", "figs"))
os.makedirs(OUT, exist_ok=True)
RNG = np.random.default_rng(11)
N = 6


def analyze(corr, thresh=0.5):
    G = nx.Graph()
    G.add_nodes_from(range(N))
    for i in range(N):
        for j in range(i + 1, N):
            if abs(corr[i, j]) >= thresh:
                G.add_edge(i, j)
    autos = list(GraphMatcher(G, G).isomorphisms_iter())
    orbit_of = {v: frozenset(phi[v] for phi in autos) for v in G.nodes()}
    k = len(set(orbit_of.values()))
    D = (N - k) / (N - 1) if N > 1 else 1.0
    mask = ~np.eye(N, dtype=bool)
    corr_mean = np.abs(corr[mask]).mean()
    return D, corr_mean


def c_normal():
    # 中密度の非対称構造（疎すぎると空グラフ＝全員孤立で対等＝D=1 になる盲点を避ける）
    base = RNG.uniform(0.0, 0.8, (N, N)); base = (base + base.T) / 2
    np.fill_diagonal(base, 1.0); return base


def c_crisis():
    c = np.full((N, N), 0.8); np.fill_diagonal(c, 1.0); return c


def c_split():
    # 2ブロックに分裂：{0,1} と {2,3,4,5}。ブロック内は連動、ブロック間は無相関
    c = np.zeros((N, N))
    c[0, 1] = c[1, 0] = 0.8
    for i in range(2, N):
        for j in range(i + 1, N):
            c[i, j] = c[j, i] = 0.8
    np.fill_diagonal(c, 1.0); return c


def main():
    phases = [("平常", c_normal, 8), ("危機", c_crisis, 6), ("分裂", c_split, 6), ("回復", c_normal, 8)]
    D_series, M_series, bounds, labels = [], [], [], []
    t = 0
    for name, fn, length in phases:
        bounds.append(t); labels.append(name)
        for _ in range(length):
            D, M = analyze(fn())
            D_series.append(D); M_series.append(M); t += 1
    bounds.append(t)

    D_series = np.array(D_series); M_series = np.array(M_series)
    x = np.arange(len(D_series))

    fig, ax = plt.subplots(figsize=(12, 5.6))
    ax.plot(x, D_series, marker="o", ms=4, color="#2c3e9e", lw=1.9, label="無分別度 D（構造で測る）")
    ax.plot(x, M_series, marker="s", ms=4, color="#dd8452", lw=1.9, label="相関のただの平均（量で測る）")
    for b in bounds[1:-1]:
        ax.axvline(b - 0.5, color="#ccc", ls="--", lw=1)
    for i, name in enumerate(labels):
        mid = (bounds[i] + bounds[i + 1]) / 2 - 0.5
        ax.text(mid, 1.08, name, ha="center", fontsize=11, color="#555")
    # 危機と分裂の平均値を比較
    cri = slice(bounds[1], bounds[2]); spl = slice(bounds[2], bounds[3])
    ax.annotate("ここがカギ：相関平均は危機>分裂で下がるが\nDは『2ブロック構造』を捉えて違う形で動く",
                xy=(bounds[2] + 2, D_series[spl].mean()), xytext=(bounds[2] - 1, 0.45),
                fontsize=9.5, color="#c0392b",
                arrowprops=dict(arrowstyle="->", color="#c0392b"))
    ax.set_xlabel("時間（平常 → 危機 → 分裂 → 回復）", fontsize=11)
    ax.set_ylabel("値（0〜1）", fontsize=11)
    ax.set_ylim(0, 1.15)
    ax.legend(fontsize=10, loc="center left")
    ax.set_title("検証：無分別度 D は『相関平均』の言い換えか？ — 分裂局面でズレれば本物の新視点", fontsize=12.5)

    print("=== 検証：無分別度 vs 相関平均 ===")
    print(f"危機フェーズ : D平均={D_series[cri].mean():.2f}  相関平均={M_series[cri].mean():.2f}")
    print(f"分裂フェーズ : D平均={D_series[spl].mean():.2f}  相関平均={M_series[spl].mean():.2f}")
    dD = D_series[cri].mean() - D_series[spl].mean()
    dM = M_series[cri].mean() - M_series[spl].mean()
    print(f"危機→分裂の変化:  ΔD={dD:+.2f}   Δ相関平均={dM:+.2f}")
    if abs(dM) > 0.05 and abs(dD - dM) > 0.1:
        print("→ DとΔ相関平均の動きがズレる＝無分別度は相関平均が見逃す『分裂構造』を捉える＝本物の新視点")
    else:
        print("→ ほぼ同じ動き＝無分別度は相関平均の言い換えの可能性。設計を見直す")

    fig.tight_layout()
    path = os.path.join(OUT, "market_vs_corr.png")
    fig.savefig(path, dpi=130, bbox_inches="tight")
    print(f"\n図を保存: {path}")


if __name__ == "__main__":
    main()
