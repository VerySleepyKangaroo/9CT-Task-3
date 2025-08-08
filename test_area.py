import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# streamlit run UI.py

# 🎉 Welcome popup
st.toast("👋 Welcome! Hope you have a great time exploring WA climate data.", icon="🌞")

# 📝 Instructions
with st.expander("📘 How to use this app"):
    st.markdown("""
    This dashboard lets you explore **Western Australia's temperature and emissions trends** over time.

    ### What you can do:
    - **View WA Temperature**: See how average temperatures have changed.
    - **View WA Emissions**: Track greenhouse gas emissions over the years.
    - **Compare Both**: See temperature and emissions side by side.

    ### How to get started:
    1. Use the dropdown menu to choose what data to view.
    2. Scroll down to see the chart.
    3. Want to dig deeper? Try comparing trends or adding filters!

    Enjoy your exploration!
    """)


# Load WA temperature data
wa_temp_df = pd.read_csv("Average WA temperatures.csv")
wa_temp_df.rename(columns={"Average Temperature (WA)": "WA Temperature"}, inplace=True)

# Load emissions data
emissions_df = pd.read_csv("Emissions_Data.csv")

# Filter for WA emissions
wa_emissions_df = emissions_df[emissions_df["Location"] == "WA"][["Year", "Total (MT)"]]
wa_emissions_df.rename(columns={"Total (MT)": "WA Emissions"}, inplace=True)

# Merge temperature and emissions data
combined_df = pd.merge(wa_temp_df, wa_emissions_df, on="Year")

# Sidebar selection
view_option = st.selectbox(
    "Choose data to view:",
    ["WA Temperature", "WA Emissions", "Compare Both"]
)

# Display header
st.subheader(f"Visualizing: {view_option}")

# Plotting
fig, ax1 = plt.subplots()

if view_option == "WA Temperature":
    ax1.plot(wa_temp_df["Year"], wa_temp_df["WA Temperature"], color="tab:red")
    ax1.set_ylabel("Temperature (°C)", color="tab:red")
    ax1.set_xlabel("Year")
    ax1.tick_params(axis="y", labelcolor="tab:red")

elif view_option == "WA Emissions":
    ax1.plot(wa_emissions_df["Year"], wa_emissions_df["WA Emissions"], color="tab:blue")
    ax1.set_ylabel("Emissions (MtCO₂e)", color="tab:blue")
    ax1.set_xlabel("Year")
    ax1.tick_params(axis="y", labelcolor="tab:blue")

else:  # Compare Both
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Temperature (°C)", color="tab:red")
    ax1.plot(combined_df["Year"], combined_df["WA Temperature"], color="tab:red", label="Temperature")
    ax1.tick_params(axis="y", labelcolor="tab:red")

    ax2 = ax1.twinx()
    ax2.set_ylabel("Emissions (MtCO₂e)", color="tab:blue")
    ax2.plot(combined_df["Year"], combined_df["WA Emissions"], color="tab:blue", label="Emissions")
    ax2.tick_params(axis="y", labelcolor="tab:blue")

fig.tight_layout()
st.pyplot(fig)