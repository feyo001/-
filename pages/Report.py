from Analytics import get_sheet_data("Expenses")
# expenses = get_sheet_data("Expenses")
expenses_df= expences_data_wrangle(expenses)
st.write(expenses_df)
