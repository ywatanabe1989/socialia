# scitex[stats] - Twitter/X Draft

## Status: READY

## Japanese

「どの統計検定を使えばいい？」

全ての研究者が直面する問い。t検定かMann-Whitney？ANOVAかKruskal-Wallis？

だからフローチャートをコード化した。

```python
from scitex.stats import StatContext, recommend_tests

ctx = StatContext(n_groups=2, paired=False)
recommend_tests(ctx)
# → ['brunner_munzel', 'ttest_ind', 'mannwhitneyu']
```

ジャーナル形式の出力も対応（APA, Nature, Cell）。

pip install scitex[stats]

#Python #Research #Statistics #OpenSource

---

## English

"Which statistical test should I use?"

Every researcher asks this. t-test or Mann-Whitney? ANOVA or Kruskal-Wallis?

So I encoded the flowchart.

```python
from scitex.stats import StatContext, recommend_tests

ctx = StatContext(n_groups=2, paired=False)
recommend_tests(ctx)
# → ['brunner_munzel', 'ttest_ind', 'mannwhitneyu']
```

Also: journal-style formatting (APA, Nature, Cell).

pip install scitex[stats]

#Python #Research #Statistics #OpenSource
