"""
空 × 米田の補題 — 最小プロトタイプ
================================
中心テーゼ:
  対象は「自性(svabhāva)」という内在的中身を持たず、
  他の全対象との関係の総体 Hom(-, A) によってのみ同定される。
  これは圏論の米田の補題が主張することと構造的に一致する（＝空 śūnyatā）。

ここでやること:
  有限な半順序圏(poset category)を作り、各対象の「関係プロファイル」
  Hom(-, A) を計算する。そして
    「2つの対象が同型 ⇔ 関係プロファイルが一致」
  を計算的に確認し、可視化する。
  対象ノードからラベル(中身)を剥がしても、関係だけで全対象が区別できる
  ＝「中身は無くても関係で決まる」を絵で示す。

注意(誠実さのための限定):
  これは米田の補題の有限・自明ケースの確認であって、空の哲学的内実を
  「証明」するものではない。先行研究 Zaghi(2025), Posina&Roy(2024) と
  コアのアナロジーは共有する。新規性は対応そのものではなく、関係プロファイル
  の定量化・可視化の手続きにある。
"""
import os
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
matplotlib.rcParams["font.family"] = "Yu Gothic"
matplotlib.rcParams["axes.unicode_minus"] = False

OUT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "docs", "figs"))
os.makedirs(OUT, exist_ok=True)


def build_category():
    """有限poset圏 C: 対象=ノード, 射 i->j = 「i が j の縁となる」関係。"""
    edges = [(0, 1), (0, 2), (1, 3), (2, 3), (2, 4), (3, 5), (4, 5), (5, 6)]
    G = nx.DiGraph(edges)
    return G


def hom_profiles(G):
    """米田プロファイル Hom(-, i) を計算。
    poset圏では射は高々1本なので Hom(k,i)=1 ⇔ k から i へ到達可能(=k≤i)。
    """
    objs = sorted(G.nodes())
    n = len(objs)
    idx = {o: i for i, o in enumerate(objs)}
    TC = nx.transitive_closure(G, reflexive=True)  # 推移閉包＋恒等射 = 合成の閉包
    Hom = np.zeros((n, n), dtype=int)  # Hom[k][i] = 1 なら k ≤ i
    for k in objs:
        for i in objs:
            if TC.has_edge(k, i):
                Hom[idx[k]][idx[i]] = 1
    # 各対象 i の関係プロファイル = Hom 行列の i 列（i に入ってくる関係の総体）
    profiles = {i: tuple(Hom[:, idx[i]]) for i in objs}
    distinct = len(set(profiles.values())) == n
    return objs, idx, Hom, profiles, distinct


def main():
    G = build_category()
    objs, idx, Hom, profiles, distinct = hom_profiles(G)
    n = len(objs)

    print("=== 空 × 米田の補題 ===")
    print(f"対象数: {n}")
    print("各対象の米田プロファイル Hom(-, A)（A に入ってくる関係の総体）:")
    for o in objs:
        print(f"  対象{o}: {profiles[o]}")
    print(f"\n米田の補題の計算的確認: すべての対象が関係プロファイルで区別できるか → {distinct}")
    print("  → True なら『中身(ラベル)を見ずとも、関係の総体だけで全対象が一意に定まる』")
    print("     ＝ 自性なし・関係のみで同定される（空 śūnyatā の計算的な姿）")

    # ---- 可視化 ----
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))

    # 左: 圏の有向グラフ（射＝縁）
    pos = nx.spring_layout(G, seed=3, k=1.2)
    nx.draw_networkx_edges(G, pos, ax=ax1, arrows=True, arrowsize=18,
                           edge_color="#9aa0aa", width=1.6,
                           connectionstyle="arc3,rad=0.06")
    nx.draw_networkx_nodes(G, pos, ax=ax1, node_size=900, node_color="#ffffff",
                           edgecolors="#3b4252", linewidths=1.8)
    nx.draw_networkx_labels(G, pos, ax=ax1, font_size=12, font_color="#3b4252")
    ax1.set_title("圏 C：対象と射（＝縁起の関係）", fontsize=13)
    ax1.axis("off")

    # 右: Hom 行列ヒートマップ（各列 = 対象の関係プロファイル Hom(-, A)）
    im = ax2.imshow(Hom, cmap="Blues", vmin=0, vmax=1, aspect="auto")
    ax2.set_xticks(range(n)); ax2.set_xticklabels([f"対象{o}" for o in objs], fontsize=9)
    ax2.set_yticks(range(n)); ax2.set_yticklabels([f"{o}から" for o in objs], fontsize=9)
    ax2.set_xlabel("各列 = Hom(−, A)：A の『関係による身元』", fontsize=11)
    ax2.set_title("関係プロファイル行列\n（列がすべて異なる＝自性なしでも一意に定まる）", fontsize=12)
    for i in range(n):
        for j in range(n):
            if Hom[i, j]:
                ax2.text(j, i, "→", ha="center", va="center", color="#1c4f8f", fontsize=11)
    fig.colorbar(im, ax=ax2, fraction=0.046, pad=0.04, ticks=[0, 1])

    fig.suptitle("空 × 米田の補題：対象 = 他との関係の総体（自性 svabhāva なし）",
                 fontsize=14, y=1.02)
    fig.tight_layout()
    path = os.path.join(OUT, "sunyata_yoneda.png")
    fig.savefig(path, dpi=130, bbox_inches="tight")
    print(f"\n図を保存: {path}")


if __name__ == "__main__":
    main()
