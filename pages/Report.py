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
st.write(filtered_expenses_df.head())

# Generate the report
def generate_report(date, df):
    report = f"Date: {date.strftime('%d/%m/%Y')}\n"
    report += f"Sales: ₦{df['PRICE'].sum():,.2f}\n"
    report += f"Expense(s): ₦{filtered_expenses_df['Amount'].sum():,.2f}\n"
#   report += "Purchases:\n"
#     # purchases = df[df['Category'] == 'Purchases']
# #     report += "Exp:\n"
#     expenses = df[df['Category'] == 'Exp']
#     for index, row in expenses.iterrows():
#         report += f"{row['Details']}: N{row['Amount']} by {row['Person']}\n"
#     report += "Miscellaneous:\n"
#     miscellaneous = df[df['Category'] == 'Miscellaneous']
#     for index, row in miscellaneous.iterrows():
#         report += f"{row['Details']}: N{row['Amount']} by {row['Person']}\n"
#     report += "Contribution:\n"
#     report += "Pepvic: \n"
#     report += "mama: \n"
    return report

report = generate_report(selected_date, filtered_df)

def generate_report1(date, df):
    for index, row in filtered_expenses_df.iterrows():
        report1=""
        report1 += f"{row['Item']}: ₦{row['Amount']}\n"
    return report1
        
report1 = generate_report1(selected_date, filtered_expenses_df)

# Display the report
st.text_area("Printable Report", report, height=400)
################################################################################
st.text_area("Expense Report", report1, height=250)

################################################################################


# df = pd.DataFrame(data)
# df['Date'] = pd.to_datetime(df['Date'])

# # Get date input from the user
# selected_date = st.date_input("Select Date")

# # Filter the DataFrame by the selected date
# filtered_df = df[df['Date'] == pd.to_datetime(selected_date)]

# # Generate the report
# def generate_report(date, df):
#     report = f"Date: {date.strftime('%d/%m/%Y')}\n"
#     report += "Sale:\n"
#     report += "Purchases:\n"
#     purchases = df[df['Category'] == 'Purchases']
#     for index, row in purchases.iterrows():
#         report += f"{row['Details']}: N{row['Amount']} by {row['Person']}\n"
#     report += "Exp:\n"
#     expenses = df[df['Category'] == 'Exp']
#     for index, row in expenses.iterrows():
#         report += f"{row['Details']}: N{row['Amount']} by {row['Person']}\n"
#     report += "Miscellaneous:\n"
#     miscellaneous = df[df['Category'] == 'Miscellaneous']
#     for index, row in miscellaneous.iterrows():
#         report += f"{row['Details']}: N{row['Amount']} by {row['Person']}\n"
#     report += "Contribution:\n"
#     report += "Pepvic: \n"
#     report += "mama: \n"
#     return report

# report = generate_report(selected_date, filtered_df)

# # Display the report
# st.text_area("Printable Report", report, height=400)
