import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

st.set_page_config(page_title="Heavy Metal Contamination Blog", layout="wide")

# Load dataset
df = pd.read_excel("DATASET_v0.1.xlsx", sheet_name="Data Sheet")
df.columns = [
    "Sample", "Arsenic (mg/L)", "Cadmium (mg/L)", "Chromium (mg/L)", "Lead (mg/L)",
    "pH", "TDS (mg/L)", "Conductivity (µS/cm)", "Total Hardness (mg/L)",
    "Calcium Hardness (mg/L)", "Magnesium Hardness (mg/L)"
]

who_limits = {
    'Arsenic (mg/L)': 0.01,
    'Cadmium (mg/L)': 0.003,
    'Chromium (mg/L)': 0.05,
    'Lead (mg/L)': 0.01
}

# Navigation bar
st.markdown("""
<nav style="background-color:#004080;padding:10px;border-radius:5px">
    <h2 style="color:white;text-align:center">📘 Analyzing Heavy Metal Contamination from Illegal Mining</h2>
</nav>
""", unsafe_allow_html=True)

st.markdown("""
### ✍️ Introduction

I embarked on this project to examine how illegal mining, commonly called *galamsey* in Ghana, impacts the quality of river water in Ghana. The presence of heavy metals like **Arsenic**, **Lead**, **Cadmium**, and **Chromium** is of particular concern, given their toxicity to both humans and aquatic life.

---

### 🔍 My Objective

Through data analysis and visualization, I aimed to:

- Determine if heavy metal levels in river samples exceed WHO limits.
- Identify clustering patterns to categorize pollution severity.
- Compute a **Health Pollution Index (HPI)** to assess health risks.
- Suggest actionable steps for mitigation.

---

### 🧪 Data & Methodology

I used sample data from several river sources. For each sample, the dataset contains:

- **Heavy Metals**: Arsenic, Cadmium, Chromium, Lead
- **Water Chemistry**: pH, TDS, Conductivity, Total Hardness, Calcium & Magnesium

I applied:

- Descriptive statistics
- Visual exploration (bar plots, heatmaps, histograms)
- K-Means clustering
- HPI calculation

---

### ⚠️ Heavy Metal Concentration Levels

Below is the distribution of each heavy metal across the sampled sites.

""")

# Distribution plots
heavy_metals = list(who_limits.keys())
fig, axes = plt.subplots(1, 4, figsize=(20, 5))
for i, metal in enumerate(heavy_metals):
    sns.histplot(df[metal], kde=True, color="tomato", ax=axes[i])
    axes[i].set_title(metal)
st.pyplot(fig)

st.markdown("""
Upon reviewing the histograms, I noticed that **Chromium** showed the widest variation, with some samples showing dangerously high concentrations. **Cadmium**, on the other hand, was barely present, yet still concerning due to its toxic nature at even low levels.

---

### 📏 Exceeding WHO Standards

Here’s how the sampled rivers fared compared to WHO safe drinking water standards:
""")

# Exceedance table
for metal, limit in who_limits.items():
    df[f'{metal} Exceeds'] = df[metal] > limit
st.dataframe(df[["Sample"] + [f"{metal} Exceeds" for metal in who_limits]])

st.markdown("""
I found that many of the rivers had at least one metal exceeding WHO limits with **Chromium** and **Lead** being the most frequent offenders.

---

### 🧠 Correlation Insights

The heatmap below reveals how different water quality parameters are related.
""")

# Correlation heatmap
correlation = df.corr(numeric_only=True)
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(correlation, annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

st.markdown("""
It became evident that **TDS** and **Conductivity** were strongly correlated as expected since they both reflect dissolved solids. Similarly, **Total Hardness** correlated well with both calcium and magnesium hardness.

---

### 🎯 K-Means Clustering

To better understand contamination levels, I grouped the river samples into clusters based on their metal concentrations.

""")

# Clustering
features = df[list(who_limits.keys())]
scaled = StandardScaler().fit_transform(features)
kmeans = KMeans(n_clusters=3, random_state=0)
df['Cluster'] = kmeans.fit_predict(scaled)

fig, ax = plt.subplots()
sns.scatterplot(
    x='Cadmium (mg/L)', y='Chromium (mg/L)', hue='Cluster',
    palette='Set2', data=df, s=100, ax=ax
)
ax.set_title("Cadmium vs Chromium Clustering")
st.pyplot(fig)

st.markdown("""
The clustering helped me identify samples with **extremely high metal content**, separating them clearly from cleaner water samples. One cluster in particular grouped the most polluted rivers suggesting they require urgent intervention.

---

### 🧮 Health Pollution Index (HPI)

I computed a Health Pollution Index by comparing each metal to its permissible limit and scoring the relative risk:

""")

# HPI calculation
for metal, limit in who_limits.items():
    df[f'{metal} Qi'] = (df[metal] / limit) * 100
qi_columns = [f'{metal} Qi' for metal in who_limits]
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
I considered any **HPI > 100** as high risk. Several samples crossed this threshold, making them unsafe for consumption or use without treatment.

---

### 🛡️ What Can Be Done?

Illegal mining is a complex socio-economic issue, but I believe the following can help reduce its environmental toll:

- **Enforce stricter regulations** and real-time monitoring.
- **Install affordable water treatment systems** in affected communities.
- **Create awareness campaigns** about the health dangers of contaminated water.
- **Reclaim and reforest** degraded mining zones.

---

### 🧾 Conclusion

This analysis confirmed my suspicions — illegal mining is **heavily contaminating rivers**, with **Chromium** and **Lead** posing the greatest risk. Without immediate action, communities depending on these rivers may suffer long-term health consequences.

---

🖋️ **Prepared by:** *Prince Eugene Ofosu*
🔗 [GitHub](https://github.com/Pcosby5)
""")
