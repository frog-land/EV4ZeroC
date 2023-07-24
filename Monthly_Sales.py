#################################################################################
# Dashboard Main page
# EV Monthly Sales in New Zealand 
# Uses  st.experimental_connection for Google Trends Results
# Developed by Paula Maddigan
#################################################################################

import pandas as pd
import numpy as np
import streamlit as st
import streamlit as st
from st_gtrends_connection import GTrendsConnection
import plotly.express as px
from app_functions import get_data,show_page_header,attr_select

###############################################################################
# Run the app
###############################################################################
try:
    # Set up the page
    show_page_header()
    # Get our data
    df_ev_only = get_data()
    ##################################################################################
    # Open a connection for Google Trends using ***** st.experimental_connection *****
    ##################################################################################
    conn = st.experimental_connection("ev_trends", type=GTrendsConnection)
    # Add the filters to the sidebar
    with st.sidebar:
        # Make and Model
        df_ev_only = attr_select("Make",":red_car: ",df_ev_only)
        df_ev_only = attr_select("Model",":blue_car: ",df_ev_only)
        # Timeframe - either month/year or a date slider
        if  st.sidebar.radio(":calendar: Filter Registration Dates By:",["Timeframe","Month & Year"],horizontal=True) == "Month & Year":
            month_year = st.sidebar.columns(2)
            with month_year[0]:
                df_ev_only =  attr_select("Year","",df_ev_only)
            with month_year[1]:
                df_ev_only = attr_select("Month","",df_ev_only)
            # Get start and end dates depending on month, year, make and model already chosen.
            reg_range_start = df_ev_only["Reg Date"].min().date()
            reg_range_end = (df_ev_only["Reg Date"].max() + pd.DateOffset(months=1) - pd.DateOffset(days=1)).date()
        else:
            # Get start and end dates for the slider depending on make and model already chosen.
            slider_start = df_ev_only["Reg Date"].min().date()
            slider_end = (df_ev_only["Reg Date"].max() + pd.DateOffset(months=1) - pd.DateOffset(days=1)).date()
            reg_range = st.slider("Month/Year Range:",format='MMM YYYY',value=(slider_start,slider_end))
            reg_range_start = reg_range[0]
            reg_range_end = reg_range[1]
            df_ev_only = df_ev_only[(df_ev_only["Reg Date"]>= reg_range_start.strftime("%d %b %Y")) & 
                                    (df_ev_only["Reg Date"]<= reg_range_end.strftime("%d %b %Y"))]
        # Keywords for Google Trends
        gtrends_all_keywords = ["EV","Nissan Leaf","Tesla","BYD","Electric Vehicle","Electric Car","Atto3","MG EV","Ioniq","Kona"]
        gtrends_select_keywords = st.multiselect("Google Trends Keywords:",gtrends_all_keywords , max_selections=5,
                                    default=["EV","Nissan Leaf","Tesla","BYD"],key = "key_keywords")

    # Draw the monthly registration plot
    fig = px.line(df_ev_only.sort_values("Reg Date"), x="Reg Date", y="Count", color='Make/Model',markers=True,
                  title="EV Monthly Registrations in New Zealand",category_orders={'Make/Model': np.sort(df_ev_only['Make/Model'].unique())})
    fig.update_yaxes(title = "Number of EVs")
    fig.update_xaxes(title = "Registration Date")
    st.plotly_chart(fig,use_container_width=True)
    # Add an expander to view the underlying data
    with st.expander(":oncoming_automobile: View Monthly Registrations Data Table"):
        cols = st.columns([4,1])
        cols[0].dataframe(df_ev_only[["Year","Month","Make","Model","Count"]],hide_index=True,use_container_width=True)

except Exception as e:
    st.error("An error has occured loading the requested EV data: " + str(e))
try:
    ###############################################################################
    # Use our Google Trends **** connector **** object to get search results
    ############################################################################### 
    # Update the end date to the end of the month
    if gtrends_select_keywords:
        trend_results = conn.query(keywords=gtrends_select_keywords,
                                from_date=reg_range_start,to_date=reg_range_end)
        # Draw the Google Trends plot
        fig = px.line(trend_results.sort_values("date"), x=trend_results.index, y=gtrends_select_keywords, markers=True,
                    title=f"Google Trends Searches in New Zealand for Keywords - {'...'.join(gtrends_select_keywords)}")
        fig.update_yaxes(title = "Relative Number of EV Searches")
        fig.update_xaxes(title = "Search Date")
        fig.update_layout(legend_title_text="Search Keyword")
        st.plotly_chart(fig,use_container_width=True)
        # Add an expander to view the underlying data
        with st.expander(":chart_with_upwards_trend: View Google Trends Data Table"):
            cols = st.columns([4,1])
            cols[0].dataframe(trend_results[gtrends_select_keywords].reset_index(),use_container_width=True,hide_index=True,
                            column_config={"date": st.column_config.DateColumn("Search Date",format="DD MMM YYYY")})
    else:
        st.info("Please select up to 5 Google Trends keywords.")
except Exception as e:
    st.error("An error has occured loading Google Trends information: " + str(e))

st.caption("Dataset courtesy NZTA (https://www.nzta.govt.nz/vehicles/how-the-motor-vehicle-register-affects-you/motor-vehicle-registrations-dashboard-and-open-data/)")
# Hide menu and footer
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)