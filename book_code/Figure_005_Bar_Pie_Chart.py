
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

# Establish a connection to the database
cnxn = pyodbc.connect(f"DSN=KyvosNew", autocommit=True)
cursor = cnxn.cursor()

# Example query. Create your own queries based on your own cube structure.
sql_query = f"""SELECT SUM(`i`.`sale_dollars`) AS `sale_dollars`, `i`.`Store` AS `Store`
FROM `Eugene Training`.`iowa_liquor_sales` `i`  
WHERE `i`.`Zip Code` = '50613' 
GROUP BY `i`.`Store`"""

cursor.execute(sql_query)
result_set = cursor.fetchall()

# Create a DataFrame from the result set
df = pd.DataFrame.from_records(result_set, columns=[col[0] for col in cursor.description])
print(df)

# Generate a pie chart
plt.figure(figsize=(10, 6))
plt.pie(df['sale_dollars'], labels=df['Store'], autopct='%1.1f%%', startangle=140)
plt.title('Sales Distribution by Store')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()

# Generate a sorted bar chart
df_sorted = df.sort_values(by='sale_dollars', ascending=False)
plt.figure(figsize=(10, 6))
plt.bar(df_sorted['Store'], df_sorted['sale_dollars'], color='skyblue')
plt.xlabel('Store')
plt.ylabel('Sale Dollars')
plt.title('Sales by Store')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
