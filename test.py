import pandas as pd
import streamlit as st

# Setup some sample data
data = {
    "Name": ["Alice", "Bob", "Charlie", "Diana"],
    "Age": [28, 30, 20, 27],
    "City": ["New York", "London", "Paris", "Tokyo"],
    "Active": [True, False, True, True],
}

df = pd.DataFrame(data)

st.title("Streamlit Table Demo")

# Method 1: Interactive Dataframe
st.subheader("1. Interactive Dataframe")
st.write("This version allows users to sort columns and resize the table.")
st.dataframe(df)

# Method 2: Static Table
st.subheader("2. Static Table")
st.write("This is a traditional, non-interactive table.")
st.table(df)