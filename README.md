
# Baltimore 311 Incident Response Prediction
## Overview
City governments strive to resolve 311 service requests within a three‑day service‑level agreement (SLA). This project builds a pipeline to:  
1. **Retrieve** Baltimore 311 data (2018–2023) via ArcGIS API  
2. **Clean & engineer** features (timestamps, geolocation, request metadata)  
3. **Explore** patterns in request volume, closure times, and SLA compliance  
4. **Model** whether a request closes within three days using XGBoost  

***TL;DR*** Here's the [model](https://huggingface.co/GeraldNdawula/311-xgb-model)

## Key Questions  
- What percent of requests meet the 3‑day SLA?  
- Which factors (request type, location, district, channel) most influence timely closure?  
- How well can we predict delayed requests to proactively allocate resources?

## Dataset  
- **Raw data**: 12,000 311 requests (2018–2023) with fields like `SRType`, `MethodReceived`, `CouncilDistrict`, geolocation, and timestamps.  
- **Target**:  
  ```text
  Target = 1 if (CloseDate – CreatedDate) ≤ 3 days, else 0
Final modeling set: ~8,000 rows after dropping “Unknown” and encoding categoricals.

## Folder Structure
```text
.
├── pipeline.py                # Production ready script to fetch 2018–2023 data via ArcGIS API
├── data_processing.py         # Produection ready script to clean dates, compute  target, one‑hot encode
├── Modeling_ready_dataset.csv # Final features + Target
├── XGBoost_model.ipynb    # Train/test split, XGBoost, evaluation, importances
├── notebooks/
│   ├── eda.ipynb   # initial exploratory data analysis
|   └── dataset_retrieval.ipynb # initial dataset rerieval
├── README.md                  # Project overview (this file)
├── methods.md                 # Detailed data retrieval & cleaning
└── analysis.md                # In‑depth EDA & modeling results
```
## Requirements
Python 3.8+
`requests`, `pandas`, `numpy`, `scikit-learn`, `xgboost`, `matplotlib`

Install via:
```bash

pip install requests pandas numpy scikit-learn xgboost matplotlib seaborn
```
## Process
```bash
# Step 1: Fetch data
python pipeline.py

# Step 2: Clean & featurize
python data_processing.py

# Step 3: Explore & model
jupyter lab notebooks/eda.ipynb notebooks/XGBoost_model.ipynb

```
