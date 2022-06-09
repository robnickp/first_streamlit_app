import streamlit
import pandas
import snowflake.connector
import requests
from urllib.error import URLError

streamlit.title('My Parents New Health diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
  
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# picklist for fruit
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like info about?')
  if not fruit_choice:
    streamlit.error('Please select a fruit to get info')
  else:
    fruityvice_resp = requests.get('https://fruityvice.com/api/fruit/' + fruit_choice)
    
    # take the json version of the resp and normalize it
    fruityvice_norm = pandas.json_normalize(fruityvice_resp.json())
    streamlit.dataframe(fruityvice_norm)
except URLError as e:
  streamlit.error()
    
streamlit.stop()

# snowflake stuff
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

add_my_fruit = streamlit.text_input('Add a fruit to the list')
streamlit.write('the user entered', add_my_fruit)
my_cur.execute("insert into FRUIT_LOAD_LIST (FRUIT_NAME) VALUES ('from streamlit')")
