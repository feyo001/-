import streamlit as st
from pages.Analytics import get_sheet_data
from pages.Analytics import expences_data_wrangle
expenses = get_sheet_data("Expenses")
expenses_df= expences_data_wrangle(expenses)
st.write(expenses_df)
