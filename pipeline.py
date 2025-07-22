import requests
import pandas as pd

urls={
    2018:"https://services1.arcgis.com/UWYHeuuJISiGmgXx/ArcGIS/rest/services/311_Customer_Service_Requests_Yearly/FeatureServer/4/query",
    2019:"https://services1.arcgis.com/UWYHeuuJISiGmgXx/ArcGIS/rest/services/311_Customer_Service_Requests_Yearly/FeatureServer/3/query",
    2020:"https://services1.arcgis.com/UWYHeuuJISiGmgXx/ArcGIS/rest/services/311_Customer_Service_Requests_Yearly/FeatureServer/2/query",
    2021:"https://services1.arcgis.com/UWYHeuuJISiGmgXx/ArcGIS/rest/services/311_Customer_Service_Requests_Yearly/FeatureServer/1/query",
    2022:"https://services1.arcgis.com/UWYHeuuJISiGmgXx/ArcGIS/rest/services/311_Customer_Service_Requests_Yearly/FeatureServer/0/query",
    2023:"https://services1.arcgis.com/UWYHeuuJISiGmgXx/arcgis/rest/services/311_Customer_Service_Requests_2023/FeatureServer/0/query"
}



params = {
    "where": "1=1",               # fetch all rows
    "outFields": "*",             # all fields
    "f": "geojson"              # format as GeoJSON
}

def api_request(url):
    '''
    Makes an api request using the end point and returns a dataframe
    '''
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        records = [feature["properties"] for feature in data["features"]]
        return pd.DataFrame(records)
    else:
        print("Failed to retrieve data:", response.status_code)
        return

data_frames=[api_request(x) for x in urls.values()]


# data_frames[0].info()
data_frames[0].columns.values.tolist()== data_frames[1].columns.values.tolist()

#Checking to see if all dataframes have the same columns
col_bool=True
for i in range(len(data_frames)-2):
    col_bool = col_bool and (data_frames[i].columns.values.tolist() == data_frames[i+1].columns.values.tolist())
print(col_bool)



df=pd.concat(data_frames)

df.to_csv("311 Response Data (2018-2023).csv")