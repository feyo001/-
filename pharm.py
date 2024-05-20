import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Display Title and Description
st.title("Sales Management Portal")
st.markdown("Enter the details of products sold below:")

# Establishing a Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)


# Get all products
def get_products():
    products_list = conn.read(worksheet="Products", usecols=list(range(5)), ttl=5)
    return products_list

products_df = get_products()
products_df = products_df.dropna(how='all')


existing_data = conn.read(worksheet="Sales", usecols=list(range(5)), ttl=5)


with st.form(key="sale_form"):
    product_name = st.selectbox(label="Select Product Name*", options=products_df['NAME'], index=None)

    # Check if product is selected (avoiding potential IndexError)
    if product_name:
        price = products_df.loc[products_df['NAME'] == product_name, 'UNIT_PRICE'].values[0]
        product_reference = products_df.loc[products_df['NAME'] == product_name, 'REF'].values[0]
    else:
        price = 0  # Set a default value (optional)
        product_reference =''

    quantity = st.selectbox(label="Select Quantity*", options=list(range(1, 501)))
    sale_date = st.date_input(label='Select Date*')

    st.markdown("**required*")

    submit_button = st.form_submit_button(label="Sell")

    # If submit button is pressed
    if submit_button:
        if not product_name or not sale_date:
            st.stop()
        else:
            sale_data = pd.DataFrame(
                {
                    "NAME": [product_name],
                    "REF": [product_reference],
                    "DATE": [sale_date.strftime("%m/%d/%Y")],
                    "UNITS": [quantity],
                    "PRICE": [price * quantity],
                }
            )

            # Add the new sale data to existing data
            update_df = pd.concat([existing_data, sale_data], ignore_index=True)

            # Update Google Sheets with the new sales data
            conn.update(worksheet="Sales", data=update_df)

            st.success("Sales details successfully submitted!")

