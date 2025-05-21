import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import f_oneway
import os

# Set page config
st.set_page_config(page_title="Solar Radiation Analysis", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .reportview-container {
        background: #f0f2f5;
    }
    .sidebar .sidebar-content {
        background: #3a3f47;
        color: white;
    }
    h1 {
        color: #4A90E2;
    }
    h2 {
        color: #333;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #3a3f47;
        color: white;
        text-align: center;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

def load_data(path, country_name):
    """Load data and assign country name."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    data = pd.read_csv(path)
    data['Country'] = country_name
    return data

def combine_data(benin_data, sierra_leone_data, togo_data):
    """Combine datasets into a single DataFrame."""
    return pd.concat([benin_data, sierra_leone_data, togo_data])

def plot_boxplots(combined_data, metric):
    """Create boxplots for a selected metric."""
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Country', y=metric, data=combined_data, palette="Set2")
    plt.title(f'Boxplot of {metric}', fontsize=16)
    plt.ylabel(metric, fontsize=14)
    plt.legend(title='Country', loc='upper right')
    st.pyplot(plt)

def summary_statistics(combined_data):
    """Calculate summary statistics for GHI, DNI, and DHI."""
    summary_stats = combined_data.groupby('Country')[['GHI', 'DNI', 'DHI']].agg(['mean', 'median', 'std'])
    summary_stats.columns = ['_'.join(col).strip() for col in summary_stats.columns.values]
    return summary_stats

def run_anova(benin_data, sierra_leone_data, togo_data):
    """Run ANOVA on GHI values and return p-value."""
    benin_ghi = benin_data['GHI']
    sierra_leone_ghi = sierra_leone_data['GHI']
    togo_ghi = togo_data['GHI']
    f_statistic, p_value = f_oneway(benin_ghi, sierra_leone_ghi, togo_ghi)
    return p_value

def plot_average_ghi(combined_data):
    """Plot average GHI by country."""
    avg_ghi = combined_data.groupby('Country')['GHI'].mean().sort_values()
    plt.figure(figsize=(10, 6))
    avg_ghi.plot(kind='bar', color='skyblue', edgecolor='black', label='Average GHI')
    plt.title('Average GHI by Country', fontsize=16)
    plt.ylabel('Average GHI', fontsize=14)
    plt.xticks(rotation=45)
    plt.legend(loc='upper right')
    st.pyplot(plt)

# Sidebar for navigation
st.sidebar.title("Navigation")
st.sidebar.markdown("Select a report section to view:")
report_sections = st.sidebar.radio("Go to", ["Summary Statistics", "Boxplots", "Average GHI"])

# Streamlit app header
st.title("Solar Radiation Analysis Dashboard")
st.markdown("This dashboard provides insights into solar radiation metrics across Benin, Sierra Leone, and Togo.")

# Load datasets
try:
    benin_data = load_data('../notebooks/data/benin_clean.csv', 'Benin')
    sierra_leone_data = load_data('../notebooks/data/sierraleone-bumbuna_clean.csv', 'Sierra Leone')
    togo_data = load_data('../notebooks/data/togo-dapaong_qc_clean.csv', 'Togo')

    # Combine data
    combined_data = combine_data(benin_data, sierra_leone_data, togo_data)

    # Navigation based on sidebar selection
    if report_sections == "Summary Statistics":
        st.header("Summary Statistics")
        summary_stats = summary_statistics(combined_data)
        st.dataframe(summary_stats.style.background_gradient(cmap='Blues'))

    elif report_sections == "Boxplots":
        st.header("Boxplots of Solar Radiation Metrics")
        metric = st.selectbox("Select Metric to View", ['GHI', 'DNI', 'DHI'])
        plot_boxplots(combined_data, metric)

    elif report_sections == "Average GHI":
        st.header("Average GHI by Country")
        plot_average_ghi(combined_data)

    # Run ANOVA and display p-value
    p_value = run_anova(benin_data, sierra_leone_data, togo_data)
    st.write(f'ANOVA p-value: {p_value:.4f}')

except Exception as e:
    st.error(f"An error occurred: {e}")

# Footer
st.markdown("""
    <div class="footer">
        <p>© 2025 Solar Radiation Analysis Dashboard</p>
    </div>
""", unsafe_allow_html=True)