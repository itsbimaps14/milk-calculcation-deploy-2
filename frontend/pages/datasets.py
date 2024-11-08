import streamlit as st
import pandas as pd
import numpy as np
import time
import requests
import json

st.title('Dataset')

# URL for the FastAPI endpoint
url_material = "http://127.0.0.1:8000/material_comp"
url_recipies = "http://127.0.0.1:8000/recipies"

def fetch_data(url):
    try:
        # Fetch data from FastAPI
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()

        # Parse JSON string to dictionary
        data_dict = json.loads(data)
        return data_dict
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")

# function get data
def get_material_data():
    return fetch_data(url_material)

def get_recipe_data():
    return fetch_data(url_recipies)

# for passing data
df_compositions = pd.DataFrame.from_dict(get_material_data())
df_recepies = pd.DataFrame.from_dict(get_recipe_data())

# Display the data in Streamlit
st.write("Data Composition : ")
st.dataframe(df_compositions)

st.write("Data Recipies : ")
st.dataframe(df_recepies)