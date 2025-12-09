import streamlit as st
import sqlite3
import pandas as pd
import pydeck as pdk

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

    # Map Visualization
    st.subheader("臺灣天氣地圖")
    
    # Prepare data for map
    # We want to show temperature on the map.
    # Pydeck needs a layer.
    
    # Add a column for tooltip or display
    df['temp_display'] = df.apply(lambda row: f"{row['min_temp']} - {row['max_temp']}°C", axis=1)
    df['icon'] = df['description'].apply(get_weather_icon)
    
    # Define a layer to display text (Temperature)
    text_layer = pdk.Layer(
        "TextLayer",
        df,
        pickable=True,
        get_position='[lon, lat]',
        get_text='temp_display',
        get_size=16,
        get_color=[0, 0, 0],
        get_angle=0,
        # Note: TextLayer anchors are a bit tricky, usually center is default
        get_text_anchor='"middle"',
        get_alignment_baseline='"center"'
    )

    # Define a layer for the location name (above temp)
    name_layer = pdk.Layer(
        "TextLayer",
        df,
        pickable=True,
        get_position='[lon, lat]',
        get_text='location',
        get_size=14,
        get_color=[0, 0, 128], # Navy blue
        get_pixel_offset=[0, -20], # Shift up
        get_text_anchor='"middle"',
        get_alignment_baseline='"center"'
    )
    
    # Define a layer for scatter plot (dots) to mark the spot
    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        df,
        get_position='[lon, lat]',
        get_color=[255, 0, 0, 160],
        get_radius=5000, # 5km radius
    )

    # Set the view state
    view_state = pdk.ViewState(
        latitude=23.7,
        longitude=121.0,
        zoom=7,
        pitch=0,
    )

    # Render the deck.gl map
    r = pdk.Deck(
        layers=[scatter_layer, name_layer, text_layer],
        initial_view_state=view_state,
        tooltip={"text": "{location}\n{description}\n{min_temp}°C - {max_temp}°C"},
        # Remove explicit map_style to use Streamlit's default (which doesn't require a token)
        # map_style="mapbox://styles/mapbox/light-v9" 
    )
    
    st.pydeck_chart(r)


    # Display as metrics in columns
    st.subheader("各地區預報詳細")
    
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
        df[['location', 'min_temp', 'max_temp', 'description']], 
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
