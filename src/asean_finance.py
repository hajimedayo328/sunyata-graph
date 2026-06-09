"""
ASEAN金融 × 無分別度 — 手札を東南アジアに展開
==========================================
市場プロト（market_mufunbetsu）の枠組みを、銘柄→ASEAN+各国に差し替えただけ。
同じ尺度が別ドメインで動く＝手札の汎用性。

アジア通貨危機(1997)のような連動危機を無分別度で見る：
- 平常：各国経済が個別事情でバラバラに動く＝多様＝無分別度ひくい
- 危機：通貨・株が一斉連動して下落＝みんな同じ動き＝無分別度たかい（ASEANの無分別化）

合成データで概念実証。
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

COUNTRIES = ["タイ", "インドネシア", "マレーシア", "フィリピン", "シンガポール", "韓国", "香港", "ベトナム"]
N = len(COUNTRIES)


def mufunbetsu_and_graph(corr, thresh=0.5):
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
    return D, G


def main():
    RNG = np.random.default_rng(7)
    base = RNG.uniform(0.0, 0.8, (N, N)); base = (base + base.T) / 2
    np.fill_diagonal(base, 1.0)
    crisis = np.concatenate([
        np.linspace(0.0, 0.95, 12),  # 危機が伝播
        np.full(6, 0.95),            # 危機ピーク（全国連動）
        np.linspace(0.95, 0.0, 14),  # 回復
    ])

    D_series = []
    for c in crisis:
        corr = (1 - c) * base + c * 1.0
        np.fill_diagonal(corr, 1.0)
        D, _ = mufunbetsu_and_graph(corr)
        D_series.append(D)
    D_series = np.array(D_series)

    _, G_normal = mufunbetsu_and_graph((1 - 0.0) * base + 0.0)
    _, G_crisis = mufunbetsu_and_graph((1 - 0.95) * base + 0.95 * 1.0)

    fig = plt.figure(figsize=(14, 6))
    gs = fig.add_gridspec(2, 2, width_ratios=[1.7, 1])
    ax0 = fig.add_subplot(gs[:, 0])
    ax1 = fig.add_subplot(gs[0, 1])
    ax2 = fig.add_subplot(gs[1, 1])

    t = np.arange(len(crisis))
    ax0.fill_between(t, crisis, color="#e74c3c", alpha=0.12, label="危機度（背景）")
    ax0.plot(t, D_series, marker="o", ms=4, color="#2c3e9e", lw=1.9, label="無分別度 D（ASEANの平等さ）")
    ax0.axvspan(12, 18, color="#e74c3c", alpha=0.08)
    ax0.text(15, 1.03, "危機ピーク", ha="center", color="#c0392b", fontsize=10)
    ax0.set_xlabel("時間（平常 → 危機伝播 → 回復）", fontsize=11)
    ax0.set_ylabel("無分別度 D / 危機度", fontsize=11)
    ax0.set_ylim(-0.05, 1.12)
    ax0.legend(fontsize=9.5, loc="center left")
    ax0.set_title("ASEAN金融 × 無分別度：危機で全国が一斉連動＝ASEANの無分別化", fontsize=12.5)

    pos = nx.circular_layout(list(range(N)))
    labels = {i: COUNTRIES[i] for i in range(N)}
    for ax, G, title, col in [(ax1, G_normal, "平常時：各国バラバラ（多様）", "#4c72b0"),
                              (ax2, G_crisis, "危機時：全国連動（無分別化）", "#c0392b")]:
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#c4c8cf", width=1.3)
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=col, node_size=420,
                               edgecolors="#333", linewidths=1.0, alpha=0.85)
        nx.draw_networkx_labels(G, pos, ax=ax, labels=labels, font_size=7.5, font_color="#fff")
        ax.set_title(title, fontsize=10.5)
        ax.axis("off")

    print("=== ASEAN金融 × 無分別度 ===")
    print(f"平常時の D = {D_series[:5].mean():.2f}（各国バラバラ＝多様）")
    print(f"危機ピークの D = {D_series[12:18].mean():.2f}（全国連動＝ASEANの無分別化）")
    print(f"平常時の連動エッジ数 = {G_normal.number_of_edges()} / 危機時 = {G_crisis.number_of_edges()}（最大{N*(N-1)//2}）")
    print("→ 市場プロトと同じ尺度が、ドメイン（銘柄→国）を変えても動く＝手札の汎用性")

    fig.tight_layout()
    path = os.path.join(OUT, "asean_finance.png")
    fig.savefig(path, dpi=130, bbox_inches="tight")
    print(f"\n図を保存: {path}")


if __name__ == "__main__":
    main()
