import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = 'C:/MapRock/IntelligenceBusiness/demo_input/stock_closes.csv'
data = pd.read_csv(file_path)

# Convert the 'Date' column to datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Calculate the percent day-to-day change for MSFT and NVDA
data['MSFT_pct_change'] = data['MSFT'].pct_change()
data['NVDA_pct_change'] = data['NVDA'].pct_change()

# Plot the percent changes
plt.figure(figsize=(15, 6))
plt.plot(data['Date'], data['MSFT_pct_change'], label='MSFT')
plt.plot(data['Date'], data['NVDA_pct_change'], label='NVDA', linestyle=':', color='orange')

# Calculate Pearson correlation coefficient for the percent changes
pearson_corr = data[['MSFT_pct_change', 'NVDA_pct_change']].corr().iloc[0, 1]

# Add title and labels
plt.title('MSFT vs. NVDA - Close Price - Percent Day to Day Change - July 2022 through July 2023')
plt.xlabel('Date')
plt.ylabel('Percent Change')
plt.legend()

# Add Pearson correlation coefficient text
plt.text(0.05, 0.95, f'Pearson: {pearson_corr:.6f}', transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))

# Show the plot
plt.show()
