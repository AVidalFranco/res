"""This program loads a csv with the FDA outlier for each variable.
Then converts each starting and last day of the outlying weeks
to binary values added as a new column to the original dataset 
for each variable."""

import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
plt.style.use('ggplot')

# Read the data
data = pd.read_csv("data/data_pro.csv", delimiter=';', parse_dates=["date"], index_col="date")

# Read the FDA outliers
for column in data.columns:

    try:
        outliers = pd.read_csv(f"results/{column}_out.csv", delimiter=';')
        outlying_weeks = outliers.timeStamps
        
        # Create a new DataFrame with the date, the original data, 0 label for all instances
        new_data = pd.DataFrame({
            'date': data.index,
            column: data[column],
            'fda_' + column: 0
        })

        # Convert the starting and last day of the outlying weeks to binary values
        for week in outlying_weeks:
            
            # Split the week into start_date_str and end_date_str
            start_date_str, end_date_str = week.split(', ')
            
            # Remove the parentheses
            start_date_str = start_date_str[1:]
            end_date_str = end_date_str[:-1]
            
            # Convert the strings to datetime objects
            start_date = datetime.strptime(start_date_str, "'%Y %m %d'")
            end_date = datetime.strptime(end_date_str, "'%Y %m %d'")
            
            # Use the datetime objects in the DataFrame
            new_data.loc[start_date:end_date, 'fda_' + column] = 1
        
        # Save the new DataFrame to a CSV file
        new_data.to_csv(f"results/{column}_fda.csv", sep=";", index=False)

        # Plot the data
        plt.figure(figsize=(10, 6))
        plt.plot(new_data['date'], new_data[column], label=column, color='royalblue')
        
        # Mark the anomalous days with a red dot
        anomalies = new_data[new_data['fda_' + column] == 1]
        plt.plot(anomalies['date'], anomalies[column], 'o', label='Anomalía', color='tomato')
        
        # Add labels and title
        plt.xlabel('Data')
        plt.ylabel(column)
        plt.title(f'Anomalías FDA {column}')
        plt.legend()
        
        # Show the plot
        # plt.show()

        # Save the plot to a PNG file
        plt.savefig(f"results/{column}_fda.png", dpi=300)

    except FileNotFoundError:
        # No FDA outliers found for the variable PM2_5, therefore all instances are labeled as 0 
        new_data = pd.DataFrame({
            'date': data.index,
            column: data[column],
            'fda_' + column: 0
        })

        # Save the new DataFrame to a CSV file
        new_data.to_csv(f"results/{column}_fda.csv", sep=";", index=False)


