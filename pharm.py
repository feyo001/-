import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Display Title and Description
st.title("Sales Management Portal")
st.markdown("Enter the details of products sold below:")

# Establishing a Google Sheets connection
conn = st.experimental_connection("gsheets", type=GSheetsConnection)

# Get all products
def get_products():
    products_list = conn.read(worksheet="Products", usecols=list(range(5)), ttl=5)
    return products_list

products_df = get_products()
products_df = products_df.dropna(how='all')

# st.write("Select Product")
# st.dataframe(products_df.loc[:,'NAME'])
# st.dataframe(products_df['NAME'])

existing_data = conn.read(worksheet="Sales", usecols=list(range(5)), ttl=5)
# st.dataframe(existing_data)


with st.form(key="sale_form"):
    product_name = st.selectbox(label="Select Product Name*", options=products_df['NAME'], index=None)
    sale_date = st.date_input(label='Select Date*')
    unit = st.selectbox(label="Select Quantity*", options=list(range(1,501)))

    st.markdown("**required*")

    submit_button = st.form_submit_button(label="Sell")

    # If submit button is pressed
    if submit_button:
        if not product_name or not sale_date:
            st.stop()
        else:
            # Create a new row of sale data
            # sale_data = pd.DataFrame(
            #     {
            #         "NAME": product_name,
            #         "DATE": sale_date.strftime("%m/%d/%Y"),
            #         "UNITS": unit

            #     }
            # )
            sale_data = pd.DataFrame(
                {
                    "NAME": [product_name],
                    "DATE": [sale_date.strftime("%m/%d/%Y")],
                    "UNITS": [unit]
                }
            )


            # Add the new sale data to existing data
            update_df = pd.concat([existing_data, sale_data], ignore_index=True)
        
            # Update Google Sheets withthe new sales data
            conn.update(worksheet="Sales", data=update_df)



    # if submit_button:
    #     st.write("You clicked submt")

