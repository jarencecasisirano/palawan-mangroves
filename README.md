# Mangrove Change and Biogeographical Drivers in Palawan

This project analyzes the spatial and temporal dynamics of mangrove cover change in Palawan, Philippines (1996–2020), and investigates the environmental and anthropogenic factors influencing mangrove loss using regression and spatial modeling techniques.

---

## 🔍 Objectives

1. **Map and quantify** spatial and temporal patterns of mangrove cover change using Global Mangrove Watch data (1996, 2010, 2015, 2020).
2. **Analyze** the relationship between mangrove change and drivers using Ordinary Least Squares (OLS) logistic regression.
3. **Evaluate** the spatial variability of driver influence using Geographically Weighted Regression (GWR).

---

## 📂 Folder Structure

```
data/
├── mosaics/                # Mangrove rasters (yearly mosaics)
├── mangroves_filtered/     # Tiles clipped to Palawan
├── processed_rasters/      # Preprocessed explanatory rasters
├── csv/                    # Extracted regression datasets
├── stats/                  # Summary stats, regression results
├── gwr_outputs/            # GWR coefficient GeoJSONs
├── admin_boundaries/       # Municipal boundaries
```

---

## 🧭 Methodological Workflow

```mermaid
flowchart TD

%% Input Sources
A1[Download GMW Mangrove Rasters]
A2[Download Environmental Rasters: CHIRPS, MODIS LST, SRTM]

%% Mangrove Processing
A1 --> B1[Prepare Mangrove Tiles: Clip and Mosaic]
B1 --> C1[Perform Change Detection: 1996–2010, 2010–2015, 2015–2020]
C1 --> D1[Compute Gain, Loss, No Change]

%% Environmental Data Prep
A2 --> B2[Preprocess Rasters: Clip, Align, Reproject]
B2 --> C2[Match Raster Years to Change Intervals]

%% Alignment and Sampling
D1 --> E1[Generate Centroid Points from Change Pixels]
C2 --> E2[Extract Predictor Values at Centroids]
E1 --> F1[Save Combined Dataset to CSV]
E2 --> F1

%% Visualization
E1 --> V1[Visualize Heatmaps in QGIS using Symbology Renderer]

%% Logistic Regression Path
F1 --> R1[Run Logistic Regression per Interval]
R1 --> R2[Summarize Logistic Coefficients]
R2 --> R3[Check Multicollinearity using VIF]
R3 --> R4[Evaluate Logistic Model Fit using R2 AIC LLF]

%% GWR Path
F1 --> GWR1[Run GWR per Interval using 6000 meter Bandwidth]
GWR1 --> GWR2[Generate Spatial Coefficient Maps]
GWR2 --> GWR3[Summarize Spatial Trends and Variable Importance]
GWR3 --> GWR4[Evaluate GWR Fit using Local R2 AIC LLF]
```

---

## 📦 Key Tools and Libraries

- `rasterio`, `numpy`, `geopandas` for spatial preprocessing
- `statsmodels` for logistic regression
- `mgwr` for spatial modeling (GWR)
- `QGIS` for heatmap visualization
- Data sources: Global Mangrove Watch, CHIRPS, MODIS LST, GPW v4, ESA CCI, SRTM

---

## 🗺️ Outputs

- Change maps and centroids for mangrove loss/gain
- Municipality-level loss/gain statistics
- Predictor-prepared CSVs (2010, 2015, 2020)
- OLS regression summaries and importance rankings
- GWR coefficient maps and model evaluations
