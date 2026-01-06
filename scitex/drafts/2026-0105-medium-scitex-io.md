# scitex[io] - Medium Draft

## Status: READY

## English

# Stop Memorizing File I/O APIs
## One function for 30+ formats, because extensions already tell us what to do

On a Mac or Windows, you double-click a file and the right app opens. You don't think about it. The extension tells the system what to do, and the system handles the rest.

I've been doing research programming for years, and this simplicity never existed in my code. Every day, I touch CSV files, NumPy arrays, PyTorch checkpoints, YAML configs, HDF5 datasets, images... Each format has its own library, its own syntax. `pd.read_csv()`, `np.load()`, `torch.load()`, `json.load()`, `yaml.safe_load()`, `h5py.File()`.

I can never remember them all. And why should I? The file extension already tells me what format it is.

After writing the same format-detection boilerplate for the hundredth time, I decided to just make it work the way it should have from the start.

## The Solution

**scitex[io]** - one function to save, one function to load. Format auto-detected from the extension.

```python
from scitex.io import save, load

# Just save. Extension determines format.
save(dataframe, "results.csv")
save(numpy_array, "embeddings.npy")
save(torch_model, "checkpoint.pth")
save(config_dict, "settings.yaml")

# Just load. Same simplicity.
df = load("results.csv")
embeddings = load("embeddings.npy")
model = load("checkpoint.pth")

# Glob patterns work too
all_yamls = load("configs/*.yaml")  # Returns list
```

No format-specific imports. No remembering which library handles what. The extension is the API.

## What It Supports

- **Tabular data**: CSV, TSV, Excel (.xlsx), Parquet, Feather
- **Arrays**: NPY, NPZ, HDF5, Zarr, MAT (MATLAB)
- **ML models**: PTH (PyTorch), ONNX, Joblib, Pickle
- **Configuration**: JSON, YAML, TOML, INI
- **Documents**: PDF, DOCX, TXT, Markdown
- **Images**: PNG, JPG, TIFF, SVG, GIF
- **Audio**: WAV, MP3

30+ formats total. If you work with a format not listed, it's probably easy to add.

## Key Features

1. **Zero format-specific code** - The extension is the interface
2. **Glob pattern support** - Load multiple files matching a pattern
3. **Consistent return types** - Always get what you expect
4. **Graceful fallbacks** - Missing optional dependencies handled cleanly

## Installation

```bash
pip install scitex[io]
```

## Closing Thoughts

I built this because I was tired of the cognitive load. Not the hard kind - the annoying kind. The "wait, is it `yaml.load()` or `yaml.safe_load()`?" kind.

File extensions already contain the information we need. The save/load functions should just use it.

If you've felt the same low-grade frustration, give it a try. Feedback welcome.

---

*This is part of a larger research toolkit I'm building. More modules coming.*

---

## Japanese

# ファイルI/O APIを覚えるのをやめよう
## 拡張子がすでに答えを教えてくれている

MacやWindowsでは、ファイルをダブルクリックすれば適切なアプリが開く。意識することはない。拡張子がシステムに何をすべきか教え、システムが残りを処理する。

研究プログラミングを何年も続けてきたが、この単純さはコードの中には存在しなかった。毎日、CSVファイル、NumPy配列、PyTorchチェックポイント、YAML設定、HDF5データセット、画像を扱う。それぞれのフォーマットに独自のライブラリ、独自の構文がある。`pd.read_csv()`, `np.load()`, `torch.load()`, `json.load()`, `yaml.safe_load()`, `h5py.File()`。

全部は覚えられない。そもそも覚える必要があるのか？ファイル拡張子がすでにフォーマットを教えてくれている。

同じフォーマット検出のボイラープレートを100回目に書いた後、最初からそうあるべきだった形で動くようにすることにした。

## 解決策

**scitex[io]** - 保存に1つの関数、読み込みに1つの関数。フォーマットは拡張子から自動検出。

```python
from scitex.io import save, load

# 保存するだけ。拡張子がフォーマットを決める。
save(dataframe, "results.csv")
save(numpy_array, "embeddings.npy")
save(torch_model, "checkpoint.pth")
save(config_dict, "settings.yaml")

# 読み込むだけ。同じシンプルさ。
df = load("results.csv")
embeddings = load("embeddings.npy")
model = load("checkpoint.pth")

# globパターンも対応
all_yamls = load("configs/*.yaml")  # リストを返す
```

フォーマット固有のインポートなし。どのライブラリが何を扱うか覚える必要なし。拡張子がAPIになる。

## 対応フォーマット

- **表形式データ**: CSV, TSV, Excel (.xlsx), Parquet, Feather
- **配列**: NPY, NPZ, HDF5, Zarr, MAT (MATLAB)
- **MLモデル**: PTH (PyTorch), ONNX, Joblib, Pickle
- **設定**: JSON, YAML, TOML, INI
- **ドキュメント**: PDF, DOCX, TXT, Markdown
- **画像**: PNG, JPG, TIFF, SVG, GIF
- **音声**: WAV, MP3

合計30種類以上。リストにないフォーマットでも、追加は簡単。

## 主な機能

1. **フォーマット固有のコード不要** - 拡張子がインターフェース
2. **globパターン対応** - パターンに一致する複数ファイルを読み込み
3. **一貫した戻り値の型** - 期待通りのものが返る
4. **優雅なフォールバック** - オプション依存関係がなくてもクリーンに処理

## インストール

```bash
pip install scitex[io]
```

## おわりに

認知負荷に疲れたから作った。難しい種類ではなく、煩わしい種類の。「`yaml.load()`だっけ、`yaml.safe_load()`だっけ？」という種類の。

ファイル拡張子にはすでに必要な情報が含まれている。save/load関数はそれを使うべき。

同じ小さな不満を感じていたら、試してみてください。フィードバック歓迎。

---

*より大きなリサーチツールキットの一部として開発中。他のモジュールも順次公開予定。*
