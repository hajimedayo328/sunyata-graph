"""
無分別度 — 対称性で「優劣のなさ」を測る指標
=========================================
無分別度 D(G) = (n − 軌道数) / (n − 1)
  軌道1つ（全頂点が自己同型で入れ替え可能＝完全な無分別）→ D = 1.0
  軌道n個（全頂点が構造的に区別される＝完全な分別）→ D = 0.0

土台: automorphic equivalence（社会ネットワーク分析の確立概念。同じ軌道の頂点は
構造的に区別不能）。穴の数（コホモロジー）でなく対称性で「優劣のなさ」を測る。

典型グラフで比較し、指標の限界（星・ホイールが直感より高く出る）も正直に見る。
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


def orbit_data(G):
    """自己同型群の軌道分類を返す。"""
    autos = list(GraphMatcher(G, G).isomorphisms_iter())
    orbit_of = {v: frozenset(phi[v] for phi in autos) for v in G.nodes()}
    n_orbit = len(set(orbit_of.values()))
    return n_orbit, len(autos), orbit_of


def mufunbetsu(G):
    """無分別度 D = (n − 軌道数)/(n − 1)。"""
    n = G.number_of_nodes()
    k, a, orbit_of = orbit_data(G)
    D = (n - k) / (n - 1) if n > 1 else 1.0
    return D, k, a, orbit_of


def main():
    graphs = {
        "完全グラフ K₆": nx.complete_graph(6),
        "サイクル C₆": nx.cycle_graph(6),
        "ホイール W₅": nx.wheel_graph(5),       # 中心 + C5 = 6頂点
        "道 P₆": nx.path_graph(6),
        "星 S₅": nx.star_graph(5),               # 中心 + 5葉 = 6頂点
        "ランダム G(6,0.45)": nx.gnp_random_graph(6, 0.45, seed=2),
    }
    cmap = plt.cm.Set2

    fig, axes = plt.subplots(2, 3, figsize=(14, 8.6))
    print("=== 無分別度 D=(n−軌道数)/(n−1) ===")
    rows = []
    for ax, (name, G) in zip(axes.flat, graphs.items()):
        D, k, a, orbit_of = mufunbetsu(G)
        rows.append((name, D, k, a))
        uniq = list(dict.fromkeys(orbit_of.values()))
        cidx = {o: i for i, o in enumerate(uniq)}
        colors = [cmap(cidx[orbit_of[v]] % 8) for v in G.nodes()]
        pos = nx.spring_layout(G, seed=4)
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#c4c8cf", width=1.6)
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=colors, node_size=520,
                               edgecolors="#333", linewidths=1.3)
        ax.set_title(f"{name}\n無分別度 D = {D:.2f}（軌道 {k}・|Aut|={a}）", fontsize=11)
        ax.axis("off")
        print(f"  {name:18s}: D={D:.3f}  軌道={k}  |Aut|={a}")

    fig.suptitle("無分別度 D = (n−軌道数)/(n−1)：対等な世界(D=1)から序列のある世界(D→0)まで",
                 fontsize=14, y=1.0)
    fig.tight_layout()
    path = os.path.join(OUT, "mufunbetsu_index.png")
    fig.savefig(path, dpi=130, bbox_inches="tight")

    print("\n--- 無分別度ランキング ---")
    for name, D, k, a in sorted(rows, key=lambda r: -r[1]):
        print(f"  D={D:.2f}  {name}")
    print("\n注意（指標の限界）: 星・ホイールは中心が特別なのに D が高めに出る。")
    print("  葉/外周が互いに対等（同一軌道）だから。軌道数だけでは『中心の重み』を捉えない。")
    print(f"\n図を保存: {path}")


if __name__ == "__main__":
    main()
