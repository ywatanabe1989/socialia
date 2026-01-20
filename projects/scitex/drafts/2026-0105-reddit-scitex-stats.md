# scitex[stats] - Reddit Draft

## Status: READY

## Japanese

**タイトル:** scitex[stats] - 統計検定の自動推薦

「どの統計検定を使えばいい？」- 何度もググった。

決定木はいつも同じ：2群か3群以上か？対応ありか？正規分布？そして検定後、Natureは`P = 0.003`、APAは`p = .003`。

だからコード化した：

```python
from scitex.stats import StatContext, recommend_tests, format_test_line

# デザインを記述
ctx = StatContext(n_groups=2, paired=False)

# 推薦を取得（頑健性でランキング）
recommend_tests(ctx)
# → ['brunner_munzel', 'ttest_ind', 'mannwhitneyu']

# Brunner-Munzelがデフォルト：正規性・等分散性の仮定不要

# ジャーナル形式でフォーマット
format_test_line(result, style="nature")  # P = 0.003, d = 0.85
format_test_line(result, style="apa")     # p = .003, d = 0.85
```

**他の機能:**
- `recommend_effect_sizes(ctx)` - Cohen's d, η², Cliff's delta
- `recommend_posthoc(ctx)` - Tukey, Dunnett, Games-Howell
- `apply_multiple_correction(p_values, method="fdr")`

```bash
pip install scitex[stats]
```

より大きなツールキットの一部。フィードバック歓迎。

#Python #Research #Statistics #OpenSource

---

## English

**Title:** scitex[stats] - automatic statistical test recommendation

"Which statistical test should I use?" - Googled this many times.

The decision tree is always the same: 2 groups or more? Paired? Normal? And after: Nature wants `P = 0.003`, APA wants `p = .003`.

So I encoded it:

```python
from scitex.stats import StatContext, recommend_tests, format_test_line

# Describe your design
ctx = StatContext(n_groups=2, paired=False)

# Get recommendations (ranked by robustness)
recommend_tests(ctx)
# → ['brunner_munzel', 'ttest_ind', 'mannwhitneyu']

# Brunner-Munzel is default: no normality/equal variance assumptions

# Format for journal
format_test_line(result, style="nature")  # P = 0.003, d = 0.85
format_test_line(result, style="apa")     # p = .003, d = 0.85
```

**Also:**
- `recommend_effect_sizes(ctx)` - Cohen's d, η², Cliff's delta
- `recommend_posthoc(ctx)` - Tukey, Dunnett, Games-Howell
- `apply_multiple_correction(p_values, method="fdr")`

```bash
pip install scitex[stats]
```

Part of a larger toolkit. Feedback welcome.

#Python #Research #Statistics #OpenSource
