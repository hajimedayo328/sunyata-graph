"""
無分別度・2つの測り方の比較
=========================
同じ「優劣のなさ」でも、測り方が2つある：

- 軌道数版 D_orbit = (n − 軌道数)/(n − 1)
    「立場の種類」で測る。立場が1種類＝全員対等＝1.0。粗い。

- 対称性版 D_aut = log|Aut| / log(n!)
    「入れ替え方が何通りあるか（対等さの豊かさ）」で測る。
    完全グラフ（どんな並べ替えもOK＝n!通り）＝1.0。

星問題：軌道数版だと星もホイールも「中心＋対等な周り」で似た値になるが、
対称性版だと、星の葉は自由に入れ替わる（5!=120通り）のに対し
ホイールの外周は輪の順序に縛られる（8通り）ので、はっきり差がつく。
→ 2つの指標は「平等さ」の別の側面を捉えている。
"""
import os
import math
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
matplotlib.rcParams["font.family"] = "Yu Gothic"
matplotlib.rcParams["axes.unicode_minus"] = False

OUT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "docs", "figs"))
os.makedirs(OUT, exist_ok=True)


def stats(G):
    n = G.number_of_nodes()
    autos = list(GraphMatcher(G, G).isomorphisms_iter())
    a = len(autos)
    orbit_of = {v: frozenset(phi[v] for phi in autos) for v in G.nodes()}
    k = len(set(orbit_of.values()))
    D_orbit = (n - k) / (n - 1) if n > 1 else 1.0
    D_aut = math.log(a) / math.log(math.factorial(n)) if (n > 1 and a > 1) else (1.0 if a >= math.factorial(n) else 0.0)
    return D_orbit, D_aut, k, a


def main():
    graphs = {
        "完全 K₆": nx.complete_graph(6),
        "サイクル C₆": nx.cycle_graph(6),
        "星 S₅": nx.star_graph(5),
        "ホイール W₅": nx.wheel_graph(5),
        "道 P₆": nx.path_graph(6),
        "ランダム": nx.gnp_random_graph(6, 0.45, seed=2),
    }

    names, d_orbit, d_aut = [], [], []
    print("=== 無分別度：2つの測り方 ===")
    print(f"{'グラフ':14s} {'軌道数版':>8s} {'対称性版':>8s}  (軌道, |Aut|)")
    for name, G in graphs.items():
        Do, Da, k, a = stats(G)
        names.append(name); d_orbit.append(Do); d_aut.append(Da)
        print(f"{name:14s} {Do:8.2f} {Da:8.2f}  (軌道{k}, |Aut|={a})")

    x = range(len(names))
    w = 0.38
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.bar([i - w/2 for i in x], d_orbit, width=w, label="軌道数版 D=(n−軌道数)/(n−1)", color="#4c72b0")
    ax.bar([i + w/2 for i in x], d_aut, width=w, label="対称性版 D=log|Aut|/log(n!)", color="#dd8452")
    ax.set_xticks(list(x)); ax.set_xticklabels(names, fontsize=11)
    ax.set_ylabel("無分別度（優劣のなさ）", fontsize=11)
    ax.set_ylim(0, 1.05)
    ax.legend(fontsize=10)
    ax.set_title("無分別度の2つの測り方：星とホイールの差が、対称性版でくっきり出る", fontsize=13)
    for i, (o, a_) in enumerate(zip(d_orbit, d_aut)):
        ax.text(i - w/2, o + 0.02, f"{o:.2f}", ha="center", fontsize=8, color="#34495e")
        ax.text(i + w/2, a_ + 0.02, f"{a_:.2f}", ha="center", fontsize=8, color="#8c4a26")

    fig.tight_layout()
    path = os.path.join(OUT, "mufunbetsu_compare.png")
    fig.savefig(path, dpi=130, bbox_inches="tight")
    print("\n注目：サイクルC₆と星S₅。軌道数版では C₆(1.0) > S₅(0.8) だが、")
    print("  対称性版では S₅(0.73) > C₆(0.38) と逆転する。")
    print("  星は葉が自由に入れ替わる(5!=120通り)＝『対等な部分の自由度』が大きいから。")
    print(f"\n図を保存: {path}")


if __name__ == "__main__":
    main()
