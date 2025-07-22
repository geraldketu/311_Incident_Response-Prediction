# Methods & Pipeline
## 1. Data Retrieval (pipeline.py)
-API endpoints (2018–2023) from Baltimore’s ArcGIS 311 service.
-Query: `where=1=1`, `outFields=*`, `f=geojson`.
-Schema consistency: Confirmed all yearly endpoints share identical fields.
-Concatenate GeoJSON → Pandas → save `311 Response Data (2018-2023).csv.`
```python
# Example endpoint fetch
import requests, pandas as pd

url = urls[2021]
resp = requests.get(url, params={"where":"1=1","outFields":"*","f":"geojson"})
df21 = pd.DataFrame([f["properties"] for f in resp.json()["features"]])
```
## 2. Data Cleaning & Feature Engineering (data_processing.py)
### 1 Load raw CSV, drop index column.
### 2 Convert timestamps (ms since epoch → `datetime`):
```python
df['CreatedDate'] = pd.to_datetime(df['CreatedDate'], unit='ms')
df['CloseDate']   = pd.to_datetime(df['CloseDate'], unit='ms')
```
### 3 Compute closure time
```python
df['ReqLengthOpen'] = (df['CloseDate'] - df['CreatedDate']).dt.days
df['Target'] = (df['ReqLengthOpen'] <= 3).astype(int)
```
### 4 Select features
- Drop identifiers & raw dates
- Keep `RowID`, `CouncilDistrict`, `Latitude`, `Longitude`, `Target`

### 5 Encoding Categoricals
- One‑Hot Encode remaining categoricals (`SRType`, `MethodReceived`, `SRStatus`, `Agency`, `Outcome`, `ZipCode`, `Neighborhood`, `PoliceDistrict`, `PolicePost`)

### 6 Final Dataset formatting 
- Concatenate numeric + encoded features → Modeling_ready_dataset.csv

#### Key rationale:
- SLA target is binary for easy classification.
- One‑hot encoding preserves nominal categories without ordinality.
- Geographic coords and district may capture locational effects.

## 3. Exploratory Data Analysis (eda.ipynb)
- Volume by year: consistent $~2,000$ requests/year
- Closure time distribution: heavy right skew; `median $= 1$ day
- SLA compliance: $~74.3%$ closed $≤3$ days
- Channel impact: requests via `Phone` slightly slower than `API`

## 4. Modeling with XGBoost (notebooks/XGBoost_model.ipynb)
- Train/test split: 80/20, `random_state=42`
- Model:
```python

model = xgb.XGBClassifier(
    use_label_encoder=False,
    eval_metric='logloss',
    random_state=42
)
model.fit(X_train, y_train)
```
- Evaluation:
 ```
python
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report
y_pred      = model.predict(X_test)
y_proba     = model.predict_proba(X_test)[:,1]
acc   = accuracy_score(y_test, y_pred)
auc   = roc_auc_score(y_test, y_proba)
report = classification_report(y_test, y_pred)
```
- Feature importances: Top 20 features plotted via `model.feature_importances_.`

- Hyperparameter rationale: default XGBoost settings are robust for tabular data; future work will include tuning via `GridSearchCV`.
