import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file
file_path = 'C:/MapRock/IntelligenceBusiness/demo_input/stock_closes.csv'
data = pd.read_csv(file_path)

# Convert the 'Date' column to datetime format if not already done
data['Date'] = pd.to_datetime(data['Date'])

# Filter the data for the first period (July 25, 2022 - Dec 27, 2022)
first_period_start = '2022-07-25'
first_period_end = '2022-12-27'
title1 = f'MSFT vs. NVDA\n{first_period_start} - {first_period_end}'
data_first_period = data[(data['Date'] >= first_period_start) & (data['Date'] <= first_period_end)]

# Filter the data for the second period (Dec 28, 2022 - July 24, 2023)
second_period_start = '2022-12-28'
second_period_end = '2023-07-24'
title2 = f'MSFT vs. NVDA\n{second_period_start} - {second_period_end}'
data_second_period = data[(data['Date'] >= second_period_start) & (data['Date'] <= second_period_end)]


# Display the first few rows of the dataframe to understand its structure
print(data.head())

# Create scatter plots for the given periods
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Plot for the first period
sns.regplot(ax=axes[0], data=data_first_period, x='MSFT', y='NVDA', ci=None)
axes[0].set_title(title1)
axes[0].set_xlabel('MSFT')
axes[0].set_ylabel('NVDA')
# Pearson correlation coefficient
pearson_first_period = data_first_period[['MSFT', 'NVDA']].corr().iloc[0, 1]
axes[0].text(0.05, 0.95, f'Pearson: {pearson_first_period:.6f}', transform=axes[0].transAxes, fontsize=12, verticalalignment='top')

# Plot for the second period
# Assuming we have another dataframe for the second period (data_second_period)
# If the second period data is part of the same CSV, we would need to filter it based on the dates.
# Here, we assume it's a separate dataframe for simplicity.

# data_second_period = ... (load the second period data here)
# For demonstration, let's duplicate the data

sns.regplot(ax=axes[1], data=data_second_period, x='MSFT', y='NVDA', ci=None)
axes[1].set_title(title2)
axes[1].set_xlabel('MSFT')
axes[1].set_ylabel('NVDA')
# Pearson correlation coefficient for the second period
pearson_second_period = data_second_period[['MSFT', 'NVDA']].corr().iloc[0, 1]
axes[1].text(0.05, 0.95, f'Pearson: {pearson_second_period:.6f}', transform=axes[1].transAxes, fontsize=12, verticalalignment='top')

plt.tight_layout()
plt.show()
