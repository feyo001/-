import streamlit as st
import pandas as pd
from pages.Analytics import get_sheet_data
from pages.Analytics import expences_data_wrangle
from pages.Analytics import data_wrangle



sales = get_sheet_data("Sales")
sales_df = data_wrangle(sales)
expenses = get_sheet_data("Expenses")
expenses_df= expences_data_wrangle(expenses)

# st.write(sales_df)
# st.write(expenses_df)



df = pd.DataFrame(sales_df)
# st.write(df)
df['DATE'] = pd.to_datetime(df['DATE'])
st.write(df.head())

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