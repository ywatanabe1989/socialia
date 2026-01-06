# scitex[stats] - LinkedIn Draft

## Status: READY

## Japanese

「どの統計検定を使えばいい？」

研究者なら誰でもググったことがある。t検定かMann-Whitney？ANOVAかKruskal-Wallis？そして検定後、NatureとCellとAPAでフォーマットが違う。

頭の中のフローチャートをコードにした。

**scitex[stats]** - データを記述すれば、検定を推薦。

```python
from scitex.stats import StatContext, recommend_tests

# 実験デザインを記述
ctx = StatContext(n_groups=2, paired=False)

# 推薦を取得
recommend_tests(ctx)
# → ['brunner_munzel', 'ttest_ind', 'mannwhitneyu']

# ジャーナル形式でフォーマット
format_test_line(result, style="nature")  # P = 0.003
format_test_line(result, style="apa")     # p = .003
```

他にも: 効果量 / 事後検定 / 多重比較補正

pip install scitex[stats]

自分の分析ワークフロー用に作った。同じ決定木を毎回たどっていたら、試してみてください。

#Python #Research #Statistics #DataScience #OpenSource

---

## English

"Which statistical test should I use?"

Every researcher has Googled this. t-test or Mann-Whitney? ANOVA or Kruskal-Wallis? And after the test, Nature vs Cell vs APA formatting.

I encoded the mental flowchart.

**scitex[stats]** - describe your data, get test recommendations.

```python
from scitex.stats import StatContext, recommend_tests

# Describe your design
ctx = StatContext(n_groups=2, paired=False)

# Get recommendations
recommend_tests(ctx)
# → ['brunner_munzel', 'ttest_ind', 'mannwhitneyu']

# Format for journal
format_test_line(result, style="nature")  # P = 0.003
format_test_line(result, style="apa")     # p = .003
```

Also: effect sizes / post-hoc tests / multiple comparison correction

pip install scitex[stats]

Built for my own workflow. If you've been walking the same decision tree, give it a try.

#Python #Research #Statistics #DataScience #OpenSource
