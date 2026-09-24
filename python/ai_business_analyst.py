import pandas as pd
from pathlib import Path


# ============================================================
# 1. LOAD DATASET
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "customer_churn_dashboard.csv"

df = pd.read_csv(DATA_FILE)


# ============================================================
# 2. BUSINESS SUMMARY
# ============================================================

def get_business_summary(df):

    return {
        "total_customers": len(df),

        "actual_churners": int(
            df["actual_churn"].sum()
        ),

        "actual_churn_rate": round(
            df["actual_churn"].mean() * 100,
            2
        ),

        "high_risk_customers": int(
            (df["risk_segment"] == "High Risk").sum()
        ),

        "critical_customers": int(
            (df["retention_priority"] == "Critical Priority").sum()
        ),

        "total_historical_profit": round(
            df["total_profit"].sum(),
            2
        ),

        "high_risk_profit": round(
            df.loc[
                df["risk_segment"] == "High Risk",
                "total_profit"
            ].sum(),
            2
        ),
    }


# ============================================================
# 3. RISK ANALYSIS
# ============================================================

def get_risk_analysis(df):

    return (
        df.groupby("risk_segment")
        .agg(
            customers=("customer_id", "count"),
            avg_churn_probability=(
                "churn_probability",
                "mean"
            ),
            total_profit=("total_profit", "sum"),
            avg_profit=("total_profit", "mean"),
        )
        .round(4)
        .sort_values(
            "avg_churn_probability",
            ascending=False
        )
    )


# ============================================================
# 4. RETENTION ANALYSIS
# ============================================================

def get_retention_analysis(df):

    return (
        df.groupby("retention_priority")
        .agg(
            customers=("customer_id", "count"),
            avg_churn_probability=(
                "churn_probability",
                "mean"
            ),
            total_profit=("total_profit", "sum"),
            avg_profit=("total_profit", "mean"),
            actual_churners=("actual_churn", "sum"),
        )
        .round(4)
        .sort_values(
            "avg_churn_probability",
            ascending=False
        )
    )


# ============================================================
# 5. HIGH-RISK + HIGH-VALUE CUSTOMERS
# ============================================================

def get_high_value_risk_customers(df, n=10):

    result = df[
        (df["risk_segment"] == "High Risk")
        &
        (df["value_segment"] == "High Value")
    ].copy()

    return (
        result
        .sort_values(
            "churn_probability",
            ascending=False
        )
        .head(n)
        [
            [
                "customer_id",
                "churn_probability",
                "total_revenue",
                "total_profit",
                "retention_priority",
                "recency_days",
            ]
        ]
    )


# ============================================================
# 6. CUSTOMER PROFILE
# ============================================================

def get_customer_profile(df, customer_id):

    customer_id = str(customer_id).strip().upper()

    customer = df[
        df["customer_id"]
        .astype(str)
        .str.upper()
        == customer_id
    ]

    if customer.empty:
        return None

    row = customer.iloc[0]

    return {
        "customer_id": row["customer_id"],

        "churn_probability": round(
            float(row["churn_probability"]) * 100,
            2
        ),

        "risk_score": round(
            float(row["risk_score"]),
            2
        ),

        "risk_segment": row["risk_segment"],

        "value_segment": row["value_segment"],

        "retention_priority": row[
            "retention_priority"
        ],

        "total_orders": int(
            row["total_orders"]
        ),

        "total_revenue": round(
            float(row["total_revenue"]),
            2
        ),

        "total_profit": round(
            float(row["total_profit"]),
            2
        ),

        "profit_margin": round(
            float(row["profit_margin"]) * 100,
            2
        ),

        "avg_order_value": round(
            float(row["avg_order_value"]),
            2
        ),

        "recency_days": int(
            row["recency_days"]
        ),

        "age": int(
            row["age"]
        ),

        "region": row["region"],

        "subscription_type": row[
            "subscription_type"
        ],

        "acquisition_channel": row[
            "acquisition_channel"
        ],

        "cancellation_rate": round(
            float(row["cancellation_rate"]) * 100,
            2
        ),

        "return_rate": round(
            float(row["return_rate"]) * 100,
            2
        ),
    }


# ============================================================
# 7. QUESTION ROUTER
# ============================================================

def route_question(question, df):

    q = question.lower().strip()

    # --------------------------------------------------------
    # CUSTOMER-SPECIFIC QUESTIONS
    # --------------------------------------------------------

    for customer_id in df["customer_id"].astype(str):

        if customer_id.lower() in q:

            profile = get_customer_profile(
                df,
                customer_id
            )

            return {
                "type": "customer_profile",
                "customer": profile
            }


    # --------------------------------------------------------
    # SPECIFIC HIGH-RISK CUSTOMER COUNT
    # --------------------------------------------------------

    if (
        "how many" in q
        and "high risk" in q
        and "customer" in q
    ):

        summary = get_business_summary(df)

        return {
            "type": "high_risk_count",
            "data": summary["high_risk_customers"]
        }


    # --------------------------------------------------------
    # SPECIFIC CRITICAL CUSTOMER COUNT
    # --------------------------------------------------------

    if (
        "how many" in q
        and (
            "critical customer" in q
            or "critical priority" in q
        )
    ):

        summary = get_business_summary(df)

        return {
            "type": "critical_count",
            "data": summary["critical_customers"]
        }


    # --------------------------------------------------------
    # HIGH-RISK + HIGH-VALUE
    # --------------------------------------------------------

    if (
        ("high risk" in q or "high-risk" in q)
        and
        ("high value" in q or "high-value" in q)
    ):

        customers = get_high_value_risk_customers(
            df,
            n=10
        )

        return {
            "type": "high_risk_high_value",
            "data": customers.to_dict(
                orient="records"
            )
        }


    # --------------------------------------------------------
    # RETENTION / PRIORITY
    # --------------------------------------------------------

    if (
        "retention" in q
        or "priority" in q
        or "prioritize" in q
    ):

        analysis = get_retention_analysis(df)

        return {
            "type": "retention_analysis",
            "data": analysis.reset_index().to_dict(
                orient="records"
            )
        }


    # --------------------------------------------------------
    # RISK ANALYSIS
    # --------------------------------------------------------

    if (
        "risk" in q
        or "risky" in q
        or "risk segment" in q
    ):

        analysis = get_risk_analysis(df)

        return {
            "type": "risk_analysis",
            "data": analysis.reset_index().to_dict(
                orient="records"
            )
        }


    # --------------------------------------------------------
    # PROFIT / REVENUE
    # --------------------------------------------------------

    if (
        "profit" in q
        or "money" in q
        or "financial" in q
        or "revenue" in q
    ):

        summary = get_business_summary(df)

        return {
            "type": "business_summary",
            "data": summary
        }


    # --------------------------------------------------------
    # GENERAL SUMMARY / CHURN
    # --------------------------------------------------------

    if (
        "summary" in q
        or "overview" in q
        or "business" in q
        or "customers" in q
        or "churn" in q
    ):

        summary = get_business_summary(df)

        return {
            "type": "business_summary",
            "data": summary
        }


    # --------------------------------------------------------
    # UNKNOWN
    # --------------------------------------------------------

    return {
        "type": "unknown",
        "message": (
            "I couldn't identify the business question. "
            "Try asking about churn, risk, retention, "
            "profit, customers, or a specific Customer ID."
        )
    }


# ============================================================
# 8. COMMAND-LINE TEST
# ============================================================

def run_qna():

    print("\n")
    print("=" * 60)
    print("AI BUSINESS ANALYST")
    print("=" * 60)

    print(
        "\nAsk a business question."
        "\nType 'exit' to stop."
    )

    while True:

        question = input("\nYou: ")

        if question.lower().strip() == "exit":

            print("\nGoodbye!")
            break

        result = route_question(
            question,
            df
        )

        print("\nAnalyst:")

        print(result)


# ============================================================
# 9. START
# ============================================================

if __name__ == "__main__":

    print("Dataset loaded successfully!")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    run_qna()