import pandas as pd
import streamlit as st
import plotly.express as px

# Streamlit Title
st.title("Google Form Responses Dashboard")

# Introductory Section
st.write("""
Welcome to the **Product Distribution Dashboard**!  
This dashboard provides an analysis of product distribution data collected via Google Forms.  
Below, you will find interactive visualizations showcasing key insights:
1. **Product Distribution Overview**: Total products distributed across various product types.
2. **Location Analysis**: Breakdown of product distribution across locations.
3. **Trends Over Time**: Insights into how product distribution has varied over time.
4. **Top Contributors**: Highlighting the individuals who have distributed the most products.
5. **Heatmap Analysis**: A detailed visualization of product type distributions by location.
6. **Specific Product Insights**: Sum of products distributed for a selected product type.
""")

# Google Sheets Public URL
sheet_url = "https://docs.google.com/spreadsheets/d/1Uiu2k6612HQWJbOSj-fWY_ZdrFuPEv0s7OL12oH-KIk/export?format=csv&gid=1398230424"

# Load the data from Google Sheets (CSV export link), and set header row to 2 (index 1)
df = pd.read_csv(sheet_url, header=1)  # Read the second row as the header

# Clean column names: Strip any extra spaces or special characters
df.columns = df.columns.str.strip()

# Convert the 'How many?' column to numeric values, handling non-numeric values
df['How many?'] = pd.to_numeric(df['How many?'], errors='coerce')

# Drop rows where 'How many?' is NaN (invalid entries)
df = df.dropna(subset=['How many?'])

# Bar Chart: Total Products Distributed by Product Type
product_type_total = df.groupby('Product type:')['How many?'].sum().reset_index()



# Plot the bar chart
fig1 = px.bar(product_type_total, x='Product type:', y='How many?',
              labels={'Product type:': 'Product Type', 'How many?': 'Total Distribution'},
              text='How many?')
fig1.update_traces(textposition='outside')
st.plotly_chart(fig1)

# Bar Chart: Total Products Distributed by Location (Where?)
st.subheader("Distribution by Location")
location_total = df.groupby('Where?')['How many?'].sum().reset_index()
fig2 = px.bar(location_total, x='Where?', y='How many?',
              title="Total Products Distributed by Location",
              labels={'Where?': 'Location', 'How many?': 'Total Distribution'},
              text='How many?')
fig2.update_traces(textposition='outside')
st.plotly_chart(fig2)

# Line Chart: Distribution Trends Over Time
if 'Date of distribution' in df.columns:
    st.subheader("Trends in Product Distribution Over Time")
    df['Date of distribution'] = pd.to_datetime(df['Date of distribution'], errors='coerce')
    time_total = df.groupby('Date of distribution')['How many?'].sum().reset_index()
    fig3 = px.line(time_total, x='Date of distribution', y='How many?',
                   labels={'Date of distribution': 'Date', 'How many?': 'Total Distribution'})
    st.plotly_chart(fig3)

# Bar Chart: Top Distributors
st.subheader("Top Distributors")
distributor_total = df.groupby('Your name:')['How many?'].sum().reset_index()
top_distributors = distributor_total.sort_values(by='How many?', ascending=False).head(10)
fig4 = px.bar(top_distributors, x='Your name:', y='How many?',
              title="Top 10 Distributors",
              labels={'Your name:': 'Distributor Name', 'How many?': 'Total Distribution'},
              text='How many?')
fig4.update_traces(textposition='outside')
st.plotly_chart(fig4)

# Heatmap: Product Type vs Location
st.subheader("Product Distribution Heatmap by Location and Type")
pivot_data = df.pivot_table(index='Where?', columns='Product type:', values='How many?', aggfunc='sum', fill_value=0)
fig5 = px.imshow(pivot_data, labels=dict(color="Quantity"), aspect="auto")
st.plotly_chart(fig5)

# Sum for Specific Product Type
st.subheader("Sum of 'How many?' for Specific Product Types")
product_type = 'Condoms (& lube)'  # Product type to check
specific_sum = df[df['Product type:'] == product_type]['How many?'].sum()
st.write(f"**Total for '{product_type}': {specific_sum}**")
