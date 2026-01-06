# scitex[stats] - Note Draft

## Status: READY

## Japanese

# scitex[stats] - 「どの検定？」をコードで答える

## なぜ作ったか

「どの統計検定を使えばいい？」

研究者なら何度も調べたことがある質問だ。

- 2群比較ならt検定？でも正規分布じゃなかったら？
- 3群以上ならANOVA？でも等分散じゃなかったら？
- 対応ありならpaired t-test？対応なしなら？

いつも同じ決定木をたどる。そして毎回ググる。

さらに面倒なのが、検定後のフォーマット。Natureは「P = 0.003」、APAは「p = .003」。微妙に違う。

頭の中のフローチャートをコードにした。

## 使い方

```python
from scitex.stats import StatContext, recommend_tests

# 実験デザインを記述
ctx = StatContext(
    n_groups=2,           # 群数
    paired=False,         # 対応なし
    outcome_type="continuous"  # 連続量
)

# 推薦を取得
tests = recommend_tests(ctx, top_k=3)
# → ['brunner_munzel', 'ttest_ind', 'mannwhitneyu']
```

デフォルトはBrunner-Munzel検定。正規性や等分散性の仮定がいらない頑健な検定。

## ジャーナル形式

```python
from scitex.stats import format_test_line

# Nature形式
format_test_line(result, style="nature")
# → "P = 0.003, d = 0.85"

# APA形式
format_test_line(result, style="apa")
# → "t(58) = 2.45, p = .003, d = 0.85"

# Cell形式
format_test_line(result, style="cell")
```

## 他の機能

```python
from scitex.stats import recommend_effect_sizes, recommend_posthoc

# 効果量の推薦
recommend_effect_sizes(ctx)
# → ["cohens_d", "cliffs_delta"]

# 事後検定の推薦（3群以上の場合）
recommend_posthoc(ctx)
# → ["tukey", "games_howell"]

# 多重比較補正
from scitex.stats import apply_multiple_correction
corrected = apply_multiple_correction(p_values, method="fdr")
```

## インストール

```bash
pip install scitex[stats]
```

## おわりに

自分の分析ワークフロー用に作った。
「どの検定？」で毎回調べるのが面倒だった。

同じことを繰り返していたら、試してみてください。フィードバック歓迎。

---

*より大きなリサーチツールキットの一部として開発中。*

---

## English

# scitex[stats] - "Which test?" answered in code

## Why I Built This

"Which statistical test should I use?"

A question every researcher has looked up multiple times.

- t-test for 2 groups? But what if it's not normally distributed?
- ANOVA for 3+ groups? But what if variances aren't equal?
- Paired t-test for related samples? Unpaired for independent?

Always the same decision tree. Always Googling again.

And the formatting after the test. Nature wants "P = 0.003", APA wants "p = .003". Subtle differences.

I encoded the mental flowchart.

## Usage

```python
from scitex.stats import StatContext, recommend_tests

# Describe your design
ctx = StatContext(
    n_groups=2,
    paired=False,
    outcome_type="continuous"
)

# Get recommendations
tests = recommend_tests(ctx, top_k=3)
# → ['brunner_munzel', 'ttest_ind', 'mannwhitneyu']
```

Default is Brunner-Munzel test. Robust - no normality or equal variance assumptions.

## Journal Formatting

```python
from scitex.stats import format_test_line

format_test_line(result, style="nature")  # "P = 0.003, d = 0.85"
format_test_line(result, style="apa")     # "t(58) = 2.45, p = .003, d = 0.85"
format_test_line(result, style="cell")
```

## Other Features

- Effect size recommendations: Cohen's d, Cliff's delta
- Post-hoc tests: Tukey, Games-Howell
- Multiple comparison correction: Bonferroni, FDR, Holm

## Install

```bash
pip install scitex[stats]
```

## Closing

Built for my own analysis workflow.
Got tired of looking up "which test" every time.

If you've been doing the same, give it a try. Feedback welcome.

---

*Part of a larger research toolkit in development.*
