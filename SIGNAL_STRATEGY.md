# Signal Strategy — Lean In Data Scientist Assignment
**Part 1: Which signals I'd measure and why**

---

## The Framing Question

Before picking metrics, I asked: *what decision does each metric enable?*

Lean In has one north star: **accelerate women's advancement into leadership**. Every signal I chose must connect to that — either by measuring outcomes directly, tracking the community engine that drives them, or providing early warning when something is breaking.

I also deliberately ruled out vanity metrics (total registered users, website traffic) that look good in headlines but don't predict mission success.

---

## Tier 1 — Mission-Critical (Non-negotiable)

### 1. Member Promotion Rate
**What it measures**: % of Circle members promoted within a 12-month cohort window.  
**Why it matters**: This is Lean In's impact claim — "women in Circles are nearly 2× as likely to be promoted." If we can't measure it, we can't defend it. If we can measure it, it's the single most powerful signal for fundraising, corporate partnerships, and organizational legitimacy.  
**Formula**: `# members promoted / # members tracked over trailing 12 months`  
**Segments to track**: By seniority level (the broken rung is at IC→Manager), industry, and Circle type (Workplace vs. Community).  
**Limitation**: Self-reported data with selection bias — more ambitious women join Circles. Requires a matched control group for causal claims.

---

### 2. Active Circle Rate
**What it measures**: % of registered Circles with ≥1 meeting in the past 30 days.  
**Why it matters**: A dormant Circle is a broken promise. This is the leading indicator for all downstream outcomes — a Circle that doesn't meet generates no advancement, no support, no NPS. Track weekly; alert when it drops below 75%.  
**Formula**: `Circles with ≥1 meeting in last 30 days / Total registered circles`  
**Limitation**: Meeting frequency doesn't capture meeting quality. Needs to be paired with attendance rate and NPS to tell the full story.

---

### 3. Circle NPS (Net Promoter Score)
**What it measures**: "How likely are you to recommend your Circle to a friend?" (0–10 scale)  
**Why it matters**: NPS is the CEO-legible single number that captures community health. Circles where women feel supported and valued will retain members and generate referrals — the organic growth engine. A declining NPS is the earliest signal that something is wrong before we see it in churn or promotion data.  
**Formula**: `% Promoters (9–10) − % Detractors (0–6)`  
**Target**: >60 (currently at ~65 for active circles with facilitator training)  
**Limitation**: Survey response bias; lags real experience by weeks. Segment by Circle type to diagnose.

---

## Tier 2 — Growth & Scale

### 4. New Circles Started (Month-over-Month)
**What it measures**: Number of new Circles launched each month.  
**Why it matters**: Pipeline of future impact. Also tracks the effectiveness of our recruitment/onboarding funnel.  
**Key insight**: Watch the ratio of new circles started to new circles that survive 90 days. A spike in starts followed by early churn = a marketing problem, not a product win.

---

### 5. Geographic Reach (# Countries with Active Circles)
**What it measures**: Number of countries with ≥1 active Circle.  
**Why it matters**: Lean In's mission is explicitly global. Breadth signals movement legitimacy to funders and partners. Tracks whether growth is concentrated or genuinely distributed.  
**Limitation**: 1 circle in 50 countries tells a worse story than 50 circles in 1 country. Pair with depth metrics (circles per 1M women in workforce).

---

### 6. Corporate Partners (Circles for Companies)
**What it measures**: # organizations actively running Circles for Companies programs.  
**Why it matters**: Corporate partnerships are a force multiplier — one partnership can reach thousands of women at once and drives systematic change inside organizations. This is also Lean In's primary revenue signal.  
**Limitation**: Count doesn't equal utilization. Track active employee participation rate within partner companies.

---

## Tier 3 — Health & Early Warning

### 7. Circle Lifecycle Funnel (Founded → 3rd Meeting)
**What it measures**: % of new circles reaching each milestone — First Meeting, 3rd Meeting, 6th Meeting, Annual.  
**Why it matters**: The 3rd meeting is the "sticky threshold" — circles that reach it are dramatically more likely to survive. This funnel tells us where to intervene (automated nudges at day 14 and day 45 have shown impact in community platform research).  
**Formula**: Cohort conversion rate per milestone window.

---

### 8. Engagement Depth (Avg Sessions Attended per Member)
**What it measures**: Average number of sessions a member attends over trailing 6 months.  
**Why it matters**: There's a clear dose-response relationship — members with 16+ sessions are promoted at nearly double the rate of those with 1–3 sessions. This is the engagement depth signal most predictive of outcomes. Focus retention on getting members past session 8.  
**Limitation**: Average masks the bimodal distribution (power users vs. lurkers). Track median and P25.

---

### 9. Facilitator Training Adoption Rate
**What it measures**: % of Circle leaders who have completed facilitator training.  
**Why it matters**: Trained facilitators run better Circles — higher attendance, lower churn, higher NPS. This is an input metric and an actionable lever. We control it directly through our programs.  
**Formula**: `# circle leaders with training completed / # active circle leaders`  
**Target**: >65%

---

## What I Deliberately Left Out

- **Website traffic / page views**: Doesn't connect to mission outcomes.
- **Social media followers**: Awareness ≠ impact.
- **Total registered members**: Inflated by dormant accounts. Active members is the right denominator.
- **Curriculum downloads**: Proxy too removed from outcomes.

---

## The Signal Hierarchy (Summary)

```
NORTH STAR: Women advancing into leadership
    │
    ├── OUTCOME: Member Promotion Rate  (did it work?)
    │
    ├── COMMUNITY ENGINE:
    │       Active Circle Rate           (are circles alive?)
    │       Circle NPS                   (are circles valued?)
    │       Engagement Depth             (are members going deep?)
    │
    ├── SCALE:
    │       New Circles MoM              (are we growing?)
    │       Geographic Reach             (are we global?)
    │       Corporate Partners           (are we institutional?)
    │
    └── EARLY WARNING:
            Circle Lifecycle Funnel      (where do circles die?)
            Facilitator Training Rate    (are leaders equipped?)
```

---

*"Metrics are a proxy for truth — they're incomplete. Context always matters."*
