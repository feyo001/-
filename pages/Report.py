import streamlit as st
import pandas as pd
from pages.Analytics import get_sheet_data
from pages.Analytics import expences_data_wrangle
from pages.Analytics import data_wrangle




sales = get_sheet_data("Sales")
sales_df = data_wrangle(sales)
expenses = get_sheet_data("Expenses")
expenses_df= expences_data_wrangle(expenses)


df = pd.DataFrame(sales_df)
# st.write(df)
df['DATE'] = pd.to_datetime(df['DATE'])
# st.write(df.head())

# Get date input from the user
selected_date = st.date_input("Select Date")

# Filter the DataFrame by the selected date
filtered_df = df[df['DATE'] == pd.to_datetime(selected_date)]
filtered_df = filtered_df[['DATE', 'NAME', 'UNITS', 'PRICE']]
st.write(filtered_df.head())


filtered_expenses_df = expenses_df[['Date','Item','Description','Amount']]
filtered_expenses_df = filtered_expenses_df[filtered_expenses_df['Date'] == pd.to_datetime(selected_date)]
total_expenses = filtered_expense_df.query('~(Item == "Pepvic Ventures" or Item == "Weekly Contribution(Mama)")')['Amount'].sum()
            
# comfort_df = filtered_expenses_df.query('Item == "Comfort"')
# peter_df = filtered_expenses_df.query('Item == "Peter"')


# Generate the report
# filtered_expenses_df['Amount'].sum()
def generate_report(date, df):
    report = f"Date: {date.strftime('%d/%m/%Y')}\n"
    report += f"Sales: ₦{df['PRICE'].sum():,.2f}\n"
    report += f"Expense(s): ₦{total_expenses:,.2f}\n"

    return report

report = generate_report(selected_date, filtered_df)
 
# Display the report
st.text_area("Report", report, height=120)


# Expense breakdown Table
st.write(filtered_expenses_df[['Item','Description','Amount']].reset_index(drop=True))

