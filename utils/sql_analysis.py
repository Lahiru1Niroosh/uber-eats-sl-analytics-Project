import pandas as pd
import sqlite3
import os

# ─────────────────────────────────────────
# SETUP — Load CSVs into SQLite database
# ─────────────────────────────────────────
print("📦 Loading data into SQLite database...")

conn = sqlite3.connect("data/uber_eats_sl.db")

pd.read_csv("data/restaurants.csv").to_sql("restaurants",     conn, if_exists="replace", index=False)
pd.read_csv("data/drivers.csv").to_sql("drivers",             conn, if_exists="replace", index=False)
pd.read_csv("data/orders.csv").to_sql("orders",               conn, if_exists="replace", index=False)
pd.read_csv("data/pricing_history.csv").to_sql("pricing_history", conn, if_exists="replace", index=False)

print("✅ Database created: data/uber_eats_sl.db\n")

os.makedirs("data/sql_results", exist_ok=True)

def run_query(title, sql):
    """Run a SQL query, print results, and save to CSV."""
    print(f"{'─'*60}")
    print(f"📊 {title}")
    print(f"{'─'*60}")
    df = pd.read_sql_query(sql, conn)
    print(df.to_string(index=False))
    filename = title.lower().replace(" ","_").replace("&","and")[:50] + ".csv"
    df.to_csv(f"data/sql_results/{filename}", index=False)
    print(f"💾 Saved → data/sql_results/{filename}\n")
    return df

# ─────────────────────────────────────────
# QUERY 1: Overall Marketplace KPIs
# ─────────────────────────────────────────
run_query("Overall Marketplace KPIs", """
SELECT
    COUNT(*)                                        AS total_orders,
    SUM(CASE WHEN status='Delivered' THEN 1 ELSE 0 END)  AS delivered_orders,
    SUM(CASE WHEN status='Cancelled' THEN 1 ELSE 0 END)  AS cancelled_orders,
    ROUND(
        100.0 * SUM(CASE WHEN status='Delivered' THEN 1 ELSE 0 END) / COUNT(*), 2
    )                                               AS conversion_rate_pct,
    ROUND(SUM(CASE WHEN status='Delivered' THEN total_lkr ELSE 0 END), 2)  AS total_gmv_lkr,
    ROUND(SUM(CASE WHEN status='Delivered' THEN commission_lkr ELSE 0 END), 2) AS total_revenue_lkr,
    ROUND(AVG(CASE WHEN status='Delivered' THEN delivery_time_min END), 1) AS avg_delivery_min
FROM orders
""")

# ─────────────────────────────────────────
# QUERY 2: Monthly Revenue Trend
# ─────────────────────────────────────────
run_query("Monthly Revenue Trend", """
SELECT
    SUBSTR(order_date, 1, 7)                        AS month,
    COUNT(*)                                        AS total_orders,
    SUM(CASE WHEN status='Delivered' THEN 1 ELSE 0 END) AS delivered,
    ROUND(100.0 * SUM(CASE WHEN status='Delivered' THEN 1 ELSE 0 END) / COUNT(*), 2) AS conversion_pct,
    ROUND(SUM(CASE WHEN status='Delivered' THEN total_lkr ELSE 0 END), 0) AS gmv_lkr,
    ROUND(SUM(CASE WHEN status='Delivered' THEN commission_lkr ELSE 0 END), 0) AS revenue_lkr
FROM orders
GROUP BY month
ORDER BY month
""")

# ─────────────────────────────────────────
# QUERY 3: Top 10 Restaurants by Revenue
# ─────────────────────────────────────────
run_query("Top 10 Restaurants by Revenue", """
SELECT
    r.restaurant_id,
    r.name,
    r.category,
    r.zone,
    r.pricing_tier,
    COUNT(o.order_id)                               AS total_orders,
    ROUND(SUM(CASE WHEN o.status='Delivered' THEN o.commission_lkr ELSE 0 END), 0) AS revenue_lkr,
    ROUND(100.0 * SUM(CASE WHEN o.status='Delivered' THEN 1 ELSE 0 END) / COUNT(*), 1) AS conversion_pct,
    ROUND(AVG(CASE WHEN o.status='Delivered' THEN o.delivery_time_min END), 1) AS avg_delivery_min
FROM orders o
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
GROUP BY r.restaurant_id
ORDER BY revenue_lkr DESC
LIMIT 10
""")

# ─────────────────────────────────────────
# QUERY 4: Revenue by Category
# ─────────────────────────────────────────
run_query("Revenue by Category", """
SELECT
    r.category,
    COUNT(o.order_id)                               AS total_orders,
    ROUND(SUM(CASE WHEN o.status='Delivered' THEN o.total_lkr ELSE 0 END), 0)      AS gmv_lkr,
    ROUND(SUM(CASE WHEN o.status='Delivered' THEN o.commission_lkr ELSE 0 END), 0) AS revenue_lkr,
    ROUND(100.0 * SUM(CASE WHEN o.status='Delivered' THEN 1 ELSE 0 END) / COUNT(*), 1) AS conversion_pct,
    ROUND(AVG(CASE WHEN o.status='Delivered' THEN o.total_lkr END), 0)             AS avg_order_value_lkr
FROM orders o
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
GROUP BY r.category
ORDER BY revenue_lkr DESC
""")

# ─────────────────────────────────────────
# QUERY 5: Peak Hour Analysis
# ─────────────────────────────────────────
run_query("Peak Hour Analysis", """
SELECT
    order_hour                                      AS hour,
    COUNT(*)                                        AS total_orders,
    SUM(CASE WHEN status='Delivered' THEN 1 ELSE 0 END) AS delivered,
    ROUND(100.0 * SUM(CASE WHEN status='Delivered' THEN 1 ELSE 0 END) / COUNT(*), 1) AS conversion_pct,
    ROUND(AVG(CASE WHEN status='Delivered' THEN total_lkr END), 0) AS avg_order_value_lkr
FROM orders
GROUP BY order_hour
ORDER BY order_hour
""")

# ─────────────────────────────────────────
# QUERY 6: Zone Performance
# ─────────────────────────────────────────
run_query("Zone Performance", """
SELECT
    r.zone,
    COUNT(DISTINCT r.restaurant_id)                 AS active_restaurants,
    COUNT(o.order_id)                               AS total_orders,
    ROUND(SUM(CASE WHEN o.status='Delivered' THEN o.total_lkr ELSE 0 END), 0)      AS gmv_lkr,
    ROUND(SUM(CASE WHEN o.status='Delivered' THEN o.commission_lkr ELSE 0 END), 0) AS revenue_lkr,
    ROUND(100.0 * SUM(CASE WHEN o.status='Delivered' THEN 1 ELSE 0 END) / COUNT(*), 1) AS conversion_pct
FROM orders o
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
GROUP BY r.zone
ORDER BY revenue_lkr DESC
""")

# ─────────────────────────────────────────
# QUERY 7: Cancellation Root Cause Analysis
# ─────────────────────────────────────────
run_query("Cancellation Root Cause Analysis", """
SELECT
    cancel_reason,
    COUNT(*)                                        AS cancellations,
    ROUND(100.0 * COUNT(*) /
        (SELECT COUNT(*) FROM orders WHERE status IN ('Cancelled','Refunded')), 2) AS pct_of_cancellations
FROM orders
WHERE status IN ('Cancelled','Refunded')
  AND cancel_reason IS NOT NULL
GROUP BY cancel_reason
ORDER BY cancellations DESC
""")

# ─────────────────────────────────────────
# QUERY 8: Driver Performance Tier
# ─────────────────────────────────────────
run_query("Driver Performance Tier", """
SELECT
    d.vehicle_type,
    COUNT(DISTINCT d.driver_id)                     AS drivers,
    COUNT(o.order_id)                               AS total_deliveries,
    ROUND(AVG(o.delivery_time_min), 1)              AS avg_delivery_min,
    ROUND(AVG(d.rating), 2)                         AS avg_driver_rating
FROM orders o
JOIN drivers d ON o.driver_id = d.driver_id
WHERE o.status = 'Delivered'
GROUP BY d.vehicle_type
ORDER BY avg_delivery_min
""")

# ─────────────────────────────────────────
# QUERY 9: Restaurant Churn Risk Signals
# ─────────────────────────────────────────
run_query("Restaurant Churn Risk Signals", """
SELECT
    r.restaurant_id,
    r.name,
    r.zone,
    r.pricing_tier,
    COUNT(o.order_id)                               AS total_orders,
    ROUND(100.0 * SUM(CASE WHEN o.status='Delivered' THEN 1 ELSE 0 END) / COUNT(*), 1) AS conversion_pct,
    ROUND(AVG(CASE WHEN o.status='Delivered' THEN o.delivery_time_min END), 1) AS avg_delivery_min,
    ROUND(AVG(CASE WHEN o.customer_rating IS NOT NULL THEN o.customer_rating END), 2) AS avg_customer_rating,
    CASE
        WHEN COUNT(o.order_id) < 50
             AND ROUND(100.0 * SUM(CASE WHEN o.status='Delivered' THEN 1 ELSE 0 END)/COUNT(*),1) < 75
        THEN 'HIGH RISK'
        WHEN COUNT(o.order_id) < 100
             OR ROUND(100.0 * SUM(CASE WHEN o.status='Delivered' THEN 1 ELSE 0 END)/COUNT(*),1) < 80
        THEN 'MEDIUM RISK'
        ELSE 'LOW RISK'
    END                                             AS churn_risk
FROM orders o
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
GROUP BY r.restaurant_id
ORDER BY
    CASE churn_risk WHEN 'HIGH RISK' THEN 1 WHEN 'MEDIUM RISK' THEN 2 ELSE 3 END,
    total_orders ASC
LIMIT 20
""")

# ─────────────────────────────────────────
# QUERY 10: Pricing Tier vs Conversion
# ─────────────────────────────────────────
run_query("Pricing Tier vs Conversion & Revenue", """
SELECT
    r.pricing_tier,
    COUNT(DISTINCT r.restaurant_id)                 AS restaurants,
    COUNT(o.order_id)                               AS total_orders,
    ROUND(AVG(o.total_lkr), 0)                      AS avg_order_value_lkr,
    ROUND(100.0 * SUM(CASE WHEN o.status='Delivered' THEN 1 ELSE 0 END) / COUNT(*), 1) AS conversion_pct,
    ROUND(SUM(CASE WHEN o.status='Delivered' THEN o.commission_lkr ELSE 0 END), 0) AS total_revenue_lkr
FROM orders o
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
GROUP BY r.pricing_tier
ORDER BY avg_order_value_lkr
""")

conn.close()

print("="*60)
print("✅ ALL SQL ANALYSIS COMPLETE!")
print("📁 Results saved to: data/sql_results/")
print("📦 Database saved to: data/uber_eats_sl.db")
print("\n➡️  Next Step: Run the Jupyter notebook for deeper analysis")
print("="*60)