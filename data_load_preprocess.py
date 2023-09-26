import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    # Load the dataset_olympics.csv and noc_region.csv files
    df = pd.read_csv("dataset_olympics.csv")
    df2 = pd.read_csv("noc_region.csv")
    
    # Replace NaN values in the "Medal" column with "No Medal"
    df['Medal'].fillna("No Medal", inplace=True)
    
    # Merge df and df2 to add the "Country" column
    df = df.merge(df2[['noc_region', 'reg']], left_on='NOC', right_on='noc_region', how='left')
    
    # Rename the newly added "reg" column to "Country"
    df.rename(columns={'reg': 'Country'}, inplace=True)
    
    # Drop the redundant "noc_region" column and other columns from df2 if needed
    df.drop(columns=['noc_region'], inplace=True)
    
    # Create new columns for Gold, Silver, and Bronze counts
    df['Gold'] = df['Medal'].apply(lambda x: x.count('Gold'))
    df['Silver'] = df['Medal'].apply(lambda x: x.count('Silver'))
    df['Bronze'] = df['Medal'].apply(lambda x: x.count('Bronze'))
    
    # # Filter out rows with "No Medal" in the "Medal" column
    # df = df[df['Medal'] != 'No Medal']
    
    return df
