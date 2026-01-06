# scitex[io] - Twitter/X Draft

## Status: READY

## Japanese

MacやWindowsでは、ファイルをクリックすれば適切なアプリが開く。

コードでも同じにできないか？

```python
from scitex.io import save, load

save(df, "data.csv")
save(model, "model.pth")

df = load("data.csv")
model = load("model.pth")
```

拡張子から自動判定。30種類以上対応。

pip install scitex[io]

#Python #Research #DataScience #OpenSource

---

## English

On Mac/Windows, you click a file and the right app opens.

Why not in Python?

```python
from scitex.io import save, load

save(df, "data.csv")
save(model, "model.pth")

df = load("data.csv")
model = load("model.pth")
```

Format auto-detected. 30+ types supported.

pip install scitex[io]

#Python #Research #DataScience #OpenSource
