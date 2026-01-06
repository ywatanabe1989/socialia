# scitex[io] - Note Draft

## Status: READY

## Japanese

# scitex[io] - ファイル形式を意識しないsave/load

## なぜ作ったか

MacやWindowsでは、ファイルをダブルクリックすれば適切なアプリが開く。拡張子を見て、システムが判断してくれる。

研究では毎日さまざまなファイル形式を扱う。CSV、JSON、NPY、PTH、HDF5、画像... それぞれ別のライブラリ、別のAPI。`pd.read_csv()`, `np.load()`, `torch.load()`, `json.load()`, `yaml.safe_load()`... 全部覚えていられない。

コードでも同じ「クリックすれば開く」感覚が欲しかった。

## 使い方

```python
from scitex.io import save, load

# 拡張子から自動判定
save(dataframe, "results.csv")
save(array, "data.npy")
save(model, "checkpoint.pth")
save(config, "settings.yaml")

# 読み込みも同様
df = load("results.csv")
arr = load("data.npy")

# globパターンも対応
all_configs = load("configs/*.yaml")
```

## 対応フォーマット

30種類以上に対応：

- **表形式**: CSV, TSV, Excel, Parquet, Feather
- **配列**: NPY, NPZ, HDF5, Zarr
- **モデル**: PTH, ONNX, Joblib, Pickle
- **設定**: JSON, YAML, TOML
- **ドキュメント**: PDF, DOCX, TXT, Markdown
- **画像**: PNG, JPG, TIFF, SVG
- **音声**: WAV, MP3

## インストール

```bash
pip install scitex[io]
```

## おわりに

自分の研究ワークフロー用に作ったもの。
「このファイル形式、どうやって読むんだっけ？」と毎回調べるのが面倒だった。

同じ不便を感じていた方がいれば、フィードバック歓迎です。

---

*より大きなリサーチツールキットの一部として開発中。*

---

## English

# scitex[io] - Format-agnostic save/load

## Why I Built This

On a Mac or Windows, you double-click a file and the right app opens. The system looks at the extension and figures it out.

In research, we work with many formats daily. CSV, JSON, NPY, PTH, HDF5, images... each with its own library, its own API. `pd.read_csv()`, `np.load()`, `torch.load()`, `json.load()`, `yaml.safe_load()`... too many to remember.

I wanted that same "click and it opens" feeling in code.

## Usage

```python
from scitex.io import save, load

# Auto-detect from extension
save(dataframe, "results.csv")
save(array, "data.npy")
save(model, "checkpoint.pth")
save(config, "settings.yaml")

# Loading works the same
df = load("results.csv")
arr = load("data.npy")

# Glob patterns supported
all_configs = load("configs/*.yaml")
```

## Supported Formats

30+ formats:

- **Tabular**: CSV, TSV, Excel, Parquet, Feather
- **Arrays**: NPY, NPZ, HDF5, Zarr
- **Models**: PTH, ONNX, Joblib, Pickle
- **Config**: JSON, YAML, TOML
- **Documents**: PDF, DOCX, TXT, Markdown
- **Images**: PNG, JPG, TIFF, SVG
- **Audio**: WAV, MP3

## Install

```bash
pip install scitex[io]
```

## Closing

Built for my own research workflow.
Got tired of looking up "how do I read this format again?" every time.

If you've felt the same frustration, feedback welcome.

---

*Part of a larger research toolkit in development.*
