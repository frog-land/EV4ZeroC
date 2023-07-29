#################################################################################
# Dashboard additional page 
# Yearly EV Sales in New Zealand 
# Developed by Paula Maddigan
#################################################################################

import pandas as pd
import numpy as np
import streamlit as st
import streamlit as st
import plotly.express as px
from app_functions import get_data,show_page_header

try:
    # Set up the page
    show_page_header()
    # Get our data
    df_ev_only = get_data()
    # Filter by year and plot
    ev_by_year = st.session_state["data"].groupby(["Year","Make/Model"]).sum().reset_index().sort_values(["Year","Count"],ascending=[True,False])
    for year_loop in np.flip(ev_by_year["Year"].unique()):
        fig = px.bar(ev_by_year[ev_by_year["Year"]==year_loop].head(10), x="Make/Model", y="Count",
                    title="EV Yearly Registrations in New Zealand for the Top 10 Make/Models in " + year_loop,color='Make/Model',text_auto=True,
                     color_discrete_sequence=px.colors.sequential.Viridis )
        fig.update_layout(bargap=.5) 
        st.plotly_chart(fig,use_container_width=True)
except Exception as e:
    # Something has gone wrong
    st.error("An error has occured loading this page: " + str(e))

st.caption("Dataset courtesy of NZTA (https://www.nzta.govt.nz/vehicles/how-the-motor-vehicle-register-affects-you/motor-vehicle-registrations-dashboard-and-open-data/)")

# Hide menu and footer
hide_streamlit_style = "<style>footer {visibility: hidden;}</style>"
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
