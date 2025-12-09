import streamlit as st
import sqlite3
import pandas as pd

# Set page config for better title and layout
st.set_page_config(page_title="CWA 天氣預報", layout="wide", page_icon="🌤️")

# Custom CSS to make it look a bit more like a dashboard
st.markdown("""
    <style>
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌤️ 全臺天氣預報概況")
st.markdown("參考中央氣象局 (CWA) 資料，顯示各地區預報資訊。")

# Connect to database
db_path = "data.db"

def get_weather_icon(description):
    if "晴" in description and "雨" not in description:
        return "☀️"
    elif "雨" in description:
        return "🌧️"
    elif "雲" in description or "陰" in description:
        return "☁️"
    else:
        return "🌡️"

try:
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM weather"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Display as metrics in columns
    st.subheader("各地區預報")
    
    # Create a grid layout
    # We have 6 regions usually. 3 columns x 2 rows looks good.
    cols = st.columns(3)
    
    for index, row in df.iterrows():
        col = cols[index % 3]
        with col:
            icon = get_weather_icon(row['description'])
            temp_range = f"{row['min_temp']}°C - {row['max_temp']}°C"
            
            # Use a container for a card-like effect
            with st.container(border=True):
                st.markdown(f"### {row['location']}")
                st.markdown(f"#### {icon} {row['description']}")
                st.metric(label="氣溫範圍", value=temp_range)

    # Detailed Table
    st.markdown("---")
    st.subheader("詳細資料列表")
    
    # Style the dataframe
    st.dataframe(
        df, 
        use_container_width=True,
        column_config={
            "location": "地區",
            "min_temp": st.column_config.NumberColumn("最低溫 (°C)", format="%.1f°C"),
            "max_temp": st.column_config.NumberColumn("最高溫 (°C)", format="%.1f°C"),
            "description": "天氣現象"
        },
        hide_index=True
    )

except Exception as e:
    st.error(f"讀取資料庫時發生錯誤: {e}")
    st.info("請先執行 'etl.py' 以產生資料庫。")
