"""
無常 × 無分別度 — 手札の掛け算①
=============================
グラフを時間で動かし（エッジが1本ずつ生えたり消えたり）、各時刻の無分別度を追う。
完全に平等な状態（D=1）も永続せず崩れ、また偶然生まれる ＝ 無分別すら無常。

無常プロト（持続ホモロジーの birth-death）の「対称性版」。
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
RNG = np.random.default_rng(5)


def mufunbetsu(G):
    autos = list(GraphMatcher(G, G).isomorphisms_iter())
    orbit_of = {v: frozenset(phi[v] for phi in autos) for v in G.nodes()}
    k = len(set(orbit_of.values()))
    n = G.number_of_nodes()
    return (n - k) / (n - 1) if n > 1 else 1.0


def main():
    n = 6
    G = nx.cycle_graph(n)  # 初期：D=1（完全な平等）
    steps = 45
    series = []
    for _ in range(steps):
        series.append(mufunbetsu(G))
        i, j = RNG.choice(n, 2, replace=False)  # ランダムなペアの辺をトグル
        if G.has_edge(i, j):
            G.remove_edge(i, j)
        else:
            G.add_edge(i, j)

    series = np.array(series)
    perfect = np.where(series >= 0.999)[0]  # 完全な平等(D=1)に戻った時刻

    fig, ax = plt.subplots(figsize=(11.5, 5.2))
    ax.plot(series, marker="o", ms=4, color="#c0392b", lw=1.5)
    ax.axhline(1.0, ls="--", color="#bbb", lw=1)
    ax.scatter(perfect, series[perfect], s=120, facecolor="none",
               edgecolor="#1c7c3f", linewidths=2, zorder=5, label="完全な平等(D=1)＝初期条件のみ")
    ax.set_xlabel("時間ステップ（エッジが1本ずつ変化）", fontsize=11)
    ax.set_ylabel("無分別度 D（平等さ）", fontsize=11)
    ax.set_ylim(-0.05, 1.08)
    ax.set_title("無常 × 無分別度：完全な平等(D=1)は初期だけ。揺らぐ世界では絶えず分別が生じ、完全な無分別はほぼ戻らない", fontsize=11.5)
    ax.legend(fontsize=10)

    print("=== 無常 × 無分別度 ===")
    print(f"無分別度の時系列（{steps}ステップ）: 平均={series.mean():.2f} 最大={series.max():.2f} 最小={series.min():.2f}")
    print(f"完全な平等(D=1)の出現: {len(perfect)} 回（時刻 {list(perfect)}）")
    print("→ 完全な無分別(D=1)は揺らぐ世界ではほぼ実現しない理想。現実は絶えず何らかの分別が生じる")

    fig.tight_layout()
    path = os.path.join(OUT, "anitya_symmetry.png")
    fig.savefig(path, dpi=130, bbox_inches="tight")
    print(f"\n図を保存: {path}")


if __name__ == "__main__":
    main()
