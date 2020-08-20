import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px


st.title("Motor Vehicle Collisions in New York City")
st.markdown("Application to visualize car accidents in the city of New York. ")

# Geting the data and keep the data in cache
@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(
        "./Data/Motor_Vehicle_Collisions_-_Crashes.csv",
        nrows=nrows,
        parse_dates=[["CRASH DATE", "CRASH TIME"]],
    )
    data.dropna(subset=["LONGITUDE", "LATITUDE"], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data.rename(columns={"crash date_crash time": "date/time"}, inplace=True)
    return data


# Loading the data
data = load_data(100000)
original_data = data

st.header("Where are the most people injured in NYC?")
injured_people = st.slider("Number of people injured in car accident", 0, 19, 3)

# Map of positions by number of people injured
st.map(
    data[data["number of persons injured"] >= injured_people][
        ["latitude", "longitude"]
    ].dropna(how="any")
)

# Filter number of colissions by hour of the day
st.header("How many collisions occure during a givin time in NYC?")
hour = st.slider("Hour to look at", 0, 23)
data = data[data["date/time"].dt.hour == hour]

st.markdown("Vehicles collision between %i:00 and %i:00" % (hour, hour + 1))

midpoint = (np.average(data["latitude"]), np.average(data["longitude"]))

st.pydeck_chart(
    pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": midpoint[0],
            "longitude": midpoint[1],
            "zoom": 12,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data[["date/time", "latitude", "longitude"]],
                get_position=["longitude", "latitude"],
                radius=75,
                extruded=True,
                pickable=True,
                elevation_scale=4,
                elevation_range=[0, 1000],
            ),
        ],
    )
)

# Filter number of accidents by minutes between to hours
st.header("Breackdown by minute between %i:00 and %i:00" % (hour, hour + 1))
filtered_data = data[
    (data["date/time"].dt.hour >= hour) & (data["date/time"].dt.hour < (hour + 1))
]
histogram = np.histogram(filtered_data["date/time"].dt.minute, bins=60)[0]
chart_data = pd.DataFrame({"minute": range(60), "crashes": histogram})
st.write(
    px.bar(
        chart_data,
        x="minute",
        y="crashes",
        hover_data=["minute", "crashes"],
        height=400,
        range_x=(0, 60),
    )
)

# Filter the top dangerous streets by affected type
st.header("Top 5 dangerous streets by affected type")
select = st.selectbox(
    "Affected type of people", ["Pedestrians", "Cyclist", "Motorists"]
)

if select == "Pedestrians":
    st.write(
        original_data[original_data["number of pedestrians injured"] >= 1][
            ["on street name", "number of pedestrians injured"]
        ]
        .sort_values(by=["number of pedestrians injured"], ascending=False)
        .dropna(how="any")[:5]
    )
elif select == "Cyclist":
    st.write(
        original_data[original_data["number of cyclist injured"] >= 1][
            ["on street name", "number of cyclist injured"]
        ]
        .sort_values(by=["number of cyclist injured"], ascending=False)
        .dropna(how="any")[:5]
    )
else:
    st.write(
        original_data[original_data["number of motorist injured"] >= 1][
            ["on street name", "number of motorist injured"]
        ]
        .sort_values(by=["number of motorist injured"], ascending=False)
        .dropna(how="any")[:5]
    )

# Show the original data in a table
if st.checkbox("Show Raw Data", False):
    st.subheader("Raw Data")
    st.write(data.head(300))

st.markdown(
    'Made with *Love!*  <a href="https://github.com/serdubon"> <img src="https://img.icons8.com/material-rounded/24/000000/github.png"/> </a> :heartbeat:',
    unsafe_allow_html=True,
)
