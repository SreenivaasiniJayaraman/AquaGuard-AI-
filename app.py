
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="AquaGuard AI",
    page_icon="💧",
    layout="wide"
)

# ---------- HEADER ----------
st.title("💧 AquaGuard AI")
st.markdown(
    "### Smart Water Waste & Leakage Risk Detection System"
)
st.caption("AI-powered sustainability decision support • SDG 6")

# ---------- LOAD DATA ----------
df = pd.read_csv("aquaguard_final_dataset.csv")

# ---------- SIDEBAR ----------
st.sidebar.header("🔎 Analysis")

locations = ["All Locations"] + sorted(df["Location"].unique().tolist())

selected_location = st.sidebar.selectbox(
    "Select Location",
    locations
)

if selected_location != "All Locations":
    data = df[df["Location"] == selected_location].copy()
else:
    data = df.copy()

# ---------- KPI ----------
total_usage = data["Water_Usage_Liters"].sum()
average_usage = data["Water_Usage_Liters"].mean()
abnormal = (data["Status"] == "Abnormal").sum()
potential_saving = data["Estimated_Saving_Liters"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💧 Total Usage", f"{total_usage:,.0f} L")
col2.metric("📊 Average Usage", f"{average_usage:,.0f} L")
col3.metric("⚠️ Abnormal Events", abnormal)
col4.metric("🌱 Potential Saving", f"{potential_saving:,.0f} L")

st.divider()

# ---------- RISK ----------
st.subheader("🚨 Water Risk Analysis")

high_risk = data[data["Leak_Risk_Score"] >= 70]

if len(high_risk) > 0:
    st.error(
        f"🚨 {len(high_risk)} high-risk water usage event(s) detected!"
    )
    st.write(
        "Recommended action: inspect pipes, taps, tanks and other "
        "high-consumption areas."
    )
else:
    st.success("✅ No high-risk usage detected.")

# ---------- CHART ----------
st.subheader("📈 Water Consumption Pattern")

chart_data = data.set_index("Day")["Water_Usage_Liters"]

st.line_chart(chart_data)

# ---------- LOCATION COMPARISON ----------
st.subheader("🏢 Location Risk Comparison")

location_summary = df.groupby("Location").agg(
    Average_Usage=("Water_Usage_Liters", "mean"),
    Average_Risk=("Leak_Risk_Score", "mean"),
    Potential_Saving=("Estimated_Saving_Liters", "sum")
).round(1)

st.dataframe(location_summary, use_container_width=True)

# ---------- AI RECOMMENDATION ----------
st.subheader("🤖 AI Recommendation")

if len(data) > 0:

    highest = data.loc[data["Leak_Risk_Score"].idxmax()]

    st.warning(
        f"**Highest Risk:** {highest['Location']} | "
        f"Risk Score: {highest['Leak_Risk_Score']}"
    )

    if highest["Leak_Risk_Score"] >= 70:
        recommendation = (
            "Immediate inspection recommended. Check pipelines, "
            "taps, storage tanks and continuously running water sources."
        )
    elif highest["Leak_Risk_Score"] >= 40:
        recommendation = (
            "Monitor the location closely and inspect areas with "
            "unusual water consumption."
        )
    else:
        recommendation = (
            "Water consumption is within the expected range. "
            "Continue regular monitoring."
        )

    st.info(recommendation)

# ---------- IMPACT ----------
st.subheader("🌍 Sustainability Impact")

monthly_projection = data["Estimated_Saving_Liters"].mean() * 30

st.write(
    f"Based on the analyzed data, the estimated potential saving "
    f"is **{monthly_projection:,.0f} liters/month** if abnormal "
    f"consumption is corrected."
)

st.success(
    "🎯 SDG 6 — Clean Water and Sanitation | "
    "Promoting responsible and efficient water use."
)

# ---------- RESPONSIBLE AI ----------
with st.expander("🔐 Responsible AI Considerations"):
    st.write("""
    • The system provides risk indicators, not confirmed leakage diagnoses.
    
    • Water usage data should be handled responsibly and securely.
    
    • Predictions should be verified by maintenance personnel before action.
    
    • The prototype uses simulated data and should be validated with
      real-world measurements before deployment.
    """)

st.divider()

st.caption(
    "AquaGuard AI | AI for Sustainability Virtual Internship | 2026"
)
