import pandas as pd
import streamlit as st
import plotly.express as px

# Streamlit Title
st.title("Google Form Responses Dashboard")
st.subheader("Visualize and Analyze Product Distribution Data")

# Google Sheets Public URL
sheet_url = "https://docs.google.com/spreadsheets/d/1Uiu2k6612HQWJbOSj-fWY_ZdrFuPEv0s7OL12oH-KIk/export?format=csv&gid=1398230424"

# Load the data from Google Sheets (CSV export link), and set header row to 2 (index 1)
df = pd.read_csv(sheet_url, header=1)  # Read the second row as the header

# Clean column names: Strip any extra spaces or special characters
df.columns = df.columns.str.strip()

# Convert the 'How many?' column to numeric values, handling non-numeric values (errors='coerce' will convert invalid entries to NaN)
df['How many?'] = pd.to_numeric(df['How many?'], errors='coerce')

# Group by 'Product type:' and calculate the sum of 'How many?' to get the total number of products distributed by product type
product_type_total = df.groupby('Product type:')['How many?'].sum().reset_index()

# Plot bar chart for total number of products distributed by product type
st.subheader("Total Products Distributed by Product Type")
fig1 = px.bar(product_type_total, x='Product type:', y='How many?', 
              title="Total Products Distributed by Product Type", 
              labels={'Product type:': 'Product Type', 'How many?': 'Total Distribution'})
st.plotly_chart(fig1)

# 2. Visualize Distribution Locations (Where?)
location_count = df['Where?'].value_counts().reset_index()
location_count.columns = ['Location', 'Count']

# Plot bar chart for Locations
st.subheader("Distribution Locations")
fig2 = px.bar(location_count, x='Location', y='Count', 
              title="Distribution Count by Location", 
              labels={'Location': 'Location', 'Count': 'Distribution Count'})
st.plotly_chart(fig2)

# 3. Visualize Total Distribution Over Time (by Date of Distribution)
if 'Date of distribution' in df.columns:
    # Convert 'Date of distribution' to datetime, handle errors if the column has incorrect formats
    df['Date of distribution'] = pd.to_datetime(df['Date of distribution'], errors='coerce')
    
    # Drop rows where 'Date of distribution' or 'How many?' is NaT or NaN
    df_clean = df.dropna(subset=['Date of distribution', 'How many?'])
    
    # Group by date and sum the 'How many?' values for total distribution on that date
    df_grouped_by_date = df_clean.groupby('Date of distribution').agg({'How many?': 'sum'}).reset_index()

    # Plot time series for total distribution over time
    st.subheader("Total Distribution Over Time")
    fig3 = px.line(df_grouped_by_date, x='Date of distribution', y='How many?', 
                   title="Total Products Distributed Over Time", 
                   labels={'Date of distribution': 'Date', 'How many?': 'Total Count'})
    st.plotly_chart(fig3)

# 4. Visualize Top Distribution Names (Who Distributed the Products)
name_count = df['Your name:'].value_counts().reset_index()
name_count.columns = ['Name', 'Distribution Count']

# Show top distributors
st.subheader("Top Distributors")
top_names = name_count.head(10)  # Top 10 distributors
fig4 = px.bar(top_names, x='Name', y='Distribution Count', 
              title="Top 10 Distributors", 
              labels={'Name': 'Distributor Name', 'Distribution Count': 'Distribution Count'})
st.plotly_chart(fig4)
