"""
data_generator.py
-----------------
Generates realistic synthetic data for the dashboard.
All data reflects Lean In's mission context: Circles growth, member engagement,
career advancement outcomes, and geographic expansion.

Seeded for reproducibility. No external data sources required.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

RNG = np.random.default_rng(42)
random.seed(42)

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
START_DATE = datetime(2022, 1, 1)
END_DATE   = datetime(2025, 3, 31)
N_CIRCLES  = 1_200
N_MEMBERS  = 18_000

COUNTRIES = {
    "United States": 0.42,
    "United Kingdom": 0.09,
    "Canada": 0.07,
    "India": 0.08,
    "Germany": 0.05,
    "Australia": 0.04,
    "Brazil": 0.04,
    "Nigeria": 0.03,
    "Mexico": 0.03,
    "France": 0.03,
    "Japan": 0.03,
    "Singapore": 0.02,
    "South Africa": 0.02,
    "Other": 0.05,
}

INDUSTRIES = [
    "Technology", "Finance", "Healthcare", "Education",
    "Consulting", "Media & Comms", "Government/NGO",
    "Legal", "Consumer/Retail", "Manufacturing",
]

CIRCLE_TYPES = ["Workplace", "Community", "University", "Military", "Online-Only"]

SENIORITY_LEVELS = [
    "Individual Contributor", "Manager", "Senior Manager",
    "Director", "VP / SVP", "C-Suite / Exec",
]


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def random_dates(start: datetime, end: datetime, n: int) -> pd.Series:
    delta = (end - start).days
    offsets = RNG.integers(0, delta, n)
    return pd.Series([start + timedelta(days=int(d)) for d in offsets])


def weighted_choice(options: dict, n: int) -> list:
    keys = list(options.keys())
    weights = list(options.values())
    return RNG.choice(keys, size=n, p=weights).tolist()


# ─────────────────────────────────────────────
# 1. CIRCLES TABLE
# ─────────────────────────────────────────────
def generate_circles() -> pd.DataFrame:
    circle_ids = [f"CIR-{i:05d}" for i in range(1, N_CIRCLES + 1)]
    founded = random_dates(START_DATE, END_DATE, N_CIRCLES)

    # Circles started in last 6 months have higher churn risk
    status_probs = []
    for d in founded:
        age_months = (END_DATE - d).days / 30
        if age_months < 3:
            probs = [0.65, 0.20, 0.15]   # active / at_risk / inactive
        elif age_months < 12:
            probs = [0.72, 0.15, 0.13]
        else:
            probs = [0.78, 0.12, 0.10]
        status_probs.append(RNG.choice(["Active", "At Risk", "Inactive"], p=probs))

    circle_size = RNG.integers(4, 16, N_CIRCLES)

    df = pd.DataFrame({
        "circle_id":       circle_ids,
        "founded_date":    founded,
        "country":         weighted_choice(COUNTRIES, N_CIRCLES),
        "circle_type":     RNG.choice(CIRCLE_TYPES, N_CIRCLES).tolist(),
        "size":            circle_size,
        "status":          status_probs,
        "meetings_held":   RNG.integers(0, 36, N_CIRCLES),
        "avg_attendance_pct": np.clip(RNG.normal(0.72, 0.15, N_CIRCLES), 0.20, 1.0).round(2),
        "has_facilitator_training": RNG.choice([True, False], N_CIRCLES, p=[0.58, 0.42]).tolist(),
        "uses_curriculum": RNG.choice([True, False], N_CIRCLES, p=[0.64, 0.36]).tolist(),
        "nps_score":       np.clip(RNG.normal(62, 18, N_CIRCLES), -100, 100).round(0),
    })

    # Circles with training + curriculum skew better NPS
    mask = df["has_facilitator_training"] & df["uses_curriculum"]
    df.loc[mask, "nps_score"] = np.clip(df.loc[mask, "nps_score"] + 15, -100, 100)

    return df


# ─────────────────────────────────────────────
# 2. MEMBERS TABLE
# ─────────────────────────────────────────────
def generate_members(circles: pd.DataFrame) -> pd.DataFrame:
    member_ids = [f"MEM-{i:07d}" for i in range(1, N_MEMBERS + 1)]

    # Assign each member to a circle (weighted by circle size)
    weights = circles["size"].values / circles["size"].sum()
    assigned_circles = RNG.choice(circles["circle_id"].values, size=N_MEMBERS, p=weights)

    # Join date >= circle founded date
    circle_founded = circles.set_index("circle_id")["founded_date"]
    join_dates = []
    for cid in assigned_circles:
        cf = circle_founded[cid]
        days_available = max((END_DATE - cf).days, 1)
        offset = RNG.integers(0, days_available)
        join_dates.append(cf + timedelta(days=int(offset)))

    seniority_at_join = RNG.choice(SENIORITY_LEVELS, N_MEMBERS,
                                    p=[0.30, 0.28, 0.18, 0.12, 0.08, 0.04]).tolist()

    # Simulate promotion: higher probability for Circle members (mission proof-point)
    promotion_base = {"Individual Contributor": 0.22, "Manager": 0.18,
                      "Senior Manager": 0.14, "Director": 0.10, "VP / SVP": 0.06, "C-Suite / Exec": 0.02}
    got_promoted = []
    seniority_now = []
    for s in seniority_at_join:
        idx = SENIORITY_LEVELS.index(s)
        promoted = RNG.random() < promotion_base[s]
        got_promoted.append(bool(promoted))
        if promoted and idx < len(SENIORITY_LEVELS) - 1:
            seniority_now.append(SENIORITY_LEVELS[idx + 1])
        else:
            seniority_now.append(s)

    df = pd.DataFrame({
        "member_id":          member_ids,
        "circle_id":          assigned_circles,
        "join_date":          join_dates,
        "country":            RNG.choice(list(COUNTRIES.keys()), N_MEMBERS,
                                          p=list(COUNTRIES.values())).tolist(),
        "industry":           RNG.choice(INDUSTRIES, N_MEMBERS).tolist(),
        "seniority_at_join":  seniority_at_join,
        "seniority_now":      seniority_now,
        "promoted":           got_promoted,
        "sessions_attended":  RNG.integers(0, 30, N_MEMBERS),
        "resources_accessed": RNG.integers(0, 50, N_MEMBERS),
        "is_active_30d":      RNG.choice([True, False], N_MEMBERS, p=[0.55, 0.45]).tolist(),
        "is_facilitator":     RNG.choice([True, False], N_MEMBERS, p=[0.08, 0.92]).tolist(),
        "referred_member":    RNG.choice([True, False], N_MEMBERS, p=[0.18, 0.82]).tolist(),
    })

    return df


# ─────────────────────────────────────────────
# 3. MONTHLY KPI TIME SERIES
# ─────────────────────────────────────────────
def generate_monthly_kpis() -> pd.DataFrame:
    months = pd.date_range(START_DATE, END_DATE, freq="MS")
    n = len(months)

    # Circles: growing trend with some seasonality
    base_circles = np.linspace(600, 1200, n)
    seasonal = 30 * np.sin(np.linspace(0, 4 * np.pi, n))
    noise = RNG.normal(0, 15, n)
    total_circles = np.clip(base_circles + seasonal + noise, 0, None).astype(int)

    new_circles = np.clip(np.diff(total_circles, prepend=total_circles[0]), 0, None)
    active_circles = (total_circles * RNG.uniform(0.74, 0.82, n)).astype(int)

    # Members
    base_members = np.linspace(8000, 18000, n)
    total_members = np.clip(base_members + RNG.normal(0, 200, n), 0, None).astype(int)

    # Engagement rate (meetings/month per active circle) — slight upward drift
    engagement = np.clip(np.linspace(0.68, 0.76, n) + RNG.normal(0, 0.03, n), 0.40, 1.0)

    # Promotion rate among members (annual, shown monthly)
    promotion_rate = np.clip(np.linspace(0.17, 0.22, n) + RNG.normal(0, 0.01, n), 0.10, 0.35)

    # NPS
    nps = np.clip(np.linspace(55, 68, n) + RNG.normal(0, 4, n), 0, 100)

    # Geographic reach (# of countries)
    geo_reach = np.clip(np.linspace(120, 183, n) + RNG.normal(0, 2, n), 100, 183).astype(int)

    # Churn (inactive circles / total)
    churn = np.clip(np.linspace(0.14, 0.10, n) + RNG.normal(0, 0.01, n), 0.04, 0.25)

    # Corporate partnerships
    partnerships = np.clip(np.linspace(180, 320, n) + RNG.normal(0, 8, n), 0, None).astype(int)

    df = pd.DataFrame({
        "month":              months,
        "total_circles":      total_circles,
        "new_circles":        new_circles,
        "active_circles":     active_circles,
        "total_members":      total_members,
        "engagement_rate":    engagement.round(3),
        "promotion_rate":     promotion_rate.round(3),
        "nps":                nps.round(1),
        "countries_reached":  geo_reach,
        "circle_churn_rate":  churn.round(3),
        "corporate_partners": partnerships,
    })

    return df


# ─────────────────────────────────────────────
# 4. CIRCLE HEALTH EVENTS (for funnel / cohort)
# ─────────────────────────────────────────────
def generate_circle_events(circles: pd.DataFrame) -> pd.DataFrame:
    rows = []
    event_types = ["Founded", "First Meeting", "3rd Meeting", "6th Meeting",
                   "Annual Milestone", "Facilitator Trained", "Became Inactive"]

    for _, row in circles.iterrows():
        base = row["founded_date"]
        rows.append({"circle_id": row["circle_id"], "event": "Founded", "event_date": base})
        if row["meetings_held"] >= 1:
            rows.append({"circle_id": row["circle_id"], "event": "First Meeting",
                          "event_date": base + timedelta(days=int(RNG.integers(7, 30)))})
        if row["meetings_held"] >= 3:
            rows.append({"circle_id": row["circle_id"], "event": "3rd Meeting",
                          "event_date": base + timedelta(days=int(RNG.integers(60, 120)))})
        if row["meetings_held"] >= 6:
            rows.append({"circle_id": row["circle_id"], "event": "6th Meeting",
                          "event_date": base + timedelta(days=int(RNG.integers(150, 240)))})
        if row["meetings_held"] >= 12:
            rows.append({"circle_id": row["circle_id"], "event": "Annual Milestone",
                          "event_date": base + timedelta(days=int(RNG.integers(340, 380)))})
        if row["has_facilitator_training"]:
            rows.append({"circle_id": row["circle_id"], "event": "Facilitator Trained",
                          "event_date": base + timedelta(days=int(RNG.integers(0, 60)))})
        if row["status"] == "Inactive":
            rows.append({"circle_id": row["circle_id"], "event": "Became Inactive",
                          "event_date": base + timedelta(days=int(RNG.integers(30, 400)))})

    return pd.DataFrame(rows)


# ─────────────────────────────────────────────
# MAIN ENTRY POINT
# ─────────────────────────────────────────────
def load_all():
    circles = generate_circles()
    members = generate_members(circles)
    monthly_kpis = generate_monthly_kpis()
    circle_events = generate_circle_events(circles)
    return circles, members, monthly_kpis, circle_events


if __name__ == "__main__":
    c, m, k, e = load_all()
    print(f"Circles: {len(c):,} | Members: {len(m):,} | Monthly KPI rows: {len(k)} | Events: {len(e):,}")
    print(c.head(3))
    print(m.head(3))
    print(k.head(3))
