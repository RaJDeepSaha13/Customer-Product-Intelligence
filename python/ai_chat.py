import streamlit as st
import pandas as pd

from ai_business_analyst import (
    df,
    route_question
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Business Analyst",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    max-width: 1100px;
    padding-bottom: 120px;
}

.hero {
    padding: 25px 30px;
    border-radius: 18px;
    background: linear-gradient(
        135deg,
        #1e293b,
        #111827
    );
    margin-bottom: 25px;
}

.hero-title {
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 5px;
}

.hero-subtitle {
    font-size: 15px;
    color: #94a3b8;
}

.user-message {
    background-color: #2563eb;
    padding: 14px 18px;
    border-radius: 15px 15px 3px 15px;
    margin: 12px 0 12px auto;
    max-width: 75%;
    color: white;
}

.ai-message {
    background-color: #1e293b;
    padding: 18px 20px;
    border-radius: 15px 15px 15px 3px;
    margin: 12px 0;
    max-width: 90%;
    border: 1px solid #334155;
}

.ai-label {
    font-weight: 700;
    margin-bottom: 10px;
}

.quick-title {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="hero">

<div class="hero-title">
🤖 AI Business Analyst
</div>

<div class="hero-subtitle">
Customer Product Intelligence • AI-powered business insights
</div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_table" not in st.session_state:
    st.session_state.last_table = None


# ============================================================
# QUICK QUESTIONS
# ============================================================

st.markdown(
    '<div class="quick-title">💡 Quick Analysis</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)


with col1:
    q1 = st.button(
        "📊 Churn Overview",
        use_container_width=True
    )

with col2:
    q2 = st.button(
        "🔴 Highest Risk",
        use_container_width=True
    )

with col3:
    q3 = st.button(
        "💰 Profit Risk",
        use_container_width=True
    )

with col4:
    q4 = st.button(
        "🎯 Prioritize Customers",
        use_container_width=True
    )


# ============================================================
# GENERATE ANSWER
# ============================================================

def generate_answer(result):

    result_type = result["type"]


    # --------------------------------------------------------
    # HIGH-RISK COUNT
    # --------------------------------------------------------

    if result_type == "high_risk_count":

        return (
            "### 🔴 High-Risk Customers\n\n"
            f"There are **{result['data']:,} "
            "high-risk customers** in the dataset.\n\n"
            "These customers have been classified as "
            "**High Risk** based on their churn-risk assessment."
        )


    # --------------------------------------------------------
    # CRITICAL COUNT
    # --------------------------------------------------------

    if result_type == "critical_count":

        return (
            "### 🚨 Critical-Priority Customers\n\n"
            f"There are **{result['data']:,} "
            "critical-priority customers** in the dataset.\n\n"
            "These customers should receive the highest "
            "retention attention."
        )


    # --------------------------------------------------------
    # BUSINESS SUMMARY
    # --------------------------------------------------------

    if result_type == "business_summary":

        data = result["data"]

        return f"""
### 📊 Business Overview

| KPI | Value |
|---|---:|
| Total Customers | {data["total_customers"]:,} |
| Actual Churners | {data["actual_churners"]:,} |
| Actual Churn Rate | {data["actual_churn_rate"]:.2f}% |
| High-Risk Customers | {data["high_risk_customers"]:,} |
| Critical Customers | {data["critical_customers"]:,} |
| Historical Profit | ₹{data["total_historical_profit"]:,.2f} |
| High-Risk Profit | ₹{data["high_risk_profit"]:,.2f} |

**Key observation:** High-risk customers account for
₹{data["high_risk_profit"]:,.2f} of historical profit.
"""


    # --------------------------------------------------------
    # RISK ANALYSIS
    # --------------------------------------------------------

    if result_type == "risk_analysis":

        data = pd.DataFrame(result["data"])

        data["avg_churn_probability"] = (
            data["avg_churn_probability"] * 100
        ).round(2)

        data["total_profit"] = (
            data["total_profit"].round(2)
        )

        data["avg_profit"] = (
            data["avg_profit"].round(2)
        )

        data = data.rename(
            columns={
                "risk_segment": "Risk Segment",
                "customers": "Customers",
                "avg_churn_probability":
                    "Avg Churn Probability %",
                "total_profit": "Historical Profit",
                "avg_profit": "Avg Profit"
            }
        )

        st.session_state.last_table = data

        return (
            "### 🔴 Risk Analysis\n\n"
            "The customer base is divided into three risk "
            "segments.\n\n"
            "**High Risk has the highest average churn "
            "probability.**"
        )


    # --------------------------------------------------------
    # RETENTION ANALYSIS
    # --------------------------------------------------------

    if result_type == "retention_analysis":

        data = pd.DataFrame(result["data"])

        data["avg_churn_probability"] = (
            data["avg_churn_probability"] * 100
        ).round(2)

        data["total_profit"] = (
            data["total_profit"].round(2)
        )

        data["avg_profit"] = (
            data["avg_profit"].round(2)
        )

        data = data.rename(
            columns={
                "retention_priority":
                    "Retention Priority",
                "customers": "Customers",
                "avg_churn_probability":
                    "Avg Churn Probability %",
                "total_profit":
                    "Historical Profit",
                "avg_profit":
                    "Avg Profit",
                "actual_churners":
                    "Actual Churners"
            }
        )

        st.session_state.last_table = data

        return (
            "### 🎯 Retention Analysis\n\n"
            "Retention priority combines customer risk "
            "and business importance.\n\n"
            "The table below shows the distribution across "
            "retention-priority groups."
        )


    # --------------------------------------------------------
    # HIGH-RISK + HIGH-VALUE
    # --------------------------------------------------------

    if result_type == "high_risk_high_value":

        data = pd.DataFrame(result["data"])

        data["churn_probability"] = (
            data["churn_probability"] * 100
        ).round(2)

        data["total_revenue"] = (
            data["total_revenue"].round(2)
        )

        data["total_profit"] = (
            data["total_profit"].round(2)
        )

        data = data.rename(
            columns={
                "customer_id":
                    "Customer ID",
                "churn_probability":
                    "Churn Probability %",
                "total_revenue":
                    "Revenue",
                "total_profit":
                    "Profit",
                "retention_priority":
                    "Retention Priority",
                "recency_days":
                    "Recency Days"
            }
        )

        st.session_state.last_table = data

        return (
            "### 🚨 High-Risk + High-Value Customers\n\n"
            "These customers combine **high churn risk** "
            "with **high customer value**.\n\n"
            "They are strong candidates for immediate "
            "retention attention."
        )


    # --------------------------------------------------------
    # CUSTOMER PROFILE
    # --------------------------------------------------------

    if result_type == "customer_profile":

        customer = result["customer"]

        return f"""
### 👤 Customer {customer["customer_id"]}

#### Risk & Retention

| Metric | Value |
|---|---|
| Churn Probability | {customer["churn_probability"]:.2f}% |
| Risk Score | {customer["risk_score"]:.2f} |
| Risk Segment | {customer["risk_segment"]} |
| Value Segment | {customer["value_segment"]} |
| Retention Priority | {customer["retention_priority"]} |

#### Financial Performance

| Metric | Value |
|---|---:|
| Total Revenue | ₹{customer["total_revenue"]:,.2f} |
| Total Profit | ₹{customer["total_profit"]:,.2f} |
| Profit Margin | {customer["profit_margin"]:.2f}% |
| Average Order Value | ₹{customer["avg_order_value"]:,.2f} |
| Total Orders | {customer["total_orders"]} |

#### Customer Behaviour

| Metric | Value |
|---|---:|
| Recency | {customer["recency_days"]} days |
| Cancellation Rate | {customer["cancellation_rate"]:.2f}% |
| Return Rate | {customer["return_rate"]:.2f}% |

#### Customer Information

- **Age:** {customer["age"]}
- **Region:** {customer["region"]}
- **Subscription:** {customer["subscription_type"]}
- **Acquisition Channel:** {customer["acquisition_channel"]}
"""


    # --------------------------------------------------------
    # UNKNOWN
    # --------------------------------------------------------

    return result["message"]


# ============================================================
# PROCESS QUESTION
# ============================================================

def process_question(question):

    st.session_state.last_table = None

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    # Send question to Python engine
    result = route_question(
        question,
        df
    )

    # Generate answer
    answer = generate_answer(result)

    # Add assistant message
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


# ============================================================
# QUICK BUTTONS
# ============================================================

if q1:
    process_question(
        "Give me a churn overview"
    )
    st.rerun()


if q2:
    process_question(
        "Who are the highest-risk customers?"
    )
    st.rerun()


if q3:
    process_question(
        "Where is the most profit at risk?"
    )
    st.rerun()


if q4:
    process_question(
        "Which customers should I prioritize?"
    )
    st.rerun()


# ============================================================
# DISPLAY CHAT
# ============================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"""
<div class="user-message">
👤 <b>You</b><br><br>
{message["content"]}
</div>
""",
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
<div class="ai-message">
<div class="ai-label">
🤖 Business Analyst
</div>

{message["content"]}

</div>
""",
            unsafe_allow_html=True
        )


# ============================================================
# DISPLAY TABLE
# ============================================================

if st.session_state.last_table is not None:

    st.dataframe(
        st.session_state.last_table,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask a business question..."
)


# ============================================================
# HANDLE QUESTION
# ============================================================

if question:

    process_question(question)

    st.rerun()