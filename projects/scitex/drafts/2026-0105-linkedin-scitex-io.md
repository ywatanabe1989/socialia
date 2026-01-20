<!-- ---
!-- Timestamp: 2026-01-05 21:56:44
!-- Author: ywatanabe
!-- File: /home/ywatanabe/proj/social/scitex/drafts/2026-0105-linkedin-scitex-io.md
!-- --- -->

# scitex[io] - LinkedIn Draft

## Status: READY

## Japanese

MacやWindowsでは、ファイルをクリックすれば適切なアプリが開きます。この「当たり前」がコードにもあるべきだと思いました。

そこで **scitex[io]** を作りました。一つの関数で、拡張子から自動判定します。

```python
from scitex.io import save, load

# 保存 - 拡張子から自動判定
save(dataframe, "results.csv")
save(numpy_array, "features.npy")
save(figure, "plot.png")

# 読み込み - Round trip
dataframe = load("results.csv")
numpy_array = load("features.npy")
fig = load("plot.png")
```

対応形式: CSV / Excel / JSON / YAML / NPY / HDF5 / Zarr / PTH / PKL / PDF / DOCX / 画像など 30種類以上

pip install scitex[io]

フィードバックをお待ちしています。

#Python #Research #DataScience #OpenSource

---

## English

On Mac/Windows, you click a file and the right app opens.
That "just works" simplicity should exist in code too.

So I built **scitex[io]**.
One function, format auto-detected from the file extension.

```python
from scitex.io import save, load

# Save — format inferred from extension
save(dataframe, "results.csv")
save(numpy_array, "features.npy")
save(figure, "plot.png")

# Load — same API, round-trip
dataframe = load("results.csv")
numpy_array = load("features.npy")
fig = load("plot.png")
```

Supports CSV / Excel / JSON / YAML / NPY / HDF5 / Zarr / PTH / PKL / PDF / DOCX / images, etc.

pip install scitex[io]

Built for my own research workflow.
Feedback welcome.

#Python #Research #DataScience #OpenSource


## Memo
  SAVE (37 extensions):
  | Category  | Extensions                                       |
|-----------|--------------------------------------------------|
  | Tabular   | .csv, .xlsx, .xls                                |
  | Arrays    | .npy, .npz, .hdf5, .h5, .zarr, .mat              |
  | Models    | .pth, .pt, .pkl, .pickle, .pkl.gz, .joblib, .cbm |
  | Config    | .json, .yaml, .yml                               |
  | Documents | .txt, .md, .tex, .bib, .html, .py, .css, .js     |
  | Images    | .png, .jpg, .jpeg, .gif, .tiff, .tif, .svg, .pdf |
  | Video     | .mp4                                             |
  | Bundles   | .zip (FTS)                                       |

  LOAD (45+ extensions):
  | Category  | Extensions                                                 |
|-----------|------------------------------------------------------------|
  | Tabular   | .csv, .tsv, .xlsx, .xls, .xlsm, .xlsb, .db                 |
  | Arrays    | .npy, .npz, .hdf5, .h5, .zarr, .mat, .con                  |
  | Models    | .pth, .pt, .pkl, .pickle, .gz, .joblib                     |
  | Config    | .json, .yaml, .yml, .xml                                   |
  | Documents | .txt, .tex, .log, .event, .py, .sh, .md, .docx, .pdf, .bib |
  | Images    | .png, .jpg, .tiff, .tif                                    |
  | EEG       | .vhdr, .vmrk, .edf, .bdf, .gdf, .cnt, .egi, .eeg, .set     |
  | Bundles   | .figz, .pltz, .statsz                                      |

<!-- EOF -->