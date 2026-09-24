import os
import json
import pandas as pd

from dotenv import load_dotenv
from google import genai

load_dotenv()
from python.ai_business_analyst import (
    df,
    get_business_summary,
    get_risk_analysis,
    get_retention_analysis,
    get_high_value_risk_customers,
)


# ============================================================
# GEMINI CLIENT
# ============================================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY environment variable is not set."
    )

client = genai.Client(
    api_key=api_key
)


# ============================================================
# VERIFIED BUSINESS SUMMARY
# ============================================================

def get_verified_business_summary():
    """
    Return verified business KPIs from the
    Python analytics engine.
    """

    return get_business_summary(df)


# ============================================================
# VERIFIED RISK ANALYSIS
# ============================================================

def get_verified_risk_analysis():
    """
    Return verified risk-segment analysis.
    """

    result = get_risk_analysis(df)

    return result.reset_index().to_dict(
        orient="records"
    )


# ============================================================
# VERIFIED RETENTION ANALYSIS
# ============================================================

def get_verified_retention_analysis():
    """
    Return verified retention-priority analysis.
    """

    result = get_retention_analysis(df)

    return result.reset_index().to_dict(
        orient="records"
    )


# ============================================================
# VERIFIED HIGH-RISK + HIGH-VALUE CUSTOMERS
# ============================================================

def get_verified_high_risk_high_value_customers():
    """
    Return the top High Risk + High Value customers.
    """

    result = get_high_value_risk_customers(
        df,
        n=10
    )

    return result.to_dict(
        orient="records"
    )


# ============================================================
# COMPLETE CUSTOMER 360 PROFILE
# ============================================================

def get_verified_customer_profile(customer_id):
    """
    Return every available field for a specific customer.

    Works with ANY customer ID that exists in the dataset.
    """

    # Clean customer ID
    customer_id = str(
        customer_id
    ).strip().upper()

    # Make sure customer_id exists
    if "customer_id" not in df.columns:
        return {
            "found": False,
            "error": (
                "The dataset does not contain "
                "a customer_id column."
            )
        }

    # Search customer
    matches = df[
        df["customer_id"]
        .astype(str)
        .str.strip()
        .str.upper()
        == customer_id
    ]

    # Customer not found
    if matches.empty:
        return {
            "found": False,
            "customer_id": customer_id,
            "error": (
                f"Customer {customer_id} "
                "was not found in the dataset."
            )
        }

    # Get complete customer row
    customer = matches.iloc[0].to_dict()

    # Convert NumPy/Pandas values into JSON-safe values
    customer = json.loads(
        json.dumps(
            customer,
            default=str
        )
    )

    return {
        "found": True,
        "customer_id": customer_id,
        "field_count": len(df.columns),
        "available_fields": list(df.columns),
        "profile": customer
    }


# ============================================================
# GENERAL CUSTOMER DATA ANALYSIS
# ============================================================

def analyze_customer_data(
    filters=None,
    group_by=None,
    metric=None,
    operation="count",
    sort_by=None,
    ascending=False,
    limit=20
):
    """
    Flexible analysis engine for the customer dataset.

    Supports:
        - filtering
        - grouping
        - count
        - sum
        - mean
        - median
        - min
        - max
        - sorting
        - limiting
    """

    data = df.copy()

    # --------------------------------------------------------
    # DEFAULT VALUES
    # --------------------------------------------------------

    if filters is None:
        filters = {}

    try:
        limit = int(limit)
    except (TypeError, ValueError):
        limit = 20

    if limit <= 0:
        limit = 20

    operation = str(
        operation
    ).lower().strip()

    # --------------------------------------------------------
    # VALID COLUMNS
    # --------------------------------------------------------

    valid_columns = set(
        df.columns
    )

    # --------------------------------------------------------
    # APPLY FILTERS
    # --------------------------------------------------------

    for column, value in filters.items():

        if column not in valid_columns:
            return {
                "error": (
                    f"Invalid filter column: {column}"
                ),
                "available_columns": list(
                    df.columns
                )
            }

        # Multiple filter values
        if isinstance(value, list):
            data = data[
                data[column].isin(value)
            ]

        else:
            data = data[
                data[column] == value
            ]

    # --------------------------------------------------------
    # NO RESULTS
    # --------------------------------------------------------

    if data.empty:
        return {
            "customers_found": 0,
            "message": (
                "No customers matched "
                "the requested filters."
            )
        }

    # ========================================================
    # SIMPLE COUNT
    # ========================================================

    if (
        operation == "count"
        and not group_by
    ):
        return {
            "customers_found": int(
                len(data)
            ),
            "operation": "count",
            "result": int(
                len(data)
            )
        }

    # ========================================================
    # GROUPED ANALYSIS
    # ========================================================

    if group_by:

        if group_by not in valid_columns:
            return {
                "error": (
                    f"Invalid group_by column: "
                    f"{group_by}"
                ),
                "available_columns": list(
                    df.columns
                )
            }

        # ----------------------------------------------------
        # COUNT BY GROUP
        # ----------------------------------------------------

        if operation == "count":

            result = (
                data
                .groupby(
                    group_by,
                    dropna=False
                )
                .size()
                .reset_index(
                    name="result"
                )
            )

        # ----------------------------------------------------
        # METRIC-BASED GROUPING
        # ----------------------------------------------------

        else:

            if not metric:
                return {
                    "error": (
                        f"A metric is required "
                        f"for {operation}."
                    )
                }

            if metric not in valid_columns:
                return {
                    "error": (
                        f"Invalid metric column: "
                        f"{metric}"
                    ),
                    "available_columns": list(
                        df.columns
                    )
                }

            grouped = data.groupby(
                group_by,
                dropna=False
            )

            if operation == "sum":

                result = (
                    grouped[metric]
                    .sum()
                    .reset_index(
                        name="result"
                    )
                )

            elif operation == "mean":

                result = (
                    grouped[metric]
                    .mean()
                    .reset_index(
                        name="result"
                    )
                )

            elif operation == "median":

                result = (
                    grouped[metric]
                    .median()
                    .reset_index(
                        name="result"
                    )
                )

            elif operation == "min":

                result = (
                    grouped[metric]
                    .min()
                    .reset_index(
                        name="result"
                    )
                )

            elif operation == "max":

                result = (
                    grouped[metric]
                    .max()
                    .reset_index(
                        name="result"
                    )
                )

            else:
                return {
                    "error": (
                        f"Unsupported operation: "
                        f"{operation}"
                    )
                }

    # ========================================================
    # OVERALL METRIC ANALYSIS
    # ========================================================

    else:

        if not metric:
            return {
                "error": (
                    f"A metric is required "
                    f"for {operation}."
                )
            }

        if metric not in valid_columns:
            return {
                "error": (
                    f"Invalid metric column: "
                    f"{metric}"
                ),
                "available_columns": list(
                    df.columns
                )
            }

        if operation == "sum":

            value = data[metric].sum()

        elif operation == "mean":

            value = data[metric].mean()

        elif operation == "median":

            value = data[metric].median()

        elif operation == "min":

            value = data[metric].min()

        elif operation == "max":

            value = data[metric].max()

        else:
            return {
                "error": (
                    f"Unsupported operation: "
                    f"{operation}"
                )
            }

        # Convert NumPy values
        try:
            value = float(value)
        except (TypeError, ValueError):
            value = str(value)

        return {
            "customers_found": int(
                len(data)
            ),
            "metric": metric,
            "operation": operation,
            "result": value
        }

    # ========================================================
    # SORT RESULTS
    # ========================================================

    if sort_by:

        if sort_by in result.columns:

            result = result.sort_values(
                by=sort_by,
                ascending=ascending
            )

        elif "result" in result.columns:

            result = result.sort_values(
                by="result",
                ascending=ascending
            )

    elif "result" in result.columns:

        result = result.sort_values(
            by="result",
            ascending=ascending
        )

    # ========================================================
    # LIMIT RESULTS
    # ========================================================

    result = result.head(
        limit
    )

    # ========================================================
    # CLEAN NaN / NumPy VALUES
    # ========================================================

    result = result.astype(
        object
    ).where(
        pd.notna(result),
        None
    )

    result = json.loads(
        json.dumps(
            result.to_dict(
                orient="records"
            ),
            default=str
        )
    )

    # ========================================================
    # RETURN RESULT
    # ========================================================

    return {
        "customers_found": int(
            len(data)
        ),
        "group_by": group_by,
        "metric": metric,
        "operation": operation,
        "analysis": result
    }


# ============================================================
# GEMINI TOOL DEFINITIONS
# ============================================================

BUSINESS_TOOLS = [

    # --------------------------------------------------------
    # BUSINESS SUMMARY
    # --------------------------------------------------------

    {
        "type": "function",
        "name": "get_verified_business_summary",
        "description": (
            "Get verified overall business KPIs from "
            "the customer dataset. Includes total "
            "customers, actual churners, actual churn "
            "rate, high-risk customers, critical customers, "
            "total historical profit and historical profit "
            "associated with high-risk customers."
        ),
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },

    # --------------------------------------------------------
    # RISK ANALYSIS
    # --------------------------------------------------------

    {
        "type": "function",
        "name": "get_verified_risk_analysis",
        "description": (
            "Analyze customers by High Risk, Medium Risk "
            "and Low Risk segments. Returns customer count, "
            "average churn probability, total profit and "
            "average profit."
        ),
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },

    # --------------------------------------------------------
    # RETENTION ANALYSIS
    # --------------------------------------------------------

    {
        "type": "function",
        "name": "get_verified_retention_analysis",
        "description": (
            "Analyze customers by retention priority. "
            "Returns customer count, average churn "
            "probability, total profit, average profit "
            "and actual churners."
        ),
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },

    # --------------------------------------------------------
    # HIGH RISK + HIGH VALUE
    # --------------------------------------------------------

    {
        "type": "function",
        "name": (
            "get_verified_high_risk_high_value_customers"
        ),
        "description": (
            "Find the top customers who are both High Risk "
            "and High Value. Use for retention prioritization."
        ),
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },

    # --------------------------------------------------------
    # CUSTOMER 360
    # --------------------------------------------------------

    {
        "type": "function",
        "name": "get_verified_customer_profile",
        "description": (
            "Get the complete profile of ANY customer "
            "that exists in the dataset. Returns every "
            "available field for that customer. ALWAYS "
            "use this tool when the user asks about a "
            "specific customer ID."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": (
                        "Exact customer ID from the "
                        "dataset, for example C04291, "
                        "C00385 or C09624."
                    )
                }
            },
            "required": [
                "customer_id"
            ]
        }
    },

    # --------------------------------------------------------
    # GENERAL DATA ANALYSIS
    # --------------------------------------------------------

    {
        "type": "function",
        "name": "analyze_customer_data",
        "description": (
            "Perform flexible analysis on any available "
            "customer dataset column. Supports filtering, "
            "grouping, counting, sum, mean, median, min, "
            "max and sorting. Use this for questions about "
            "region, age, subscription type, acquisition "
            "channel, churn, risk, value, revenue, profit, "
            "orders, returns, discounts, recency, "
            "cancellations, customer lifetime and "
            "revenue per order."
        ),
        "parameters": {
            "type": "object",
            "properties": {

                "filters": {
                    "type": "object",
                    "description": (
                        "Optional filters using valid "
                        "dataset column names."
                    )
                },

                "group_by": {
                    "type": "string",
                    "description": (
                        "Optional dataset column to "
                        "group by."
                    )
                },

                "metric": {
                    "type": "string",
                    "description": (
                        "Dataset column to calculate."
                    )
                },

                "operation": {
                    "type": "string",
                    "enum": [
                        "count",
                        "sum",
                        "mean",
                        "median",
                        "min",
                        "max"
                    ],
                    "description": (
                        "Calculation to perform."
                    )
                },

                "sort_by": {
                    "type": "string",
                    "description": (
                        "Optional column used for sorting."
                    )
                },

                "ascending": {
                    "type": "boolean",
                    "description": (
                        "True for ascending sorting; "
                        "false for descending."
                    )
                },

                "limit": {
                    "type": "integer",
                    "description": (
                        "Maximum number of grouped "
                        "results to return."
                    )
                }
            },
            "required": [
                "operation"
            ]
        }
    }
]


# ============================================================
# TOOL EXECUTOR
# ============================================================

def execute_business_tool(
    tool_name,
    arguments=None
):
    """
    Execute the verified Python tool selected by Gemini.
    """

    if arguments is None:
        arguments = {}

    # --------------------------------------------------------
    # BUSINESS SUMMARY
    # --------------------------------------------------------

    if tool_name == "get_verified_business_summary":

        return get_verified_business_summary()

    # --------------------------------------------------------
    # RISK ANALYSIS
    # --------------------------------------------------------

    if tool_name == "get_verified_risk_analysis":

        return get_verified_risk_analysis()

    # --------------------------------------------------------
    # RETENTION ANALYSIS
    # --------------------------------------------------------

    if tool_name == "get_verified_retention_analysis":

        return get_verified_retention_analysis()

    # --------------------------------------------------------
    # HIGH RISK + HIGH VALUE
    # --------------------------------------------------------

    if (
        tool_name
        == "get_verified_high_risk_high_value_customers"
    ):

        return (
            get_verified_high_risk_high_value_customers()
        )

    # --------------------------------------------------------
    # CUSTOMER PROFILE
    # --------------------------------------------------------

    if tool_name == "get_verified_customer_profile":

        customer_id = arguments.get(
            "customer_id"
        )

        if not customer_id:

            return {
                "found": False,
                "error": (
                    "No customer ID was provided."
                )
            }

        return get_verified_customer_profile(
            customer_id
        )

    # --------------------------------------------------------
    # GENERAL DATA ANALYSIS
    # --------------------------------------------------------

    if tool_name == "analyze_customer_data":

        return analyze_customer_data(
            filters=arguments.get(
                "filters"
            ),
            group_by=arguments.get(
                "group_by"
            ),
            metric=arguments.get(
                "metric"
            ),
            operation=arguments.get(
                "operation",
                "count"
            ),
            sort_by=arguments.get(
                "sort_by"
            ),
            ascending=arguments.get(
                "ascending",
                False
            ),
            limit=arguments.get(
                "limit",
                20
            )
        )

    # --------------------------------------------------------
    # UNKNOWN TOOL
    # --------------------------------------------------------

    return {
        "error": (
            f"Unknown business tool: {tool_name}"
        )
    }


# ============================================================
# SYSTEM INSTRUCTIONS
# ============================================================

SYSTEM_INSTRUCTIONS = """
You are an AI Business Analyst for a Customer Product
Intelligence system.

You have access to a verified Python/Pandas analytics
engine. The Python dataset is the SOURCE OF TRUTH.

============================================================
DATASET FIELDS
============================================================

The dataset contains:

customer_id
churn_probability
risk_score
risk_segment
value_segment
retention_priority
actual_churn
predicted_churn
total_orders
total_revenue
total_profit
profit_margin
avg_order_value
avg_discount
recency_days
age
region
subscription_type
acquisition_channel
cancelled_orders
cancellation_rate
customer_lifetime_days
returned_orders
return_rate
revenue_per_order

============================================================
IMPORTANT RULES
============================================================

1. NEVER invent dataset numbers.

2. NEVER invent customer IDs.

3. Python tool results are the source of truth.

4. If the user asks about a specific customer ID,
   ALWAYS use get_verified_customer_profile.

5. The customer profile tool works with ANY valid
   customer ID in the dataset.

6. Do not assume C04291 is the only customer.

7. Extract the exact customer ID from the question.

8. If the customer exists, answer using the verified
   profile.

9. If the customer does not exist, clearly say that
   the customer was not found.

10. If the user asks for "everything", "all details",
    "full profile" or "complete profile", provide
    all available customer fields.

11. For calculations, comparisons, grouping, filtering
    and rankings, use analyze_customer_data.

12. You may call multiple tools if a question requires
    multiple verified analyses.

13. Do not guess information that a tool can calculate.

14. If the dataset does not contain requested
    information, clearly say so.

============================================================
CUSTOMER FIELD MEANINGS
============================================================

actual_churn:
Whether the customer actually churned.

predicted_churn:
The model's predicted churn classification.

churn_probability:
The model's predicted probability of churn.

risk_score:
The customer's risk score.

total_profit:
Historical profit generated by the customer.

Historical profit associated with high-risk customers
must not automatically be described as guaranteed
future financial loss.

============================================================
CUSTOMER ANALYSIS
============================================================

When analyzing a customer, consider:

- churn probability
- risk score
- risk segment
- value segment
- retention priority
- actual churn
- predicted churn
- orders
- revenue
- profit
- profit margin
- average order value
- discount
- recency
- age
- region
- subscription
- acquisition channel
- cancelled orders
- cancellation rate
- customer lifetime
- returned orders
- return rate
- revenue per order

Do not claim that one field alone proves why a customer
will churn. Describe it as a business signal when
appropriate.

============================================================
BUSINESS QUESTIONS
============================================================

Use verified tools for questions such as:

- How many customers are there?
- How many customers churned?
- What is the churn rate?
- Which region has the highest profit?
- Which subscription has the highest churn?
- Which acquisition channel has the most customers?
- Which segment is most profitable?
- What is the average order value?
- Which customers have high return rates?
- How many High Risk customers are from North?
- Compare Free and Premium customers.
- Which region has the most customers?
- Who are the most profitable customers?

============================================================
MULTI-TOOL QUESTIONS
============================================================

If a question requires multiple analyses, call multiple
tools before giving the final answer.

For example:

"Give me a complete business overview"

may require:

- business summary
- risk analysis
- retention analysis

Do not invent missing information.

============================================================
ANSWER STYLE
============================================================

Give the answer clearly.

For business questions explain:

1. What is happening
2. Why it matters
3. Which customers or segments are affected
4. What action could be considered

For individual customer questions:

1. Present verified customer information
2. Explain the important business signals
3. Give useful business interpretation
4. Do not claim unsupported causes

Never claim that a recommendation guarantees a result.
"""


# ============================================================
# GEMINI MULTI-TOOL REASONING
# ============================================================

def ask_gemini(question):
    """
    Send a question to Gemini.

    Gemini can call one or multiple verified Python
    analytics tools before producing the final answer.
    """

    # --------------------------------------------------------
    # INITIAL REQUEST
    # --------------------------------------------------------

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=(
            SYSTEM_INSTRUCTIONS
            + "\n\nUSER QUESTION:\n"
            + question
        ),
        tools=BUSINESS_TOOLS
    )

    # --------------------------------------------------------
    # MULTI-TOOL LOOP
    # --------------------------------------------------------

    max_tool_rounds = 10

    for _ in range(max_tool_rounds):

        # Find function calls
        function_calls = [
            step
            for step in interaction.steps
            if step.type == "function_call"
        ]

        # ----------------------------------------------------
        # NO MORE TOOLS
        # ----------------------------------------------------

        if not function_calls:

            if interaction.output_text:
                return interaction.output_text

            return (
                "I could not generate a final answer."
            )

        # ----------------------------------------------------
        # EXECUTE ALL REQUESTED TOOLS
        # ----------------------------------------------------

        function_results = []

        for step in function_calls:

            print(
                f"Gemini selected tool: {step.name}"
            )

            print(
                f"Tool arguments: {step.arguments}"
            )

            try:

                result = execute_business_tool(
                    step.name,
                    step.arguments
                )

            except Exception as error:

                result = {
                    "error": str(error)
                }

            print(
                "\nVerified tool result:"
            )

            print(
                result
            )

            # Convert result to JSON text
            result_text = json.dumps(
                result,
                default=str
            )

            function_results.append(
                {
                    "type": "function_result",
                    "name": step.name,
                    "call_id": step.id,
                    "result": [
                        {
                            "type": "text",
                            "text": result_text
                        }
                    ]
                }
            )

        # ----------------------------------------------------
        # SEND RESULTS BACK TO GEMINI
        # ----------------------------------------------------

        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            previous_interaction_id=interaction.id,
            input=function_results,
            tools=BUSINESS_TOOLS
        )

    # --------------------------------------------------------
    # SAFETY FALLBACK
    # --------------------------------------------------------

    return (
        "I reached the maximum number of analytical "
        "steps while processing this question. "
        "Please try asking the question more specifically."
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("GEMINI AI BUSINESS ANALYST")
    print("=" * 60)

    print("\nTesting Gemini...")

    answer = ask_gemini(
        "Give me the complete profile of C04291, "
        "including every available field."
    )

    print("\nGemini:")
    print(answer)

    print("\n")
    print("=" * 60)
    print("GEMINI CONNECTION TEST COMPLETE")
    print("=" * 60)