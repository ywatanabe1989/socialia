# scitex[fig] - Twitter/X Draft

## Status: DRAFT

## Japanese

研究者のためのmatplotlib wrapper作った。

グラフを保存するとき、こう書いてない？

```python
fig.savefig("plot.png", dpi=300, bbox_inches='tight')
plt.close()
```

これ、毎回書くの面倒。だから1行にした。

```python
from scitex.fig import quick_save

quick_save(fig, "results")
# -> results.png, results.pdf, results.svg 全部出る
```

論文用のPDF、発表用のPNG、編集用のSVG。一発で。

pip install scitex[fig]

#Python #Research #DataViz #OpenSource

---

## English

Made a matplotlib wrapper for researchers.

When saving figures, do you write this every time?

```python
fig.savefig("plot.png", dpi=300, bbox_inches='tight')
plt.close()
```

Tedious. So I made it one line.

```python
from scitex.fig import quick_save

quick_save(fig, "results")
# -> results.png, results.pdf, results.svg all at once
```

PDF for papers. PNG for slides. SVG for editing. One call.

pip install scitex[fig]

#Python #Research #DataViz #OpenSource
