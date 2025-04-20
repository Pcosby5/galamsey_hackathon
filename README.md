# 📘 Heavy Metal Water Quality Dashboard

This project presents an interactive **Streamlit dashboard** designed to analyze and visualize the impact of **illegal mining (galamsey)** on the quality of river water in Ghana. The dashboard focuses on **heavy metal contamination**, particularly **Arsenic, Cadmium, Chromium**, and **Lead**, using clustering, correlation, WHO threshold checks, and a custom **Health Pollution Index (HPI)**.

---

## 🧠 Objective

To provide a comprehensive tool for:

- Understanding the levels and spread of heavy metal pollutants in water bodies
- Identifying river samples exceeding WHO safety thresholds
- Categorizing contamination severity through clustering
- Quantifying health risks using a computed HPI score
- Recommending actionable interventions

---

## 📊 Features

- 📦 Loads and renames dataset columns automatically
- 📈 **Bar charts** showing metal concentrations per sample
- 📉 **Distribution plots** (histogram + KDE) for overall heavy metal trends
- ✅ **WHO threshold check** — highlights samples exceeding safe limits
- 🔥 **Correlation heatmap** of water quality parameters
- 🧬 **K-Means clustering** to group similar pollution levels
- 🧮 **HPI Score** and health risk categorization
- ✍️ Markdown-based explanations and recommendations

---

## 📁 Dataset

The dashboard uses an Excel file named `DATASET_v0.1.xlsx` with a sheet titled `"Data Sheet"` containing:

- Heavy Metal Concentrations (mg/L):
  - Arsenic
  - Cadmium
  - Chromium
  - Lead
- Water Chemistry Metrics:
  - pH
  - TDS (Total Dissolved Solids)
  - Conductivity
  - Total Hardness
  - Calcium & Magnesium Hardness

---

## 🚀 How to Run

### 1. Clone this repository

```bash
git clone https://github.com/your-username/heavy-metal-dashboard.git
cd heavy-metal-dashboard

## 2. Install Dependencies

Using a virtual environment is recommended:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

If `requirements.txt` is not provided, install dependencies manually:

```bash
pip install streamlit pandas seaborn matplotlib scikit-learn openpyxl
```

---

## 3. Add Your Dataset

Ensure `DATASET_v0.1.xlsx` is in the project root with the correct structure.

---

## 4. Run the Dashboard

```bash
streamlit run dashboard.py
```

---

## 🧮 Health Pollution Index (HPI)

To assess health risk from heavy metals, the dashboard calculates:

```
Qi = (Observed Concentration / WHO Limit) * 100
HPI = Average of all Qi scores
```

### Risk Categories:

| HPI Score | Risk Level |
|-----------|------------|
| 0–50      | Low        |
| 51–100    | Medium     |
| >100      | High       |

This approach helps visualize and quantify the cumulative health threat posed by heavy metal contamination in each sample.

---

## 💬 Discussion & Impact

The dashboard reveals that certain river sources are contaminated well beyond WHO's acceptable limits—especially for **Chromium and Lead**. By combining clustering and correlation analyses with visualizations, it empowers users to:

- Identify high-risk zones
- Understand pollution patterns
- Advocate for environmental health interventions

**Illegal mining (galamsey)** has contributed significantly to this degradation, making this tool vital for:

- Policymakers
- Scientists & Environmental Analysts
- Local communities
- NGOs & Advocacy groups

---

## 🛡️ Recommendations

Based on insights from the analysis, we recommend:

- Real-time water monitoring systems to detect illegal discharges
- Reforestation and land reclamation projects in affected areas
- Public education campaigns on the dangers of consuming contaminated water
- Provision of water purification kits or boreholes for safe drinking
- Strict enforcement of mining regulations and sustainable mining alternatives

---

## 🧠 Behind the Dashboard: `dashboard.py`

The logic includes:

- Loading and renaming Excel columns
- Bar plots and histograms using Seaborn and Matplotlib
- Threshold logic against WHO safety values
- Correlation heatmap via Seaborn
- K-Means clustering using `sklearn`
- HPI computation and health classification

This structure makes the dashboard adaptable to similar public health or environmental datasets.

---

## 📄 Requirements

You can create a `requirements.txt` with the following:

```
streamlit
pandas
matplotlib
seaborn
scikit-learn
openpyxl
```

To generate it manually, run:

```bash
pip freeze > requirements.txt
```

---

## ✍️ Author

**Prince Eugene Ofosu**
Biomedical Scientist & Software Developer
📧 [pcosby50@gmail.com](mailto:pcosby50@gmail.com)
🔗 GitHub: [@pcosby5](https://github.com/pcosby5)

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 🙌 Acknowledgements

- **World Health Organization (WHO)** for health standards
- **Streamlit, Pandas, Scikit-learn, Seaborn & Matplotlib** for data science tools
- **Ghana’s local communities** facing the effects of illegal mining
