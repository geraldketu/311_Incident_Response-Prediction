import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_selection import chi2
from sklearn.preprocessing import OneHotEncoder

df=pd.read_csv('311 Response Data (2018-2023).csv')
df.drop('Unnamed: 0',axis=1, inplace=True)

df['StatusDate'] = pd.to_datetime(df['StatusDate'], unit='ms')
df['DueDate'] = pd.to_datetime(df['DueDate'], unit='ms')
df['CloseDate'] = pd.to_datetime(df['CloseDate'], unit='ms')
df['LastActivityDate'] = pd.to_datetime(df['LastActivityDate'], unit='ms')
df['CreatedDate'] = pd.to_datetime(df['CreatedDate'], unit='ms')
df['GeoLocation'].value_counts()
df['ReqLengthOpen'] = df['CloseDate'] - df['CreatedDate']
df['ReqLengthOpen'] = df['ReqLengthOpen'].dt.days
df['Target'] = (df['ReqLengthOpen']<=3).astype(int)

to_drop=['SRRecordID','ServiceRequestNum','CreatedDate','StatusDate','DueDate','CloseDate','GeoLocation','ReqLengthOpen','LastActivityDate'  ]
df2 = df.drop(columns=to_drop)

categorical_columns = df2.select_dtypes(include=['object']).columns.tolist()
encoder = OneHotEncoder(sparse_output=False, drop='first', handle_unknown='ignore')
encoded_categoricals = encoder.fit_transform(df2[categorical_columns])
feature_names = encoder.get_feature_names_out(categorical_columns)
df_encoded_cat = pd.DataFrame(encoded_categoricals, 
                                columns=feature_names, 
                                index=df2.index)

numerical_columns = ['RowID', 'CouncilDistrict', 'Latitude', 'Longitude', 'Target']
df_final = pd.concat([df2[numerical_columns], df_encoded_cat], axis=1)
df_final.to_csv("Modeling_ready_dataset.csv")

