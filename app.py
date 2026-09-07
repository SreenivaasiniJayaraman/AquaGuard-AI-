import streamlit as st
import pandas as pd
import numpy as np

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AquaGuard AI",
    page_icon="💧",
    layout="wide"
)

# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv("aquaguard_final_dataset.csv")

# Safety check for saving column
if "Estimated_Saving_Liters" not in df.columns:
    if "Potential_Saving_Liters" in df.columns:
        df["Estimated_Saving_Liters"] = df["Potential_Saving_Liters"]
    else:
        df["Estimated_Saving_Liters"] = 0

# =========================================================
# HEADER
# =========================================================

st.title("💧 AquaGuard AI")
st.markdown(
    "### Smart Water Waste & Leakage Risk Detection System"
)

st.caption(
    "🤖 AI-powered water sustainability decision-support system | "
    "🌍 SDG 6 – Clean Water and Sanitation"
)

st.divider()

# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

st.sidebar.title("💧 AquaGuard AI")

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Dashboard",
        "🚨 Leakage Detection",
        "📊 Usage Analytics",
        "🤖 AI Recommendations",
        "💧 Water Savings",
        "🔔 Alert Center",
        "🌍 Sustainability Impact",
        "🔐 Responsible AI"
    ]
)

st.sidebar.divider()

locations = ["All Locations"] + sorted(
    df["Location"].unique().tolist()
)

selected_location = st.sidebar.selectbox(
    "🏢 Select Location",
    locations
)

if selected_location == "All Locations":
    data = df.copy()
else:
    data = df[df["Location"] == selected_location].copy()

# =========================================================
# COMMON CALCULATIONS
# =========================================================

total_usage = data["Water_Usage_Liters"].sum()

average_usage = data["Water_Usage_Liters"].mean()

abnormal_events = (
    data["Status"] == "Abnormal"
).sum()

potential_saving = (
    data["Estimated_Saving_Liters"].sum()
)

average_risk = data["Leak_Risk_Score"].mean()

monthly_saving = (
    data["Estimated_Saving_Liters"].mean() * 30
)

yearly_saving = monthly_saving * 12

# =========================================================
# 🏠 DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.header("🏠 Water Management Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💧 Total Water Usage",
        f"{total_usage:,.0f} L"
    )

    col2.metric(
        "📊 Average Usage",
        f"{average_usage:,.0f} L"
    )

    col3.metric(
        "⚠️ Abnormal Events",
        abnormal_events
    )

    col4.metric(
        "🌱 Potential Saving",
        f"{potential_saving:,.0f} L"
    )

    st.divider()

    st.subheader("📈 Water Consumption Trend")

    chart_data = data.groupby(
        "Day"
    )["Water_Usage_Liters"].sum()

    st.line_chart(chart_data)

    st.subheader("🚨 Current Risk Status")

    if average_risk >= 70:
        st.error(
            f"🔴 HIGH RISK — Average risk score: "
            f"{average_risk:.1f}"
        )
    elif average_risk >= 40:
        st.warning(
            f"🟡 MEDIUM RISK — Average risk score: "
            f"{average_risk:.1f}"
        )
    else:
        st.success(
            f"🟢 LOW RISK — Average risk score: "
            f"{average_risk:.1f}"
        )

    st.subheader("🏢 Location Overview")

    summary = df.groupby("Location").agg(
        Average_Usage=("Water_Usage_Liters", "mean"),
        Abnormal_Events=("Status",
                         lambda x: (x == "Abnormal").sum()),
        Average_Risk=("Leak_Risk_Score", "mean"),
        Potential_Saving=("Estimated_Saving_Liters", "sum")
    ).round(1)

    st.dataframe(
        summary,
        use_container_width=True
    )

# =========================================================
# 🚨 LEAKAGE DETECTION
# =========================================================

elif page == "🚨 Leakage Detection":

    st.header("🚨 Leakage Risk Detection")

    st.write(
        "The AI model identifies unusual water consumption "
        "patterns that may indicate possible wastage or leakage."
    )

    high_risk = data[
        data["Leak_Risk_Score"] >= 70
    ]

    medium_risk = data[
        (data["Leak_Risk_Score"] >= 40) &
        (data["Leak_Risk_Score"] < 70)
    ]

    low_risk = data[
        data["Leak_Risk_Score"] < 40
    ]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🔴 High Risk",
        len(high_risk)
    )

    col2.metric(
        "🟡 Medium Risk",
        len(medium_risk)
    )

    col3.metric(
        "🟢 Low Risk",
        len(low_risk)
    )

    st.divider()

    st.subheader("🔎 Highest Risk Events")

    display_columns = [
        "Day",
        "Location",
        "Water_Usage_Liters",
        "Leak_Risk_Score",
        "Risk_Level"
    ]

    st.dataframe(
        data.sort_values(
            "Leak_Risk_Score",
            ascending=False
        )[display_columns].head(15),
        use_container_width=True
    )

    st.info(
        "⚠️ A high-risk score indicates unusual consumption. "
        "It does NOT confirm an actual leak."
    )

# =========================================================
# 📊 USAGE ANALYTICS
# =========================================================

elif page == "📊 Usage Analytics":

    st.header("📊 Water Usage Analytics")

    st.subheader("📈 Daily Consumption")

    daily_usage = data.groupby(
        "Day"
    )["Water_Usage_Liters"].sum()

    st.line_chart(daily_usage)

    st.subheader("🏢 Location Comparison")

    location_summary = df.groupby("Location").agg(
        Average_Usage=("Water_Usage_Liters", "mean"),
        Average_Risk=("Leak_Risk_Score", "mean"),
        Abnormal_Events=("Status",
                         lambda x: (x == "Abnormal").sum()),
        Potential_Saving=("Estimated_Saving_Liters", "sum")
    ).round(1)

    st.dataframe(
        location_summary,
        use_container_width=True
    )

    st.subheader("📌 Usage Statistics")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Minimum Usage",
        f"{data['Water_Usage_Liters'].min():,.0f} L"
    )

    col2.metric(
        "Maximum Usage",
        f"{data['Water_Usage_Liters'].max():,.0f} L"
    )

    col3.metric(
        "Average Risk",
        f"{average_risk:.1f}"
    )

# =========================================================
# 🤖 AI RECOMMENDATIONS
# =========================================================

elif page == "🤖 AI Recommendations":

    st.header("🤖 AI Recommendations")

    st.write(
        "AquaGuard AI converts detected risk patterns "
        "into practical maintenance recommendations."
    )

    if len(data) > 0:

        highest = data.loc[
            data["Leak_Risk_Score"].idxmax()
        ]

        st.subheader("🚨 Priority Location")

        st.warning(
            f"**{highest['Location']}** | "
            f"Risk Score: {highest['Leak_Risk_Score']:.1f}"
        )

        if highest["Leak_Risk_Score"] >= 70:

            recommendation = """
            🚨 **Immediate inspection recommended**

            • Check pipelines and water connections  
            • Inspect continuously running taps  
            • Check storage tanks and overflow  
            • Verify abnormal consumption at the location  
            """

        elif highest["Leak_Risk_Score"] >= 40:

            recommendation = """
            ⚠️ **Monitoring recommended**

            • Monitor water consumption  
            • Inspect high-use areas  
            • Compare with normal consumption  
            • Check for minor wastage sources  
            """

        else:

            recommendation = """
            ✅ **Normal usage**

            Continue regular monitoring and preventive maintenance.
            """

        st.info(recommendation)

    st.subheader("🧠 Why was this location flagged?")

    st.write(
        "The system compares observed water consumption "
        "with historical normal usage patterns and calculates "
        "a risk indicator based on the deviation."
    )

# =========================================================
# 💧 WATER SAVINGS
# =========================================================

elif page == "💧 Water Savings":

    st.header("💧 Water Saving Analysis")

    st.write(
        "Estimate how much water could potentially be saved "
        "if abnormal consumption is corrected."
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "💧 Current Potential Saving",
        f"{potential_saving:,.0f} L"
    )

    col2.metric(
        "📅 Monthly Projection",
        f"{monthly_saving:,.0f} L"
    )

    col3.metric(
        "📆 Yearly Projection",
        f"{yearly_saving:,.0f} L"
    )

    st.divider()

    st.subheader("🎯 What-if Water Saving Simulator")

    reduction = st.slider(
        "Expected reduction in abnormal consumption (%)",
        min_value=10,
        max_value=100,
        value=30,
        step=10
    )

    simulated_saving = (
        potential_saving * reduction / 100
    )

    monthly_simulated = (
        simulated_saving / max(len(data), 1) * 30
    )

    st.success(
        f"💧 With a **{reduction}% reduction**, "
        f"approximately **{simulated_saving:,.0f} L** "
        f"could potentially be recovered from the analyzed records."
    )

    st.info(
        f"📅 Projected monthly saving: "
        f"**{monthly_simulated:,.0f} L**"
    )

# =========================================================
# 🔔 ALERT CENTER
# =========================================================

elif page == "🔔 Alert Center":

    st.header("🔔 Water Risk Alert Center")

    high = data[
        data["Leak_Risk_Score"] >= 70
    ].sort_values(
        "Leak_Risk_Score",
        ascending=False
    )

    medium = data[
        (data["Leak_Risk_Score"] >= 40) &
        (data["Leak_Risk_Score"] < 70)
    ].sort_values(
        "Leak_Risk_Score",
        ascending=False
    )

    st.subheader("🔴 Critical Alerts")

    if len(high) > 0:

        for _, row in high.head(8).iterrows():

            st.error(
                f"🚨 {row['Location']} | "
                f"Day {row['Day']} | "
                f"Risk Score: {row['Leak_Risk_Score']:.1f}"
            )

    else:

        st.success("✅ No critical alerts.")

    st.subheader("🟡 Warning Alerts")

    if len(medium) > 0:

        for _, row in medium.head(8).iterrows():

            st.warning(
                f"⚠️ {row['Location']} | "
                f"Day {row['Day']} | "
                f"Risk Score: {row['Leak_Risk_Score']:.1f}"
            )

    else:

        st.success("✅ No medium-risk alerts.")

# =========================================================
# 🌍 SUSTAINABILITY IMPACT
# =========================================================

elif page == "🌍 Sustainability Impact":

    st.header("🌍 Sustainability Impact")

    st.subheader("🎯 SDG 6 — Clean Water and Sanitation")

    st.write(
        "AquaGuard AI supports responsible water management "
        "by identifying abnormal consumption and helping "
        "organizations take corrective action."
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "💧 Potential Saving",
        f"{potential_saving:,.0f} L"
    )

    col2.metric(
        "📅 Monthly Estimate",
        f"{monthly_saving:,.0f} L"
    )

    col3.metric(
        "📆 Yearly Estimate",
        f"{yearly_saving:,.0f} L"
    )

    st.divider()

    st.subheader("🌱 Expected Impact")

    st.markdown("""
    **AquaGuard AI can help:**

    - Detect unusual water consumption earlier
    - Prioritize locations requiring inspection
    - Reduce avoidable water wastage
    - Support data-driven maintenance decisions
    - Promote responsible water consumption
    """)

    st.success(
        "🌍 Small improvements in water-use efficiency "
        "can contribute to long-term sustainability."
    )

# =========================================================
# 🔐 RESPONSIBLE AI
# =========================================================

elif page == "🔐 Responsible AI":

    st.header("🔐 Responsible AI")

    st.subheader("⚖️ Important Considerations")

    st.markdown("""
    ### 1. Transparency
    The system provides a risk indicator based on observed
    consumption patterns.

    ### 2. Human Verification
    A high-risk result should be verified by maintenance
    personnel before taking corrective action.

    ### 3. Privacy
    Water usage data should be stored and handled securely.

    ### 4. No False Diagnosis
    AquaGuard AI does not claim that an actual pipe leak
    has been confirmed.

    ### 5. Data Limitation
    This prototype uses simulated data and should be
    validated with real-world measurements before deployment.
    """)

    st.info(
        "🤖 AI assists decision-making; humans remain responsible "
        "for final maintenance decisions."
    )

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "💧 AquaGuard AI | AI for Sustainability Virtual Internship | 2026"
)
