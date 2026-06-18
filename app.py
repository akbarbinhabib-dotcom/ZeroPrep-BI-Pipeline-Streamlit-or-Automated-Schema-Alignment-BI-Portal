import numpy as np
import pandas as pd
import streamlit as st

# ==============================================================================
# 1. STREAMLIT APPLICATION CONFIGURATION
# ==============================================================================
# Setting up page layouts and window configurations to ensure responsiveness.
st.set_page_config(page_title="Mock data generate & robut coloumns mapping", layout="centered")

st.title("Mock Data Generation & Robust Column Mapping")
st.write("Yeh Streamlit app aapko mock data generate karne aur client ke custom columns ko robustly map karne mein madad karega.")


# ==============================================================================
# 2. FAILSAFE SIMULATION ENGINE (Mock Data Generator)
# ==============================================================================
def generate_simple_data():
    """
    Simulates a synthetic transactional dataset to keep the application active
    and test python scripts before the client uploads their actual CSV database.
    """
    np.random.seed(7)
    data = {
        "Date" : pd.date_range(start="2026-01-01", end="2026-06-13", periods=100),
        "Category" : np.random.choice(['electronic', 'assisries', 'fine'], 100),
        "Price" : np.random.uniform(100, 1000, 100),
        "Quantity" : np.random.randint(1, 5, 100)
    }
    return pd.DataFrame(data)


# ==============================================================================
# 3. SCHEMA ALIGNMENT & MAPPING LOGIC (The Core ETL Layer)
# ==============================================================================
def mapped_col(df):
    """
    Normalizes chaotic user column headers and maps them to program standards.
    Converts headers to lowercase, strips trailing spaces, and replaces empty gaps with underscores.
    """
    mapped_df = df.copy()
    
    # Standardizing incoming column strings to prevent capitalization and spacing errors
    mapped_df.columns = mapped_df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Declaring the schema translation dictionary to align client database fields
    mapping = {
        'unit_price' : 'Price',
        'product_line' : "Category",
        "total" : "Total_Revenue"
    }
    return mapped_df.rename(columns=mapping)


# ==============================================================================
# 4. DATA INGESTION & ROUTING (File Upload Control Panel)
# ==============================================================================
st.sidebar.header("Swift-Mart control panel")
uploaded_file = st.sidebar.file_uploader("Client CSV Data File Upload karein", type=["csv"])

# Determining the active dataset state (Client uploaded data vs Fallback mock data)
if uploaded_file is not None:
    rew_df = pd.read_csv(uploaded_file)
    process_df = mapped_col(rew_df)
    st.sidebar.success("CSV File Successfully Uploaded")
else:
    st.info("Backup Mock Data Is Active")
    process_df = generate_simple_data()


# ==============================================================================
# 5. DYNAMIC FEATURE ENGINEERING (Safety Calculation Net)
# ==============================================================================
# Autocalculates the missing 'Total_Revenue' column on-the-fly if it was excluded in the upload,
# preventing downstream aggregation errors and system crashes.
if "Total_Revenue" not in process_df.columns and 'Price' in process_df.columns and 'Quantity' in process_df.columns:
    process_df["Total_Revenue"] = process_df['Price'] * process_df["Quantity"]


# ==============================================================================
# 6. BUSINESS PERFORMANCE METRICS (KPI Summary Block)
# ==============================================================================
# Dividing page workspace into 3 equal columns for executive dashboard placement
col1, col2, col3 = st.columns(3)

# Executing safe calculations with default fallbacks to prevent NaN runtime exceptions
total_rev = process_df['Total_Revenue'].sum() if 'Total_Revenue' in process_df.columns else 0
avg_price = process_df['Price'].mean() if "Price" in process_df.columns else 0
total_records = len(process_df)

# Rendering the Key Performance Indicator (KPI) metric cards
with col1:
    st.metric(label='Total Revenue', value=f"${total_rev:,.1f}")
with col2:
    st.metric(label='Average Unit Price', value=f'${avg_price:.2f}')
with col3:
    st.metric(label="Total Transactions Processed", value=f'{total_records:,.1f}')


# ==============================================================================
# 7. INTERACTIVE DATA INSPECTOR
# ==============================================================================
st.write("---")
st.subheader("Cleaned Data Preview (Top 10 Records)")
# Displaying the clean transactional logs in a responsive data-table view
st.dataframe(process_df.head(10), use_container_width=True)
