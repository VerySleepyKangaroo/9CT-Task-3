import pandas as pd
import matplotlib.pyplot as plt

# Load the datasets
emissions_df = pd.read_csv("Emissions_Data.csv")
temperature_df = pd.read_csv("Average NSW temperatures.csv")

# Display column names for verification
print("Emissions columns:", emissions_df.columns)
print("Temperature columns:", temperature_df.columns)

# Filter emissions data for NSW only
nsw_emissions = emissions_df[emissions_df['Location'] == 'NSW']

# Rename the correct column
nsw_emissions = nsw_emissions.rename(columns={'Total (MT)': 'NSW Emissions'})
temperature_df = temperature_df.rename(columns={'Average Temperature (NSW)': 'NSW Temperature'})

# Merge datasets on Year
merged_df = pd.merge(nsw_emissions[['Year', 'NSW Emissions']], temperature_df, on='Year')

# Confirm merged columns
print("Merged columns:", merged_df.columns)

# Plotting with dual y-axis
fig, ax1 = plt.subplots(figsize=(10, 6))

# Emissions on left y-axis
ax1.set_xlabel('Year')
ax1.set_ylabel('NSW Emissions (Mt CO₂e)', color='red')
ax1.plot(merged_df['Year'], merged_df['NSW Emissions'], color='red', marker='o', label='NSW Emissions')
ax1.tick_params(axis='y', labelcolor='red')

# Temperature on right y-axis
ax2 = ax1.twinx()
ax2.set_ylabel('NSW Avg Temperature (°C)', color='blue')
ax2.plot(merged_df['Year'], merged_df['NSW Temperature'], color='blue', marker='s', label='NSW Temperature')
ax2.tick_params(axis='y', labelcolor='blue')

# Title and layout
plt.title('NSW Emissions vs Temperature Over Time')
fig.tight_layout()
plt.grid(True)
plt.show()

# Correlation
correlation = merged_df['NSW Emissions'].corr(merged_df['NSW Temperature'])
print(f"\n🔍 Correlation between emissions and temperature: {correlation:.2f}")