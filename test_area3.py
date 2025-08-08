import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# ─────────────────────────────────────────────────────────────
# Load data
emissions_df = pd.read_csv("Emissions_Data.csv")
nsw_temp_df = pd.read_csv("Average NSW temperatures.csv")
wa_temp_df = pd.read_csv("Average WA temperatures.csv")
vic_temp_df = pd.read_csv("Average VIC temperatures.csv")
qld_temp_df = pd.read_csv("Average QLD temperatures.csv")

# ─────────────────────────────────────────────────────────────
# Prepare NSW data
nsw_emissions = emissions_df[emissions_df['Location'] == 'NSW'].rename(columns={'Total (MT)': 'NSW Emissions'})
nsw_temp_df = nsw_temp_df.rename(columns={'Average Temperature (NSW)': 'NSW Temperature'})
nsw_df = pd.merge(nsw_emissions, nsw_temp_df, on='Year')

# ─────────────────────────────────────────────────────────────
# Prepare WA data
wa_emissions = emissions_df[emissions_df['Location'] == 'WA'].rename(columns={'Total (MT)': 'WA Emissions'})
wa_temp_df = wa_temp_df.rename(columns={'Average Temperature (WA)': 'WA Temperature'})
wa_df = pd.merge(wa_emissions, wa_temp_df, on='Year')

# ─────────────────────────────────────────────────────────────
# Prepare VIC data with safe renaming
vic_emissions = emissions_df[emissions_df['Location'] == 'VIC'].rename(columns={'Total (MT)': 'VIC Emissions'})
for col in vic_temp_df.columns:
    if 'Temperature' in col and 'VIC' in col:
        vic_temp_df = vic_temp_df.rename(columns={col: 'VIC Temperature'})
        break
vic_df = pd.merge(vic_emissions, vic_temp_df, on='Year')

# ─────────────────────────────────────────────────────────────
# Prepare QLD data with safe renaming
qld_emissions = emissions_df[emissions_df['Location'] == 'QLD'].rename(columns={'Total (MT)': 'QLD Emissions'})
for col in qld_temp_df.columns:
    if 'Temperature' in col and 'QLD' in col:
        qld_temp_df = qld_temp_df.rename(columns={col: 'QLD Temperature'})
        break
qld_df = pd.merge(qld_emissions, qld_temp_df, on='Year')

# ─────────────────────────────────────────────────────────────
# Page selector
page = st.sidebar.radio("Select State", ["NSW", "WA", "VIC", "QLD"])

# ─────────────────────────────────────────────────────────────
# NSW Page
if page == "NSW":
    st.header("NSW Climate Data")
    st.info("This page shows climate data for New South Wales. Use the sidebar to toggle emissions and temperature views.")

    st.sidebar.subheader("NSW Options")
    show_nsw_emissions = st.sidebar.checkbox("Show NSW Emissions")
    show_nsw_temperature = st.sidebar.checkbox("Show NSW Temperature")

    selected_columns = ['Year']
    if show_nsw_emissions:
        selected_columns.append('NSW Emissions')
    if show_nsw_temperature:
        selected_columns.append('NSW Temperature')

    st.subheader("NSW Data Table")
    st.dataframe(nsw_df[selected_columns])

    if show_nsw_emissions or show_nsw_temperature:
        fig, ax1 = plt.subplots(figsize=(10, 6))
        ax1.set_xlabel('Year')

        if show_nsw_emissions:
            ax1.set_ylabel('NSW Emissions (Mt CO₂e)', color='red')
            ax1.plot(nsw_df['Year'], nsw_df['NSW Emissions'], color='red', label='NSW Emissions')
            ax1.tick_params(axis='y', labelcolor='red')

        if show_nsw_temperature:
            ax2 = ax1.twinx()
            ax2.set_ylabel('NSW Avg Temperature (°C)', color='blue')
            ax2.plot(nsw_df['Year'], nsw_df['NSW Temperature'], color='blue', label='NSW Temperature')
            ax2.tick_params(axis='y', labelcolor='blue')

        plt.title('NSW Emissions vs Temperature Over Time')
        fig.tight_layout()
        st.pyplot(fig)

# ─────────────────────────────────────────────────────────────
# WA Page
elif page == "WA":
    st.header("WA Climate Data")
    st.info("This page shows climate data for Western Australia. Use the sidebar to toggle emissions and temperature views.")

    st.sidebar.subheader("WA Options")
    show_wa_emissions = st.sidebar.checkbox("Show WA Emissions")
    show_wa_temperature = st.sidebar.checkbox("Show WA Temperature")

    wa_columns = ['Year']
    if show_wa_emissions:
        wa_columns.append('WA Emissions')
    if show_wa_temperature:
        wa_columns.append('WA Temperature')

    st.subheader("WA Data Table")
    st.dataframe(wa_df[wa_columns])

    if show_wa_emissions or show_wa_temperature:
        fig, ax1 = plt.subplots(figsize=(10, 6))
        ax1.set_xlabel('Year')

        if show_wa_emissions:
            ax1.set_ylabel('WA Emissions (Mt CO₂e)', color='orange')
            ax1.plot(wa_df['Year'], wa_df['WA Emissions'], color='orange', label='WA Emissions')
            ax1.tick_params(axis='y', labelcolor='orange')

        if show_wa_temperature:
            ax2 = ax1.twinx()
            ax2.set_ylabel('WA Avg Temperature (°C)', color='green')
            ax2.plot(wa_df['Year'], wa_df['WA Temperature'], color='green', label='WA Temperature')
            ax2.tick_params(axis='y', labelcolor='green')

        plt.title('WA Emissions vs Temperature Over Time')
        fig.tight_layout()
        st.pyplot(fig)

# ─────────────────────────────────────────────────────────────
# VIC Page
elif page == "VIC":
    st.header("VIC Climate Data")
    st.info("This page shows climate data for Victoria. Use the sidebar to toggle emissions and temperature views.")

    st.sidebar.subheader("VIC Options")
    show_vic_emissions = st.sidebar.checkbox("Show VIC Emissions")
    show_vic_temperature = st.sidebar.checkbox("Show VIC Temperature")

    vic_columns = ['Year']
    if show_vic_emissions:
        vic_columns.append('VIC Emissions')
    if show_vic_temperature:
        vic_columns.append('VIC Temperature')

    st.subheader("VIC Data Table")
    st.dataframe(vic_df[vic_columns])

    if show_vic_emissions or show_vic_temperature:
        fig, ax1 = plt.subplots(figsize=(10, 6))
        ax1.set_xlabel('Year')

        if show_vic_emissions:
            ax1.set_ylabel('VIC Emissions (Mt CO₂e)', color='purple')
            ax1.plot(vic_df['Year'], vic_df['VIC Emissions'], color='purple', label='VIC Emissions')
            ax1.tick_params(axis='y', labelcolor='purple')

        if show_vic_temperature:
            ax2 = ax1.twinx()
            ax2.set_ylabel('VIC Avg Temperature (°C)', color='brown')
            ax2.plot(vic_df['Year'], vic_df['VIC Temperature'], color='brown', label='VIC Temperature')
            ax2.tick_params(axis='y', labelcolor='brown')

        plt.title('VIC Emissions vs Temperature Over Time')
        fig.tight_layout()
        st.pyplot(fig)

# ─────────────────────────────────────────────────────────────
# QLD Page
elif page == "QLD":
    st.header("QLD Climate Data")
    st.info("This page shows climate data for Queensland. Use the sidebar to toggle emissions and temperature views.")

    st.sidebar.subheader("QLD Options")
    show_qld_emissions = st.sidebar.checkbox("Show QLD Emissions")
    show_qld_temperature = st.sidebar.checkbox("Show QLD Temperature")

    qld_columns = ['Year']
    if show_qld_emissions:
        qld_columns.append('QLD Emissions')
    if show_qld_temperature:
        qld_columns.append('QLD Temperature')

    st.subheader("QLD Data Table")
    st.dataframe(qld_df[qld_columns])

    if show_qld_emissions or show_qld_temperature:
        fig, ax1 = plt.subplots(figsize=(10, 6))
        ax1.set_xlabel('Year')

        if show_qld_emissions:
            ax1.set_ylabel('QLD Emissions (Mt CO₂e)', color='darkred')
            ax1.plot(qld_df['Year'], qld_df['QLD Emissions'], color='darkred', label='QLD Emissions')
            ax1.tick_params(axis='y', labelcolor='darkred')

        if show_qld_temperature:
            ax2 = ax1.twinx()
            ax2.set_ylabel('QLD Avg Temperature (°C)', color='teal')
            ax2.plot(qld_df['Year'], qld_df['QLD Temperature'], color='teal', label='QLD Temperature')
            ax2.tick_params(axis='y', labelcolor='teal')

        plt.title('QLD Emissions vs Temperature Over Time')
        fig.tight_layout()
        st.pyplot(fig)