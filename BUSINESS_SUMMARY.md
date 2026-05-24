# Uber Eats Sri Lanka — Marketplace Business Review
**Period:** Full Year 2024 · **Market:** Colombo Region · **Prepared by:** Analytics Team

---

## Executive Summary

The Uber Eats Sri Lanka platform processed over **70,000 orders** in 2024, generating approximately **LKR 180M+ in GMV** and **LKR 45M+ in commission revenue** across 200 restaurant partners in the Colombo region. The platform demonstrates strong fundamentals with an **82% delivery conversion rate**, but faces clear operational challenges in supply-side reliability and partner retention that represent meaningful growth opportunities.

---

## 1. Marketplace Health

### What the data shows
- **Conversion rate of ~82%** is solid but leaves ~18% of orders failing — primarily from cancellations
- **GMV grew consistently** across the year with strong weekend uplift (+25–30% vs weekdays)
- **Peak windows are narrow:** 12–14h and 19–21h account for nearly half of all daily order volume
- **Payment mix:** Card and UberCash dominate, indicating a digitally-engaged customer base

### Business implication
The platform's core demand engine is healthy. The bottleneck is not demand — it is **supply reliability during peaks**. Every cancelled order during peak hours is a lost customer experience and potential long-term churn.

### Recommendation
Introduce **dynamic driver incentives** during 11:30–14:30 and 18:30–21:30 to ensure courier availability matches demand. A 10% reduction in peak cancellations would recover approximately LKR 2–3M in annual GMV.

---

## 2. Pricing & Revenue

### What the data shows
- **Mid-range tier restaurants** generate the highest total commission despite lower per-order values — driven by volume
- **Premium tier** has highest average order value (LKR 900–2,500) but lower order frequency
- **Price elasticity coefficient ≈ -0.5:** For every 10% price increase, order volume drops ~5%
- **Discount usage:** ~30% of orders include a discount, averaging LKR 80–120 per order

### Business implication
The platform is moderately price-sensitive. Aggressive commission increases will have a measurable negative impact on order volume. Pricing changes must be modelled against elasticity estimates before implementation.

### Recommendation
- For **Budget tier restaurants:** keep commission stable (18–22%) to protect order volume
- For **Premium tier:** test a 2% commission increase with 30-day monitoring — low elasticity risk
- **Discount strategy:** shift from blanket discounts to targeted promotions for lapsed customers only

---

## 3. Restaurant Partner Performance

### What the data shows
- **Top 10 restaurants** account for a disproportionate share of platform revenue — classic Pareto distribution
- **Conversion rate variance is wide:** some restaurants convert at 90%+, others below 70%
- **Colombo 3, Rajagiriya, and Battaramulla** are top revenue zones — high-density, high-income areas
- **Rice & Curry and Kottu** are the highest-revenue categories — core Sri Lankan demand

### Business implication
Partner quality is uneven. Low-converting restaurants drag down platform metrics and create poor customer experiences. The gap between top and bottom performers suggests an **onboarding and operational coaching gap**, not a demand problem.

### Recommendation
- Introduce a **Partner Health Score** (conversion rate + rating + order volume) to segment partners
- Assign Partner Success Managers to bottom-quartile restaurants for 60-day coaching sprints
- Create a **"Platinum Partner" programme** for top 20 restaurants with premium placement and dedicated support

---

## 4. Driver & Courier Operations

### What the data shows
- **Motorbikes are the most efficient vehicle** — fastest average delivery times across all zones
- **Driver-unavailable** and **Timeout** cancellations represent the largest cancel categories
- **Average delivery time: ~32 minutes** — competitive but with room to improve in outer zones (Kottawa, Ratmalana)
- **Driver ratings are high overall** (avg 4.2★) but distribution shows a long tail of low-rated couriers

### Business implication
Supply-side failures (driver unavailability, timeouts) are the primary driver of cancellations. This is a **solvable operational problem** — not a structural market issue.

### Recommendation
- Launch **"Peak Guarantee" programme:** guaranteed minimum earnings for drivers active during 12–14h and 19–21h
- Implement **auto-reassignment logic** for orders not accepted within 90 seconds to reduce timeouts
- Introduce **quarterly driver rating reviews** — couriers below 3.8★ for 2 consecutive quarters enter a performance improvement programme

---

## 5. Partner Churn Risk

### What the data shows
- **~15% of restaurant partners** are flagged as High churn risk by the ML model
- High-risk partners show: fewer than 50 monthly orders, conversion below 75%, low customer ratings
- **Churn risk varies by category:** some food categories show systematically higher churn — likely due to higher competition or lower demand density
- Partners without Promoted Listings churn at a higher rate

### Business implication
Losing a restaurant partner has a compounding cost: lost commission revenue, reduced menu variety for customers, and potential customer churn if their favourite restaurant disappears. **Proactive retention is far cheaper than reacquisition.**

### Recommendation

**Immediate (0–30 days)**
- Contact all 30 High Risk restaurants this week
- Offer 30-day commission reduction (5–8%) in exchange for a commitment to improve operational metrics
- Activate free Promoted Listing for 2 weeks to boost order volume

**Short-term (30–90 days)**
- Assign dedicated Partner Success Manager to each High Risk account
- Run bi-weekly check-in calls to diagnose operational blockers (menu quality, fulfilment speed, pricing)
- Track weekly: if conversion does not improve by week 6, escalate to regional head

**Long-term (90+ days)**
- Build an **early warning system** that flags restaurants moving toward High Risk 60 days before they reach that state
- Integrate churn score into the Partner Success team's weekly dashboard as a core KPI

---

## Summary: Priority Actions

| Priority | Action | Expected Impact |
|---|---|---|
| 🔴 High | Peak-hour driver incentive programme | -10% cancellation rate |
| 🔴 High | Contact 30 High Risk restaurant partners | Prevent LKR 3–5M revenue loss |
| 🟡 Medium | Partner Health Score + coaching programme | +5% avg conversion rate |
| 🟡 Medium | Targeted discount strategy (lapsed customers only) | -15% discount spend |
| 🟢 Low | Premium tier commission test (+2%) | +LKR 500K annual revenue |
| 🟢 Low | Quarterly driver rating review programme | +0.2 avg delivery rating |

---

*This analysis is based on simulated 2024 platform data. All figures are illustrative and designed to demonstrate analytical methodology and business thinking.*