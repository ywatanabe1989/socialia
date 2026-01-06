# scitex[io] - Reddit Draft

## Status: READY

## Japanese

**タイトル:** scitex[io] - 拡張子から自動判定するsave/load

MacやWindowsでは、ファイルをクリックすれば適切なアプリが開く。この「当たり前」がコードにもあるべきだと思った。

毎日、CSV、NPY、PTH、JSON、HDF5... それぞれ違うAPI。覚えていられない。

だから **scitex[io]** を作った：

```python
from scitex.io import save, load

# 保存 - 拡張子から自動判定
save(dataframe, "results.csv")
save(numpy_array, "features.npy")
save(torch_model, "checkpoint.pth")
save(config, "settings.yaml")

# 読み込み - Round trip
dataframe = load("results.csv")
numpy_array = load("features.npy")
torch_model = load("checkpoint.pth")

# globパターンも対応
all_configs = load("configs/*.yaml")
```

**対応形式:**
- 表形式: CSV, TSV, Excel, Parquet, Feather
- 配列: NPY, NPZ, HDF5, Zarr, MAT
- モデル: PTH, ONNX, Joblib, Pickle
- 設定: JSON, YAML, TOML
- ドキュメント: PDF, DOCX, TXT, Markdown
- 画像: PNG, JPG, TIFF, SVG

```bash
pip install scitex[io]
```

より大きなツールキットの一部。フィードバック歓迎。

#Python #Research #DataScience #OpenSource

---

## English

**Title:** scitex[io] - save/load with format auto-detection from extension

On Mac/Windows, you click a file and the right app opens. This "just works" simplicity should exist in code too.

Daily I touch CSV, NPY, PTH, JSON, HDF5... each with different APIs. Can't remember them all.

So I built **scitex[io]**:

```python
from scitex.io import save, load

# Save - format from extension
save(dataframe, "results.csv")
save(numpy_array, "features.npy")
save(torch_model, "checkpoint.pth")
save(config, "settings.yaml")

# Load - Round trip
dataframe = load("results.csv")
numpy_array = load("features.npy")
torch_model = load("checkpoint.pth")

# Glob patterns work too
all_configs = load("configs/*.yaml")
```

**Supported formats:**
- Tabular: CSV, TSV, Excel, Parquet, Feather
- Arrays: NPY, NPZ, HDF5, Zarr, MAT
- Models: PTH, ONNX, Joblib, Pickle
- Config: JSON, YAML, TOML
- Documents: PDF, DOCX, TXT, Markdown
- Images: PNG, JPG, TIFF, SVG

```bash
pip install scitex[io]
```

Part of a larger toolkit. Feedback welcome.

#Python #Research #DataScience #OpenSource
