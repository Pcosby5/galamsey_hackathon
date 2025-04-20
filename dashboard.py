import os
import pandas as pd
import seaborn as sns
import streamlit as st
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Ensure visuals directory exists
os.makedirs("visuals", exist_ok=True)

# Load your Excel file
df = pd.read_excel("DATASET_v0.1.xlsx", sheet_name="Data Sheet")

# Rename columns
df.columns = [
    "Sample", "Arsenic (mg/L)", "Cadmium (mg/L)", "Chromium (mg/L)", "Lead (mg/L)",
    "pH", "TDS (mg/L)", "Conductivity (µS/cm)", "Total Hardness (mg/L)",
    "Calcium Hardness (mg/L)", "Magnesium Hardness (mg/L)"
]

# Melt the DataFrame for plotting
melted_df = df.melt(id_vars="Sample", value_vars=[
    "Arsenic (mg/L)", "Cadmium (mg/L)", "Chromium (mg/L)", "Lead (mg/L)"
], var_name="Metal", value_name="Concentration")

# Navigation bar
st.markdown("""
<nav style="background-color:#004080;padding:10px;border-radius:5px">
    <h2 style="color:white;text-align:center">📘 Analyzing Heavy Metal Contamination from Illegal Mining</h2>
</nav>
""", unsafe_allow_html=True)

# Introduction
st.markdown("""
### ✍️ Introduction

I embarked on this project to examine how illegal mining, commonly called *galamsey* in Ghana, impacts the quality of river water. The presence of heavy metals like **Arsenic**, **Lead**, **Cadmium**, and **Chromium** is of particular concern, given their toxicity to both humans and aquatic life.

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
- Visual exploration (bar plots, histograms, KDE)
- K-Means clustering
- HPI calculation

---

### ⚠️ Heavy Metal Concentration Levels by Sample
""")

# Bar plot (concentration levels per sample)
sns.set(style="whitegrid")
plt.figure(figsize=(12, 6))
sns.barplot(data=melted_df, x="Sample", y="Concentration", hue="Metal")
plt.title("Heavy Metal Concentration Levels in River Samples (mg/L)")
plt.ylabel("Concentration (mg/L)")
plt.xlabel("River Sample")
plt.xticks(rotation=45)
plt.legend(title="Metal")
plt.tight_layout()
plt.savefig("visuals/heavy_metal_concentrations.png")
st.image("visuals/heavy_metal_concentrations.png")

# Distribution
st.markdown("""
---

### 📈 Distribution of Heavy Metals Across All Samples

While the bar plot gives a snapshot of how each river sample fares in terms of metal levels, it's also important to look at **how concentrations of each metal are distributed overall**.
""")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
metals = ["Arsenic (mg/L)", "Cadmium (mg/L)", "Chromium (mg/L)", "Lead (mg/L)"]

for ax, metal in zip(axes.flatten(), metals):
    sns.histplot(df[metal], kde=True, bins=10, ax=ax, color="skyblue", edgecolor="black")
    ax.set_title(f'Distribution of {metal}')
    ax.set_xlabel("Concentration (mg/L)")
    ax.set_ylabel("Frequency")

plt.tight_layout()
st.pyplot(fig)

st.markdown("""
#### 📌 Discussion

- **Arsenic** and **Cadmium** are mostly low in concentration but have rare spikes.
- **Chromium** shows a wide range of concentrations, with some samples being extremely polluted.
- **Lead** presents two clusters, indicating two sets of river samples: mildly and highly contaminated.

These distributions show **how widespread and inconsistent** the pollution is. This is a red flag for public health monitoring.

---

### 📏 Exceeding WHO Standards
""")

# WHO limits for heavy metals
who_limits = {
    'Arsenic (mg/L)': 0.01,
    'Cadmium (mg/L)': 0.003,
    'Chromium (mg/L)': 0.05,
    'Lead (mg/L)': 0.01
}

# Check for exceedances
for metal, limit in who_limits.items():
    df[f'{metal} Exceeds'] = df[metal] > limit
st.dataframe(df[["Sample"] + [f"{metal} Exceeds" for metal in who_limits]])

st.markdown("""
Many rivers had at least one metal exceeding WHO limits. This is a concern for public health. It's worth noting that **Arsenic** and **Cadmium** were not consistently high in any sample, but particularly **Chromium** and **Lead**, which were consistently high in some samples.

---

### 🧠 Correlation Insights
""")

# Correlation heatmap
correlation = df.corr(numeric_only=True)
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(correlation, annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

st.markdown("""
**TDS** and **Conductivity** had the strongest correlation with heavy metals. This makes sense because they both measure water quality. **Hardness** is also correlated, but it's not as strong as expected. Calcium and magnesium also closely follow hardness levels. These insights validate the integrity of the dataset.

---

### 🎯 K-Means Clustering

Clustering river samples by metal content to identify risk categories.
""")

# KMeans clustering
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
Clustering identified a group of highly polluted samples, visually separating them from relatively safer ones. This helps prioritize which rivers need **urgent attention**.

---

### 🧮 Health Pollution Index (HPI)

A composite risk index using WHO limits to assess each sample.
""")

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
Samples with **HPI > 100** are marked as high risk. These rivers are **not safe** for domestic use without immediate intervention.

---

### 🛡️ What Can Be Done?

To mitigate the effects of illegal mining on rivers:

- Enforce **stricter mining regulations** and conduct **real-time monitoring**.
- Provide **low-cost water treatment solutions** to rural communities.
- Launch **education campaigns** about water safety and pollution.
- Reclaim degraded land through **reforestation and rehabilitation**.

---

### 🧾 Conclusion

The data confirms that **illegal mining is a major contributor** to heavy metal pollution in Ghanaian rivers. Without proper intervention, **Chromium** and **Lead** levels will continue to pose a serious public health threat.

---

🖋️ **Prepared by:** *Prince Eugene Ofosu*
🔗 [GitHub](https://github.com/Pcosby5)
""")
