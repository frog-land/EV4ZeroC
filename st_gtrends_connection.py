#################################################################################
# Connector for Google Trends using pytrends
# Uses  st.experimental_connection for Google Trends Results
# Developed by Paula Maddigan
#################################################################################

from streamlit.connections import ExperimentalBaseConnection
from pytrends.request import TrendReq
from datetime import datetime
import pandas as pd
import numpy as np
from streamlit.runtime.caching import cache_data

class GTrendsConnection(ExperimentalBaseConnection[TrendReq]):

    def _connect(self, **kwargs) -> TrendReq:
        if 'geo' in kwargs:
            self.geo = kwargs.pop('geo')
        else:
            self.geo = self._secrets['geo']
        return TrendReq()
    
    def cursor(self) -> TrendReq:
        return self._instance
    
    def query(self, keywords: list, from_date: datetime, to_date: datetime, ttl: int = 3600, **kwargs) -> pd.DataFrame:
        @cache_data(ttl=ttl,show_spinner="Please wait ...")
        def _query(keywords: list, from_date: datetime, to_date: datetime, **kwargs) -> pd.DataFrame:
            cursor = self.cursor()
            cursor.build_payload(kw_list=keywords, geo=self.geo, timeframe=from_date.strftime("%Y-%m-%d") + " " + to_date.strftime("%Y-%m-%d"))
            df = cursor.interest_over_time()
            return df
        return _query(keywords,from_date, to_date, **kwargs)
    
