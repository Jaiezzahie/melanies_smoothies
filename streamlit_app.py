import streamlit as st
import requests
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Customise Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie")

name_on_order = st.text_input("Name on Smoothie: ")
st.write("The name on your smoothie is", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingrediants_list = st.multiselect('Choose uo to 5 ingredients:', my_dataframe, max_selections=5)

if ingrediants_list:
    ingredients_string = ''

    for fruit_chosen in ingrediants_list:
        ingredients_string += fruit_chosen + ' '

    my_insert_stmt = """ INSERT INTO smoothies.public.orders(ingredients, name_on_order)
            VALUES ('""" + ingredients_string + """', '""" + name_on_order + """')"""
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)
