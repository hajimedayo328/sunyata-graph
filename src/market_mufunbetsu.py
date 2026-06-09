"""
market_graph × 無分別度 — 手札の掛け算②
====================================
市場の相関ネットワークの「平等さ（無分別度）」を時系列で測る。

- 平常時：銘柄がバラバラに動く＝相関が低くまばら＝立場が多様＝無分別度ひくい
- 危機時：全銘柄が一斉に同じ動き（相関1に収束）＝みんな同じ立場＝無分別度たかい

＝「金融危機 = 市場の無分別化」。普段は対称性が破れている（個性がある）市場が、
危機で対称性が回復する（みんな同じになる）。

合成データで概念実証。相関を閾値で2値化してグラフ化（重み付き→重みなしの前処理）。
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


def mufunbetsu_from_corr(corr, thresh=0.5):
    """相関行列を閾値で2値化してグラフ化し、無分別度を返す。"""
    n = corr.shape[0]
    G = nx.Graph()
    G.add_nodes_from(range(n))
    for i in range(n):
        for j in range(i + 1, n):
            if abs(corr[i, j]) >= thresh:
                G.add_edge(i, j)
    autos = list(GraphMatcher(G, G).isomorphisms_iter())
    orbit_of = {v: frozenset(phi[v] for phi in autos) for v in G.nodes()}
    k = len(set(orbit_of.values()))
    D = (n - k) / (n - 1) if n > 1 else 1.0
    return D, G.number_of_edges()


def main():
    n = 6
    # 危機度：平常 → 危機 → 回復 の山
    crisis = np.concatenate([
        np.linspace(0.0, 0.9, 12),   # 危機が高まる
        np.full(6, 0.9),             # 危機ピーク
        np.linspace(0.9, 0.0, 14),   # 回復
    ])

    # 平常時の素の構造（固定・非対称）：銘柄ごとに個別の相関で、一部のペアだけ繋がる中密度グラフ
    base = RNG.uniform(0.0, 0.8, (n, n))
    base = (base + base.T) / 2
    np.fill_diagonal(base, 1.0)

    D_series, edge_series = [], []
    for c in crisis:
        # 危機度 c で全ペアが一斉に連動（相関→1）。平常時(c=0)は base の非対称構造のまま
        corr = (1 - c) * base + c * 1.0
        np.fill_diagonal(corr, 1.0)
        D, m = mufunbetsu_from_corr(corr, thresh=0.5)
        D_series.append(D); edge_series.append(m)

    D_series = np.array(D_series)
    t = np.arange(len(crisis))

    fig, ax1 = plt.subplots(figsize=(11.5, 5.4))
    ax1.fill_between(t, crisis, color="#e74c3c", alpha=0.12, label="危機度（背景）")
    ax1.plot(t, D_series, marker="o", ms=4, color="#2c3e9e", lw=1.8, label="無分別度 D（市場の平等さ）")
    ax1.axvspan(12, 18, color="#e74c3c", alpha=0.08)
    ax1.text(15, 1.02, "危機ピーク", ha="center", color="#c0392b", fontsize=10)
    ax1.set_xlabel("時間（平常 → 危機 → 回復）", fontsize=11)
    ax1.set_ylabel("無分別度 D / 危機度", fontsize=11)
    ax1.set_ylim(-0.05, 1.12)
    ax1.legend(fontsize=10, loc="upper right")
    ax1.set_title("market × 無分別度：危機で全銘柄が連動＝市場が無分別化する（D が上がる）", fontsize=12.5)

    print("=== market × 無分別度 ===")
    print(f"平常時(最初)の D = {D_series[:5].mean():.2f}（銘柄バラバラ＝多様）")
    print(f"危機ピーク時の D = {D_series[12:18].mean():.2f}（全銘柄連動＝無分別化）")
    print(f"回復後(最後)の D = {D_series[-5:].mean():.2f}")
    print("→ 危機で市場の『平等さ』が跳ね上がる＝個性が消えてみんな同じ動きになる")

    fig.tight_layout()
    path = os.path.join(OUT, "market_mufunbetsu.png")
    fig.savefig(path, dpi=130, bbox_inches="tight")
    print(f"\n図を保存: {path}")


if __name__ == "__main__":
    main()
