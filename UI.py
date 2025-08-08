import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Title
st.title("NSW Emissions vs Temperature Over Time")

# Load data
emissions_df = pd.read_csv("Emissions_Data.csv")
temperature_df = pd.read_csv("Average NSW temperatures.csv")

# Filter and rename
nsw_emissions = emissions_df[emissions_df['Location'] == 'NSW']
nsw_emissions = nsw_emissions.rename(columns={'Total (MT)': 'NSW Emissions'})
temperature_df = temperature_df.rename(columns={'Average Temperature (NSW)': 'NSW Temperature'})

# Merge datasets
merged_df = pd.merge(nsw_emissions[['Year', 'NSW Emissions']], temperature_df, on='Year')

# Sidebar filters
year_range = st.slider("Select Year Range", int(merged_df['Year'].min()), int(merged_df['Year'].max()), (2000, 2020))
filtered_df = merged_df[(merged_df['Year'] >= year_range[0]) & (merged_df['Year'] <= year_range[1])]

# Plotting
fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.set_xlabel('Year')
ax1.set_ylabel('NSW Emissions (Mt CO₂e)', color='red')
ax1.plot(filtered_df['Year'], filtered_df['NSW Emissions'], color='red', marker='o')
ax1.tick_params(axis='y', labelcolor='red')

ax2 = ax1.twinx()
ax2.set_ylabel('NSW Avg Temperature (°C)', color='blue')
ax2.plot(filtered_df['Year'], filtered_df['NSW Temperature'], color='blue', marker='s')
ax2.tick_params(axis='y', labelcolor='blue')

fig.tight_layout()
st.pyplot(fig)

# Correlation
correlation = filtered_df['NSW Emissions'].corr(filtered_df['NSW Temperature'])
st.markdown(f"### Correlation between emissions and temperature: `{correlation:.2f}`")

# Data preview
with st.expander("Show Raw Data"):
    st.dataframe(filtered_df)