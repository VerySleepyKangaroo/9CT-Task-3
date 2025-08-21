import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import time


# Copy and Paste this into the terminal:

# streamlit run UI.py

# Also make sure that you have streamlit installed.

VALID_USERS = {
    "Pranav": "123",
    "MrGroom": "123"
}

def show_login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("Sign in to Access Data")
        st.caption("Access is restricted. Enter your username and passcode to continue.")

        username = st.text_input("Username")
        pwd = st.text_input("Passcode", type="password")
        login_clicked = st.button("Sign in", use_container_width=True)

        if login_clicked:
            if username in VALID_USERS and pwd == VALID_USERS[username]:
                with st.spinner("Checking Login Details..."):
                    time.sleep(3)
                st.session_state.logged_in = True
                with st.spinner("Logging In..."):
                    time.sleep(1.5)
                st.session_state.username = username
                st.rerun()
            else:
                with st.spinner("Checking Login Details..."):
                    time.sleep(3)
                st.error("Incorrect username or passcode. Please try again.")

        st.stop()

show_login()

if "username" in st.session_state:
    st.success(f"Welcome, {st.session_state.username}!")

# 1) Gate the app
show_login()


@st.cache_data # My code either took too long to load or just would not load so I had to search up how to solve the problem and I found that "cache_data" can help increase the loading speed.
def load_data():
    emissions = pd.read_csv("Emissions_Data.csv")
    nsw_temp = pd.read_csv("Average NSW temperatures.csv")
    wa_temp = pd.read_csv("Average WA temperatures.csv")
    vic_temp = pd.read_csv("Average VIC temperatures.csv")
    qld_temp = pd.read_csv("Average QLD temperatures.csv")
    act_temp = pd.read_csv("Average ACT temperatures.csv")
    sa_temp = pd.read_csv("Average SA temperatures.csv")
    nt_temp = pd.read_csv("Average NT temperatures.csv")
    return emissions, nsw_temp, wa_temp, vic_temp, qld_temp, act_temp, sa_temp, nt_temp


# Everything Below is me just setting up the data for the actual app


# Load all at once
emissions_df, nsw_temp_df, wa_temp_df, vic_temp_df, qld_temp_df, act_temp_df, sa_temp_df, nt_temp_df = load_data()

# -------------------------------------------------------------
# Prepare NSW data
nsw_emissions = emissions_df[emissions_df['Location'] == 'NSW'].rename(columns={'Total (MT)': 'NSW Emissions'})
nsw_temp_df = nsw_temp_df.rename(columns={'Average Temperature (NSW)': 'NSW Temperature'})
nsw_df = pd.merge(nsw_emissions, nsw_temp_df, on='Year')

# -------------------------------------------------------------
# Prepare WA data
wa_emissions = emissions_df[emissions_df['Location'] == 'WA'].rename(columns={'Total (MT)': 'WA Emissions'})
wa_temp_df = wa_temp_df.rename(columns={'Average Temperature (WA)': 'WA Temperature'})
wa_df = pd.merge(wa_emissions, wa_temp_df, on='Year')

# -------------------------------------------------------------
# Prepare VIC data
vic_emissions = emissions_df[emissions_df['Location'] == 'VIC'].rename(columns={'Total (MT)': 'VIC Emissions'})
for col in vic_temp_df.columns:
    if 'Temperature' in col and 'VIC' in col:
        vic_temp_df = vic_temp_df.rename(columns={col: 'VIC Temperature'})
        break
vic_df = pd.merge(vic_emissions, vic_temp_df, on='Year')

# -------------------------------------------------------------
# Prepare QLD data
qld_emissions = emissions_df[emissions_df['Location'] == 'QLD'].rename(columns={'Total (MT)': 'QLD Emissions'})
for col in qld_temp_df.columns:
    if 'Temperature' in col and 'QLD' in col:
        qld_temp_df = qld_temp_df.rename(columns={col: 'QLD Temperature'})
        break
qld_df = pd.merge(qld_emissions, qld_temp_df, on='Year')

# -------------------------------------------------------------
# Prepare ACT data
act_emissions = emissions_df[emissions_df['Location'] == 'ACT'].rename(columns={'Total (MT)': 'ACT Emissions'})

for col in act_temp_df.columns:
    if 'Temperature' in col and 'ACT' in col:
        act_temp_df = act_temp_df.rename(columns={col: 'ACT Temperature'})
        break

act_df = pd.merge(act_emissions, act_temp_df, on='Year')

# -------------------------------------------------------------
# Prepare SA data
sa_emissions = emissions_df[emissions_df['Location'] == 'SA'].rename(columns={'Total (MT)': 'SA Emissions'})

for col in sa_temp_df.columns:
    if 'Temperature' in col and 'SA' in col:
        sa_temp_df = sa_temp_df.rename(columns={col: 'SA Temperature'})
        break

sa_df = pd.merge(sa_emissions, sa_temp_df, on='Year')

# -------------------------------------------------------------
# Prepare NT datas
nt_emissions = emissions_df[emissions_df['Location'] == 'NT'].rename(columns={'Total (MT)': 'NT Emissions'})

# Clean and rename NT temperature column
nt_temp_df.columns = nt_temp_df.columns.str.strip()
for col in nt_temp_df.columns:
    if 'Temperature' in col and 'NT' in col:
        nt_temp_df = nt_temp_df.rename(columns={col: 'NT Temperature'})
        break

# Convert 'Year' in both DataFrames to int
nt_emissions['Year'] = pd.to_numeric(nt_emissions['Year'], errors='coerce').astype('Int64')
nt_temp_df['Year'] = pd.to_numeric(nt_temp_df['Year'], errors='coerce').astype('Int64')

# Drop rows with missing years (if any)
nt_emissions = nt_emissions.dropna(subset=['Year'])
nt_temp_df = nt_temp_df.dropna(subset=['Year'])

# Merge
nt_df = pd.merge(nt_emissions, nt_temp_df, on='Year')

# -------------------------------------------------------------


# Underneath is the sidebar which helps the user choose their preffered state to compare their data.


# Page selector
st.sidebar.header("Climate Data")
page = st.sidebar.radio("Select State", ["NSW", "WA", "VIC", "QLD", "ACT", "SA", "NT"])



# Everything Below here is the actual UI of the APP.
# It shows the columns and the graphs for every single state.
# It compares the temperature of the selected state with the emissions of the selected state. 

# -------------------------------------------------------------
# NSW Page (I just copied and pasted this part for the other sections and changed 'NSW' to something else)
if page == "NSW":
    st.header("NSW Climate Data")
    st.info("This page shows climate data for New South Wales. Use the sidebar to view emissions and temperature.")

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

# -------------------------------------------------------------
# WA Page
elif page == "WA":
    st.header("WA Climate Data")
    st.info("This page shows climate data for Western Australia. Use the sidebar to view emissions and temperature.")

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

# -------------------------------------------------------------
# VIC Page
elif page == "VIC":
    st.header("VIC Climate Data")
    st.info("This page shows climate data for Victoria. Use the sidebar to view emissions and temperature.")

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

# -------------------------------------------------------------
# QLD Page
elif page == "QLD":
    st.header("QLD Climate Data")
    st.info("This page shows climate data for Queensland. Use the sidebar to view emissions and temperature.")

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

# -------------------------------------------------------------
# ACT Page
elif page == "ACT":
    st.header("ACT Climate Data")
    st.info("This page shows climate data for the Australian Capital Territory. Use the sidebar to view emissions and temperature.")

    st.sidebar.subheader("ACT Options")
    show_act_emissions = st.sidebar.checkbox("Show ACT Emissions")
    show_act_temperature = st.sidebar.checkbox("Show ACT Temperature")

    act_columns = ['Year']
    if show_act_emissions:
        act_columns.append('ACT Emissions')
    if show_act_temperature:
        act_columns.append('ACT Temperature')

    st.subheader("ACT Data Table")
    st.dataframe(act_df[act_columns])

    if show_act_emissions or show_act_temperature:
        fig, ax1 = plt.subplots(figsize=(10, 6))
        ax1.set_xlabel('Year')

        if show_act_emissions:
            ax1.set_ylabel('ACT Emissions (Mt CO₂e)', color='darkblue')
            ax1.plot(act_df['Year'], act_df['ACT Emissions'], color='darkblue', label='ACT Emissions')
            ax1.tick_params(axis='y', labelcolor='darkblue')

        if show_act_temperature:
            ax2 = ax1.twinx()
            ax2.set_ylabel('ACT Avg Temperature (°C)', color='magenta')
            ax2.plot(act_df['Year'], act_df['ACT Temperature'], color='magenta', label='ACT Temperature')
            ax2.tick_params(axis='y', labelcolor='magenta')

        plt.title('ACT Emissions vs Temperature Over Time')
        fig.tight_layout()
        st.pyplot(fig)

# -------------------------------------------------------------
# SA Page
elif page == "SA":
    st.header("SA Climate Data")
    st.info("This page shows climate data for South Australia. Use the sidebar to view emissions and temperature.")

    st.sidebar.subheader("SA Options")
    show_sa_emissions = st.sidebar.checkbox("Show SA Emissions")
    show_sa_temperature = st.sidebar.checkbox("Show SA Temperature")

    sa_columns = ['Year']
    if show_sa_emissions:
        sa_columns.append('SA Emissions')
    if show_sa_temperature:
        sa_columns.append('SA Temperature')

    st.subheader("SA Data Table")
    st.dataframe(sa_df[sa_columns])

    if show_sa_emissions or show_sa_temperature:
        fig, ax1 = plt.subplots(figsize=(10, 6))
        ax1.set_xlabel('Year')

        if show_sa_emissions:
            ax1.set_ylabel('SA Emissions (Mt CO₂e)', color='orange')
            ax1.plot(sa_df['Year'], sa_df['SA Emissions'], color='orange', label='SA Emissions')
            ax1.tick_params(axis='y', labelcolor='orange')

        if show_sa_temperature:
            ax2 = ax1.twinx()
            ax2.set_ylabel('SA Avg Temperature (°C)', color='forestgreen')
            ax2.plot(sa_df['Year'], sa_df['SA Temperature'], color='forestgreen', label='SA Temperature')
            ax2.tick_params(axis='y', labelcolor='forestgreen')

        plt.title('SA Emissions vs Temperature Over Time')
        fig.tight_layout()
        st.pyplot(fig)

# -------------------------------------------------------------
# NT Page
elif page == "NT":
    st.header("NT Climate Data")
    st.info("This page shows climate data for Northern Territory. Use the sidebar to view emissions and temperature.")

    st.sidebar.subheader("NT Options")
    show_nt_emissions = st.sidebar.checkbox("Show NT Emissions")
    show_nt_temperature = st.sidebar.checkbox("Show NT Temperature")

    nt_columns = ['Year']
    if show_nt_emissions:
        nt_columns.append('NT Emissions')
    if show_nt_temperature:
        nt_columns.append('NT Temperature')

    st.subheader("NT Data Table")
    st.dataframe(nt_df[nt_columns])

    if show_nt_emissions or show_nt_temperature:
        fig, ax1 = plt.subplots(figsize=(10, 6))
        ax1.set_xlabel('Year')

        if show_nt_emissions:
            ax1.set_ylabel('NT Emissions (Mt CO₂e)', color='crimson')
            ax1.plot(nt_df['Year'], nt_df['NT Emissions'], color='crimson', label='NT Emissions')
            ax1.tick_params(axis='y', labelcolor='crimson')

        if show_nt_temperature:
            ax2 = ax1.twinx()
            ax2.set_ylabel('NT Avg Temperature (°C)', color='purple')
            ax2.plot(nt_df['Year'], nt_df['NT Temperature'], color='purple', label='NT Temperature')
            ax2.tick_params(axis='y', labelcolor='purple')

        plt.title('NT Emissions vs Temperature Over Time')
        fig.tight_layout()
        st.pyplot(fig)

# -------------------------------------------------------------
# Log Out sidebar

def show_logout():
    with st.sidebar:
        if st.button("Log out", use_container_width=True):
            st.session_state.pop("logged_in", None)
            st.rerun()

show_logout()