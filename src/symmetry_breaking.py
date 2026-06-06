"""
無分別 × 対称性の破れ — 最小プロト
=================================
中心アイデア:
  頂点推移グラフ（全頂点が自己同型で入れ替え可能＝対等＝無分別、軌道は1つ）に
  エッジを足すと自己同型群が縮み、軌道が分裂する。
  ＝ 対等だったものに「区別・特別さ・優劣」が生まれる ＝ 分別の発生。

  「優劣のなさ」を測る道具は、コホモロジー（穴の数）ではなく
  自己同型群と軌道（automorphic equivalence）。軌道が1つ＝完全な無分別。

preflight確定: 賈先生に見せて教えを乞う＋圏論的思考の訓練 / 動くプロト / とりあえず動かす。
"""
import os
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
matplotlib.rcParams["font.family"] = "Yu Gothic"
matplotlib.rcParams["axes.unicode_minus"] = False

OUT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "docs", "figs"))
os.makedirs(OUT, exist_ok=True)


def automorphisms(G):
    """グラフ G の自己同型を全列挙（小さいグラフ専用）。"""
    return list(GraphMatcher(G, G).isomorphisms_iter())


def orbits(G):
    """自己同型群の軌道で頂点を分類する。
    頂点 v の軌道 = { φ(v) : φ ∈ Aut(G) }。同じ軌道の頂点は構造的に区別不能。
    軌道が1つ ⇔ 頂点推移的 ⇔ 完全な無分別。
    """
    autos = automorphisms(G)
    orbit_of = {v: frozenset(phi[v] for phi in autos) for v in G.nodes()}
    unique = list(dict.fromkeys(orbit_of.values()))  # 出現順ユニーク
    color_idx = {orb: i for i, orb in enumerate(unique)}
    node_color = {v: color_idx[orbit_of[v]] for v in G.nodes()}
    return node_color, len(unique), len(autos), unique


def build_stages():
    """軌道数が 1 → 2 → 3+ と単調に増える（＝分別が進む）3段階を作る。"""
    g0 = nx.cycle_graph(6)
    g1 = nx.cycle_graph(6); g1.add_edge(0, 3)
    g2 = nx.cycle_graph(6); g2.add_edge(0, 3); g2.add_edge(0, 6)  # 頂点6＝突起(葉)
    return [
        (g0, [], "無分別：六角形 C₆", "どの点も入れ替え可能。軌道は1つ＝特別な点なし"),
        (g1, [(0, 3)], "分別の芽：弦を1本", "自己同型が縮み軌道が2つに。区別が生まれる"),
        (g2, [(0, 3), (0, 6)], "分別が深まる：突起を1つ", "非対称な要素で軌道がさらに増える"),
    ]


def main():
    import numpy as np
    stages = build_stages()

    pos = nx.circular_layout(nx.cycle_graph(6))
    pos[6] = pos[0] * 1.7  # 突起(頂点6)を頂点0の外側に置く
    cmap = plt.cm.Set2

    fig, axes = plt.subplots(1, 3, figsize=(15.5, 5.8))
    print("=== 無分別 × 対称性の破れ ===")
    for ax, (G, extra, title, sub) in zip(axes, stages):
        node_color, n_orbit, n_auto, orbs = orbits(G)
        colors = [cmap(node_color[v]) for v in G.nodes()]

        nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#aab", width=2.0)
        if extra:
            nx.draw_networkx_edges(G, pos, ax=ax, edgelist=extra,
                                   edge_color="#c0392b", width=2.6, style="dashed")
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=colors, node_size=950,
                               edgecolors="#333", linewidths=1.6)
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=12)
        ax.set_title(f"{title}\n軌道数 = {n_orbit}（色の種類）   |Aut(G)| = {n_auto}", fontsize=12)
        ax.text(0.5, -0.08, sub, transform=ax.transAxes, ha="center", fontsize=10, color="#555")
        ax.set_aspect("equal")
        ax.axis("off")

        print(f"  {title}: 軌道数={n_orbit}, |Aut(G)|={n_auto}, 軌道={[sorted(o) for o in orbs]}")

    fig.suptitle("無分別 × 対称性の破れ：対等な点（軌道1）に、エッジ1本で区別＝軌道分裂（分別）が生まれる",
                 fontsize=14, y=1.02)
    fig.tight_layout()
    path = os.path.join(OUT, "symmetry_breaking.png")
    fig.savefig(path, dpi=130, bbox_inches="tight")
    print(f"\n図を保存: {path}")


if __name__ == "__main__":
    main()
