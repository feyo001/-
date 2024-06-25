# import streamlit as st
# from streamlit_gsheets import GSheetsConnection
# import pandas as pd

# # Display Title and Description
# st.title("Sales Management Portal")
# st.markdown("Enter the details of products sold below:")

# # Establishing a Google Sheets connection
# @st.cache_resource
# def connect_to_gsheet():
#     conn = st.connection("gsheets", type=GSheetsConnection)
#     return conn


# # Get data
# def get_gsheet_tab(worksheet_name):
#     conn = connect_to_gsheet()
#     products_list = conn.read(worksheet=worksheet_name, usecols=list(range(5)), ttl=5)
#     return products_list

# products_df = get_gsheet_tab("Products")
# products_df = products_df.dropna(how='all')


# # existing_data = conn.read(worksheet="Sales", usecols=list(range(5)), ttl=5)
# sales_df = get_gsheet_tab("Sales")


# with st.form(key="sale_form"):
#     product_name = st.selectbox(label="Select Product Name*", options=products_df['NAME'], index=None)

#     # Check if product is selected (avoiding potential IndexError)
#     if product_name:
#         price = products_df.loc[products_df['NAME'] == product_name, 'UNIT_PRICE'].values[0]
#         product_reference = products_df.loc[products_df['NAME'] == product_name, 'REF'].values[0]
#     else:
#         price = 0  # Set a default value (optional)
#         product_reference =''

#     quantity = st.selectbox(label="Select Quantity*", options=list(range(1, 501)))
#     sale_date = st.date_input(label='Select Date*')

#     st.markdown("**required*")

#     submit_button = st.form_submit_button(label="Sell")

#     # If submit button is pressed
#     if submit_button:
#         if not product_name or not sale_date:
#             st.stop()
#         else:
#             sale_data = pd.DataFrame(
#                 {
#                     "NAME": [product_name],
#                     "REF": [product_reference],
#                     "DATE": [sale_date.strftime("%m/%d/%Y")],
#                     "UNITS": [quantity],
#                     "PRICE": [price * quantity],
#                 }
#             )

#             # Add the new sale data to existing data
#             update_df = pd.concat([sales_df, sale_data], ignore_index=True)

#             # Update Google Sheets with the new sales data
#             conn = connect_to_gsheet()
#             conn.update(worksheet="Sales", data=update_df)

#             st.success("Sales details successfully submitted!")





import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Display Title and Description
st.title("Sales Management Portal")
st.markdown("Enter the details of products sold below:")

# Establishing a Google Sheets connection
@st.cache_resource
def connect_to_gsheet():
    conn = st.connection("gsheets", type=GSheetsConnection)
    return conn

# Get data
@st.cache_data
def get_gsheet_tab(worksheet_name):
    conn = connect_to_gsheet()
    products_list = conn.read(worksheet=worksheet_name, usecols=list(range(5)), ttl=5)
    return products_list

products_df = get_gsheet_tab("Products")
products_df = products_df.dropna(how='all')

# Existing sales data
sales_df = get_gsheet_tab("Sales")

# Initialize session state variables
if 'selected_product' not in st.session_state:
    st.session_state.selected_product = products_df['NAME'][0]
if 'quantity' not in st.session_state:
    st.session_state.quantity = 1
if 'total_price' not in st.session_state:
    st.session_state.total_price = 0.0

def update_total_price():
    if st.session_state.selected_product and st.session_state.quantity:
        price = products_df.loc[products_df['NAME'] == st.session_state.selected_product, 'UNIT_PRICE'].values[0]
        st.session_state.total_price = price * st.session_state.quantity

# Create widgets outside the form
st.selectbox(
    label="Select Product Name*",
    options=products_df['NAME'],
    index=products_df['NAME'].tolist().index(st.session_state.selected_product),
    key='selected_product',
    on_change=update_total_price
)

st.selectbox(
    label="Select Quantity*",
    options=list(range(1, 501)),
    index=st.session_state.quantity - 1,
    key='quantity',
    on_change=update_total_price
)

st.date_input(label='Select Date*', key='sale_date')

# Display the total price
st.markdown(f"**Total Price: {st.session_state.total_price:,.0f}**")

# Form with submit button
with st.form(key="sale_form"):
    st.markdown("**required**")
    submit_button = st.form_submit_button(label="Sell")

# Ensure the total price is updated initially
update_total_price()

# If submit button is pressed
if submit_button:
    product_name = st.session_state.selected_product
    quantity = st.session_state.quantity
    sale_date = st.session_state.sale_date

    if not product_name or not sale_date:
        st.stop()
    else:
        price = products_df.loc[products_df['NAME'] == product_name, 'UNIT_PRICE'].values[0]
        product_reference = products_df.loc[products_df['NAME'] == product_name, 'REF'].values[0]

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
        update_df = pd.concat([sales_df, sale_data], ignore_index=True)

        # Update Google Sheets with the new sales data
        conn = connect_to_gsheet()
        conn.update(worksheet="Sales", data=update_df)

        st.success("Sales details successfully submitted!")
