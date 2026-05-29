"""
無常 × 持続ホモロジー — 最小プロトタイプ
=====================================
中心テーゼ:
  諸行無常(anitya)＝あらゆる現象は生じて滅する。常住するものはない。
  持続ホモロジー(TDA)のトポロジカル特徴は filtration の進行とともに
  birth(生)→death(滅)する。「生まれて消える」という構造そのものが無常の像。

ここでやること:
  ノイズを乗せた円周上の点群を作る。円は H1(1次元の穴=ループ)を1つ持つ。
  ノイズを 3 段階で増やし、各段階で persistence diagram を計算する。
  ノイズが増えるほど「ループの寿命(death - birth)」が縮み、やがて消える。
  ＝ 同一の構造でも条件(縁)が変われば生滅する＝無常の動的可視化。

誠実さのための限定:
  TDA は「無常」がなくとも金融・神経データで自立して成立する(Gidea 2017 等)。
  仏教フレーミングは動機・解釈であって、数学的内実は純粋な persistence。
  この点を曖昧にしない。
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from ripser import ripser
matplotlib.rcParams["font.family"] = "Yu Gothic"
matplotlib.rcParams["axes.unicode_minus"] = False

OUT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "docs", "figs"))
os.makedirs(OUT, exist_ok=True)

RNG = np.random.default_rng(7)


def noisy_circle(n=120, r=1.0, noise=0.05):
    """半径 r の円周上に n 点 + ガウスノイズ。"""
    theta = RNG.uniform(0, 2 * np.pi, n)
    pts = np.stack([r * np.cos(theta), r * np.sin(theta)], axis=1)
    pts += RNG.normal(0, noise, pts.shape)
    return pts


def longest_h1(dgm_h1):
    """H1 の中で最も寿命(persistence)の長いループの (birth, death, lifetime)。"""
    if len(dgm_h1) == 0:
        return None
    life = dgm_h1[:, 1] - dgm_h1[:, 0]
    k = int(np.argmax(life))
    return dgm_h1[k, 0], dgm_h1[k, 1], life[k]


def main():
    noises = [0.05, 0.18, 0.38]  # 縁(条件)の乱れの度合い
    fig, axes = plt.subplots(2, 3, figsize=(14, 8.5))

    print("=== 無常 × 持続ホモロジー ===")
    for col, noise in enumerate(noises):
        pts = noisy_circle(noise=noise)
        res = ripser(pts, maxdim=1)
        dgms = res["dgms"]
        h1 = dgms[1]
        info = longest_h1(h1)

        # 上段: 点群
        ax = axes[0, col]
        ax.scatter(pts[:, 0], pts[:, 1], s=10, c="#3b4252")
        ax.set_aspect("equal")
        ax.set_title(f"点群（ノイズ={noise}）", fontsize=12)
        ax.set_xticks([]); ax.set_yticks([])

        # 下段: persistence diagram
        ax = axes[1, col]
        if len(dgms[0]) > 0:
            ax.scatter(dgms[0][:, 0], np.where(np.isinf(dgms[0][:, 1]), 0, dgms[0][:, 1]),
                       s=14, c="#9aa0aa", label="H0（連結成分）")
        if len(h1) > 0:
            ax.scatter(h1[:, 0], h1[:, 1], s=40, c="#c0392b", label="H1（ループ）", zorder=3)
        lim = 1.75  # 低ノイズの円は death~1.6 まで伸びるので上限を確保
        ax.plot([0, lim], [0, lim], "--", c="#cccccc", lw=1)
        ax.set_xlim(0, lim); ax.set_ylim(0, lim)
        ax.set_xlabel("birth（生）"); ax.set_ylabel("death（滅）")
        if info:
            b, d, life = info
            ax.annotate(f"寿命={life:.2f}", (b, d), textcoords="offset points",
                        xytext=(8, -2), fontsize=10, color="#c0392b")
            print(f"  ノイズ={noise}: 最長H1ループ birth={b:.3f} death={d:.3f} 寿命={life:.3f}")
        else:
            ax.text(0.5, 0.6, "ループ消滅", color="#c0392b", fontsize=12, ha="center")
            print(f"  ノイズ={noise}: H1ループ消滅（無常）")
        ax.legend(fontsize=8, loc="lower right")
        ax.set_title("persistence diagram", fontsize=12)

    fig.suptitle("無常 × 持続ホモロジー：ループは生じ(birth)、滅する(death)。条件が乱れるほど寿命は縮む",
                 fontsize=14, y=1.0)
    fig.tight_layout()
    path = os.path.join(OUT, "anitya_homology.png")
    fig.savefig(path, dpi=130, bbox_inches="tight")
    print(f"\n図を保存: {path}")


if __name__ == "__main__":
    main()
