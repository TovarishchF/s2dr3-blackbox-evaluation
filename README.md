# S2DR3 Black‑Box Evaluation

**No‑reference, black‑box quality assessment** of the S2DR3 super‑resolution model for Sentinel‑2.  
The model is treated as a black box – no access to architecture, weights, or training data – and evaluated solely through its outputs.

## Key idea
- **Wald protocol**: downscale the super‑resolved image to the original 10 m resolution and compare it with the real Sentinel‑2 L2A reference.
- **Quantitative metrics**:
  - Spectral: RMSE, bias, SAM (Spectral Angle Mapper), ERGAS, per‑band and overall correlation (*r*).
  - Spatial: GLCM contrast, edge density (Canny).
  - Frequency: radial power spectrum, spectral ratio, difference plots.
- **Visualisation**: bias maps (absolute and relative), SAM map, per‑band bar charts, spectral profiles for selected land‑cover classes.
- **Classification** (optional, not detailed in this update): Random Forest with manual ground truth (OA, F1, IoU).

## Why black‑box?
- Simulates a real‑world scenario where only the API or output files are available.
- Guarantees an independent, reproducible evaluation without internal knowledge of the algorithm.
- The methodology can be applied to any super‑resolution service.

## Repository structure

s2dr4-blackbox-evaluation/  
├── main.py # Main entry point  
├── src/ # Reusable modules  
│ ├── preprocess.py # Load rasters, downscale (Wald protocol)  
│ ├── spectral_metrics.py # RMSE, Bias, SAM (pixel‑wise + maps)  
│ ├── spatial_metrics.py # GLCM contrast, edge density  
│ ├── freq_metrics.py # FFT, radial power spectrum  
│ ├── classification.py # Random Forest, OA, F1, IoU  
│ └── utils.py # Visualisation helpers, config  
├── data/ # (ignored) – original S2, S2DR4 outputs, ground truth  
├── results/ # (auto‑created) – tables, plots, maps  
├── config.yaml # Configuration file containing paths, etc.  
├── requirements.txt  
├── LICENSE  
└── .gitignore  

## All implemented no‑reference metrics

| Category    | Metric                                | Module            |
|-------------|---------------------------------------|-------------------|
| Spectral    | RMSE (total + per band)               | `spectral_metrics` |
| Spectral    | SAM (mean + map)                      | `spectral_metrics` |
| Spectral    | Bias (mean radiometric shift + maps)  | `spectral_metrics` |
| Spectral    | ERGAS                                 | `spectral_metrics` |
| Spectral    | Per‑band & overall Pearson correlation | `spectral_metrics` |
| Spatial     | GLCM contrast                         | `spatial_metrics`  |
| Spatial     | Edge density (Canny)                  | `spatial_metrics`  |
| Frequency   | Radial power spectrum, slopes         | `freq_metrics`     |
| Visual      | Spectral profiles per land‑cover class | `utils`            |
| Classification | Overall Accuracy, F1, IoU           | `classification`   |  

All spectral and spatial metrics are computed **after downscaling the S2DR3 output to 10 m** (Wald protocol).

## Usage
1. **Clone repository**  
   ```bash
   git clone https://github.com/yourusername/s2dr3-blackbox-evaluation.git
   cd s2dr3-blackbox-evaluation
   ```
2. Install dependencies
    ```bash
   pip install -r requirements.txt
   ```
3. **Prepare data** (see `data/` folder structure)  
   - Place original Sentinel‑2 L2A crops (GeoTIFF, 10 m) into `data/s2_10m/`  
   - Place S2DR3 outputs (1 m) into `data/s2sr_1m/`  
   - (Optional) Place ground‑truth shapefiles for classification into `data/ground_truth/`

4. **Run the evaluation**  
   Open `main.ipynb` in Jupyter / VS Code / Colab and execute cells.  
   The notebook will:
   - Load each polygon
   - Downscale S2DR3 to 10 m
   - Compute all metrics
   - Run Random Forest classification (if ground truth available)
   - Save results to `results/`

## Data sources

- **Sentinel‑2 L2A** – [Copernicus Open Access Hub](https://scihub.copernicus.eu/)  
- **S2DR3** – public Colab notebook by Gamma Earth  
  ([Medium article](https://medium.com/@ya_71389/c71a601a2253))

## Citation 

If you use this module in your work, please cite the original author:  
> Yosef Akhtman, S2DR3: Effective 12-Band 10x Single Image Super-Resolution for Sentinel-2, October 2, 2023. https://medium.com/@yakhtman/s2dr3


## License

Code in this repository is released under the **Apache 2.0**.  
Data (Sentinel‑2, S2DR3 outputs, ground truth) are subject to their own licenses.