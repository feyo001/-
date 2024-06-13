import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Display Title and Description
st.title("Expense Form")
st.markdown("Enter the details of expenses made:")

# Establishing a Google Sheets connection
# @st.cache_resource
def connect_to_gsheet():
    conn = st.connection("gsheets", type=GSheetsConnection)
    return conn


# Get data
@st.cache_data
def get_gsheet_tab(worksheet_name):
    conn = connect_to_gsheet()
    expense_form = conn.read(worksheet=worksheet_name, usecols=list(range(4)), ttl=5)
    return expense_form

expenses_df = get_gsheet_tab("Expenses")
# expenses_df = expenses_df.dropna(how='all')
# st.write(expenses_df['Item'].str.strip().unique())


left_col, right_col = st.columns([1,1])
with left_col:
    with st.form(key="expense_form"):
        expense_date = st.date_input("Select Date")
        item = st.selectbox(label="Select Expense", options=expenses_df['Item'].str.strip().unique(), index=None)
        description = st.text_input("Description",max_chars=200)
        amount = st.number_input(label="Total Amount") 
    
        submit_button = st.form_submit_button(label='Post')
        if submit_button:
            if not item and amount:
                st.stop()
            else:  
                expense_data = pd.DataFrame(
                    {
                        "Date":[expense_date.strftime("%d/%m/%Y")],
                        "Item":[item],
                        "Description":[description],
                        "Amount":[amount],
                    }
                )
                
                # Add the new sale data to existing data
                update_df = pd.concat([expenses_df, expense_data], ignore_index=True)

                conn = connect_to_gsheet()
                conn.update(worksheet="Expenses", data=update_df)
                
           st.success("Expense details successfully submitted!")

                # Clear cache for expenses_df on successful submission (prevents outdated data)
           st.session_state["expense_form"] = {}
           st.cache_data.clear()

@st.experimental_fragment
def daily_expense_view():
    expense_date = st.date_input("Select Date")
    expenses_df['Date'] = pd.to_datetime(expenses_df['Date'], format='%d/%m/%Y')
    expenses_df['Date'] = expenses_df['Date'].dt.date
    temp = expenses_df.query('Date == @expense_date').reset_index(drop=True)
    st.write(temp)
              

with right_col:
    with st.expander("View Expense Table", expanded=False):
        daily_expense_view()
        



