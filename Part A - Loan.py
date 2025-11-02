# FINE 3300 Assignment 2 
#--------------------- Part A ---------------------
import pandas as pd
import matplotlib.pyplot as plt

class MortgagePayment():
    def __init__(self, quoted_rate, amortization_period, term):
        self.quoted_rate = quoted_rate
        self.amortization_period = amortization_period
        self.term = term

    def pva_factor(self, periodic_rate, num_payments):
        """
        Function to calculate the Present Value of Annuity Factor
        """
        pva = (1 - (1 + periodic_rate) ** -num_payments) / periodic_rate
        return pva

    def payments(self, principal):
        """
        Takes the principal amount and returns a tuple of all the periodic payment options
        """   
        # Dict with number of payments in year for each payment option
        pmt_frequencies = {
            "monthly": 12,
            "semi-monthly": 24,
            "bi-weekly": 26,
            "weekly": 52
        }

        # Convert semi annual quoted rate to effective annual rate (EAR)
        ear = (1 + self.quoted_rate / 2)**2 - 1

        payment_amounts = [] # list holding calculated payment option amounts
    
        # Loop through payment frequencies dict for each option
        for freq in pmt_frequencies.values():
            periodic_rate = (1 + ear) ** (1 / freq) - 1 # calculate rate for the period with EAR and yearly payment frequency 
            num_pmts = freq * self.amortization_period # calculate number of payments across the amortization period
            payment_amount = principal / self.pva_factor(periodic_rate, num_pmts) # calculate the payment amount
            payment_amounts.append(payment_amount) # add to list of payment amounts

        # Add accelerated payment options to list
        monthly_pmt = payment_amounts[0] # monthly payment amount is first index
        rapid_bi_pmt = monthly_pmt / 2 # calculate accelerated bi-weekly payment amount from monthly amount
        rapid_weekly_pmt = monthly_pmt / 4 # calculate accelerated weekly payment amount from monthly amount
        payment_amounts.append(rapid_bi_pmt) # add rapid bi-weekly payment amount to list
        payment_amounts.append(rapid_weekly_pmt) # add rapid weekly payment amount to list

        # Return all payment options as tuple
        return tuple(payment_amounts)
    

    def generate_schedule(self):
        """
        Uses a data frame to build out a payment schedule.
        Includes the period, starting balance, interest amount, payment, and ending balance.
        """
        pass


    
# Prompt user to collect relevant data and convert data type from str
principal_amount = float(input("Enter the principal ($): "))
interest_rate = float(input("Enter the quoted interest rate % (e.g 4.85): ")) / 100 # convert from percentage to decimal
amortization_period = int(input("Enter the amortization period in years: "))
term = int(input("Enter the mortgage term: "))

# Instantiate object of MortgagePayment
mortgage = MortgagePayment(interest_rate, amortization_period, term)

# Format and display output
payment_amounts = mortgage.payments(principal_amount) # tuple of payment options amounts

labels = ["Monthly", "Semi-monthly", "Bi-weekly", "Weekly", "Rapid Bi-weekly", "Rapid Weekly"]

print("-" * 25) # line break

# Loop through labels list and payment amounts tuple
for i in range(len(payment_amounts)):
    print(f"{labels[i]} Payment: ${payment_amounts[i]:.2f}") # print each label and corresponding value rounded 2 decimals




# Create six data frames for six payment options


# Save each data frame into single Excel file with multiple worksheets labelled appropriately


# Generate single graph with Matplotlib depicting loan balance decline (all 6 plots with legends)


# Save graph as a PNG file
