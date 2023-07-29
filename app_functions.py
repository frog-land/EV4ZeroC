#################################################################################
# Dashboard functions
# Developed by Paula Maddigan
#################################################################################


import pandas as pd
#import numpy as np
import streamlit as st
import calendar
import streamlit as st
from streamlit.runtime.caching import cache_data
from st_gtrends_connection import GTrendsConnection
from st_evroam_connection import EVRoamConnection

###############################################################################
# Define some functions
###############################################################################
def show_page_header():
    # Write the page header so its the same on each page
    st.set_page_config(page_icon="ev4zeroc.png",layout="wide",page_title="EV4ZeroC")
    st.markdown("<h1 style='text-align: center; font-weight:bold; font-family:comic sans ms; padding-top: 0rem;'>EV4ZeroC</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;padding-top: 0rem;'>Electric Vehicles in New Zealand </h2>", unsafe_allow_html=True)
    st.sidebar.caption("Developed by Paula Maddigan",help="i.build.apps.4.u@gmail.com")

def get_data():
    # If the data is already in the session state then return it, else load it from file
    if "data" in st.session_state:
        return st.session_state["data"]
    filename = "EV_Sales.csv"
    df_evs = pd.read_csv(filename)#
    df_evs["Year"] = df_evs["Year"].astype(str)
    df_evs["Make"] = df_evs["Make"].fillna("")
    df_evs["Model"] = df_evs["Model"].fillna("")
    df_evs["Make/Model"] = df_evs["Make"] + "/" + df_evs["Model"]
    df_evs["Reg Date"] = pd.to_datetime(df_evs["Reg Date"],format="%Y-%m-%d")
    st.session_state["data"] = df_evs
    #st.toast("Welcome to my Streamlit Connections Hackathon Entry!",icon="🇳🇿")
    return df_evs

def initialise_conns():
    ##################################################################################
    # Use our st.experimental_connection objects and put in session_state so we can 
    # use on every page if we wish without creating a new one every time
    # Open a connection for Google Trends using ***** st.experimental_connection *****
    # Open a connection for EV Roam using ***** st.experimental_connection *****
    ##################################################################################
    if "gt_conn" not in st.session_state:
        st.session_state["gt_conn"] = st.experimental_connection("ev_trends", type=GTrendsConnection)
    if "ev_conn" not in st.session_state:
        st.session_state["ev_conn"] = st.experimental_connection("ev_roam", type=EVRoamConnection)


def attr_select(attr,icon,df):
    # Adds a multiselect widget and returns the filtered dataset
    attr_list = df[attr].drop_duplicates()
    if attr =="Month":
        attr_list = sorted(attr_list, key=month_dict.get)
    else:
        attr_list = attr_list.sort_values()
    the_attr = st.multiselect(icon + attr + ":", attr_list,key = "key_"+attr)
    if len(the_attr) == 0:
        return df
    df = df[df[attr].isin(the_attr)]
    return df

# A month dictionary so we can display the months in the custom calendar order not alphabetical order
month_dict = {}
for i in range(1, 13): 
    month = calendar.month_abbr[i] 
    month_dict[month] = i  
