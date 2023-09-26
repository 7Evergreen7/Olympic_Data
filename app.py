# Import necessary libraries for using Streamlit
import streamlit as st
from data_load_preprocess import load_data
import vis as visuals

# Load data using the data_loader
preprocessed_df = load_data()

# # Call the preprocessing function
# preprocessed_df = data_processing.preprocess_data(df1, df2)

# Create a sidebar for the main page
st.sidebar.title("Filters")

# Page selection
page = st.sidebar.radio("Select Page", ["Main Page", "Visualizations"])

if page == "Main Page":
    # Main page content goes here, unrelated to filters
    # Unicode characters for filled circles (●) and medals (🥇 🥈 🥉)
    # olympic_rings = "●" * 5
    # olympic_rings = 🔵🟡🔴⚫⚪
    medals = "🥇 🥈 🥉"

    # Display the title with Olympic rings and medals
    # Insert the Olympic logo image
    olympic_logo = 'Olympic_cover.jpg'  # Replace with the actual filename of your logo image
    st.image(olympic_logo, use_column_width=True)  # Adjust image size as needed
    
    st.title(f'OLYMPIC PERFORMANCE DASHBOARD {medals}')

    st.header("**Finding the best performing countries and athletes in the Olympics**", divider='green')

    st.write('''The ***Olympic Games*** are one of the most prestigious international multi-sport event held every four years in which athletes from around the globe participate in various sports competitions. The main aim of the Olympics is to promote unity, friendship, and fair play among nations.
    The purpose of this dashboard is to present different insights and patterns throughout the Olympic history.
    The dataset comprises all Summer and Winter Games from 1896 Athens to 2016 Rio de Janeiro. It is collected from [Kaggle's Olympic Data](https://www.kaggle.com/datasets/bhanupratapbiswas/olympic-data).''')

    # Custom footer
    st.markdown(
        """<div style="display: flex; justify-content: space-between; padding-top: 10px; font-size: 12px;">
            <div>Made with Streamlit</div>
            <div style="font-style: italic;">Developed by Talar Boyajian for AUB OSB-MSBA325</div>
        </div>""",
        unsafe_allow_html=True
    )
    # Display a checkbox to show data
    show_data = st.checkbox("Show Sample Data")

    # Check if the "Show Data" checkbox is selected
    if show_data:
        # Display the first 10 rows of the preprocessed DataFrame
        st.markdown('💾 The Data:')
        st.dataframe(preprocessed_df.head(10))

        # Define data loading state text
        data_load_state = st.empty()
        data_load_state.text("Data displayed!")
else:  # if page == "Visualizations":
    medals = "🥇 🥈 🥉"
    st.title(f'VISUALIZATIONS {medals}')

    # Create buttons for selecting visualizations in the sidebar
    visualization_option = st.sidebar.radio("Select Visualization", [
        "Map of Medals",
        "Participating countries by year",
        "Athletes across the years",
        "Medals across the years",
        "Top countries",
        "Medals by Country",
        "Male Vs Female performance"
     ])
    
    if visualization_option == "Map of Medals":
        visuals.create_choropleth_map(preprocessed_df)
    elif visualization_option == "Participating countries by year":
        visuals.create_participating_countries_bar_chart(preprocessed_df)
    elif visualization_option == "Athletes across the years":
        visuals.participants_per_year(preprocessed_df)
    elif visualization_option == "Medals across the years":
        visuals.scatterplot_medals_by_year(preprocessed_df)
    elif visualization_option == "Top countries":
        visuals.stacked_bar_total_medals(preprocessed_df)
    elif visualization_option == "Medals by Country":
        visuals.stacked_bar_medal_counts(preprocessed_df)      
    elif visualization_option == "Male Vs Female performance":
        visuals.MF_sunburst_graph(preprocessed_df)
