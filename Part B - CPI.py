# FINE 3300 Assignment 2 
#--------------------- Part B ---------------------
import pandas as pd

jurisdictions = ["Canada", "AB", "BC", "MB", "NB", "NL", "NS", "ON", "PEI", "QC", "SK"] # list of CPI data jurisdictions for provinces and Canada overall

# Read 11 files into Python and form a data frame
dataframes = [] # list to hold the 11 individual data frames for each jurisdiction

for jurisdiction in jurisdictions: # loop through jurisdictions list to get its respective data file
    df = pd.read_csv(f"A2 Data/{jurisdiction}.CPI.1810000401.csv") # read individual CPI data file and form a data frame

        # Reshape from wide to long using melt
    df = df.melt(id_vars=["Item"], var_name="Month", value_name="CPI") 
        # item and Jurisdiction stay fixed. They are repeated for each melted row
        # the original column headers for each month become values in a new column, Month
        # the actual CPI values from each month go into a new column, CPI

    df.insert(2, "Jurisdiction", jurisdiction) # add a column at index 2 (after month) to identify the province
    dataframes.append(df) # add data frame to list of 11 dataframes

# 1. Combine the 11 data frames into one dataframe with columns Item, Month, Jurisdiction, CPI
cpi_df = pd.concat(dataframes, ignore_index=True) 


# 2. Print first 12 lines of new data frame
print(cpi_df.head(12)) 


# 3. Report average month-to-month changes in food, shelter, All-items excluding food and energy as % 1 dec for Canada and each province
avg_change_results = [] # list to hold dicts of month-to-month change results

items = ["Food", "Shelter", "All-items excluding energy"] # items to calculate avg month-to-month change for

for jurisdiction in jurisdictions: # loop for each item in each jurisdiction
    for item in items:
        filtered_df = cpi_df.query("Jurisdiction == @jurisdiction and Item == @item").copy() # filter cpi dataframe by jurisdiction and item and make a copy 
            # query allows sql style filtering which makes it easy to read (@ neeeded to pass variables)

        filtered_df["% Change"] = filtered_df["CPI"].pct_change() # create new column for fractional change between CPI values for each row (displayed as decimal e.g 2% shown as 0.02)

        avg_change = filtered_df["% Change"].mean() * 100 # take average of % changes column and multiply by 100 for a % value (e.g 2.0%)

        avg_change_results.append({ # add to list containing average month-to-month changes
        "Jurisdiction": jurisdiction,
        "Item": item,
        "Avg % Change": round(avg_change, 1) # round % to one decimal (e.g 4.1 = 4.1%)
        })

avg_change_results_df = pd.DataFrame(avg_change_results) # convert avg change results list into dataframe
print() # new line
print(avg_change_results_df) # output results
print() # new line


# 4. Province with highest average change across the select categories
for item in items: # for each category
    item_filter_df = avg_change_results_df.query("Item == @item").copy() # filter dataframe for category and make copy

    top_jurisdiction = item_filter_df.sort_values(by="Avg % Change", ascending=False).iloc[0] # sort by Avg % Change column descending so the top row will be the max

    print(f"Highest Average % Change in {item}\nJurisdiction: {top_jurisdiction["Jurisdiction"]}\nAvg % Change: {top_jurisdiction["Avg % Change"]}%\n") # output results    


# 5. Equivalent salary to $100k received in Ontario in all other provinces using All-items CPI
all_item_cpi_filter = cpi_df.query("Item == 'All-items' and Month == '24-Dec'") # get dataframe for all-items CPI for each jurisdiction, Dec 2024

salary = 100000
ontario_cpi = all_item_cpi_filter.loc[all_item_cpi_filter["Jurisdiction"] == "ON", "CPI"].iloc[0] # get Ontario CPI to use as base

equivalent_salaries = [] # list to hold dict of provinces and their equivalent salaries

for jurisdiction in jurisdictions[1:]:# loop through jurisdictions but skip Canada at first index
    province_cpi = all_item_cpi_filter.loc[all_item_cpi_filter["Jurisdiction"] == jurisdiction, "CPI"].iloc[0]
    equivalent_salary =  (province_cpi / ontario_cpi) * salary # equivalent salary calculation
     
    equivalent_salaries.append({ # add equivalent salary and jurisdiction to list
        "Jurisdiction": jurisdiction,
        "Equivalent Salary": round(equivalent_salary, 2) # round equivalent salary to 2 decimals
    })

equivalent_salaries_df = pd.DataFrame(equivalent_salaries) # make into dataframe

print("Equivalent salaries in all other provinces to $100,000 received in Ontario as at Dec 2024 ")
print(equivalent_salaries_df) # output results


# 6. Minimum wage
minimum_wage_df = pd.read_csv("A2 Data/MinimumWages.csv") # open minimum wages file and read to data frame
print(minimum_wage_df)

highest_min_wage = minimum_wage_df.sort_values(by="Minimum Wage", ascending=False).iloc[0] # sort by descending and grab top row which will be the max
lowest_min_wage = minimum_wage_df.sort_values(by="Minimum Wage", ascending=True).iloc[0] # sort by ascending and grab top row which will be the lowest

print(f"\nHighest minimum wage (nominal)\nProvince: {highest_min_wage["Province"]}\nMinimum wage: {highest_min_wage["Minimum Wage"]}") # output highest nominal minimum wage
print(f"\nLowest minimum wage (nominal)\nProvince: {lowest_min_wage["Province"]}\nMinimum wage: {lowest_min_wage["Minimum Wage"]}") # output lowest nominal minimum wage


"""
Finish below: finding max real minimum wage
    - Make new col for real min wage using Dec 2024 CPI for and nominal min wage values for respective province
    - Then find max after
"""
#print(all_item_cpi_filter)
#minimum_wage_df["Dec 24 CPI"] = all_item_cpi_filter.loc[all_item_cpi_filter["Jurisdiction"] == "Province", "CPI"].iloc[0]

#max_real_wage = all_item_cpi_filter.sort_values(by="CPI", ascending=False).iloc[0] # get first row which will be the max from descending list of all-items CPI for Dec 2024
#print(f"\nHighest minimum wage (real)\nProvince: {max_real_wage["Province"]}\nCPI: {max_real_wage["CPI"]}") # print highest real minimum wage


# 7. Annual change in CPI for services across all jurisdictions reported as % 1 decimal
print(cpi_df)
services_cpi = cpi_df.query("Item == 'Services'")
print(services_cpi)


# 8. Region experiencing highest inflation in services
