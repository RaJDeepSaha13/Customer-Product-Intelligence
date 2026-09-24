# 🛍️ Customer & Product Intelligence

An end-to-end **Customer & Product Intelligence platform** built for **ShopSphere**, a fictional e-commerce company.

The project combines **SQL, Python, Machine Learning, Power BI, and Streamlit** to transform raw e-commerce data into actionable insights around **customer behavior, churn, retention, revenue, profitability, products, and operations**.

---

## 📌 Project Overview

E-commerce businesses generate large amounts of customer, order, product, session, support, and operational data. However, raw data alone does not answer important business questions such as:

* Which customers are likely to churn?
* Which customers are high-value?
* Which customers require immediate retention attention?
* What factors are associated with customer churn?
* Which products and customer segments generate the most revenue and profit?
* Where are cancellations and returns occurring?
* How can the business prioritize retention efforts?
* What business questions can be answered directly from the data?

**Customer & Product Intelligence** addresses these questions through an integrated analytics pipeline.

### Core Pipeline

```text
Raw Data
   ↓
Data Cleaning & Validation
   ↓
SQL Analysis / PostgreSQL
   ↓
Feature Engineering
   ↓
Machine Learning
   ↓
Customer Risk & Value Segmentation
   ↓
Business Analytics
   ↓
Power BI Dashboards
   ↓
Streamlit Intelligence App
   ↓
Business Insights & Recommendations
```

---

# 🎯 Objectives

The main objectives of this project are:

* Analyze customer purchasing behavior
* Measure revenue and profitability
* Identify customer churn patterns
* Predict customer churn probability
* Segment customers based on risk and value
* Prioritize customers for retention
* Analyze product performance
* Analyze orders, cancellations, returns, and operations
* Understand customer lifetime value and engagement
* Build interactive Power BI dashboards
* Provide an interactive Streamlit-based analytics interface
* Convert analytical results into actionable business insights

---

# 🗂️ Dataset

The project uses a relational e-commerce dataset representing the operations of **ShopSphere**.

The analytical customer-level dataset contains **25 features** covering customer behavior, revenue, profitability, churn, retention, and segmentation.

### Customer-Level Features

| Feature                  | Description                         |
| ------------------------ | ----------------------------------- |
| `customer_id`            | Unique customer identifier          |
| `churn_probability`      | Predicted probability of churn      |
| `risk_score`             | Customer risk score                 |
| `risk_segment`           | Customer churn-risk segment         |
| `value_segment`          | Customer value segment              |
| `retention_priority`     | Priority for retention efforts      |
| `actual_churn`           | Actual churn outcome                |
| `predicted_churn`        | Model-predicted churn               |
| `total_orders`           | Total number of orders              |
| `total_revenue`          | Total customer revenue              |
| `total_profit`           | Total customer profit               |
| `profit_margin`          | Customer profit margin              |
| `avg_order_value`        | Average order value                 |
| `avg_discount`           | Average discount received           |
| `recency_days`           | Days since recent activity/order    |
| `age`                    | Customer age                        |
| `region`                 | Customer region                     |
| `subscription_type`      | Subscription category               |
| `acquisition_channel`    | Customer acquisition source         |
| `cancelled_orders`       | Number of cancelled orders          |
| `cancellation_rate`      | Customer cancellation rate          |
| `customer_lifetime_days` | Customer lifetime                   |
| `returned_orders`        | Number of returned orders           |
| `return_rate`            | Customer return rate                |
| `revenue_per_order`      | Average revenue generated per order |

---

# 🗄️ Source Tables

The original relational dataset contains multiple business tables:

```text
customers
products
orders
order_items
sessions
user_events
operations
support_tickets
experiments
```

These tables allow analysis across multiple dimensions of the e-commerce business.

---

# 🛠️ Technology Stack

### Data & Database

* Python
* Pandas
* NumPy
* PostgreSQL
* SQL

### Machine Learning

* Scikit-learn
* Logistic Regression
* Random Forest
* Feature engineering
* Classification metrics

### Visualization & BI

* Power BI
* Matplotlib
* Data visualization

### Application

* Streamlit
* Python

### Development Tools

* VS Code / Antigravity
* Git
* GitHub

---

# 🤖 Machine Learning

A customer churn prediction model is used to identify customers who are at higher risk of leaving.

### ML Workflow

```text
Customer Data
      ↓
Data Preprocessing
      ↓
Feature Engineering
      ↓
Train/Test Split
      ↓
Model Training
      ↓
Churn Prediction
      ↓
Risk Segmentation
      ↓
Retention Prioritization
```

Two classification models were explored:

* Logistic Regression
* Random Forest

The model output is used to generate:

* Churn probability
* Predicted churn
* Risk score
* Risk segment
* Retention priority

---

# 📊 Business Intelligence

The project uses **Power BI** to convert analytical data into interactive dashboards.

### Dashboard Areas

#### 1. Executive Overview

Provides a high-level view of:

* Customers
* Revenue
* Profit
* Orders
* Churn
* Customer value
* Overall business performance

#### 2. Customer Intelligence

Analyzes:

* Customer segments
* Customer value
* Purchasing behavior
* Revenue contribution
* Customer lifetime
* Regional patterns

#### 3. Risk & Retention Intelligence

Focuses on:

* Churn probability
* High-risk customers
* Retention priority
* Churn drivers
* Customer risk segmentation

#### 4. Product Intelligence

Analyzes:

* Product performance
* Revenue
* Profit
* Orders
* Returns
* Product-level trends

#### 5. Operations Intelligence

Analyzes:

* Order operations
* Cancellations
* Returns
* Delivery-related metrics
* Operational performance

#### 6. Root Cause & Recommendations

Connects analytical findings with potential business actions.

---

# 🧠 Customer Intelligence

Customers are segmented using multiple dimensions.

### Risk Segmentation

Customers can be classified according to their estimated churn risk.

```text
Customer
   ↓
Churn Probability
   ↓
Risk Score
   ↓
Risk Segment
```

### Value Segmentation

Customers are also analyzed based on their economic value using metrics such as:

* Revenue
* Profit
* Order frequency
* Average order value
* Customer lifetime

### Retention Priority

Risk and customer value can be combined to identify customers who may deserve greater retention attention.

Example:

```text
High Risk + High Value
        ↓
High Retention Priority
```

---

# 📈 Key Business Metrics

The project tracks metrics such as:

### Customer Metrics

* Total Customers
* Churn Rate
* Customer Lifetime
* Recency
* Customer Segments

### Revenue Metrics

* Total Revenue
* Revenue per Order
* Average Order Value
* Revenue by Region
* Revenue by Customer Segment

### Profitability Metrics

* Total Profit
* Profit Margin
* Profit by Segment
* Profit by Product

### Retention Metrics

* Churn Probability
* High-Risk Customers
* Retention Priority
* Cancellation Rate
* Return Rate

---

# 💬 AI Business Analyst Layer

The project is designed to move beyond static dashboards by providing an interactive analytical interface.

The Streamlit application can be used to answer business questions based on the processed customer data.

Example questions include:

```text
Which customers are at high risk of churn?

Who are the high-risk high-value customers?

What is the overall churn rate?

Which region generates the most revenue?

Which customers should receive retention attention?

Show me the complete profile of a customer.

Compare customers by region.

What are the major customer risk patterns?
```

The architecture is designed around:

```text
User Question
      ↓
Question / Intent Detection
      ↓
Analytical Tool Selection
      ↓
Data Processing
      ↓
Business Calculation
      ↓
Result
      ↓
Business Explanation
```

---

# 🖥️ Streamlit Application

The project includes a Streamlit application:

```text
streamlit_app.py
```

The application is intended to provide an interactive interface for:

* Uploading/using supported datasets
* Data validation
* Data processing
* Customer analytics
* Churn analysis
* Risk analysis
* Retention analysis
* Customer 360 analysis
* Business questions
* Analytical results

---

# 📁 Project Structure

```text
Customer_Porduct_Intelligence/
│
├── data/
│   └── Dataset files
│
├── documentation/
│   └── Project documentation
│
├── powerbi/
│   └── Power BI dashboards
│
├── python/
│   ├── Data processing
│   ├── Feature engineering
│   ├── Machine learning
│   └── Analytics
│
├── sql/
│   └── SQL queries and database scripts
│
├── streamlit_app.py
│   └── Streamlit application
│
├── .gitignore
├── .env
└── README.md
```

---

# 🔄 End-to-End Workflow

```text
              ┌─────────────────┐
              │   Raw E-Commerce│
              │       Data      │
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │ Data Cleaning & │
              │  Validation     │
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │ PostgreSQL / SQL│
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │ Feature         │
              │ Engineering     │
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │ Churn ML Model  │
              └────────┬────────┘
                       ↓
        ┌──────────────┴──────────────┐
        ↓                             ↓
┌───────────────┐             ┌───────────────┐
│ Risk / Value  │             │ Business      │
│ Segmentation  │             │ Analytics     │
└───────┬───────┘             └───────┬───────┘
        │                             │
        └──────────────┬──────────────┘
                       ↓
              ┌─────────────────┐
              │    Power BI     │
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │    Streamlit    │
              │ Intelligence App│
              └─────────────────┘
```

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/RaJDeepSaha13/Customer-Churn.git
cd Customer-Churn
```

## 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

## 3. Install Dependencies

If a `requirements.txt` file is available:

```bash
pip install -r requirements.txt
```

Otherwise, install the required Python packages used by the project.

## 4. Configure Environment Variables

Create a `.env` file for required API keys or configuration values.

**Do not commit `.env` to GitHub.**

The `.gitignore` file should contain:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

## 5. Run the Streamlit Application

```bash
streamlit run streamlit_app.py
```

The application will open in your browser.

---

# 📌 Future Improvements

Potential future improvements include:

* Automated data ingestion
* Real-time customer risk monitoring
* Improved churn prediction models
* Model explainability
* Automated retention recommendations
* More advanced Customer 360 analytics
* Real-time dashboards
* Automated anomaly detection
* Advanced product recommendation analysis
* Natural-language business intelligence
* Deployment to a cloud platform

---


## ⭐ Project Highlights

This project demonstrates an end-to-end approach to turning raw e-commerce data into business intelligence:

```text
DATA
 ↓
SQL
 ↓
PYTHON
 ↓
MACHINE LEARNING
 ↓
CUSTOMER INTELLIGENCE
 ↓
POWER BI
 ↓
STREAMLIT
 ↓
BUSINESS INSIGHTS
```

The goal is not only to visualize data, but to build a complete analytical system that helps businesses understand **customers, products, revenue, profitability, churn, risk, and retention opportunities**.
