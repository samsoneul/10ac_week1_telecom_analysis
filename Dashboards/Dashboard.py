import streamlit as st
import pandas as pd 
import sys
import os 
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler



sys.path.append('C:\\Users\\Ourba\\Desktop\\10Academy\\10ac_week1_telecom_analysis\\src')
print(os.getcwd())
df=pd.read_csv('./Dashboards/final_df.csv')
from utils import DataProcessor
DataProcessor=DataProcessor()

# Function to preprocess categorical data
def preprocess_categorical_data(df):
    df[["Handset Manufacturer", "Handset Type"]] = DataProcessor.preproccess_categorical_data(df[["Handset Manufacturer", "Handset Type"]])

# Function to plot top 10 handsets
def plot_top_10_handsets(df):
    value_counts = df["Handset Type"].value_counts().reset_index()
    value_counts.columns=['Handset Type','Handset count']
    top_ten_values = value_counts.head(10)
    top_ten_values = top_ten_values[top_ten_values['Handset Type'] != 'undefined']

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='Handset count', y='Handset Type', data=top_ten_values, palette='Blues', orient='h', ci=None, ax=ax)
    plt.title('Top 10 Handsets Used')
    plt.xlabel('Handset count')
    plt.ylabel('Handset Type')
    plt.xticks(rotation=45)
    st.pyplot(fig)




# Function to display top 3 handset manufacturers
def display_top_manufacturers(df):
    value_counts = df["Handset Manufacturer"].value_counts()
    top_three_values = value_counts.head(3)

    fig, ax = plt.subplots(figsize=(8, 5))
    plt.bar(top_three_values.index, top_three_values.values)
    plt.title('Top 3 Handset Manufacturers')
    plt.xlabel('Manufacturer')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    st.pyplot(fig)

def perform_engagement_analysis(df):
    # Calculate session frequency per customer (MSISDN)
    session_frequency = df.groupby('MSISDN/Number').size().reset_index(name='Session Frequency')

    # Calculate session duration per customer (MSISDN) in milliseconds
    session_duration = df.groupby('MSISDN/Number')['Dur. (ms)'].sum().reset_index(name='Session Duration (ms)')

    # Calculate total session traffic (download + upload) per customer (MSISDN) in bytes
    session_traffic = df.groupby('MSISDN/Number')[['Total UL (Bytes)', 'Total DL (Bytes)']].sum().sum(axis=1).reset_index(name='Total Session Traffic (Bytes)')

    # Merge the aggregated metrics into a single DataFrame
    engagement_metrics = pd.merge(session_frequency, session_duration, on='MSISDN/Number')
    engagement_metrics = pd.merge(engagement_metrics, session_traffic, on='MSISDN/Number')

    # Rank the customers based on each engagement metric
    engagement_metrics['Rank - Session Frequency'] = engagement_metrics['Session Frequency'].rank(ascending=False)
    engagement_metrics['Rank - Session Duration'] = engagement_metrics['Session Duration (ms)'].rank(ascending=False)
    engagement_metrics['Rank - Total Session Traffic'] = engagement_metrics['Total Session Traffic (Bytes)'].rank(ascending=False)

    return engagement_metrics

# Function to plot engagement metrics
def plot_engagement_metrics(engagement_metrics):
    # Visualize the results
    metrics = ['Session Frequency', 'Session Duration (ms)', 'Total Session Traffic (Bytes)']

    # Reshape the data for plotting
    plot_data = pd.melt(engagement_metrics, id_vars=['Cluster'], var_name='Metric', value_name='Value')

    # Plot grouped bar charts
    plt.figure(figsize=(12, 8))
    sns.barplot(x='Metric', y='Value', hue='Cluster', data=plot_data, ci=None)
    plt.title('Comparison of Engagement Metrics Across Clusters')
    plt.xlabel('Engagement Metric')
    plt.ylabel('Value')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Cluster', loc='upper right')
    st.pyplot(plt.gcf())



# Load data
@st.cache_data


# Main function to run the Streamlit app

def main():
    st.title('Telecom Data Analysis Dashboard')

    # Load data
    

    # Sidebar for navigation
    
    # Overview Analysis dashboard
    if dashboard_option == 'Overview Analysis':
        st.header('Overview Analysis')

        preprocess_categorical_data(df)

        st.subheader('Top 10 Handsets Used')
        plot_top_10_handsets(df)

        st.subheader('Top 3 Handset Manufacturers')
        display_top_manufacturers(df)

    if dashboard_option == 'Engagement Analysis':
        st.header('Engagement Analysis')

        # Perform engagement analysis
        engagement_metrics = perform_engagement_analysis(df)

        # Run k-means clustering with k=3
        scaler = StandardScaler()
        normalized_metrics = scaler.fit_transform(engagement_metrics[['Session Frequency', 'Session Duration (ms)', 'Total Session Traffic (Bytes)']])
        kmeans = KMeans(n_clusters=3, random_state=42)
        engagement_metrics['Cluster'] = kmeans.fit_predict(normalized_metrics)

        # Plot engagement metrics
        plot_engagement_metrics(engagement_metrics)
    


        
        
dashboard_option = st.sidebar.selectbox('Select Dashboard', 
                                            ['Overview Analysis', 'Engagement Analysis', 'Experience Analysis', 'Satisfaction Analysis'])
        

    

# Run the app
if __name__ == '__main__':
    main()
