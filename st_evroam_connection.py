#################################################################################
# Connector for NZTA EV Roam using Waka Kotahi open data portal
# Uses  st.experimental_connection to connect to the GeoJSON API Service
# https://opendata-nzta.opendata.arcgis.com/datasets/NZTA::ev-roam-charging-stations/explore?location=-39.597221%2C-6.762266%2C5.81
# Developed by Paula Maddigan
#################################################################################

from streamlit.connections import ExperimentalBaseConnection
from datetime import datetime
import pandas as pd
import numpy as np
from streamlit.runtime.caching import cache_data
import requests
import json


class EVRoamConnection(ExperimentalBaseConnection[requests.models.Response]):

    def _connect(self, **kwargs) -> requests.models.Response:
        url = self._secrets['url']
        #url="https://services.arcgis.com/CXBb7LAjgIIdcsPt/arcgis/rest/services/EV_Roam_charging_stations/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"
        response = requests.get(url)
        if response.status_code != 200:
            # NEED TO FIX
            print("Error reading URL. Status Code:", response.status_code)
        else:
            return response
    
    def cursor(self) -> requests.models.Response:
        return self._instance
    
    def query(self, ttl: int = 3600, **kwargs) -> pd.DataFrame:
        @cache_data(ttl=ttl,show_spinner="Please wait ...")
        def _query( **kwargs) -> pd.DataFrame:
            cursor = self.cursor()
            # API loaded successfully
            result = json.loads(cursor.content)

            # Convert results into a dataframe
            df_stations = pd.DataFrame.from_dict(result["features"])
            # Remove unnecessary columns
            df_stations = df_stations.drop(columns=["type","id","geometry"])
            # The properties column contains a dictionary of values so expand this into columns
            df_stations = pd.concat([df_stations, pd.DataFrame(df_stations['properties'].tolist())], axis=1)
            # Create a dataframe of the columns we want
            df_stations = df_stations[['name', 'operator', 'owner', 'address',
            'is24Hours', 'carParkCount', 'hasCarparkCost', 'maxTimeLimit',
                'currentType',
                'numberOfConnectors', 'connectorsList',
            'hasChargingCost',"latitude","longitude"]]
            # The connectors list is a string but really it is a list so split it up
            df_stations['connectorsList'] = df_stations['connectorsList'].str.split("},{")
            return df_stations
        return _query( **kwargs)
    
