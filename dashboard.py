import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Load dataset
df = pd.read_excel("DATASET_v0.1.xlsx", sheet_name="Data Sheet")
df.columns = [
    "Sample", "Arsenic (mg/L)", "Cadmium (mg/L)", "Chromium (mg/L)", "Lead (mg/L)", "pH",
    "TDS (mg/L)", "Conductivity (µS/cm)", "Total Hardness (mg/L)",
    "Calcium Hardness (mg/L)", "Magnesium Hardness (mg/L)"
]

# WHO Limits
who_limits = {
    'Arsenic (mg/L)': 0.01,
    'Cadmium (mg/L)': 0.003,
    'Chromium (mg/L)': 0.05,
    'Lead (mg/L)': 0.01
}

# Sidebar Navigation
st.sidebar.title("💧 Galamsey Water Dashboard")
section = st.sidebar.radio("Go to", [
    "Executive Summary",
    "Overview",
    "Metal Distributions",
    "HPI & Risk",
    "Clustering",
    "Correlation Heatmap",
    "Mitigation Strategies"
])

# Executive Summary
if section == "Executive Summary":
    st.header("💡 Executive Summary")
    st.markdown("""
This analysis explores the impact of illegal mining (galamsey) on river water quality, focusing on heavy metal contamination. Using samples from affected water bodies, we evaluated concentrations of Arsenic, Cadmium, Chromium, and Lead—comparing them to WHO permissible limits.

**Key Findings**:
- **Chromium** displayed the widest concentration spread, suggesting inconsistent contamination likely due to localized mining hotspots.
- **Cadmium** levels were generally low, but several samples still exceeded safe limits.
- Both **Lead** and **Arsenic** were moderately present, with over 60% of samples surpassing WHO guidelines—indicating persistent health risks.

The **Heavy Metal Pollution Index (HPI)** was computed to assess cumulative toxicity. Samples were categorized into **low**, **medium**, and **high** risk groups. A significant number of samples fell into the **high-risk** category, confirming urgent environmental health concerns.

Using unsupervised **KMeans clustering**, we identified distinct patterns of contamination. This clustering helps pinpoint severely affected zones for targeted intervention.

A **correlation analysis** showed strong positive relationships between some metal concentrations, suggesting shared contamination sources—likely linked to illegal mining discharges.

**Recommendations**:
- **Strengthen monitoring and enforcement** to halt illegal mining activities.
- **Rehabilitate polluted sites** using affordable eco-remediation technologies.
- **Educate local communities** on the risks of contaminated water and promote safe alternatives.
- **Invest in sustainable livelihoods** to reduce dependence on illegal mining.

This dashboard provides an interactive tool for policymakers, researchers, and NGOs to visualize water quality threats and drive impactful decisions toward water safety and public health.
""")

# Overview
elif section == "Overview":
    st.title("🌍 Environmental Pollution: River Water Quality Analysis")
    st.markdown("""
    This dashboard explores heavy metal contamination in river water samples due to illegal mining activities (galamsey).

    **Heavy Metals Analyzed**:
    - Arsenic
    - Cadmium
    - Chromium
    - Lead

    **WHO Guidelines** help assess which samples exceed safe limits and their risk to health and environment.
    """)

# Metal Distributions + WHO Exceedances
elif section == "Metal Distributions":
    st.header("📊 Heavy Metal Concentration Distributions")
    heavy_metals = ["Arsenic (mg/L)", "Lead (mg/L)", "Cadmium (mg/L)", "Chromium (mg/L)"]

    fig, axes = plt.subplots(1, 4, figsize=(18, 5))
    for i, metal in enumerate(heavy_metals):
        sns.histplot(df[metal], kde=True, ax=axes[i], color='tomato')
        axes[i].set_title(f"{metal}")
    st.pyplot(fig)

    st.subheader("🚨 Samples Exceeding WHO Limits")
    exceed_df = df[
        (df['Arsenic (mg/L)'] > who_limits['Arsenic (mg/L)']) |
        (df['Cadmium (mg/L)'] > who_limits['Cadmium (mg/L)']) |
        (df['Chromium (mg/L)'] > who_limits['Chromium (mg/L)']) |
        (df['Lead (mg/L)'] > who_limits['Lead (mg/L)'])
    ]
    st.dataframe(exceed_df[['Sample', 'Arsenic (mg/L)', 'Cadmium (mg/L)', 'Chromium (mg/L)', 'Lead (mg/L)']])

# HPI & Risk
elif section == "HPI & Risk":
    st.header("⚠️ Heavy Metal Pollution Index (HPI)")

    for metal, limit in who_limits.items():
        df[f'{metal} Qi'] = (df[metal] / limit) * 100
    qi_columns = [f'{metal} Qi' for metal in who_limits.keys()]
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

    fig, ax = plt.subplots()
    sns.barplot(data=df, x="Sample", y="HPI", hue="Risk Category", palette="coolwarm", ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Clustering
elif section == "Clustering":
    st.header("🔍 Clustering of River Samples")

    # Cluster on all metals
    features_all = df[list(who_limits.keys())]
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(features_all)

    kmeans = KMeans(n_clusters=3, random_state=42)
    df['Cluster'] = kmeans.fit_predict(scaled_data)

    st.subheader("Arsenic vs Lead Cluster View")
    fig1 = plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x='Arsenic (mg/L)', y='Lead (mg/L)', hue='Cluster', palette='Set2', s=100)
    plt.grid(True)
    st.pyplot(fig1)

    # Cadmium vs Chromium
    st.subheader("Cadmium vs Chromium Cluster View")
    sub_data = df[['Cadmium (mg/L)', 'Chromium (mg/L)']]
    scaled_sub = scaler.fit_transform(sub_data)
    kmeans_sub = KMeans(n_clusters=3, random_state=0)
    df['Cluster_Cd_Cr'] = kmeans_sub.fit_predict(scaled_sub)

    fig2 = plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x='Cadmium (mg/L)', y='Chromium (mg/L)', hue='Cluster_Cd_Cr', palette='Set2', s=100)
    plt.grid(True)
    st.pyplot(fig2)

# Correlation Heatmap
elif section == "Correlation Heatmap":
    st.header("🧪 Correlation Heatmap of Water Quality Indicators")
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    corr = numeric_df.corr()

    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, ax=ax)
    ax.set_title("Correlation Matrix of Water Quality Indicators", fontsize=16)
    st.pyplot(fig)

# Mitigation
elif section == "Mitigation Strategies":
    st.header("🌱 Solutions to Mitigate Illegal Mining Impacts")
    st.markdown("""
    To reduce environmental damage from illegal mining (galamsey), consider the following solutions:

    - 🛑 **Enforcement**: Strengthen law enforcement to stop unauthorized mining.
    - 📡 **Monitoring**: Use satellite imagery, drones, and IoT sensors for real-time tracking.
    - 💧 **Rehabilitation**: Restore polluted water bodies through phytoremediation and bioremediation.
    - 👥 **Community Education**: Educate miners and locals about health/environmental risks.
    - ♻️ **Alternative Livelihoods**: Promote farming, aquaculture, and skills training.

    Collaborative approaches between government, communities, and NGOs are vital for long-term success.
    """)
