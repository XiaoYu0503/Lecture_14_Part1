# Conversation Log - Lecture 14 Part 1

**Date:** 2025-12-09

## Summary of Actions

1.  **Initial Setup**:
    -   Created project folder structure.
    -   Created `inspect_data.py` to analyze the CWA API JSON structure.
    -   Identified key data fields: Location Name, Min Temp, Max Temp, Weather Description.

2.  **ETL Process Implementation**:
    -   Created `etl.py` to:
        -   Download JSON data from CWA API.
        -   Parse the JSON to extract weather forecasts.
        -   Create a SQLite database (`data.db`) with a `weather` table.
        -   Insert parsed data into the database.
    -   Ran `etl.py` to populate the initial database.

3.  **Streamlit App Development**:
    -   Created `app.py` to visualize the data.
    -   Implemented a basic table and bar chart view.
    -   Created `requirements.txt` with dependencies (`streamlit`, `pandas`, `requests`).
    -   Created `README.md` with usage instructions.

4.  **Version Control (Git/GitHub)**:
    -   Initialized a local Git repository.
    -   Committed all files.
    -   Added remote origin: `https://github.com/XiaoYu0503/Lecture_14_Part1`.
    -   Pushed code to the `main` branch.

5.  **UI Improvements (Dashboard Style)**:
    -   Updated `app.py` to mimic the CWA website style.
    -   Added card-like layout for each region.
    -   Added weather icons (☀️, 🌧️, ☁️) based on descriptions.
    -   Pushed updates to GitHub.

6.  **Map Visualization**:
    -   Investigated API for coordinates (found none).
    -   Updated `etl.py` to include hardcoded coordinates for Taiwan's regions.
    -   Updated database schema to include `lat` and `lon`.
    -   Re-ran `etl.py` to update `data.db`.
    -   Updated `app.py` to use `pydeck` for map visualization.
    -   Added `pydeck` to `requirements.txt`.
    -   Pushed updates to GitHub.

7.  **Bug Fix (Blank Map)**:
    -   Identified issue with Mapbox style requiring an API token.
    -   Updated `app.py` to remove the explicit `map_style` argument, reverting to the default Streamlit map style.
    -   Pushed the fix to GitHub.

8.  **Documentation**:
    -   Created this log file (`conversation_log.md`) to record the session history.
    -   Uploading this log to GitHub.
