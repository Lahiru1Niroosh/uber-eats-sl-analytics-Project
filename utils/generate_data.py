import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os

fake = Faker()
random.seed(42)
np.random.seed(42)

os.makedirs("data", exist_ok=True)

# ─────────────────────────────────────────
# 1. RESTAURANTS (200 restaurants)
# ─────────────────────────────────────────
colombo_zones = ["Colombo 1","Colombo 2","Colombo 3","Colombo 4",
                 "Colombo 5","Colombo 6","Colombo 7","Colombo 8",
                 "Nugegoda","Dehiwala","Ratmalana","Maharagama",
                 "Kottawa","Battaramulla","Rajagiriya"]

categories = ["Rice & Curry","Burgers","Pizza","Chinese","Kottu",
              "Seafood","Desserts","Beverages","Sandwiches","Indian"]

pricing_tiers = ["Budget","Mid-range","Premium"]

restaurants = []
for i in range(1, 201):
    tier = random.choice(pricing_tiers)
    base_rating = {"Budget": 3.8, "Mid-range": 4.1, "Premium": 4.4}[tier]
    restaurants.append({
        "restaurant_id": f"R{i:03d}",
        "name": fake.company().replace(",","") + " " + random.choice(["Kitchen","Eats","House","Bites","Cafe"]),
        "category": random.choice(categories),
        "zone": random.choice(colombo_zones),
        "pricing_tier": tier,
        "avg_item_price_lkr": round(random.uniform(
            {"Budget":150,"Mid-range":400,"Premium":900}[tier],
            {"Budget":400,"Mid-range":900,"Premium":2500}[tier]), 2),
        "commission_rate": round(random.uniform(
            {"Budget":0.18,"Mid-range":0.22,"Premium":0.27}[tier],
            {"Budget":0.22,"Mid-range":0.27,"Premium":0.32}[tier]), 3),
        "rating": round(np.clip(np.random.normal(base_rating, 0.3), 1, 5), 1),
        "total_reviews": random.randint(50, 5000),
        "is_active": random.choices([1, 0], weights=[90, 10])[0],
        "onboarded_date": fake.date_between(start_date="-3y", end_date="-1m"),
        "has_promoted_listing": random.choices([1,0], weights=[35,65])[0],
    })

restaurants_df = pd.DataFrame(restaurants)
restaurants_df.to_csv("data/restaurants.csv", index=False)
print(f"✅ Restaurants: {len(restaurants_df)} rows")

# ─────────────────────────────────────────
# 2. DRIVERS / COURIERS (300 drivers)
# ─────────────────────────────────────────
vehicle_types = ["Bicycle","Motorbike","Car"]

drivers = []
for i in range(1, 301):
    zone = random.choice(colombo_zones)
    drivers.append({
        "driver_id": f"D{i:03d}",
        "name": fake.name(),
        "zone": zone,
        "vehicle_type": random.choice(vehicle_types),
        "rating": round(np.clip(np.random.normal(4.2, 0.4), 1, 5), 1),
        "total_deliveries": random.randint(10, 3000),
        "is_active": random.choices([1,0], weights=[85,15])[0],
        "joined_date": fake.date_between(start_date="-2y", end_date="-1m"),
        "avg_delivery_time_min": round(random.uniform(15, 55), 1),
    })

drivers_df = pd.DataFrame(drivers)
drivers_df.to_csv("data/drivers.csv", index=False)
print(f"✅ Drivers: {len(drivers_df)} rows")

# ─────────────────────────────────────────
# 3. ORDERS — full year 2024 (~70,000 orders)
# ─────────────────────────────────────────
active_restaurants = restaurants_df[restaurants_df["is_active"]==1]["restaurant_id"].tolist()
active_drivers     = drivers_df[drivers_df["is_active"]==1]["driver_id"].tolist()

start_date = datetime(2024, 1, 1)
end_date   = datetime(2024, 12, 31)

order_statuses  = ["Delivered","Cancelled","Refunded"]
cancel_reasons  = ["Customer cancelled","Restaurant rejected","Driver unavailable","Timeout", None]
payment_methods = ["Card","Cash","UberCash","Corporate"]

orders = []
order_id = 1

for day_offset in range((end_date - start_date).days + 1):
    current_date = start_date + timedelta(days=day_offset)
    weekday  = current_date.weekday()
    is_weekend = weekday >= 4

    daily_orders = random.randint(180, 280) if is_weekend else random.randint(120, 200)

    for _ in range(daily_orders):
        r_id  = random.choice(active_restaurants)
        d_id  = random.choice(active_drivers)
        rdata = restaurants_df[restaurants_df["restaurant_id"]==r_id].iloc[0]

        # Realistic peak hours: lunch 11-14, dinner 18-22
        hour = random.choices(
            list(range(24)),
            weights=[1,1,1,1,1,1,2,3,4,5,6,9,10,10,7,5,4,5,9,10,9,7,4,2]
        )[0]
        minute    = random.randint(0, 59)
        order_time = current_date.replace(hour=hour, minute=minute)

        status    = random.choices(order_statuses, weights=[82,13,5])[0]
        items     = random.randint(1, 5)
        subtotal  = round(rdata["avg_item_price_lkr"] * items * random.uniform(0.8, 1.3), 2)
        delivery_fee = round(random.uniform(80, 250), 2)
        discount  = round(subtotal * random.uniform(0, 0.2) if random.random() < 0.3 else 0, 2)
        total     = round(subtotal + delivery_fee - discount, 2)
        commission = round(subtotal * rdata["commission_rate"], 2)
        delivery_time = round(rdata["avg_item_price_lkr"] / 100 + random.uniform(10, 40), 1)

        orders.append({
            "order_id":          f"ORD{order_id:06d}",
            "restaurant_id":     r_id,
            "driver_id":         d_id,
            "order_datetime":    order_time,
            "order_date":        order_time.date(),
            "order_hour":        hour,
            "day_of_week":       current_date.strftime("%A"),
            "is_weekend":        int(is_weekend),
            "status":            status,
            "num_items":         items,
            "subtotal_lkr":      subtotal,
            "delivery_fee_lkr":  delivery_fee,
            "discount_lkr":      discount,
            "total_lkr":         total,
            "commission_lkr":    commission,
            "payment_method":    random.choice(payment_methods),
            "delivery_time_min": delivery_time if status=="Delivered" else None,
            "cancel_reason":     random.choice(cancel_reasons) if status!="Delivered" else None,
            "customer_rated":    random.choices([1,0], weights=[60,40])[0] if status=="Delivered" else 0,
            "customer_rating":   round(random.uniform(3,5),1) if status=="Delivered" and random.random()<0.6 else None,
        })
        order_id += 1

orders_df = pd.DataFrame(orders)
orders_df.to_csv("data/orders.csv", index=False)
print(f"✅ Orders: {len(orders_df):,} rows")

# ─────────────────────────────────────────
# 4. PRICING HISTORY (monthly per restaurant)
# ─────────────────────────────────────────
pricing_history = []
for _, r in restaurants_df.iterrows():
    current_rate  = r["commission_rate"]
    current_price = r["avg_item_price_lkr"]
    for month in range(1, 13):
        change        = random.uniform(-0.02, 0.02)
        current_rate  = round(np.clip(current_rate + change, 0.10, 0.40), 3)
        price_change  = random.uniform(-50, 100)
        current_price = round(max(100, current_price + price_change), 2)
        pricing_history.append({
            "restaurant_id":      r["restaurant_id"],
            "month":              month,
            "year":               2024,
            "commission_rate":    current_rate,
            "avg_item_price_lkr": current_price,
            "pricing_tier":       r["pricing_tier"],
            "category":           r["category"],
        })

pricing_df = pd.DataFrame(pricing_history)
pricing_df.to_csv("data/pricing_history.csv", index=False)
print(f"✅ Pricing history: {len(pricing_df):,} rows")

# ─────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────
print("\n📁 All files saved to /data folder:")
for f in ["restaurants.csv","drivers.csv","orders.csv","pricing_history.csv"]:
    df = pd.read_csv(f"data/{f}")
    print(f"   {f}: {df.shape[0]:,} rows × {df.shape[1]} columns")

print("\n🎉 Dataset generation complete! Move to Step 2: SQL Analysis")