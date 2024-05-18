import streamlit as st
from streamlit_gsheets import GSheetsConnection


conn = st.experimental_connection("gsheets", type=GSheetsConnection)


# data = conn.read(worksheet="Products", usecols=list(range(5)))
data = conn.read(worksheet="Sales", usecols=list(range(5)))
st.dataframe(data)


st.subheader("Sales Health Check")
sql = '''
SELECT
    "NAME",
    UNIT_PRICE,
    "UNITS SOLD"
FROM
    Sales
WHERE
    "UNIT_PRICE > 10000"    
ORDER BY
    "UNITPRICE_" DESC;
'''

df_inventory_health = conn.query(sql=sql)
st.dateframe(df_inventory_health)



st.col  

