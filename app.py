#!/usr/bin/env python3
"""
METRIKA CRB v2.1 — Interactive Dashboard
Deploy: streamlit run app.py
"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import json, os

st.set_page_config(
    page_title="METRIKA CRB v2.1",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Dark theme CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
  .stApp { background-color: #0f172a; color: #e2e8f0; }
  .metric-card {
    background: #1e293b; border-radius: 10px;
    padding: 16px; border-left: 4px solid;
    margin-bottom: 12px;
  }
  .metric-val { font-size: 2rem; font-weight: 700; }
  .metric-lbl { font-size: 0.85rem; color: #94a3b8; }
  .critical { border-color: #dc2626; }
  .high     { border-color: #ea580c; }
  .medium   { border-color: #d97706; }
  .good     { border-color: #22c55e; }
  .header-bar {
    background: linear-gradient(90deg, #0f172a 0%, #1e3a5f 100%);
    padding: 20px 30px; border-radius: 12px;
    border-bottom: 2px solid #22d3ee; margin-bottom: 24px;
  }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-bar">
  <span style="font-size:2rem;font-weight:800;color:#22d3ee">METRIKA</span>
  <span style="font-size:1.2rem;color:#94a3b8"> CRB v2.1 — Climate Resilience Box</span>
  <br>
  <span style="font-size:0.9rem;color:#64748b">
    Kenya ASAL · 10 Counties · 2000–2023 · ERA5 · MODIS · CHIRPS
  </span>
</div>
""", unsafe_allow_html=True)

# ── Load data ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("output/eo_timeseries_all.csv")
    with open("crb_output/cartographer_report.json") as f:
        cart = json.load(f)
    briefs = {}
    for fname in os.listdir("crb_output/briefs"):
        if fname.endswith(".json"):
            cid = fname.replace("brief_","").replace(".json","")
            with open(f"crb_output/briefs/{fname}") as f:
                briefs[cid] = json.load(f)
    return df, cart, briefs

df, cart, briefs = load_data()

IRS = {"Turkana":0.422,"Marsabit":0.391,"Mandera":0.318,"Wajir":0.342,
       "Garissa":0.388,"Isiolo":0.461,"Samburu":0.448,"Tana River":0.412,
       "Lamu":0.489,"Kwale":0.502}
POP = {"Turkana":1366900,"Marsabit":459785,"Mandera":1185765,"Wajir":781263,
       "Garissa":841353,"Isiolo":268002,"Samburu":310327,"Tana River":315943,
       "Lamu":143920,"Kwale":866820}
CID = {"Turkana":"KEN-TRK","Marsabit":"KEN-MST","Mandera":"KEN-MAN",
       "Wajir":"KEN-WJR","Garissa":"KEN-GAR","Isiolo":"KEN-ISD",
       "Samburu":"KEN-SMB","Tana River":"KEN-TNA","Lamu":"KEN-LMU","Kwale":"KEN-KTI"}
TIER_C = {"CRITICAL":"#dc2626","HIGH":"#ea580c","MEDIUM":"#d97706","LOW":"#22c55e"}
PRI_T  = {"Mandera":"CRITICAL","Wajir":"CRITICAL","Garissa":"CRITICAL",
          "Marsabit":"HIGH","Turkana":"HIGH","Tana River":"MEDIUM",
          "Samburu":"MEDIUM","Isiolo":"MEDIUM","Lamu":"LOW","Kwale":"LOW"}

def irs_color(v):
    if v < 0.35: return "#dc2626"
    if v < 0.42: return "#f97316"
    if v < 0.50: return "#f59e0b"
    return "#22c55e"

counties = list(IRS.keys())

# ── Sidebar ─────────────────────────────────────────────────────────────────
st.sidebar.markdown("## 🗺️ County Selection")
selected = st.sidebar.selectbox("County", counties, index=2)  # default Mandera
st.sidebar.markdown("---")
st.sidebar.markdown("## 📡 EO Variable")
eo_var = st.sidebar.selectbox("Variable for time series",
    ["precip_mm","temp_anom_c","ndvi_anom","spi12","soil_moist"])
st.sidebar.markdown("---")
st.sidebar.markdown("## 📅 Year Range")
yr_range = st.sidebar.slider("Years", 2000, 2023, (2000,2023))

# ── KPI Row ──────────────────────────────────────────────────────────────────
irs_v  = IRS[selected]
tier   = PRI_T[selected]
cid    = CID[selected]
b      = briefs.get(cid, {})
spi_v  = df[(df.county_name==selected)&(df.year==2022)]["spi12"].values
spi_v  = float(spi_v[0]) if len(spi_v) else 0

col1,col2,col3,col4,col5 = st.columns(5)
cls = "critical" if irs_v < 0.35 else "high" if irs_v < 0.42 else "medium" if irs_v < 0.50 else "good"
col1.markdown(f"""<div class="metric-card {cls}">
  <div class="metric-val" style="color:{irs_color(irs_v)}">{irs_v:.3f}</div>
  <div class="metric-lbl">IRS — Resilience Score</div></div>""", unsafe_allow_html=True)
col2.markdown(f"""<div class="metric-card {'critical' if tier=='CRITICAL' else 'high' if tier=='HIGH' else 'medium'}">
  <div class="metric-val" style="color:{TIER_C[tier]}">{tier}</div>
  <div class="metric-lbl">Priority Tier</div></div>""", unsafe_allow_html=True)
col3.markdown(f"""<div class="metric-card {'critical' if spi_v<-1.5 else 'high' if spi_v<-1 else 'good'}">
  <div class="metric-val" style="color:{'#ef4444' if spi_v<-1.5 else '#22c55e'}">{spi_v:+.2f}</div>
  <div class="metric-lbl">SPI-12 (2022)</div></div>""", unsafe_allow_html=True)
col4.markdown(f"""<div class="metric-card medium">
  <div class="metric-val">{POP[selected]//1000}k</div>
  <div class="metric-lbl">Population</div></div>""", unsafe_allow_html=True)
tier_grant = b.get("tier_granted", 3)
col5.markdown(f"""<div class="metric-card {'good' if tier_grant<=2 else 'medium'}">
  <div class="metric-val">Tier {tier_grant}</div>
  <div class="metric-lbl">Data Quality (GUARDIAN)</div></div>""", unsafe_allow_html=True)

# ── Main charts row ──────────────────────────────────────────────────────────
col_a, col_b = st.columns([1.4, 1])

with col_a:
    st.subheader(f"📈 {eo_var.replace('_',' ').title()} — {selected} {yr_range[0]}–{yr_range[1]}")
    sub = df[(df.county_name==selected)&(df.year.between(*yr_range))]
    fig_ts = go.Figure()
    fig_ts.add_trace(go.Scatter(
        x=sub["year"], y=sub[eo_var], mode="lines+markers",
        line=dict(color=irs_color(irs_v), width=2.5),
        fill="tozeroy", fillcolor=f"rgba({int(irs_color(irs_v)[1:3],16)},{int(irs_color(irs_v)[3:5],16)},{int(irs_color(irs_v)[5:],16)},0.08)",
    ))
    if eo_var in ["ndvi_anom","spi12"]:
        fig_ts.add_hline(y=0, line_dash="dot", line_color="#64748b")
    if eo_var == "spi12":
        fig_ts.add_hline(y=-1.5, line_dash="dash", line_color="#ef4444",
                         annotation_text="Severe drought")
    fig_ts.add_vrect(x0=2020,x1=2022.5,fillcolor="rgba(220,38,38,0.08)",line_width=0)
    fig_ts.update_layout(
        xaxis_title="Year", yaxis_title=eo_var,
        paper_bgcolor="#1e293b", plot_bgcolor="#0f172a",
        font=dict(color="#e2e8f0"), height=300,
        margin=dict(t=10,b=40,l=60,r=20), showlegend=False
    )
    st.plotly_chart(fig_ts, use_container_width=True)

with col_b:
    st.subheader("🕸️ Resilience Radar")
    sectors = ["Adaptive","Social","Institutional","Env Stress","Exposure","Economic"]
    vals = {
        "Mandera":[0.31,0.28,0.33,0.29,0.38,0.27],
        "Kwale":[0.55,0.52,0.58,0.61,0.54,0.57],
        "Turkana":[0.41,0.39,0.44,0.35,0.46,0.38],
        "Wajir":[0.33,0.31,0.36,0.31,0.40,0.29],
        "Marsabit":[0.36,0.34,0.41,0.34,0.44,0.33],
        "Garissa":[0.38,0.36,0.40,0.37,0.42,0.35],
        "Isiolo":[0.47,0.44,0.48,0.43,0.49,0.45],
        "Samburu":[0.45,0.42,0.46,0.41,0.47,0.43],
        "Tana River":[0.41,0.39,0.43,0.40,0.44,0.40],
        "Lamu":[0.50,0.47,0.51,0.48,0.51,0.49],
    }.get(selected, [0.4]*6)
    cats = sectors + [sectors[0]]
    vals_r = vals + [vals[0]]
    fig_r = go.Figure(go.Scatterpolar(
        r=vals_r, theta=cats, fill="toself",
        line_color=irs_color(irs_v),
        fillcolor=f"rgba({int(irs_color(irs_v)[1:3],16)},{int(irs_color(irs_v)[3:5],16)},{int(irs_color(irs_v)[5:],16)},0.18)",
        name=selected,
    ))
    fig_r.update_layout(
        polar=dict(bgcolor="#0f172a",
                   radialaxis=dict(range=[0,0.75],tickfont=dict(color="#64748b",size=8)),
                   angularaxis=dict(tickfont=dict(color="#94a3b8",size=9))),
        paper_bgcolor="#1e293b", height=300,
        margin=dict(t=10,b=10,l=20,r=20), showlegend=False
    )
    st.plotly_chart(fig_r, use_container_width=True)

# ── Map + Drought row ─────────────────────────────────────────────────────────
col_c, col_d = st.columns(2)

with col_c:
    st.subheader("🗺️ Resilience Priority Map")
    lats = dict(zip(df.county_name, df.lat))
    lons = dict(zip(df.county_name, df.lon))
    fig_m = go.Figure()
    for c in counties:
        is_sel = (c == selected)
        fig_m.add_trace(go.Scattergeo(
            lat=[lats[c]], lon=[lons[c]], mode="markers+text",
            text=[c[:4]], textposition="top center",
            textfont=dict(size=8 if not is_sel else 11,
                         color="white" if is_sel else "#1e293b"),
            marker=dict(
                size=22 if is_sel else max(12, min(28, POP[c]/60000)),
                color=TIER_C[PRI_T[c]],
                opacity=1.0 if is_sel else 0.65,
                line=dict(width=3 if is_sel else 1, color="white"),
                symbol="star" if is_sel else "circle",
            ),
            showlegend=False,
            hovertemplate=f"<b>{c}</b><br>IRS: {IRS[c]:.3f}<br>Priority: {PRI_T[c]}<extra></extra>"
        ))
    fig_m.update_geos(
        scope="africa", center=dict(lat=0.8, lon=38.8), projection_scale=7.5,
        showland=True, landcolor="#1e293b",
        showocean=True, oceancolor="#0f172a",
        showcountries=True, countrycolor="#334155",
        showframe=False, bgcolor="#0f172a"
    )
    fig_m.update_layout(
        paper_bgcolor="#1e293b", height=300,
        margin=dict(t=10,b=10,l=5,r=5)
    )
    st.plotly_chart(fig_m, use_container_width=True)

with col_d:
    st.subheader("⚠️ Risk Profile")
    if b:
        risks = b.get("risk_statements", [])
        for r in risks[:5]:
            clr = "#dc2626" if r["risk_score"]>=0.88 else "#ea580c" if r["risk_score"]>=0.75 else "#d97706"
            st.markdown(f"""
            <div style="background:#1e293b;border-left:4px solid {clr};
                        padding:8px 12px;border-radius:6px;margin-bottom:8px">
              <b style="color:{clr}">[{r["risk_id"]}] {r["category"]}</b>
              <span style="float:right;color:{clr};font-weight:700">
                score {r["risk_score"]:.2f}</span><br>
              <span style="font-size:0.82rem;color:#94a3b8">
                {r["likelihood"]} / {r["impact"]} · {r["timeframe"]}</span><br>
              <span style="font-size:0.8rem">{r["statement"][:120]}...</span>
            </div>""", unsafe_allow_html=True)

# ── All-county IRS table ──────────────────────────────────────────────────────
st.subheader("📊 All-County IRS Overview")
rows = []
for c in sorted(counties, key=lambda x: IRS[x]):
    cid_k = CID[c]
    b_c = briefs.get(cid_k, {})
    rows.append({
        "County": c,
        "IRS": f"{IRS[c]:.3f}",
        "Priority": PRI_T[c],
        "3yr Forecast": f"{b_c.get('irs_forecast_3yr',IRS[c]):.3f}",
        "SPI-12 (2022)": f"{df[(df.county_name==c)&(df.year==2022)]['spi12'].values[0]:+.2f}",
        "Data Tier": f"Tier {b_c.get('tier_granted',3)}",
        "Population": f"{POP[c]//1000}k",
    })
df_tbl = pd.DataFrame(rows)
st.dataframe(df_tbl, use_container_width=True, hide_index=True)

st.markdown("""
---
<div style="text-align:center;color:#475569;font-size:0.8rem">
  METRIKA Foundation  ·  Climate Resilience Box v2.1  ·  Measuring What Matters  ·  2026
</div>
""", unsafe_allow_html=True)
