"""
縁起 × 因果グラフ / do-calculus — 最小プロトタイプ
================================================
中心テーゼ:
  十二縁起(無明→行→…→老死)は有向グラフ上の因果連鎖として書ける。
  Pearl の介入 do(X=x)（DAG のエッジ切断＋値固定）は、仏道の
  「断無明」（無明という根本条件を滅すれば後続の苦も滅す＝逆観 pratiloma）
  と操作意味論レベルで同型に対応する。

  土台: Yin & Zhang (2022) "Markov categories, causal theories, and the
  do-calculus" (arXiv:2204.04821) が do-calculus を free Markov category で
  形式化済み。本プロトタイプはその「縁起論的解釈」であり、新規の数学では
  ない（誇張しない）。ここでは確率核を最も単純な線形伝播で近似する。

ここでやること:
  1) 十二支DAGを作り、無明=1 を初期入力として活性度を順伝播させる。
  2) do(無明=0) 前後で「老死(苦)」の活性がどう変わるかを可視化。
  3) どの支を断つ(do(i=0))と老死が最も減るかをランキング
     ＝「八正道＝介入列」の萌芽。根本(無明)を断つのが最大効果になるはず。
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

NIDANA = ["無明", "行", "識", "名色", "六処", "触", "受", "愛", "取", "有", "生", "老死"]
W = 0.92  # 各縁の伝播強度（確率核の線形近似）


def build_dag():
    G = nx.DiGraph()
    for i in range(len(NIDANA) - 1):
        G.add_edge(i, i + 1, w=W)
    return G


def propagate(G, intervene=None):
    """順伝播。無明=1 を入力。intervene=i なら do(i=0)：i の活性を 0 に固定し
    i への入力エッジを断つ（Pearl の介入）。"""
    order = list(nx.topological_sort(G))
    a = {node: 0.0 for node in G.nodes()}
    a[0] = 1.0  # 無明 = 根本の入力
    for node in order:
        if node == intervene:
            a[node] = 0.0  # do(node = 0)：エッジ切断＋値固定
            continue
        if node == 0:
            continue  # 無明は外部入力
        inflow = sum(a[p] * G[p][node]["w"] for p in G.predecessors(node))
        a[node] = inflow
    return a


def main():
    G = build_dag()
    base = propagate(G)
    do_avidya = propagate(G, intervene=0)

    print("=== 縁起 × do-calculus ===")
    base_total = sum(base.values())
    print(f"介入なし   : 老死(苦)の活性 = {base[11]:.4f} / 苦の総量(全支合計) = {base_total:.4f}")
    print(f"do(無明=0) : 老死(苦)の活性 = {do_avidya[11]:.4f} / 苦の総量 = {sum(do_avidya.values()):.4f}  ← 断無明で全消滅")

    # 注意: 老死「単体」で測ると線形鎖ではどの支を断っても 0 になり差が出ない。
    # これはモデルが単純すぎる証拠。指標を「苦の総量(全支の活性合計)」に変えると、
    # 上流(無明)を断つほど多くの支が消えるため効果が大きい、が自然に出る（モデルは歪めない）。
    effects = []
    for i in range(len(NIDANA)):
        a = propagate(G, intervene=i)
        a_total = sum(a.values())
        reduction = base_total - a_total
        effects.append((i, a_total, reduction))
        print(f"  do({NIDANA[i]}=0) → 苦の総量={a_total:.4f}  減少={reduction:.4f}")

    # ---- 可視化 ----
    fig = plt.figure(figsize=(14, 9))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.1, 1])

    pos = {i: (i, 0) for i in range(len(NIDANA))}

    def draw_chain(ax, activ, title, cut=None):
        colors = [plt.cm.OrRd(0.15 + 0.8 * activ[i]) for i in range(len(NIDANA))]
        nx.draw_networkx_edges(G, pos, ax=ax, arrows=True, arrowsize=14,
                               edge_color="#b8bdc7", width=1.6)
        nx.draw_networkx_nodes(G, pos, ax=ax, node_size=820, node_color=colors,
                               edgecolors="#3b4252", linewidths=1.4)
        for i, name in enumerate(NIDANA):
            ax.text(i, 0, name, ha="center", va="center", fontsize=8.5, color="#1a1a1a")
            ax.text(i, -0.42, f"{activ[i]:.2f}", ha="center", va="center",
                    fontsize=8, color="#666")
        if cut is not None:
            ax.scatter([cut], [0.32], marker="x", s=200, c="#c0392b", linewidths=3, zorder=5)
            ax.text(cut, 0.5, "断", ha="center", color="#c0392b", fontsize=12, fontweight="bold")
        ax.set_title(title, fontsize=12)
        ax.set_xlim(-0.7, len(NIDANA) - 0.3); ax.set_ylim(-0.8, 0.8)
        ax.axis("off")

    ax1 = fig.add_subplot(gs[0, :])
    draw_chain(ax1, base, "① 介入なし：無明を根に苦(老死)まで活性が伝播する（流転）")

    ax2 = fig.add_subplot(gs[1, 0])
    draw_chain(ax2, do_avidya, "② do(無明=0)：断無明 → 下流すべて消滅（還滅）", cut=0)

    # 介入効果ランキング
    ax3 = fig.add_subplot(gs[1, 1])
    idxs = [e[0] for e in effects]
    reds = [e[2] for e in effects]
    bars = ax3.bar([NIDANA[i] for i in idxs], reds, color="#4c72b0")
    bars[0].set_color("#c0392b")  # 無明を強調
    ax3.set_ylabel("苦の総量(全支)の減少", fontsize=10)
    ax3.set_title("各支を断ったときの苦の減少\n（無明=根本が最大効果＝八正道の標的）", fontsize=11)
    ax3.tick_params(axis="x", rotation=60, labelsize=8)

    fig.suptitle("縁起 × do-calculus：介入 do(無明=0) ≅ 断無明。土台は Yin & Zhang 2022",
                 fontsize=14, y=1.0)
    fig.tight_layout()
    path = os.path.join(OUT, "engi_markov.png")
    fig.savefig(path, dpi=130, bbox_inches="tight")
    print(f"\n図を保存: {path}")


if __name__ == "__main__":
    main()
