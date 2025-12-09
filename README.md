# CWA Weather Data App

This project fetches weather data from the Central Weather Administration (CWA) API, stores it in a SQLite database, and displays it using a Streamlit app.

## Setup

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Fetch Data**: Run the ETL script to download data and populate the database.
    ```bash
    python etl.py
    ```
    This will create a `data.db` file.

2.  **Run App**: Start the Streamlit application.
    ```bash
    streamlit run app.py
    ```

## Screenshot for Assignment

Once the app is running, take a screenshot of the browser window showing the data table and chart.
