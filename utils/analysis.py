import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import sqlite3
import os
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import warnings
warnings.filterwarnings("ignore")

os.makedirs("data/charts", exist_ok=True)

# ── Style ────────────────────────────────
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({"figure.dpi": 130, "figure.facecolor": "white"})
UBER_BLACK = "#000000"
UBER_GREEN = "#06C167"

# ── Load data ────────────────────────────
conn = sqlite3.connect("data/uber_eats_sl.db")
orders_df      = pd.read_sql("SELECT * FROM orders",          conn)
restaurants_df = pd.read_sql("SELECT * FROM restaurants",     conn)
drivers_df     = pd.read_sql("SELECT * FROM drivers",         conn)
pricing_df     = pd.read_sql("SELECT * FROM pricing_history", conn)
conn.close()

orders_df["order_date"] = pd.to_datetime(orders_df["order_date"])
orders_df["month"]      = orders_df["order_date"].dt.to_period("M")
delivered = orders_df[orders_df["status"] == "Delivered"].copy()

print("✅ Data loaded")
print(f"   Orders: {len(orders_df):,}  |  Delivered: {len(delivered):,}")
print(f"   Restaurants: {len(restaurants_df)}  |  Drivers: {len(drivers_df)}\n")


# ════════════════════════════════════════
# CHART 1 — Monthly GMV & Conversion Rate
# ════════════════════════════════════════
monthly = (orders_df.groupby("month")
           .agg(total=("order_id","count"),
                delivered=("status", lambda x: (x=="Delivered").sum()),
                gmv=("total_lkr", lambda x: x[orders_df.loc[x.index,"status"]=="Delivered"].sum()))
           .reset_index())
monthly["conversion"] = monthly["delivered"] / monthly["total"] * 100
monthly["month_str"]  = monthly["month"].astype(str)

fig, ax1 = plt.subplots(figsize=(12, 5))
ax2 = ax1.twinx()
bars = ax1.bar(monthly["month_str"], monthly["gmv"]/1e6, color=UBER_GREEN, alpha=0.75, label="GMV (M LKR)")
ax2.plot(monthly["month_str"], monthly["conversion"], color=UBER_BLACK,
         marker="o", linewidth=2.2, label="Conversion %")
ax1.set_ylabel("GMV (Million LKR)", fontsize=11)
ax2.set_ylabel("Conversion Rate (%)", fontsize=11)
ax1.set_xlabel("Month", fontsize=11)
plt.title("Monthly GMV vs Order Conversion Rate — Uber Eats Sri Lanka 2024", fontsize=13, fontweight="bold")
ax1.tick_params(axis="x", rotation=45)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.1f}M"))
lines2, labels2 = ax2.get_legend_handles_labels()
lines1, labels1 = ax1.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
plt.tight_layout()
plt.savefig("data/charts/01_monthly_gmv_conversion.png")
plt.close()
print("📊 Chart 1 saved — Monthly GMV & Conversion")


# ════════════════════════════════════════
# CHART 2 — Revenue by Category (horizontal bar)
# ════════════════════════════════════════
cat_rev = (delivered.merge(restaurants_df[["restaurant_id","category"]], on="restaurant_id")
           .groupby("category")["commission_lkr"].sum()
           .sort_values(ascending=True))

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(cat_rev.index, cat_rev.values/1e6, color=UBER_GREEN, edgecolor="white")
for bar, val in zip(bars, cat_rev.values):
    ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
            f"LKR {val/1e6:.2f}M", va="center", fontsize=9)
ax.set_xlabel("Total Commission Revenue (Million LKR)", fontsize=11)
ax.set_title("Commission Revenue by Food Category — 2024", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("data/charts/02_revenue_by_category.png")
plt.close()
print("📊 Chart 2 saved — Revenue by Category")


# ════════════════════════════════════════
# CHART 3 — Peak Hour Heatmap (day × hour)
# ════════════════════════════════════════
orders_df["dow_num"] = orders_df["order_date"].dt.dayofweek
orders_df["dow"]     = orders_df["order_date"].dt.day_name()
heat = (orders_df[orders_df["status"]=="Delivered"]
        .groupby(["dow_num","dow","order_hour"])["order_id"]
        .count().reset_index())
heat.columns = ["dow_num","dow","hour","orders"]
pivot = heat.pivot_table(index="dow", columns="hour", values="orders", aggfunc="mean")
day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
pivot = pivot.reindex([d for d in day_order if d in pivot.index])

fig, ax = plt.subplots(figsize=(14, 5))
sns.heatmap(pivot, cmap="YlGn", linewidths=0.4, ax=ax,
            cbar_kws={"label": "Avg Delivered Orders"})
ax.set_title("Order Heatmap — Day of Week × Hour (Colombo, 2024)", fontsize=13, fontweight="bold")
ax.set_xlabel("Hour of Day", fontsize=11)
ax.set_ylabel("")
plt.tight_layout()
plt.savefig("data/charts/03_peak_hour_heatmap.png")
plt.close()
print("📊 Chart 3 saved — Peak Hour Heatmap")


# ════════════════════════════════════════
# CHART 4 — Pricing Elasticity Analysis
# ════════════════════════════════════════
monthly_rest = (orders_df[orders_df["status"]=="Delivered"]
                .assign(month_num=orders_df["order_date"].dt.month)
                .groupby(["restaurant_id","month_num"])
                .agg(orders=("order_id","count"))
                .reset_index())

elasticity_df = monthly_rest.merge(
    pricing_df[["restaurant_id","month","avg_item_price_lkr","commission_rate"]],
    left_on=["restaurant_id","month_num"], right_on=["restaurant_id","month"])

elasticity_df["price_pct_change"] = (
    elasticity_df.groupby("restaurant_id")["avg_item_price_lkr"].pct_change() * 100)
elasticity_df["order_pct_change"] = (
    elasticity_df.groupby("restaurant_id")["orders"].pct_change() * 100)
elasticity_clean = elasticity_df.dropna().query(
    "price_pct_change.between(-30,30) and order_pct_change.between(-60,60)")

fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(elasticity_clean["price_pct_change"],
                     elasticity_clean["order_pct_change"],
                     alpha=0.35, s=18, color=UBER_GREEN)
z = np.polyfit(elasticity_clean["price_pct_change"],
               elasticity_clean["order_pct_change"], 1)
p = np.poly1d(z)
x_line = np.linspace(-30, 30, 100)
ax.plot(x_line, p(x_line), color=UBER_BLACK, linewidth=2, linestyle="--", label=f"Trend (slope={z[0]:.2f})")
ax.axhline(0, color="grey", linewidth=0.8, linestyle=":")
ax.axvline(0, color="grey", linewidth=0.8, linestyle=":")
ax.set_xlabel("Price Change (%)", fontsize=11)
ax.set_ylabel("Order Volume Change (%)", fontsize=11)
ax.set_title("Price Elasticity of Demand — Restaurant Partners", fontsize=13, fontweight="bold")
ax.legend(fontsize=10)
elasticity_coef = z[0]
ax.text(0.02, 0.95, f"Elasticity ≈ {elasticity_coef:.2f}", transform=ax.transAxes,
        fontsize=10, va="top",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#E8F5F0", edgecolor=UBER_GREEN))
plt.tight_layout()
plt.savefig("data/charts/04_price_elasticity.png")
plt.close()
print(f"📊 Chart 4 saved — Price Elasticity (coef: {elasticity_coef:.2f})")


# ════════════════════════════════════════
# CHART 5 — Zone Revenue Map (bar)
# ════════════════════════════════════════
zone_rev = (delivered.merge(restaurants_df[["restaurant_id","zone"]], on="restaurant_id")
            .groupby("zone")["commission_lkr"].sum()
            .sort_values(ascending=False))

fig, ax = plt.subplots(figsize=(12, 5))
colors = [UBER_GREEN if i < 5 else "#AEDFC9" for i in range(len(zone_rev))]
ax.bar(zone_rev.index, zone_rev.values/1e6, color=colors, edgecolor="white")
ax.set_ylabel("Commission Revenue (Million LKR)", fontsize=11)
ax.set_title("Revenue by Colombo Zone — Top Zones Highlighted", fontsize=13, fontweight="bold")
ax.tick_params(axis="x", rotation=45)
plt.tight_layout()
plt.savefig("data/charts/05_zone_revenue.png")
plt.close()
print("📊 Chart 5 saved — Zone Revenue")


# ════════════════════════════════════════
# ML MODEL — Restaurant Churn Prediction
# ════════════════════════════════════════
print("\n🤖 Building Churn Prediction Model...")

# Build features per restaurant
rest_stats = (orders_df.groupby("restaurant_id")
              .agg(total_orders=("order_id","count"),
                   conversion_rate=("status", lambda x: (x=="Delivered").mean()),
                   avg_order_value=("total_lkr","mean"),
                   avg_delivery_time=("delivery_time_min","mean"),
                   cancellation_rate=("status", lambda x: (x=="Cancelled").mean()),
                   avg_customer_rating=("customer_rating","mean"),
                   total_revenue=("commission_lkr","sum"))
              .reset_index())

rest_features = rest_stats.merge(
    restaurants_df[["restaurant_id","pricing_tier","category","has_promoted_listing","rating"]],
    on="restaurant_id")

# Label: churn = low orders AND low conversion
rest_features["churn"] = (
    (rest_features["total_orders"] < rest_features["total_orders"].quantile(0.25)) &
    (rest_features["conversion_rate"] < 0.78)
).astype(int)

print(f"   Churn rate in dataset: {rest_features['churn'].mean()*100:.1f}%")

# Encode categoricals
le_tier = LabelEncoder()
le_cat  = LabelEncoder()
rest_features["pricing_tier_enc"] = le_tier.fit_transform(rest_features["pricing_tier"])
rest_features["category_enc"]     = le_cat.fit_transform(rest_features["category"])

feature_cols = ["total_orders","conversion_rate","avg_order_value","avg_delivery_time",
                "cancellation_rate","avg_customer_rating","total_revenue",
                "pricing_tier_enc","category_enc","has_promoted_listing","rating"]

X = rest_features[feature_cols].fillna(rest_features[feature_cols].median())
y = rest_features["churn"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Train Random Forest
rf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced")
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)
y_prob = rf.predict_proba(X_test)[:,1]

auc = roc_auc_score(y_test, y_prob)
print(f"\n   ✅ Random Forest AUC: {auc:.3f}")
print("\n   Classification Report:")
print(classification_report(y_test, y_pred, target_names=["Retained","Churned"]))

# Feature Importance Chart
importances = pd.Series(rf.feature_importances_, index=feature_cols).sort_values(ascending=True)
fig, ax = plt.subplots(figsize=(10, 6))
importances.plot(kind="barh", ax=ax, color=UBER_GREEN, edgecolor="white")
ax.set_title("Churn Prediction — Feature Importance (Random Forest)", fontsize=13, fontweight="bold")
ax.set_xlabel("Importance Score", fontsize=11)
plt.tight_layout()
plt.savefig("data/charts/06_churn_feature_importance.png")
plt.close()
print("📊 Chart 6 saved — Churn Feature Importance")

# Save churn predictions
rest_features["churn_probability"] = rf.predict_proba(X)[:,1]
rest_features["churn_risk_label"]  = pd.cut(
    rest_features["churn_probability"],
    bins=[0, 0.33, 0.66, 1.0],
    labels=["Low Risk","Medium Risk","High Risk"])

churn_output = rest_features[["restaurant_id","pricing_tier","category",
                               "total_orders","conversion_rate",
                               "churn_probability","churn_risk_label"]].sort_values(
    "churn_probability", ascending=False)
churn_output.to_csv("data/sql_results/churn_predictions.csv", index=False)
print("💾 Churn predictions saved → data/sql_results/churn_predictions.csv")


# ════════════════════════════════════════
# SUMMARY
# ════════════════════════════════════════
print("\n" + "="*60)
print("✅ FULL ANALYSIS COMPLETE")
print("="*60)
print("\n📊 Charts saved to:  data/charts/")
print("   01_monthly_gmv_conversion.png")
print("   02_revenue_by_category.png")
print("   03_peak_hour_heatmap.png")
print("   04_price_elasticity.png")
print("   05_zone_revenue.png")
print("   06_churn_feature_importance.png")
print("\n💾 Model output:     data/sql_results/churn_predictions.csv")
print(f"\n📌 Key Findings:")
print(f"   • Price Elasticity Coefficient : {elasticity_coef:.2f}")
print(f"   • Churn Prediction AUC         : {auc:.3f}")
print(f"   • High-risk restaurants        : {(rest_features['churn_risk_label']=='High Risk').sum()}")
print(f"\n➡️  Next Step: Run app.py to launch the Streamlit dashboard")