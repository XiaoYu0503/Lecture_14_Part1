import streamlit as st
import sqlite3
import pandas as pd

st.title("CWA Weather Data Viewer")
st.write("This app displays weather data fetched from the CWA API and stored in a local SQLite database.")

# Connect to database
db_path = "data.db"

try:
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM weather"
    df = pd.read_sql_query(query, conn)
    conn.close()

    st.subheader("Weather Data Table")
    st.dataframe(df)

    st.subheader("Temperature Overview")
    st.bar_chart(df.set_index("location")[["min_temp", "max_temp"]])

except Exception as e:
    st.error(f"Error reading database: {e}")
    st.info("Please run 'etl.py' first to generate the database.")
