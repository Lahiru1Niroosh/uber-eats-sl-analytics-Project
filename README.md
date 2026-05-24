# 🛵 Uber Eats Sri Lanka — Analytics Platform

> **Portfolio Project** · Senior Operations Associate Application · Built with Python, SQL, Streamlit & Machine Learning

![Python](https://img.shields.io/badge/Python-3.11-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red) ![SQLite](https://img.shields.io/badge/SQLite-3-green) ![Plotly](https://img.shields.io/badge/Plotly-5.x-purple)

---

## 📌 Project Overview

This end-to-end analytics platform simulates the real-world data operations of **Uber Eats Sri Lanka** — covering marketplace health monitoring, pricing intelligence, restaurant partner performance, driver operations, and ML-powered churn prediction.

Built to demonstrate the exact skills required for the **Senior Operations Associate** role at Uber Eats Colombo:

| JD Requirement | How It's Addressed |
|---|---|
| SQL Data Analysis | 10 business queries across marketplace KPIs, revenue, churn signals |
| Pricing Models | Price elasticity model measuring demand sensitivity |
| Data Visualization | 5-page interactive Streamlit dashboard with Plotly charts |
| Marketplace Health Monitoring | GMV, conversion rate, peak demand heatmaps |
| Root Cause Analysis | Cancellation breakdown by reason type |
| Driver / Courier Operations | Fleet performance, delivery time, zone activity |
| Churn & Retention | Random Forest ML model scoring 200 restaurant partners |
| Stakeholder Communication | Business summary with data-driven recommendations |
| Automated Workflows | Modular Python pipeline: generate → analyze → visualize |

---

## 🗂️ Project Structure

```
uber-eats-sl-analytics/
│
├── data/
│   ├── uber_eats_sl.db          ← SQLite database (4 tables)
│   ├── orders.csv               ← 70,000+ orders · Full year 2024
│   ├── restaurants.csv          ← 200 restaurant partners
│   ├── drivers.csv              ← 300 couriers
│   ├── pricing_history.csv      ← Monthly pricing per restaurant
│   ├── charts/                  ← 6 static analysis charts (PNG)
│   └── sql_results/             ← 10 SQL query outputs + churn predictions
│
├── utils/
│   ├── generate_data.py         ← Synthetic dataset generator
│   ├── sql_analysis.py          ← SQL analytics queries
│   └── analysis.py              ← Charts, elasticity model, churn ML model
│
├── app.py                       ← Streamlit dashboard (5 pages)
├── README.md                    ← This file
└── requirements.txt             ← Python dependencies
```

---

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/Lahiru1Niroosh/uber-eats-sl-analytics-Project
cd uber-eats-sl-analytics-Project
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Generate the dataset
```bash
python utils/generate_data.py
```

### 5. Run SQL analysis
```bash
python utils/sql_analysis.py
```

### 6. Run deep analysis + ML model
```bash
python utils/analysis.py
```

### 7. Launch the dashboard
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 📊 Dashboard Pages

| Page | Description |
|---|---|
| 📊 Marketplace | KPIs, GMV trend, order status, peak hour heatmap |
| 💰 Revenue & Pricing | Tier breakdown, category revenue, elasticity model |
| 🏪 Restaurants | Top partners, conversion distribution, zone performance |
| 🚴 Driver Ops | Fleet mix, delivery times, cancellation root cause |
| ⚠️ Churn Risk | ML predictions, risk scores, action list |

---

## 🤖 ML Model — Churn Prediction

- **Algorithm:** Random Forest Classifier
- **Features:** order volume, conversion rate, avg order value, delivery time, cancellation rate, customer rating, pricing tier, category
- **Target:** Binary churn label (low volume + low conversion)
- **Output:** Churn probability score (0–100%) + risk label (High / Medium / Low)
- **Use case:** Partner Success team prioritises outreach to High Risk restaurants

---

## 📈 Key Findings

- **Conversion Rate:** ~82% platform-wide (18% order fallout = revenue loss opportunity)
- **Peak Demand:** 12–14h and 19–21h account for ~45% of all daily orders
- **Price Elasticity:** Coefficient ≈ -0.5 (moderate sensitivity — 10% price rise → ~5% order drop)
- **Top Zone:** Colombo 3 / Rajagiriya consistently highest GMV
- **Churn Risk:** ~15% of restaurant partners show High churn signals

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python (Pandas, NumPy) | Data manipulation and analysis |
| SQLite + SQL | Database layer and business queries |
| Scikit-learn | Churn prediction ML model |
| Plotly | Interactive charts |
| Streamlit | Web dashboard |
| Faker | Synthetic data generation |
| Matplotlib / Seaborn | Static chart exports |

---

## 👤 Author

Built as a portfolio project for the **Senior Operations Associate** role at Uber Eats Sri Lanka (via LanceSoft).

Demonstrates: SQL analytics · Python data analysis · pricing modeling · ML churn prediction · business intelligence dashboards · stakeholder-ready insights.
