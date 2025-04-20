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

who_limits = {
    'Arsenic (mg/L)': 0.01,
    'Cadmium (mg/L)': 0.003,
    'Chromium (mg/L)': 0.05,
    'Lead (mg/L)': 0.01
}

# --- ARTICLE STYLE CONTENT ---

st.title("Analyzing Heavy Metal Contamination in River Samples from Illegal Mining Areas")
st.markdown("""
Illegal mining activities, commonly referred to as *galamsey*, have led to the widespread contamination of water bodies in Ghana. This article-style dashboard explores the presence of heavy metals in river water and the potential health and environmental risks they pose. All analyses are based on real field data and aligned with WHO guidelines.
""")

# INTRODUCTION
st.header("Introduction")
st.markdown("""
Mining, though economically beneficial, can lead to significant environmental damage when done illegally. Rivers near mining zones are often exposed to heavy metals such as **Arsenic, Lead, Cadmium**, and **Chromium**, which can severely affect human and aquatic life.

This report examines:
- The concentration levels of heavy metals
- Whether they exceed WHO permissible limits
- Clustering patterns of contamination
- Health Pollution Index (HPI)
- Proposed mitigation strategies
""")

# METHODOLOGY
st.header("Methodology")
st.markdown("""
Data was collected from multiple river sources in mining areas. Each sample was tested for several parameters including:
- **Heavy metals**: Arsenic, Cadmium, Chromium, Lead
- **Water quality**: pH, TDS, Hardness

We applied:
- **Descriptive analytics**
- **KMeans clustering**
- **HPI scoring system**
- **Visual exploration** using histograms and heatmaps
""")

# HEAVY METAL DISTRIBUTION
st.header("Heavy Metal Concentration Distribution")

st.markdown("Below is the distribution of key heavy metals across the sampled sites:")

heavy_metals = ["Arsenic (mg/L)", "Cadmium (mg/L)", "Lead (mg/L)", "Chromium (mg/L)"]
fig, axes = plt.subplots(1, 4, figsize=(20, 5))
for i, metal in enumerate(heavy_metals):
    sns.histplot(df[metal], kde=True, color="tomato", ax=axes[i])
    axes[i].set_title(metal)
st.pyplot(fig)

# WHO LIMIT EXCEEDANCE
st.header("Exceeding WHO Permissible Limits")
st.markdown("This table shows which samples exceed WHO limits:")

for metal, limit in who_limits.items():
    df[f'{metal} Exceeds'] = df[metal] > limit

st.dataframe(df[["Sample"] + [f"{metal} Exceeds" for metal in who_limits.keys()]])

# CORRELATION HEATMAP
st.header("Correlation Between Water Quality Parameters")
correlation = df.corr(numeric_only=True)
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(correlation, annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

# CLUSTERING
st.header("Clustering of Samples Based on Metal Concentration")
features = df[list(who_limits.keys())]
scaled = StandardScaler().fit_transform(features)
kmeans = KMeans(n_clusters=3, random_state=0)
df['Cluster'] = kmeans.fit_predict(scaled)

fig, ax = plt.subplots()
sns.scatterplot(
    x='Cadmium (mg/L)', y='Chromium (mg/L)', hue='Cluster', palette='Set2', data=df, ax=ax, s=100
)
ax.set_title("Cadmium vs Chromium Clustering")
st.pyplot(fig)

# HPI & RISK ASSESSMENT
st.header("Health Pollution Index (HPI) and Risk Levels")

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
- **Low**: Water is relatively safe
- **Medium**: Water may cause harm over time
- **High**: Water is highly contaminated
""")

# SOLUTIONS
st.header("Mitigation Strategies")
st.markdown("""
To tackle the environmental damage caused by illegal mining:
- **Strengthen enforcement** of environmental laws
- **Implement real-time water monitoring systems**
- **Educate communities** on the impact of illegal mining
- **Encourage sustainable mining practices**
- **Restore vegetation and natural water flow paths**
""")

# CONCLUSION
st.header("Conclusion")
st.markdown("""
This analysis reveals that many water samples contain heavy metals beyond safe limits, particularly **Chromium** and **Lead**. Immediate actions are needed to control pollution, protect lives, and restore affected ecosystems.

---
**Prepared by:** Prince Eugene Ofosu
**GitHub:** [@pcosby](https://github.com/pcosby)
""")
