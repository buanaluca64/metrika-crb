# METRIKA CRB v2.1 — Interactive Dashboard

## Run locally (2 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Launch dashboard
streamlit run app.py
```

Browser opens automatically at http://localhost:8501

## Deploy free on Streamlit Cloud

1. Create account at https://share.streamlit.io
2. Push this folder to a GitHub repo
3. Click "New app" → select repo → main file: app.py
4. Deploy (takes ~2 min)

## What's inside

- app.py                        — Streamlit dashboard
- output/eo_timeseries_all.csv  — EO time series (10 counties, 2000-2023)
- crb_output/briefs/            — 10 Decision Briefs (JSON)
- requirements.txt              — Python dependencies

## Dashboard features

- County selector (10 Kenya ASAL counties)
- EO variable selector (SPI-12, NDVI, Temp, Precip, Soil Moisture)
- Year range slider (2000-2023)
- KPI cards: IRS, Priority Tier, SPI-12, Population, Data Tier
- Interactive time series with drought bands
- Resilience radar chart
- Geo priority map
- Risk profile cards (5 risks per county)
- All-county comparison table

## Built by METRIKA Foundation — Measuring What Matters
## CRB v2.1 — 2026
