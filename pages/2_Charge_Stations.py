#################################################################################
# Dashboard additional page 
# List and map of EV charging stations throughout NZ
# Uses  st.experimental_connection for NZTA EV Roam API
# Developed by Paula Maddigan
#################################################################################

import streamlit as st
from app_functions import get_data,show_page_header,initialise_conns
import plotly.express as px

try:
    # Set up the page
    show_page_header()
    # Get our data
    df_ev_only = get_data()
    ###############################################################################
    # Initialise our connection objects if they haven't already been initialised
    ############################################################################### 
    initialise_conns()

    ###############################################################################
    # Use our EV Roam **** connector **** object to get search results
    ############################################################################### 
    df_stations = st.session_state["ev_conn"].query()
    # Make the column names nice
    df_stations = df_stations.rename(columns={"name":"Name","address":"Address",
                "currentType":"Current Type","numberOfConnectors":"Connectors",
                "connectorsList":"Connector Details","hasChargingCost":"Charging Cost",
                "is24Hours":"24Hours","maxTimeLimit":"Time Limit", 
                "carParkCount":"Car Parks", "hasCarparkCost":"Carpark Cost", 
                "operator":"Operator", "owner":"Owner"})

    st.subheader(":battery: EV Charge Stations")

    # Format the hover data
    df_stations["Connector Info"] = df_stations["Current Type"] + " x " + df_stations["Connectors"].astype(str)
    hover_dict = {"Address":True,"Current Type":False,"Connector Info":True, 
                  "latitude":False,"longitude":False}
    
    # Draw the map using plotly express
    fig = px.scatter_mapbox(df_stations, lat="latitude", lon="longitude", zoom=4,\
                            color="Current Type",hover_name="Name",hover_data=hover_dict,)
    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig,use_container_width=True)

    # Put the data table within an expander
    with st.expander(":electric_plug: View Charge Stations Data Table"):
        # Order the columns how we want
        column_order = ["Name", "Address","Current Type","Connectors", "Connector Details",
                "Charging Cost","24Hours","Time Limit", "Car Parks", "Carpark Cost", "Operator", "Owner"]
        # Configure checkboxes for the booleans
        column_config={"Charging Cost": st.column_config.CheckboxColumn("Charging Cost?"),
                    "Carpark Cost": st.column_config.CheckboxColumn("Carpark Cost?"),
                    "24Hours": st.column_config.CheckboxColumn("24 Hours?")}
        # Draw the dataframe
        st.dataframe(df_stations,hide_index=True,column_config=column_config,use_container_width=True,column_order=column_order)

except Exception as e:
    # Something has gone wrong
    st.error("An error has occured loading this page: " + str(e))

# Give credit to the datasource
st.caption("Data courtesy of NZTA EV Roam API: https://opendata-nzta.opendata.arcgis.com/datasets/NZTA::ev-roam-charging-stations/api")

# Hide menu and footer
hide_streamlit_style = "<style>footer {visibility: hidden;}</style>"
st.markdown(hide_streamlit_style, unsafe_allow_html=True)