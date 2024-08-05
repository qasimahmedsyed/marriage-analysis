import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
@st.cache_data
def load_data():
    # Update the path to the actual downloaded dataset file
    data = pd.read_csv('data/World Marriage Dataset.csv')
    return data

data = load_data()

# Define the pages
def home():
    st.title('🌍 World Marriage Dataset Analysis')

    st.write("""
    Welcome to the **World Marriage Dataset Analysis** app! 🎉

    This interactive tool provides insights into marriage trends and demographics across various countries. 
    Explore how marital status varies by age, sex, and country, and analyze trends over different time periods.

    ### What You Can Do:
    - **Explore the Data**: View a preview and basic statistics of the dataset.
    - **Visualize Trends**: Generate interactive charts to see how marital status changes over time and across different demographics.
    - **Gain Insights**: Analyze the data to uncover meaningful trends and patterns.
    - **Download Data**: Get access to the filtered dataset for your own analysis.

    Use the sidebar to navigate through different sections of the app.
    """)

    st.image("https://www.example.com/image.png", caption="Marriage Trends Visualization", use_column_width=True)  # Replace with an actual image URL

    st.write("""
    ### About the Dataset:
    This dataset includes information on marital status categorized by country, age group, and gender. 
    Data collection periods vary, and sources are provided for transparency.
    """)

    st.write("""
    ### How to Use:
    - **Data Exploration**: Check out the data overview and summary.
    - **Visualizations**: Create and interact with various charts to analyze trends.
    - **Insights**: Review key findings and insights from the data.
    - **Download**: Export the filtered data for offline analysis.
    """)

# Function to display dataset overview
def data_exploration():
    st.title('Data Exploration')

    # Show dataset overview
    dataset_overview(data)
    
    # Apply interactive filters
    filtered_data = interactive_filters(data)
    
    # Show data visualizations
    data_visualizations(filtered_data)
    
    # Show correlation analysis
    correlation_analysis(filtered_data)
    
    # Show missing values analysis
    missing_values_analysis(filtered_data)
    
    # Show data quality checks
    data_quality_checks(filtered_data)
    
    # Provide download option
    st.write('Download Filtered Data:')
    st.download_button('Download Filtered Data', filtered_data.to_csv().encode('utf-8'), 'filtered_data.csv')

def dataset_overview(data):
    st.write("### Dataset Overview")
    st.write("**Basic Statistics**")
    st.write(data.describe())
    
    st.write("**Data Summary**")
    st.write(data.info())
    
    st.write("**Data Distribution**")
    st.bar_chart(data['MaritalStatus'].value_counts())

def interactive_filters(data):
    st.write("### Interactive Filters")
    
    # Country filter
    countries = st.multiselect('Select Country', options=data['Country'].unique())
    if countries:
        data = data[data['Country'].isin(countries)]
    
    # Age group filter
    age_groups = st.multiselect('Select Age Group', options=data['AgeGroup'].unique())
    if age_groups:
        data = data[data['AgeGroup'].isin(age_groups)]
    
    # Sex filter
    sexes = st.multiselect('Select Sex', options=data['Sex'].unique())
    if sexes:
        data = data[data['Sex'].isin(sexes)]
    
    return data

def data_visualizations(data):
    st.write("### Data Visualizations")
    
    # Histogram
    st.subheader('Marital Status Distribution')
    fig_hist = px.histogram(data, x='MaritalStatus', color='Sex', barmode='group', title='Marital Status Distribution')
    st.plotly_chart(fig_hist)
    
    # Bar Chart by Age Group
    st.subheader('Marital Status by Age Group')
    fig_bar = px.bar(data, x='AgeGroup', color='MaritalStatus', barmode='group', title='Marital Status by Age Group')
    st.plotly_chart(fig_bar)
    
    # Pie Chart for Marital Status
    st.subheader('Marital Status Proportions')
    fig_pie = px.pie(data, names='MaritalStatus', title='Proportion of Marital Status')
    st.plotly_chart(fig_pie)

def correlation_analysis(data):

    st.write("### Correlation Analysis")
    
    # Filter out non-numeric columns
    numeric_data = data.select_dtypes(include=['number'])
    
    if numeric_data.empty:
        st.write("No numeric data available for correlation analysis.")
        return
    
    # Correlation Matrix
    st.write("**Correlation Matrix**")
    corr = numeric_data.corr()
    
    # Create heatmap using Plotly
    fig_corr = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale='Viridis',
        zmin=-1,
        zmax=1
    ))
    fig_corr.update_layout(title='Correlation Matrix', xaxis_title='Variables', yaxis_title='Variables')
    st.plotly_chart(fig_corr)
    
    # Scatter Plots for Numeric Data
    st.write("**Scatter Plots**")
    if len(numeric_data.columns) >= 2:
        x_col = st.selectbox('Select X-axis Column', options=numeric_data.columns)
        y_col = st.selectbox('Select Y-axis Column', options=numeric_data.columns)
        if x_col and y_col:
            fig_scatter = px.scatter(numeric_data, x=x_col, y=y_col, title=f'Scatter Plot of {x_col} vs {y_col}')
            st.plotly_chart(fig_scatter)
    else:
        st.write("Not enough numeric columns available for scatter plots.")

def missing_values_analysis(data):
    st.write("### Missing Values Analysis")
    
    st.write("**Heatmap of Missing Values**")
    fig_missing, ax = plt.subplots()
    sns.heatmap(data.isnull(), cbar=False, cmap='viridis', ax=ax)
    st.pyplot(fig_missing)
    
    st.write("**Missing Data Statistics**")
    st.write(data.isnull().sum())

def data_quality_checks(data):
    st.write("### Data Quality Checks")
    
    # Check for missing values
    st.write("**Missing Values**")
    missing_values = data.isnull().sum()
    st.write(missing_values[missing_values > 0])
    
    # Check for duplicates
    st.write("**Duplicate Rows**")
    duplicate_rows = data.duplicated().sum()
    st.write(f"Number of duplicate rows: {duplicate_rows}")
    
    # Check for data types
    st.write("**Data Types**")
    st.write(data.dtypes)
    
    # Outlier Analysis
    st.write("**Outlier Analysis**")
    
    # Filter out non-numeric columns
    numeric_data = data.select_dtypes(include=['number'])
    
    if numeric_data.empty:
        st.write("No numeric data available for outlier analysis.")
        return
    
    # Boxplots for outlier detection
    for col in numeric_data.columns:
        fig_box = px.box(numeric_data, y=col, title=f'Boxplot of {col}')
        st.plotly_chart(fig_box)
    
    st.write("**Summary Statistics**")
    st.write(numeric_data.describe())


def visualizations():
    st.title('Visualizations')
    
    st.subheader('Marital Status Distribution')
    country = st.selectbox('Select Country', data['Country'].unique())
    filtered_data = data[data['Country'] == country]
    fig = px.histogram(filtered_data, x='MaritalStatus', color='Sex', barmode='group',
                       title=f'Distribution of Marital Status in {country}')
    st.plotly_chart(fig)
    
    st.subheader('Marital Status by Age Group')
    age_group = st.selectbox('Select Age Group', data['AgeGroup'].unique())
    filtered_data_age = data[data['AgeGroup'] == age_group]
    fig2 = px.histogram(filtered_data_age, x='MaritalStatus', color='Country', barmode='group',
                        title=f'Distribution of Marital Status in Age Group {age_group}')
    st.plotly_chart(fig2)

    st.subheader('Marital Status Trends Over Time')
    start_year = int(data['Data Collection (Start Year)'].min())
    end_year = int(data['Data Collection (End Year)'].max())
    year_range = st.slider('Select Year Range', start_year, end_year, (start_year, end_year))
    filtered_data_year = data[(data['Data Collection (Start Year)'] >= year_range[0]) & 
                              (data['Data Collection (End Year)'] <= year_range[1])]
    fig3 = px.histogram(filtered_data_year, x='MaritalStatus', color='Country', barmode='group',
                        title=f'Distribution of Marital Status from {year_range[0]} to {year_range[1]}')
    st.plotly_chart(fig3)

def insights():
    st.title('Insights')
    st.write('Add your analysis and insights here.')

def download_section():
    st.title('Download Data')
    st.write('Download the filtered dataset:')
    st.download_button('Download Filtered Data', data.to_csv().encode('utf-8'), 'filtered_data.csv')

# Page navigation
PAGES = {
    "🏠 Home": home,
    "🔍 Data Exploration": data_exploration,
    "📈 Visualizations": visualizations,
    "🔍 Insights": insights,
    "📥 Download": download_section
}

# Display the sidebar with styled radio buttons
def sidebar():
    st.sidebar.title('🌟 Navigation')
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    return PAGES[selection]

# Render the selected page
page = sidebar()
page()
