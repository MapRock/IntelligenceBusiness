import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import os

from dotenv import load_dotenv

load_dotenv()

# Modified function to plot two separate heatmaps
def create_crosstab(df_path):
    # Load the dataset
    df = pd.read_csv(df_path)

    # Calculate the conditional probabilities
    df['P_A_given_B'] = df['A_Intersect_B'] / df['CountB']
    df['P_B_given_A'] = df['A_Intersect_B'] / df['CountA']

    # Create crosstabs (pivot tables)
    crosstab_a_given_b = pd.pivot_table(df, values='P_A_given_B', index='ObjectB', columns='ObjectA', aggfunc='first')
    crosstab_b_given_a = pd.pivot_table(df, values='P_B_given_A', index='ObjectA', columns='ObjectB', aggfunc='first')

    # Plot the heatmap for P(A|B)
    plt.figure(figsize=(10, 8))
    heatmap_a_given_b = sns.heatmap(crosstab_a_given_b, annot=True, fmt=".2f", cmap='viridis')
    heatmap_a_given_b.set_title('Heatmap of P(A|B)')
    heatmap_a_given_b.set_xlabel('Event A (ObjectA)')
    heatmap_a_given_b.set_ylabel('Event B (ObjectB)')
    plt.show()

    # Plot the heatmap for P(B|A)
    plt.figure(figsize=(10, 8))
    heatmap_b_given_a = sns.heatmap(crosstab_b_given_a, annot=True, fmt=".2f", cmap='viridis')
    heatmap_b_given_a.set_title('Heatmap of P(B|A)')
    heatmap_b_given_a.set_xlabel('Event A (ObjectA)')
    heatmap_b_given_a.set_ylabel('Event B (ObjectB)')
    plt.show()

    return crosstab_a_given_b, crosstab_b_given_a

if __name__ == '__main__':
    
    # Path to the CSV file
    # bayes.csv is created using bayesian_stocks.sql
    file_path = f"{os.getenv('DEFAULT_INPUT_DIR')}bayes_crosstab.csv"

    # Create the crosstab pivot table
    crosstab_a_given_b, crosstab_b_given_a = create_crosstab(file_path)
    print(crosstab_a_given_b)
    print(crosstab_b_given_a)

