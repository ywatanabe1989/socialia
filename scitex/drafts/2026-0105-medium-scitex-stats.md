# scitex[stats] - Medium Draft

## Status: READY

## English

# Stop Googling "Which Statistical Test Should I Use"
## A decision tree encoded in Python

Every researcher has been there.

You have two groups of data. You want to know if they're different. Simple enough.

But then the questions start:
- Is it normally distributed? Did I check?
- Are the variances equal? Levene's test first?
- Paired or unpaired? Wait, what counts as paired?
- t-test or Mann-Whitney? When do I use which?

You've probably bookmarked at least one "which statistical test to use" flowchart. I had three. They disagreed on edge cases.

And once you've run the test, there's the formatting. Nature wants `P = 0.003`. APA wants `p = .003` (lowercase, no leading zero). Cell has its own style. You format it wrong, it comes back in review.

After years of this dance, I decided to encode the decision tree into code.

## The Solution

**scitex[stats]** - describe your data, get test recommendations.

```python
from scitex.stats import StatContext, recommend_tests

# Describe your experimental design
ctx = StatContext(
    n_groups=2,
    sample_sizes=[30, 32],
    paired=False,
    outcome_type="continuous",
    design="between"
)

# Get ranked recommendations
tests = recommend_tests(ctx, top_k=3)
# → ['brunner_munzel', 'ttest_ind', 'mannwhitneyu']
```

The default recommendation is Brunner-Munzel. Why? It's the most robust - no normality assumption, no equal variance assumption, handles unequal sample sizes. It's what you should probably be using anyway.

## Journal-Style Formatting

```python
from scitex.stats import format_test_line

# Same result, different journals
format_test_line(result, style="nature")
# → "P = 0.003, d = 0.85"

format_test_line(result, style="apa")
# → "t(58) = 2.45, p = .003, d = 0.85"

format_test_line(result, style="cell")
# → "P = 0.003 (t = 2.45, df = 58)"
```

Built-in styles: APA, Nature, Cell, Elsevier, and a plain format.

## Beyond Basic Tests

The test is just the start. You also need:

**Effect sizes** (because p-values aren't enough):
```python
from scitex.stats import recommend_effect_sizes

recommend_effect_sizes(ctx)
# → ["cohens_d", "cliffs_delta"]
```

**Post-hoc tests** (for 3+ groups):
```python
from scitex.stats import recommend_posthoc

ctx_multi = StatContext(n_groups=4, design="between")
recommend_posthoc(ctx_multi)
# → ["tukey", "games_howell", "dunnett"]
```

**Multiple comparison correction**:
```python
from scitex.stats import apply_multiple_correction

corrected_p = apply_multiple_correction(
    p_values,
    method="fdr"  # or "bonferroni", "holm", "sidak"
)
```

## What It Supports

**Two-group comparisons:**
- t-test (independent, paired, Welch's)
- Mann-Whitney U
- Wilcoxon signed-rank
- Brunner-Munzel (recommended default)

**Multi-group comparisons:**
- One-way ANOVA, Welch's ANOVA
- Kruskal-Wallis
- Friedman (repeated measures)

**Correlation:**
- Pearson, Spearman, Kendall
- Point-biserial, phi coefficient

**Post-hoc:**
- Tukey HSD, Games-Howell
- Dunnett (vs control)
- Dunn's test (non-parametric)

## Installation

```bash
pip install scitex[stats]
```

## Closing Thoughts

Statistical testing shouldn't require a flowchart taped to your monitor. The decision logic is well-defined - it can be coded.

I built this because I was tired of the mental overhead. Not the hard part of statistics (interpreting results, understanding effect sizes), but the mechanical part (remembering which test, formatting for journals).

If you've spent time on these decisions, give it a try. Feedback welcome - especially on edge cases in test selection.

---

*This is part of a larger research toolkit I'm building. More modules coming.*

---

## Japanese

# 「どの統計検定を使うべきか」のググりをやめよう
## 決定木をPythonでコード化

研究者なら誰でも経験がある。

2群のデータがある。差があるか知りたい。シンプルな話のはずだ。

でも疑問が始まる：
- 正規分布してる？チェックした？
- 等分散？まずLevene検定？
- 対応ありか対応なし？そもそも対応ありって何？
- t検定かMann-Whitney？どっちをいつ使う？

「どの統計検定」のフローチャートをブックマークしたことがあるはず。私は3つ持っていた。エッジケースで意見が分かれていた。

そして検定が終わったら、フォーマット。Natureは`P = 0.003`。APAは`p = .003`（小文字、先頭のゼロなし）。Cellは独自スタイル。間違えると査読で戻ってくる。

何年もこれを繰り返した後、決定木をコードにすることにした。

## 解決策

**scitex[stats]** - データを記述すれば、検定を推薦。

```python
from scitex.stats import StatContext, recommend_tests

# 実験デザインを記述
ctx = StatContext(
    n_groups=2,
    sample_sizes=[30, 32],
    paired=False,
    outcome_type="continuous",
    design="between"
)

# ランク付きの推薦を取得
tests = recommend_tests(ctx, top_k=3)
# → ['brunner_munzel', 'ttest_ind', 'mannwhitneyu']
```

デフォルトの推薦はBrunner-Munzel。なぜか？最も頑健だから - 正規性の仮定なし、等分散性の仮定なし、不均等なサンプルサイズも対応。そもそもこれを使うべきだった。

## ジャーナル形式のフォーマット

```python
from scitex.stats import format_test_line

# 同じ結果、異なるジャーナル
format_test_line(result, style="nature")
# → "P = 0.003, d = 0.85"

format_test_line(result, style="apa")
# → "t(58) = 2.45, p = .003, d = 0.85"

format_test_line(result, style="cell")
# → "P = 0.003 (t = 2.45, df = 58)"
```

組み込みスタイル：APA, Nature, Cell, Elsevier, プレーン形式。

## 基本検定を超えて

検定は始まりにすぎない。他にも必要：

**効果量**（p値だけでは不十分）:
```python
from scitex.stats import recommend_effect_sizes
recommend_effect_sizes(ctx)
# → ["cohens_d", "cliffs_delta"]
```

**事後検定**（3群以上）:
```python
from scitex.stats import recommend_posthoc
ctx_multi = StatContext(n_groups=4, design="between")
recommend_posthoc(ctx_multi)
# → ["tukey", "games_howell", "dunnett"]
```

**多重比較補正**:
```python
from scitex.stats import apply_multiple_correction
corrected_p = apply_multiple_correction(p_values, method="fdr")
```

## インストール

```bash
pip install scitex[stats]
```

## おわりに

統計検定にモニターに貼ったフローチャートは要らないはず。決定ロジックは明確 - コード化できる。

精神的なオーバーヘッドに疲れたから作った。統計の難しい部分（結果の解釈、効果量の理解）ではなく、機械的な部分（どの検定を覚える、ジャーナル用にフォーマット）。

これらの判断に時間を使っていたら、試してみてください。フィードバック歓迎 - 特に検定選択のエッジケースについて。

---

*より大きなリサーチツールキットの一部として開発中。他のモジュールも順次公開予定。*
