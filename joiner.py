import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')

"""Get the results for each variable and add them to a single dataframe."""

# Read the data
data = pd.read_csv("data/data_pro.csv", delimiter=';', parse_dates=["date"], index_col="date")

variables = data.columns

# Define a new DataFrame to store the data with the dates
new_data = pd.DataFrame({'date': data.index})
new_data.set_index('date', inplace=True)

for variable in variables:
    
    new_data[variable] = data[variable]

    # Read the z-score results
    results_zscore = pd.read_csv(f"results/{variable}_zscore.csv", delimiter=';', parse_dates=["date"], index_col="date")
    new_data['zscore_' + variable] = results_zscore[f'zscore_{variable}']

    # Read the OC-SVM results
    results_ocsvm = pd.read_csv(f"results/{variable}_SVM.csv", delimiter=';', parse_dates=["date"], index_col="date")
    new_data['svm_' + variable] = results_ocsvm[f'svm_{variable}']

    # Read the FDA results
    results_fda = pd.read_csv(f"results/{variable}_fda.csv", delimiter=';', parse_dates=["date"], index_col="date")
    new_data['fda_' + variable] = results_fda[f'fda_{variable}']

# Save the new DataFrame to a CSV file
new_data.to_csv("results/data_results.csv", sep=";", index=True)