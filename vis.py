import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

def create_choropleth_map(filtered_df):
    st.header("Total Medals by Country")

    # Sidebar: Filter options
    season_options = st.sidebar.multiselect("Select Seasons", filtered_df["Season"].unique())
    type_options = st.sidebar.multiselect("Select Type", filtered_df["Type"].unique())
    year_range = st.sidebar.slider(
        "Select a Year Range",
        min(filtered_df["Year"]),
        max(filtered_df["Year"]),
        (min(filtered_df["Year"]), max(filtered_df["Year"]))
    )

    # Apply filters
    filtered_df = filtered_df[(filtered_df["Season"].isin(season_options)) &
                              (filtered_df["Type"].isin(type_options)) &
                              (filtered_df["Year"] >= year_range[0]) &
                              (filtered_df["Year"] <= year_range[1])]

    # Group by country and calculate the total number of medals
    country_medal_counts = filtered_df.groupby("Country")["Medal"].count().reset_index()

    # Create a choropleth map using Plotly Express
    fig = px.choropleth(
        country_medal_counts,
        locations="Country",
        locationmode="country names",
        color="Medal",
        color_continuous_scale="Viridis",
        title="Total Medals by Country",
    )

    # Customize the map
    fig.update_geos(
        resolution=110,
        showcoastlines=True,
        coastlinecolor="Black",
        showland=True,
        landcolor="White",
    )

    # Display the choropleth map
    st.plotly_chart(fig, use_container_width=True)

def create_participating_countries_bar_chart(filtered_df):
    st.header("Total Participating Countries per Year")

    # Sidebar: Filter options
    season_options = st.sidebar.multiselect("Select Seasons", filtered_df["Season"].unique())
    type_options = st.sidebar.multiselect("Select Type", filtered_df["Type"].unique())

    # Apply filters
    filtered_df = filtered_df[(filtered_df["Season"].isin(season_options)) &
                              (filtered_df["Type"].isin(type_options))]

    # Group by year and count the number of unique countries for each year
    country_counts = filtered_df.groupby("Year")["Country"].nunique().reset_index()

    # Create a bar chart using Plotly Express
    fig = px.bar(
        country_counts,
        x="Year",
        y="Country",
        title="Total Participating Countries per Year",
        labels={"Year": "Year", "Country": "Number of Countries"},
    )

    # Display the bar chart
    st.plotly_chart(fig, use_container_width=True)

def participants_per_year(df):
    st.header("Participants per Year (Male Vs Female)")

    # Sidebar: Filter options
    season_options = st.sidebar.multiselect("Select Seasons", df["Season"].unique())
    type_options = st.sidebar.multiselect("Select Type", df["Type"].unique())

    # Filter the data for male participants
    male_df = df[(df['Sex'] == 'M') & (df['Season'].isin(season_options)) & (df['Type'].isin(type_options))]

    # Filter the data for female participants
    female_df = df[(df['Sex'] == 'F') & (df['Season'].isin(season_options)) & (df['Type'].isin(type_options))]

    # Group the data by year and count the number of participants
    male_participants = male_df.groupby('Year')['ID'].count().reset_index()
    female_participants = female_df.groupby('Year')['ID'].count().reset_index()

    # Create a line chart using Plotly Express
    fig = px.line(title="Number of Participants per Year")
    fig.add_trace(px.line(male_participants, x='Year', y='ID', color_discrete_sequence=['blue']).data[0])
    fig.add_trace(px.line(female_participants, x='Year', y='ID', color_discrete_sequence=['pink']).data[0])

    # Customize the chart
    fig.update_layout(xaxis_title="Year", yaxis_title="Number of Participants")
    fig.update_traces(mode='markers+lines')

    # Display the line chart
    st.plotly_chart(fig, use_container_width=True)

def MF_sunburst_graph(df):
    st.header("Sunburst Graph: Male vs Female Participants by Medal Category")

    # Sidebar: Filter options
    season_options = st.sidebar.multiselect("Select Seasons", df["Season"].unique())
    type_options = st.sidebar.multiselect("Select Type", df["Type"].unique())
    
    # Filter the data based on selected Season and Type
    filtered_df = df[(df['Season'].isin(season_options)) & (df['Type'].isin(type_options))]

    # Filter years based on selected Season
    filtered_years = sorted(filtered_df["Year"].unique(), reverse=True)  # Sort in descending order
    selected_year = st.sidebar.selectbox("Select a Year", filtered_years)

    # Convert "Country" column to strings and filter data by selected country
    selected_country = st.sidebar.selectbox("Select a Country", ["All Countries"] + sorted(filtered_df["Country"].astype(str).unique()))
    
    if selected_country != "All Countries":
        filtered_df = filtered_df[filtered_df["Country"].astype(str) == selected_country]

    # Create a sunburst chart using Plotly Express
    fig = px.sunburst(
        filtered_df,
        path=["Sex", "Medal", "Sport"],
        color="Sex",
        color_discrete_map={"M": "blue", "F": "pink"},
        title=f"Male vs Female Participants by Medal Category ({selected_year})",
    )

    # Customize the sunburst chart
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        sunburstcolorway=["gold", "silver", "brown"],  # Customize medal colors
    )

    # Display the sunburst chart
    st.plotly_chart(fig, use_container_width=True)

def scatterplot_medals_by_year(df):
    st.header("Scatterplot: Olympic Medals Over the Years")

    # Sidebar: Filter options
    season_options = st.sidebar.multiselect("Select Seasons", df["Season"].unique())
    type_options = st.sidebar.multiselect("Select Type", df["Type"].unique())

    # Filter the data based on selected Season and Type
    filtered_df = df[(df['Season'].isin(season_options)) & (df['Type'].isin(type_options))]

    # Exclude "No Medal" entries
    filtered_df = filtered_df[filtered_df['Medal'] != 'No Medal']

    # Group the data by 'Year' and 'Medal' columns and count the occurrences
    medal_counts = filtered_df.groupby(['Year', 'Medal']).size().reset_index(name='Medal Count')

    # Create a scatter plot
    fig = px.scatter(
        medal_counts, x='Year', y='Medal Count', color='Medal',
        title='Olympic Medals Over the Years', labels={'Medal Count': 'Count'}
    )

    # Configure the x-axis tick values to display 8-year intervals
    fig.update_xaxes(tickvals=list(range(min(medal_counts['Year']), max(medal_counts['Year']) + 1, 8)))

    # Display the scatter plot
    st.plotly_chart(fig, use_container_width=True)

def stacked_bar_medal_counts(df):
    st.header("Stacked Bar Chart: Medal Counts by Country and Medal Category")

    # Sidebar: Filter options
    season_options = st.sidebar.multiselect("Select Seasons", df["Season"].unique())
    type_options = st.sidebar.multiselect("Select Type", df["Type"].unique())
    
    # Filter the data based on selected Season and Type
    filtered_df = df[(df['Season'].isin(season_options)) & (df['Type'].isin(type_options))]

    # Create a slider for selecting a year within the chosen season
    selected_season = st.sidebar.selectbox("Select a Season", season_options)
    years_in_season = filtered_df[filtered_df['Season'] == selected_season]['Year'].unique()

    if len(years_in_season) > 0:
        selected_year = st.sidebar.slider("Select a Year", min_value=min(years_in_season), max_value=max(years_in_season))
    else:
        selected_year = None

    # Filter the data by the selected year (if a year is selected)
    if selected_year is not None:
        filtered_df = filtered_df[filtered_df['Year'] == selected_year]

    # Group the data by 'Country' and 'Medal' columns and count the occurrences
    medal_counts = filtered_df.groupby(['Country', 'Medal']).size().reset_index(name='Count')

    # Create a stacked bar chart
    fig = px.bar(
        medal_counts, x='Country', y='Count', color='Medal',
        title='Medal Counts by Country and Medal Category', labels={'Count': 'Medal Count'},
        barmode='stack'
    )

    # Customize layout
    fig.update_layout(
        xaxis_title="Country",
        yaxis_title="Medal Count",
        legend_title="Medal",
    )

    # Display the stacked bar chart
    st.plotly_chart(fig, use_container_width=True)    

def stacked_bar_total_medals(df):
    st.header("Stacked Bar Chart: Total Medals by Country")

    # Sidebar: Filter options
    season_options = st.sidebar.multiselect("Select Seasons", df["Season"].unique())
    type_options = st.sidebar.multiselect("Select Type", df["Type"].unique())

    # Filter the data based on selected Season and Type
    filtered_df = df[(df['Season'].isin(season_options)) & (df['Type'].isin(type_options))]

    # Create a slider for selecting a year within the chosen season(s)
    selected_seasons = st.sidebar.multiselect("Select Season(s)", season_options)
    
    # Filter the data by the selected season(s)
    years_in_season = filtered_df[filtered_df['Season'].isin(selected_seasons)]['Year'].unique()

    if len(years_in_season) > 0:
        selected_year = st.sidebar.slider("Select a Year", min_value=min(years_in_season), max_value=max(years_in_season))
        # Filter the data by the selected year (if a year is selected)
        filtered_df = filtered_df[filtered_df['Year'] == selected_year]
    else:
        selected_year = None

    # Exclude "No Medal" entries
    filtered_df = filtered_df[filtered_df['Medal'] != 'No Medal']

    # Group the data by 'Country' and count the occurrences
    medal_counts = filtered_df.groupby('Country').size().reset_index(name='Count')

    # Sort countries by total medal count in descending order
    medal_counts = medal_counts.sort_values(by='Count', ascending=False)

    # Create a stacked bar chart
    fig = px.bar(
        medal_counts, x='Country', y='Count',
        title='Total Medals by Country', labels={'Count': 'Medal Count'},
        color_discrete_sequence=['royalblue']
    )

    # Customize layout
    fig.update_layout(
        xaxis_title="Country",
        yaxis_title="Medal Count",
    )

    # Display the stacked bar chart
    st.plotly_chart(fig, use_container_width=True)
