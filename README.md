# sunyata-graph

**空・縁起・無我を、グラフ理論と圏論で可視化・形式化する研究プロジェクト**

仏教（特に禅・中観・華厳）の存在論を、データ可視化と数学的形式化の両面から扱う。
理論だけで止まっている既存研究に対して、「経典データを取り込み → グラフで可視化 → 圏論で形式化」の3点セットで踏み込むのが狙い。

> Status: **最小プロトタイプ3本が動作（2026-05）**。空×米田 / 無常×持続ホモロジー / 縁起×do-calculus。
> サイト → https://hajimedayo328.github.io/sunyata-graph/ ／ コードは `src/`、図は `docs/figs/`。

## 動かし方

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install numpy networkx matplotlib scipy ripser
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe src/sunyata_yoneda.py   # 空×米田
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe src/anitya_homology.py  # 無常×持続ホモロジー
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe src/engi_markov.py      # 縁起×do-calculus
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe src/symmetry_breaking.py # 無分別×対称性の破れ
```

---

## なぜやるか

- 圏論×空（śūnyatā）の核論文は世界に事実上1グループ（Posina & Roy）しかなく、分野はまだ「最初の旗が立った」段階。
- **禅・道元・華厳を数学的に厳密に扱った研究はほぼ皆無**。空白地帯が広い。
- 「米田の補題＝対象は外部関係の総体で決まる」が龍樹の「自性なき相互依存（＝無我）」と構造対応する、というのが現在の中心テーゼ。

## 空白地帯（着手候補）

| テーマ | 内容 | 状態 |
|---|---|---|
| 空 × 米田の補題 | 対象＝関係の総体 Hom(−,A) を有限圏で計算・可視化 | ✅ プロトタイプ |
| 無分別 × 対称性の破れ | 頂点推移グラフ→エッジ追加で軌道分裂（automorphic equivalence）。優劣の発生を可視化 | ✅ プロトタイプ |
| 十二縁起の因果DAG | 無明→…→老死を有向グラフ化、do-calculus で介入シミュレート | ✅ プロトタイプ |
| 持続ホモロジー × 無常 | TDAの「特徴が生まれて消える」構造を anitya と対応 | ✅ プロトタイプ |
| 華厳「事事無礙法界」 | 「一即一切」をハイパーグラフ（ハイパーエッジ）で表現 | 未着手 |
| インドラの網 | メビウス変換・クライン群で自己相似ネットを描画 | 未着手 |
| 公案の論理構造 | 四句分別を矛盾許容論理＋グラフで可視化 | 未着手 |

## 構成

```
sunyata-graph/
├── docs/        # GitHub Pages（可視化サイト）
├── src/         # Python（縁起DAG・インドラ網・圏論実装）
├── data/        # 経典コーパス・概念対応表
└── notebooks/   # 分析・試作ノートブック
```

## 先行研究（実在確認済み・2026-05）

### 圏論 × 仏教
- Posina V. Rayudu & Sisir Roy (2017) "Buddhist Thought on Emptiness and Category Theory" — [PhilArchive](https://philarchive.org/rec/POSBTO-2)
- Posina V. Rayudu & Sisir Roy (2024) "Category Theory and the Ontology of Śūnyatā" *The Origin and Significance of Zero* (Brill, pp.450–478) — [PhilPapers](https://philpapers.org/rec/VENCTA-3)
- Arash Zaghi (2025) "Quantum Reality as Indra's Net: A Category-Theoretic Formalism for Relational Quantum Dynamics" — [PhilArchive](https://philarchive.org/rec/ARAQRA)

### 仏教論理の形式化
- Graham Priest (2010) "The Logic of the Catuṣkoṭi" *Comparative Philosophy* 1(2) — [SJSU](https://scholarworks.sjsu.edu/comparativephilosophy/vol1/iss2/6/)
- Tetu Makino (2014) "A Note on a Modified Catuskoti" — [arXiv:1405.7744](https://arxiv.org/abs/1405.7744)

### 圏論 × 自己・自律性（日本人研究者）
- R. Hirota, H. Saigo (西郷甲矢人), S. Taguchi (田口茂) (2023) "Reformalizing the notion of autonomy as closure through category theory as an arrow-first mathematics" — [arXiv:2305.15279](https://arxiv.org/abs/2305.15279) / [ALIFE 2023 (MIT Press)](https://direct.mit.edu/isal/proceedings/isal2023/35/99/116901)

### 物理 × 仏教
- Michael A. Peters (2022) "Wittgenstein, Nāgārjuna and relational quantum mechanics" *Educational Philosophy and Theory* 54(12) — [T&F](https://www.tandfonline.com/doi/full/10.1080/00131857.2022.2034620)
- D. Vernette, P. Tandan, M. Caponigro (2007) "Approach to Physical Reality: a note on Poincare Group and the philosophy of Nagarjuna" — [arXiv:0704.1665](https://arxiv.org/abs/0704.1665)

### 数学書
- D. Mumford, C. Series, D. Wright (2002) *Indra's Pearls: The Vision of Felix Klein* (Cambridge UP)

> 上記はリンク先の実在を確認済み。ただし内容の引用時は必ず原典PDFを通読すること（要約のニュアンスは二次情報に頼らない）。

## ライセンス

未定（研究メモ段階）。
