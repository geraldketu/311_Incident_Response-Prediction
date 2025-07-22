# Results & Analysis

## Model Choice
- For this classification task I selected **XGBoost** for the following reasons:
   -     XGBoost is renowned for its performance on structured, tabular datasets. It handles mixed numeric and categorical (after one‑hot encoding) features exceptionally well.
  -    Its tree‑based approach naturally splits on feature thresholds, reducing sensitivity to outliers and accommodating any remaining sparsity without extensive imputation.
  -    XGBoost incorporates L1/L2 regularization to prevent overfitting, which is crucial given the moderate size (~8 000 rows) of our modeling set.
  -    Training is efficient even with hundreds of features, and feature importance scores are straightforward to extract, enabling us to diagnose and act on the main drivers of SLA delays.

## 1. Exploratory Data Analysis Recap

- **Total records:** 12 000 Baltimore 311 requests (2018–2023)  
- **Closure time distribution:**  
  - Median: 1 day  
  - 10th–90th percentile: [0 days, 5 days]  
- **SLA compliance (≤ 3 days):** 74.3% of requests  
- **Channel differences:** “Phone” requests close slightly slower than digital channels  


## 2. Model Performance

From `XGBoost_model.ipynb`, on the 20% held‑out test set:

- **Accuracy:** 0.8928  
- **ROC AUC:** 0.9564  

These outperform the 74.3% baseline (always predicting “on‑time”) and demonstrate excellent discrimination between timely and delayed requests.


## 3. Detailed Classification Report

| Class                   | Precision | Recall | F1‑score | Support |
|-------------------------|----------:|-------:|---------:|--------:|
| **0 (On‑time)**         | 0.85      | 0.77   | 0.81     | 102     |
| **1 (Delayed)**         | 0.91      | 0.94   | 0.93     | 243     |
| **accuracy**            |           |        | **0.89** | 345     |
| **macro avg**           | 0.88      | 0.86   | 0.87     | 345     |
| **weighted avg**        | 0.89      | 0.89   | 0.89     | 345     |

- **On‑time (0):**  
  - Precision 0.85: 85% of predicted on‑time were correct  
  - Recall 0.77: captured 77% of actual on‑time  
- **Delayed (1):**  
  - Precision 0.91: 91% of predicted delayed were correct  
  - Recall 0.94: captured 94% of actual delays  

High recall on delays means the model is very effective at flagging requests likely to breach SLA.


## 4. Feature Importance

Top 10 most influential features and their importance scores:

| Feature                       | Importance |
|-------------------------------|-----------:|
| `SRType_Waste Collection`     | 0.12       |
| `MethodReceived_Phone`        | 0.10       |
| `CouncilDistrict`             | 0.08       |
| `ZipCode_21213`               | 0.07       |
| `PoliceDistrict_Northeastern` | 0.06       |
| `Neighborhood_Lauraville`     | 0.05       |
| `Agency_Solid Waste`          | 0.04       |
| `Outcome_Work completed`      | 0.03       |
| `Latitude`                    | 0.03       |
| `Longitude`                   | 0.03       |

**Interpretation:**
- **Service type** (`Waste Collection`) is the strongest predictor—waste requests require specialized crews and often take longer.  
- **Channel** (`Phone`) ranks next—manual intake delays entries.  
- **Geography** (`CouncilDistrict`, `ZipCode`, `PoliceDistrict`, `Neighborhood`) collectively explain over 25% of variance, highlighting location‑based resource imbalances.  
- **Agency & outcome** features reflect departmental workflows and closure protocols.  

These insights can guide targeted process improvements, such as reallocating crews or digitizing phone requests in high-delay areas.

## 5. Business Implications

- **High delay recall (94%)** enables proactive escalation of at-risk requests.  
- **Spatial insights** allow city planners to allocate resources more evenly across neighborhoods and districts.  
- **Service‑specific delays** (e.g., waste collection) suggest prioritizing additional capacity or faster protocols for those request types.

_For full code, ROC curves, and feature‑importance visualizations, see `notebooks/XGBoost_model.ipynb`._  

_Thanks for reading you can check out the [model](https://huggingface.co/GeraldNdawula/311-xgb-model) here_
