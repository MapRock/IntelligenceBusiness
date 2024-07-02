
"""
Enterprise Intelligence - Supplemental Code

Author: Eugene Asahara
Book: Enterprise Intelligence
Publisher: Technics Publications

Copyright (c) 2024 Eugene Asahara. All rights reserved.

This file is part of the supplemental material for the book "Enterprise Intelligence".
It is provided "as-is" without any warranty, express or implied. The author and publisher
make no guarantees regarding the accuracy, completeness, or suitability of this code
for any particular purpose.

You are granted permission to use, modify, and distribute this code for personal,
educational, or commercial purposes, provided that this notice remains intact.

For more information, visit the book's official page or contact the publisher.

Information:

Filters (Where Clauses): As you mentioned, each filter term could be of different types. We'll create individual classes for each type of filter (Equal, In, Exists, etc.).

Measures: Measures would need the field and the aggregation function. We'll create a class for that.

Dice (Non-aggregated columns): These would be straightforward, mostly a list of columns.

Main OLAP Query Class: This will tie everything together. It will have methods to add filters, measures, dices, and a method to generate the SQL query.

DataSource: It can be various sources, but for simplicity, let's assume an OLAP cube or a flat table.
"""


import matplotlib.pyplot as plt
import pyodbc
import pandas as pd



cnxn = pyodbc.connect(f"DSN=KyvosNew", autocommit=True)
cursor = cnxn.cursor()

# Example query. Create your own queries based on your own cube structure.
sql_query = f"""SELECT SUM(`i`.`sale_dollars`) AS `sale_dollars`, `i`.`Store` AS `Store`, `i`.`class` AS `class` 
FROM `Eugene Training`.`iowa_liquor_sales` `i`  
WHERE `i`.`Zip Code` = '50613' AND `i`.`class` IN ('Whiskey','Vodka','Rum','Tequila','Gin') 
GROUP BY `i`.`Store`, `i`.`class`"""

cursor.execute(sql_query)
result_set = cursor.fetchall()
df = pd.DataFrame.from_records(result_set, columns=[col[0] for col in cursor.description])

# Strip any whitespace from the 'Store' and 'class' columns
df['Store'] = df['Store'].str.strip()
df['class'] = df['class'].str.strip()

# Pivot the dataframe to prepare for the stacked bar chart
pivot_df = df.pivot_table(index='Store', columns='class', values='sale_dollars', aggfunc='sum').fillna(0)

# Normalize the data to create a 100% stacked bar chart
pivot_df_percentage = pivot_df.div(pivot_df.sum(axis=1), axis=0) * 100

# Plotting the 100% stacked bar chart
pivot_df_percentage.plot(kind='bar', stacked=True, figsize=(14, 8))

plt.title('Sales by Store and Class (100% Stacked)')
plt.xlabel('Store')
plt.ylabel('Percentage of Sales')
plt.legend(title='Class', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

