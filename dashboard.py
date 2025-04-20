import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Load dataset
df = pd.read_excel("DATASET_v0.1.xlsx", sheet_name="Data Sheet")
df.columns = [
    "Sample", "Arsenic (mg/L)", "Cadmium (mg/L)", "Chromium (mg/L)", "Lead (mg/L)", "pH",
    "TDS (mg/L)", "Conductivity (µS/cm)", "Total Hardness (mg/L)",
    "Calcium Hardness (mg/L)", "Magnesium Hardness (mg/L)"
]

# WHO limits
who_limits = {
    'Arsenic (mg/L)': 0.01,
    'Cadmium (mg/L)': 0.003,
    'Chromium (mg/L)': 0.05,
    'Lead (mg/L)': 0.01
}

# Sidebar navigation
st.sidebar.title("Table of Contents")
section = st.sidebar.radio("Go to Section:", [
    "Introduction", "Methodology", "Correlation Heatmap",
    "Heavy Metal Distribution", "Exceeding WHO Limits",
    "Clustering", "HPI & Risk Levels", "Solutions", "Conclusion"
])

# 1. INTRODUCTION
if section == "Introduction":
    st.title("Environmental Impact of Illegal Mining in Ghana")
    st.markdown("""
    This dashboard presents a detailed analysis of water pollution due to illegal mining activities,
    particularly focusing on heavy metal contamination in river samples.
    Using data analytics and visualization, we explore contamination levels, risk categories,
    and offer recommendations for mitigating environmental damage.
    """)

# 2. METHODOLOGY
elif section == "Methodology":
    st.header("Methodology")
    st.markdown("""
    - **Data Source**: Field measurements from affected rivers.
    - **Metrics Analyzed**: Heavy metals (As, Cd, Cr, Pb), pH, TDS, hardness, etc.
    - **Tools Used**: Python, Pandas, Seaborn, Scikit-learn.
    - **Analysis Techniques**:
        - Correlation heatmaps
        - Clustering using K-Means
        - Health Pollution Index (HPI)
        - Risk categorization based on WHO guidelines
    """)

# 3. CORRELATION HEATMAP
elif section == "Correlation Heatmap":
    st.header("Correlation Heatmap")
    correlation = df.corr(numeric_only=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(correlation, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

# 4. HEAVY METAL DISTRIBUTION
elif section == "Heavy Metal Distribution":
    st.header("Heavy Metal Concentration Distribution")
    st.markdown("Figure below shows the distribution of Arsenic, Cadmium, Lead, and Chromium.")

    heavy_metals = ["Arsenic (mg/L)", "Cadmium (mg/L)", "Lead (mg/L)", "Chromium (mg/L)"]
    fig, axes = plt.subplots(1, 4, figsize=(20, 5))
    for i, metal in enumerate(heavy_metals):
        sns.histplot(df[metal], kde=True, color="tomato", ax=axes[i])
        axes[i].set_title(f"{metal}")
    st.pyplot(fig)

# 5. EXCEEDING WHO LIMITS
elif section == "Exceeding WHO Limits":
    st.header("Heavy Metals Exceeding WHO Permissible Limits")
    for metal, limit in who_limits.items():
        df[f'{metal} Exceeds'] = df[metal] > limit
    st.dataframe(df[["Sample"] + [f"{metal} Exceeds" for metal in who_limits.keys()]])
    st.markdown("Red indicates samples where heavy metal levels **exceed** WHO permissible limits.")

# 6. CLUSTERING
elif section == "Clustering":
    st.header("Pollution Clustering Based on Heavy Metals")
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans

    features = df[list(who_limits.keys())]
    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)
    kmeans = KMeans(n_clusters=3, random_state=0)
    df['Cluster'] = kmeans.fit_predict(scaled)

    fig, ax = plt.subplots()
    sns.scatterplot(
        x='Arsenic (mg/L)', y='Lead (mg/L)', hue='Cluster', palette='Set2', data=df, ax=ax, s=100
    )
    ax.set_title("River Clusters Based on Arsenic and Lead Levels")
    st.pyplot(fig)

# 7. HPI & RISK
elif section == "HPI & Risk Levels":
    st.header("Health Pollution Index (HPI) and Risk Categorization")

    for metal, limit in who_limits.items():
        df[f'{metal} Qi'] = (df[metal] / limit) * 100

    qi_columns = [f'{metal} Qi' for metal in who_limits.keys()]
    df['HPI'] = df[qi_columns].mean(axis=1)

    def get_risk(hpi):
        if hpi <= 50:
            return "Low"
        elif hpi <= 100:
            return "Medium"
        else:
            return "High"

    df['Risk Category'] = df['HPI'].apply(get_risk)

    st.dataframe(df[["Sample", "HPI", "Risk Category"]])
    st.markdown("""
    - **Low**: Safe for use
    - **Medium**: Caution advised
    - **High**: Potential health hazard
    """)

# 8. SOLUTIONS
elif section == "Solutions":
    st.header("Proposed Solutions to Mitigate Environmental Damage")
    st.markdown("""
    - **Strict enforcement** of anti-galamsey regulations.
    - **Water treatment interventions** in affected communities.
    - **Public education** campaigns to raise awareness.
    - **Real-time water quality monitoring** using sensors and dashboards.
    - **Reforestation and land restoration** around mining areas.
    """)

# 9. CONCLUSION
elif section == "Conclusion":
    st.header("Conclusion")
    st.markdown("""
    This analysis highlights the critical levels of pollution present in river samples from illegal mining areas.
    Chromium and Lead pose significant concerns, often exceeding WHO standards.

    By combining data science with environmental awareness, we can identify at-risk areas and propose sustainable solutions.
    """)

    st.markdown("**Prepared by:** Prince Eugene Ofosu | [GitHub](https://github.com/pcosby)")

