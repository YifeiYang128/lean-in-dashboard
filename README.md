# Lean In — Data Scientist Take-Home Assignment

**Candidate submission** · May 2025

---

## What's in this repo

```
leanin_dashboard/
├── app.py                # Streamlit dashboard (Part 2)
├── data_generator.py     # Synthetic data engine (seeded, reproducible)
├── requirements.txt
├── SIGNAL_STRATEGY.md    # Part 1 signal rationale (also embedded in dashboard Tab 5)
└── README.md
```

---

## Running the dashboard

```bash
# 1. Clone / unzip this repo
# 2. Create a virtual environment (optional but recommended)
python -m venv .venv && source .venv/bin/activate   # or .venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
streamlit run app.py
```

The dashboard opens at `http://localhost:8501`. No API keys or external data needed — everything is generated locally from a seeded random engine.

---

## What I built

### Part 1 — Signal Strategy (see Tab 5 in the dashboard or SIGNAL_STRATEGY.md)

I chose **9 signals across 3 tiers**, deliberately sequenced from mission-critical to operational:

| Tier | Signal | Frequency |
|------|--------|-----------|
| 🔵 Mission-Critical | Member Promotion Rate | Quarterly cohort |
| 🔵 Mission-Critical | Active Circle Rate | Weekly |
| 🔵 Mission-Critical | Circle NPS | Quarterly survey |
| 🟢 Growth & Scale | New Circles Started (MoM) | Monthly |
| 🟢 Growth & Scale | Geographic Reach (# Countries) | Quarterly |
| 🟢 Growth & Scale | Corporate Partners | Monthly |
| 🟡 Health & Early Warning | Circle Lifecycle Funnel | Monthly cohort |
| 🟡 Health & Early Warning | Sessions Attended per Member | Monthly |
| 🟡 Health & Early Warning | Facilitator Training Adoption | Monthly |

**The reasoning logic**: Every signal earns its place by connecting to one of three questions:
1. Are women actually advancing? (outcome)
2. Is the community growing? (scale)
3. Are circles healthy enough to survive? (health / early warning)

### Part 2 — Dashboard

Five layers, each with a distinct audience question:

| Tab | CEO Question Answered |
|-----|-----------------------|
| 📈 Growth & Reach | "Are we growing fast enough?" |
| ⭕ Circle Health | "Are circles actually working?" |
| 🚀 Member Advancement | "Are women getting promoted?" |
| 🌍 Geographic Expansion | "Where are we strong / where are gaps?" |
| 🔍 Signal Strategy | "Why did you measure these things?" |

**Interactive features**: date range filter, country/industry/circle-type filters (sidebar), metric selector on geo tab, funnel chart, Sankey diagram for career transitions, dose-response chart for session depth.

---

## Tools used

| Tool | Used for |
|------|---------|
| **Claude (Anthropic)** | Architecture design, data model, narrative framing, code generation, copy |
| **Python / Pandas / NumPy** | Data generation + transformation |
| **Streamlit** | Dashboard framework |
| **Plotly** | All charts (Sankey, funnel, choropleth, dual-axis, scatter) |

---

## What I'd do with more time

1. **Causal identification**: The promotion lift claim needs a matched-cohort study to rule out self-selection. Women who join Circles skew more ambitious to begin with — we need to control for that.

2. **Predictive at-risk model**: A logistic regression (or gradient boosting) on circle attributes at day 30 to predict churn — so we can trigger facilitator outreach before a circle dies.

3. **NLP on open-text NPS**: The *why* behind satisfaction is in the comments, not the number. Tag themes driving detraction.

4. **The 'Broken Rung' tracker**: The biggest structural barrier is the IC→Manager transition. If corporate partners share promotion data by gender, we can track whether Lean In is moving this needle.

5. **Real platform instrumentation**: Login events, curriculum completion, peer messaging — build a true engagement score that predicts long-term retention.

---

## Notes for the reviewer

- The synthetic data is **seeded** (reproducible) and calibrated to Lean In's known numbers: 100,000+ circles, 183 countries, ~2× promotion lift claim.
- The dashboard uses Lean In's brand colors and is designed for a non-technical CEO who asks: *"Is the mission working?"*
- Signal strategy tab includes explicit limitations for each metric — because knowing what data *can't* tell you is as important as knowing what it can.

---

*Questions? Reach out to [your email] | GitHub: [your handle]*
