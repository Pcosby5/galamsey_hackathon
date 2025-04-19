import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Set Streamlit page configuration
st.set_page_config(page_title="Galamsey Pollution Dashboard", layout="wide")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_excel("DATASET_v0.1.xlsx", sheet_name="Data Sheet")
    df.columns = [
        "Sample", "Arsenic (mg/L)", "Cadmium (mg/L)", "Chromium (mg/L)", "Lead (mg/L)", "pH",
        "TDS (mg/L)", "Conductivity (µS/cm)", "Total Hardness (mg/L)",
        "Calcium Hardness (mg/L)", "Magnesium Hardness (mg/L)"
    ]
    return df

df = load_data()

# WHO Permissible Limits
who_limits = {
    'Arsenic (mg/L)': 0.01,
    'Cadmium (mg/L)': 0.003,
    'Chromium (mg/L)': 0.05,
    'Lead (mg/L)': 0.01
}

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Overview", "Metal Distributions", "HPI & Risk", "Clustering", "Mitigation Strategies"])

# Overview Section
if section == "Overview":
    st.title("🌍 Galamsey Pollution Dashboard")
    st.markdown("""
    This dashboard presents an analysis of heavy metal contamination in water bodies affected by illegal mining (galamsey) activities. It includes:
    - Distribution of heavy metals across samples
    - Heavy Metal Pollution Index (HPI) and associated risk categories
    - Clustering of samples based on metal concentrations
    - Proposed mitigation strategies
    """)
    st.markdown("**Dataset Preview:**")
    st.dataframe(df.head())

# Metal Distributions Section
elif section == "Metal Distributions":
    st.header("📊 Heavy Metal Distributions")
    heavy_metals = ["Arsenic (mg/L)", "Lead (mg/L)", "Cadmium (mg/L)", "Chromium (mg/L)"]
    fig, axes = plt.subplots(1, 4, figsize=(20, 5))
    for i, metal in enumerate(heavy_metals):
        sns.histplot(df[metal], kde=True, color="tomato", ax=axes[i])
        axes[i].axvline(who_limits[metal], color='blue', linestyle='--', label="WHO Limit")
        axes[i].set_title(f"{metal} Distribution")
        axes[i].legend()
    st.pyplot(fig)

# HPI & Risk Section
elif section == "HPI & Risk":
    st.header("⚠️ Heavy Metal Pollution Index (HPI) & Risk Categories")
    for metal, limit in who_limits.items():
        df[f'{metal} Qi'] = (df[metal] / limit) * 100
    qi_columns = [f'{metal} Qi' for metal in who_limits]
    df['HPI'] = df[qi_columns].mean(axis=1)

    def get_risk_category(hpi):
        if hpi <= 50:
            return 'Low'
        elif hpi <= 100:
            return 'Medium'
        else:
            return 'High'

    df['Risk Category'] = df['HPI'].apply(get_risk_category)
    st.dataframe(df[['Sample', 'HPI', 'Risk Category']])

# Clustering Section
elif section == "Clustering":
    st.header("🔬 Clustering Analysis")
    st.subheader("Arsenic vs Lead Clustering")
    features = df[['Arsenic (mg/L)', 'Lead (mg/L)']]
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    kmeans = KMeans(n_clusters=3, random_state=42)
    df['Cluster_As_Pb'] = kmeans.fit_predict(scaled_features)
    fig1, ax1 = plt.subplots()
    sns.scatterplot(x='Arsenic (mg/L)', y='Lead (mg/L)', hue='Cluster_As_Pb', palette='Set2', data=df, s=100, ax=ax1)
    ax1.set_title('Arsenic vs Lead Clustering')
    st.pyplot(fig1)

    st.subheader("Cadmium vs Chromium Clustering")
    features = df[['Cadmium (mg/L)', 'Chromium (mg/L)']]
    scaled_features = scaler.fit_transform(features)
    kmeans = KMeans(n_clusters=3, random_state=42)
    df['Cluster_Cd_Cr'] = kmeans.fit_predict(scaled_features)
    fig2, ax2 = plt.subplots()
    sns.scatterplot(x='Cadmium (mg/L)', y='Chromium (mg/L)', hue='Cluster_Cd_Cr', palette='Set2', data=df, s=100, ax=ax2)
    ax2.set_title('Cadmium vs Chromium Clustering')
    st.pyplot(fig2)

# Mitigation Strategies Section
elif section == "Mitigation Strategies":
    st.header("🛠️ Proposed Mitigation Strategies")
    st.markdown("""
    Based on the analysis, the following strategies are recommended to mitigate the environmental damage caused by illegal mining:
    - **Regular Monitoring:** Implement continuous monitoring of water bodies to detect contamination early.
    - **Community Engagement:** Educate local communities about the dangers of illegal mining and promote alternative livelihoods.
    - **Policy Enforcement:** Strengthen the enforcement of environmental regulations to deter illegal mining activities.
    - **Rehabilitation Programs:** Initiate programs to rehabilitate and restore contaminated sites.
    """)
