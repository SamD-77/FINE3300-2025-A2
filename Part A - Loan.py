# FINE 3300 Assignment 2 
#--------------------- Part A ---------------------
import pandas as pd
import matplotlib.pyplot as plt

class MortgagePayment():
    def __init__(self, quoted_rate, amortization_period, term):
        self.quoted_rate = quoted_rate
        self.amortization_period = amortization_period
        self.term = term
        self.ear = (1 + quoted_rate / 2)**2 - 1 # convert semi annual quoted rate to effective annual rate (EAR)
            # EAR = (1 + (i / n))^n - 1 where i is the nominal interest rate and n is number of compounding periods per year
            # use n = 2 because semi-annual compounding for quoted mortgage rates in Canada

    def pva_factor(self, periodic_rate, num_payments):
        """
        Function to calculate the Present Value of Annuity Factor
        """
        return (1 - (1 + periodic_rate) ** -num_payments) / periodic_rate
    

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

        payment_amounts = [] # list holding calculated payment option amounts
    
        # Loop through payment frequencies dict for each option
        for freq in pmt_frequencies.values():
            periodic_rate = (1 + self.ear) ** (1 / freq) - 1 # calculate rate for the period with EAR and yearly payment frequency 
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
    

    def generate_schedule(self, principal, payment_frequency, payment_amount):
        """
        Uses a data frame to build out a payment schedule.
        Includes the period, starting balance, interest amount, payment, and ending balance.
        """
        frequencies = {
            "Monthly": 12,
            "Semi-monthly": 24,
            "Bi-weekly": 26,
            "Weekly": 52,
            "Rapid Bi-weekly": 26,
            "Rapid Weekly": 52
        }

        periods_per_year = frequencies[payment_frequency] # number of pay periods per year

        periodic_rate = (1 + self.ear) ** (1 / periods_per_year) - 1 # calculate rate for the period with EAR and yearly payment frequency

        num_periods = periods_per_year * self.amortization_period # number of payment periods

        balance = principal # set balance as principal to start
        schedule = [] # list to hold dicts to make up payment schedule

        # Iteratively record values for each period
        for period in range(1, num_periods + 1): # start at period 1
            interest = balance * periodic_rate
            principal_payment = payment_amount - interest
            
            # Final payment adjustment to prevent negative balance
            if principal_payment > balance: # check if principal payment would overpay
                principal_payment = balance # cap it
                payment_amount = interest + principal_payment # adjust total payment
                ending_balance = 0 # mortgage is paid off
            else:
                ending_balance = balance - principal_payment

            # Add to schedule list
            schedule.append({
                "Period": period,
                "Starting Balance": balance,
                "Interest": interest,
                "Payment": payment_amount,
                "Ending Balance": ending_balance
            })

            balance = ending_balance # set new starting balance as last ending balance

            if balance <= 0: # stop early if mortgage is paid off
                break

        schedule_df = pd.DataFrame(schedule) # covert list of dicts to data frame for payment schedule

        # Round each value 2 decimals and return data frame
        schedule_df[["Starting Balance", "Interest", "Payment", "Ending Balance"]] = (schedule_df[["Starting Balance", "Interest", "Payment", "Ending Balance"]].round(2)) 
        return schedule_df


# Prompt user to collect relevant data and convert data type from str
principal_amount = float(input("Enter the principal ($): "))
interest_rate = float(input("Enter the quoted interest rate % (e.g 4.85): ")) / 100 # convert from percentage to decimal
amortization_period = int(input("Enter the amortization period in years: "))
term = int(input("Enter the mortgage term: "))

# Instantiate object of MortgagePayment
mortgage = MortgagePayment(interest_rate, amortization_period, term)

# Format and display output
payment_amounts = mortgage.payments(principal_amount) # tuple of payment options amounts

labels = ["Monthly", "Semi-monthly", "Bi-weekly", "Weekly", "Rapid Bi-weekly", "Rapid Weekly"] # list of payment options labels

print("-" * 25) # line break

# Loop through labels list and payment amounts tuple
for i in range(len(payment_amounts)):
    print(f"{labels[i]} Payment: ${payment_amounts[i]:.2f}") # print each label and corresponding value rounded 2 decimals


# Create six data frames for six payment options
payment_schedules = dict() # dict to hold the six payment schedules for the different payment options
for i in range(len(labels)): # loop through each payment option label
    payment_schedules[labels[i]] = mortgage.generate_schedule(principal_amount, labels[i], payment_amounts[i]) # add label and corresponding data frame to dict


# Save each data frame into single Excel file with multiple worksheets labelled appropriately
with pd.ExcelWriter("mortgage_schedules.xlsx", engine="openpyxl") as writer:
    for label, df in payment_schedules.items(): # loop through each payment schedule
        df.to_excel(writer, sheet_name=label, index=False) # write dataframe to excel and name sheet with corresponding label


# Generate single graph with Matplotlib depicting loan balance decline (all 6 plots with legends)
plt.figure(figsize=(12, 6))

for label, df in payment_schedules.items(): # loop through dict of payment schedules
    plt.plot(df["Period"], df["Ending Balance"], label=label) # plot period and ending balance from data frame

plt.title("Mortgage Balance Over Time by Payment Frequency")
plt.xlabel("Period")
plt.ylabel("Ending Balance ($)")
plt.legend()
plt.grid(True)
plt.tight_layout()

# Save graph as a PNG file
plt.savefig("mortgage_balance_plot.png", dpi=300)

plt.show() # display graph

