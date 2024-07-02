import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr

# Data setup
data = {
    'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
    'Temperature (Fahrenheit)': [45, 65, 70, 80, 73],
    'Broccoli Sales ($)': [50, 80, 130, 70, 180]
}

df = pd.DataFrame(data)

# Calculate Pearson and Spearman correlations
pearson_corr, _ = pearsonr(df['Temperature (Fahrenheit)'], df['Broccoli Sales ($)'])
spearman_corr, _ = spearmanr(df['Temperature (Fahrenheit)'], df['Broccoli Sales ($)'])

# Rank data for Spearman calculation
df['Temperature Rank'] = df['Temperature (Fahrenheit)'].rank()
df['Sales Rank'] = df['Broccoli Sales ($)'].rank()

# Print the correlation coefficients
print(f"Pearson correlation: {pearson_corr:.6f}")
print(f"Spearman correlation: {spearman_corr:.6f}")

# Plotting the data
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))

# Scatter plot for Pearson correlation
axes[0].scatter(df['Temperature (Fahrenheit)'], df['Broccoli Sales ($)'])
axes[0].set_title('Pearson')
axes[0].set_xlabel('Temperature (Fahrenheit)')
axes[0].set_ylabel('Broccoli Sales ($)')
m, b = np.polyfit(df['Temperature (Fahrenheit)'], df['Broccoli Sales ($)'], 1)
axes[0].plot(df['Temperature (Fahrenheit)'], m*df['Temperature (Fahrenheit)'] + b, color='blue', linestyle='--')

# Scatter plot for Spearman correlation
axes[1].scatter(df['Temperature Rank'], df['Sales Rank'])
axes[1].set_title('Spearman')
axes[1].set_xlabel('Temperature Rank')
axes[1].set_ylabel('Sales Rank')
m, b = np.polyfit(df['Temperature Rank'], df['Sales Rank'], 1)
axes[1].plot(df['Temperature Rank'], m*df['Temperature Rank'] + b, color='blue', linestyle='--')

# Show the plots
plt.tight_layout()
plt.show()

# Display the DataFrame
print("\nDataFrame with ranks:")
print(df)

# Add correlation values to DataFrame for display
df.loc['Pearson', 'Temperature (Fahrenheit)'] = 'Pearson'
df.loc['Pearson', 'Broccoli Sales ($)'] = pearson_corr
df.loc['Spearman', 'Temperature (Fahrenheit)'] = 'Spearman'
df.loc['Spearman', 'Broccoli Sales ($)'] = spearman_corr

print("\nDataFrame with correlation values:")
print(df)
