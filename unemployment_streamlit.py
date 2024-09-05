import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Load the data
data = pd.read_csv('unemployment.csv')

# Rename columns
data.columns = ["State", "Date", "Frequency", "Estimated Unemployment Rate", "Estimated Employed",
                "Estimated Labour Participation Rate", "Region", "Longitude", "Latitude"]

# Convert 'Date' to datetime format
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

# Sidebar filters for Region and State
st.sidebar.title("Filters")
selected_region = st.sidebar.multiselect("Regions", options=data["Region"].unique(), default=data["Region"].unique())
selected_state = st.sidebar.multiselect("States", options=data["State"].unique(), default=data["State"].unique())

# Filter data based on selection
filtered_data = data[(data["Region"].isin(selected_region)) & (data["State"].isin(selected_state))]

# Interactive Correlation Heatmap
st.title("Covid-19 Unemployment Analysis")
st.text("""
        This is an interactive app that allows you to analyze unemployment rate in India 
        during Covid. You can choose from multiple states and regions and understand how the
        data changes as you filter the data according to your choice.
        """)


# Dynamic Histograms
st.subheader("Distribution of Estimated Employed")
st.text("""
        This is an interactive histogram of the distribution of Estimated Employed 
        and allows you to select the number of bins.
        """)
bins_employed = st.slider("Number of Bins for Estimated Employed", min_value=5, max_value=50, value=20)
fig, ax = plt.subplots()
sns.histplot(filtered_data, x="Estimated Employed", bins=bins_employed, hue="Region", ax=ax)
st.pyplot(fig)

st.subheader("Distribution of Estimated Unemployment Rate")
st.text("""
        This is an interactive histogram of the distribution of Estimated Unemployment Rate 
        and allows you to select the number of bins.
        """)
bins_unemployment = st.slider("Number of Bins for Estimated Unemployment Rate", min_value=5, max_value=50, value=20)
fig, ax = plt.subplots()
sns.histplot(filtered_data, x="Estimated Unemployment Rate", bins=bins_unemployment, hue="Region", ax=ax)
st.pyplot(fig)

# Sunburst Chart
st.subheader("Regional Sunburst Chart")
st.text("""
        This is an interactive sunburst chart based on the State and Region filters,
        with Region at the root and States at the node.
        """)
data_frame = filtered_data[["State", "Region", "Estimated Unemployment Rate"]]
fig = px.sunburst(data_frame, path=["Region", "State"], values="Estimated Unemployment Rate", width=600, height=600)
st.plotly_chart(fig)

# Time Series Analysis
st.subheader("Unemployment Rate Over Time")
st.text("""
        This is an interactive line chart that allows you to see the unemployment rate 
        for different states within the selected time period.
        """)
if 'Date' in data.columns:
    min_date = data['Date'].min()
    max_date = data['Date'].max()
    start_date = st.date_input("Start Date", min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.date_input("End Date", min_value=min_date, max_value=max_date, value=max_date)
    filtered_data_ts = filtered_data[(filtered_data["State"].isin(selected_state)) &
                                     (filtered_data['Date'] >= pd.to_datetime(start_date)) &
                                     (filtered_data['Date'] <= pd.to_datetime(end_date))]
    fig = px.line(filtered_data_ts, x='Date', y='Estimated Unemployment Rate', color='State')
    st.plotly_chart(fig)
else:
    st.write("Invalid dates for Time Series Analysis.")

st.text("""
        Thank you for visiting.
        Please come back soon.
        """)