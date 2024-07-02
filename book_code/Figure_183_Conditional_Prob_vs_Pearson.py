import pandas as pd
import numpy as np

# Create the dataframe
data = {
    'Day': ['Monday (Feb 1)', 'Tuesday (Feb 2)', 'Wednesday (Feb 3)', 'Thursday (Feb 4)', 'Friday (Feb 5)', 'Saturday (Feb 6)', 'Sunday (Feb 7)'],
    'People Watching Sports (1000)': [5, 4, 6, 7, 5, 100, 23],
    'Pizza Orders (1000)': [5, 3, 4, 6, 5, 95, 90],
    'Major Sports Event': ['x', None, None, 'x', None, 'x', 'x'],
    'Pizza Discount': [None, None, None, None, None, 'x', 'x'],
    'Pizza Sales Spike': [None, None, None, 'x', None, 'x', 'x']
}

df = pd.DataFrame(data)
# Print the dataframe
print(df)

# Calculate probabilities
total_days = len(df)
major_sports_event_days = len(df[df['Major Sports Event'] == 'x'])
pizza_sales_spike_days = len(df[df['Pizza Sales Spike'] == 'x'])
both_events_days = len(df[(df['Major Sports Event'] == 'x') & (df['Pizza Sales Spike'] == 'x')])

P_A_given_B = both_events_days / major_sports_event_days
P_B_given_A = both_events_days / pizza_sales_spike_days

# Calculate Pearson correlation
correlation = df['People Watching Sports (1000)'].corr(df['Pizza Orders (1000)'])
weekday_correlation = df['People Watching Sports (1000)'].iloc[:5].corr(df['Pizza Orders (1000)'].iloc[:5])

# Display results
print(f"Given a Major Sports Event, the probability of a big spike in pizza sales: {P_A_given_B:.2f}")
print(f"Given a big spike in pizza sales, the probability that a major sports event took place on TV: {P_B_given_A:.2f}")
print(f"Correlation between People watching sports and pizza orders: {correlation:.2f}")
print(f"Weekday correlation between People watching sports and pizza orders: {weekday_correlation:.2f}")


