# FINE 3300 Assignment 2 — Mortgage Schedule & CPI Analysis

## Overview
This assignment consists of two parts:
- **Part A:** Loan amortization and payment schedule generation
- **Part B:** Consumer Price Index (CPI) analysis in Canada

---

## Part A: Loan Amortization and Payment Schedule

### Description
This section expands the mortgage class from Assignment 1 to generate detailed loan payment schedules for six payment frequencies. It calculates fixed payments based on the full amortization period and filters the output to show only the payments within the user-specified mortgage term.

### Features
- Prompts user for:
  - Principal amount
  - Annual interest rate
  - Amortization period (years)
  - Mortgage term (years)
- Calculates fixed periodic payments
- Generates six amortization schedules using Pandas
- Saves all schedules to a single Excel file with labeled worksheets
- Plots loan balance decline for all six options using Matplotlib
- Saves the plot as a `.png` file

### Output Files
- `mortgage_schedules.xlsx`: Excel file with six worksheets
- `mortgage_balance_plot.png`: Matplotlib visualization

---

## Part B: Consumer Price Index Analysis

### Description
This section analyzes monthly CPI data for 2024 across 10 provinces and Canada overall. It calculates inflation metrics, compares regional trends, and evaluates real minimum wages using CPI-adjusted values.

### Data Sources
- 11 CSV files with monthly CPI data for 2024
- `MinimumWages.csv` with nominal minimum wage values

### Implementation Steps
1. Combines all CPI files into a single DataFrame with columns: `Item`, `Month`, `Jurisdiction`, `CPI`
2. Prints the first 12 rows of the combined DataFrame
3. Calculates average month-to-month change in:
   - Food
   - Shelter
   - All-items excluding food and energy
4. Identifies the province with the highest average change
5. Computes equivalent salary to $100,000 in Ontario across other provinces (Dec 2024 CPI)
6. Determines:
   - Province with highest and lowest nominal minimum wage
   - Province with highest real minimum wage (CPI-adjusted)
7. Computes annual CPI change for services across all regions
8. Identifies the region with the highest inflation in services
---
