# PulseCommerce Analytics Platform

<div align="center">

> **Real-Time & Historical E-Commerce Analytics**

A portfolio-grade analytics platform that transforms Brazilian e-commerce transaction data into interactive business intelligence, while also supporting real-time order ingestion and monitoring.

**Python · Pandas · MySQL · FastAPI · Plotly Dash**

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Plotly Dash](https://img.shields.io/badge/Plotly%20Dash-Analytics-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://dash.plotly.com/)


<p align="center">
  <a href="#-dashboard-preview">
    <img src="https://img.shields.io/badge/📊%20Dashboard%20Preview-111827?style=for-the-badge&labelColor=0F172A&color=1E293B" alt="Dashboard Preview">
  </a>
  <a href="#-architecture">
    <img src="https://img.shields.io/badge/🏗️%20Architecture-111827?style=for-the-badge&labelColor=0F172A&color=1E293B" alt="Architecture">
  </a>
  <a href="#-getting-started">
    <img src="https://img.shields.io/badge/🚀%20Getting%20Started-111827?style=for-the-badge&labelColor=0F172A&color=1E293B" alt="Getting Started">
  </a>
</p>
</div>

---

<details>
<summary>
  <strong>📚 Explore PulseCommerce</strong>
</summary>

<br>

| Section | Explore |
| :--- | :--- |
| 📊 **Dashboard Preview** | [View Dashboard](#-dashboard-preview) |
| 🏗️ **Architecture** | [View Architecture](#-architecture) |
| 📦 **What the Platform Delivers** | [Explore](#-what-the-platform-delivers) |
| 📈 **Analytics Highlights** | [Explore](#-analytics-highlights) |
| 🧰 **Technology Stack** | [View Stack](#-technology-stack) |
| 🔄 **Data Pipeline** | [View Pipeline](#-data-pipeline) |
| 🗃️ **Dataset** | [View Dataset](#-dataset) |
| 🗂️ **Project Structure** | [View Structure](#-project-structure) |
| 🚀 **Getting Started** | [Get Started](#-getting-started) |
| ▶️ **Run the Platform** | [Run Platform](#-run-the-platform) |
| 🔌 **API Surface** | [View API](#-api-surface) |
| 🧪 **Data Quality** | [View Quality](#-data-quality) |
| 🧹 **Repository Hygiene** | [View Hygiene](#-repository-hygiene) |
| 🔮 **Future Extensions** | [Explore](#-future-extensions) |
| 👤 **Author** | [About](#-author) |

<br>

</details>

---

## ✦ Dashboard Preview

PulseCommerce is organized around five focused analytical experiences.

<details open>
<summary><strong>📊 Executive</strong></summary>

Business-level performance overview with revenue, orders, customer growth, AOV, order status, and historical trends.

![Executive Dashboard](docs/screenshots/executive.png)

</details>

<details open>
<summary><strong>👥 Customers</strong></summary>

Customer intelligence combining customer types, RFM segmentation, cohort retention, purchase behavior, and customer value.

![Customers Overview](docs/screenshots/customers-overview.png)

![Customer RFM Analysis](docs/screenshots/customers-rfm.png)

</details>

<details open>
<summary><strong>🛍️ Products</strong></summary>

Product and category performance across revenue, product contribution, units sold, pricing, and category distribution.

![Products Overview](docs/screenshots/products-overview.png)

![Product Analysis](docs/screenshots/products-analysis.png)

</details>

<details open>
<summary><strong>🌎 Regional</strong></summary>

Brazilian state-level performance with geographic distribution, revenue, orders, customers, units sold, and AOV.

![Regional Overview](docs/screenshots/regional-overview.png)

![Regional Analysis](docs/screenshots/regional-analysis.png)

</details>

<details open>
<summary><strong>⚡ Real-Time</strong></summary>

Live order monitoring powered by FastAPI and MySQL, including recent activity, incoming orders, and pipeline status.

![Real-Time Dashboard](docs/screenshots/realtime.png)

</details>

---

## 🏗️ Architecture

PulseCommerce uses two complementary pipelines that converge into a shared MySQL data layer and feed a unified Plotly Dash application.

![PulseCommerce Architecture](docs/architecture.png)

### Historical Pipeline

**Olist CSVs → Python/Pandas → Cleaning & Validation → MySQL → SQL/Python Analytics → Dashboard**

Historical workflows cover revenue, customers, RFM, cohorts, products, regions, orders, payments, reviews, delivery, sellers, and statistical analysis.

### Real-Time Pipeline

**Incoming Orders → FastAPI → SQLAlchemy/MySQL → Analytics Endpoints → Real-Time Dashboard**

The live workflow supports order ingestion with duplicate protection and analytics endpoints for current, recent, category, and state-level activity.

---

## 📦 What the Platform Delivers

| Area | Analytics |
| :--- | :--- |
| **📊 Executive** | Revenue, orders, customer growth, AOV, order status, delivery performance |
| **👥 Customers** | Customer types, RFM segmentation, cohort retention, purchase behavior |
| **🛍️ Products** | Category revenue, top products, units sold, pricing, product concentration |
| **🌎 Regional** | State revenue, orders, customers, units sold, AOV, geographic distribution |
| **⚡ Real-Time** | Order ingestion, recent orders, activity, pipeline status |
| **🧪 Data Quality** | Missing values, relationships, validation, business-field profiling |

<br>

All monetary values shown in the dashboard use **Brazilian Real (`R$`)**.

---

## 📈 Analytics Highlights

### 👥 Customer Intelligence

- RFM segmentation
- Cohort retention analysis
- Customer type analysis
- Purchase frequency
- Customer value analysis
- Returning vs. one-time customer behavior

### 🛒 Commercial Analytics

- Monthly revenue trends
- Revenue by product category
- Top products
- Units sold
- Average product price
- Order basket analysis
- Payment analysis

### 🌎 Regional Intelligence

- State-level revenue
- State-level order volume
- Customer distribution
- Units sold by state
- Average order value
- Geographic performance visualization

### ⚙️ Operational Analytics

- Review score analysis
- Delivery analysis
- Seller analysis
- Statistical analysis
- Real-time order monitoring

---

## 🧰 Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **🖥️ Frontend / BI** | Plotly Dash, Plotly |
| **⚡ Backend** | FastAPI, Pydantic |
| **🔗 Data Access** | SQLAlchemy, PyMySQL |
| **📊 Analytics** | Pandas, NumPy, SciPy |
| **📈 Visualization** | Plotly, Matplotlib, Seaborn |
| **🗄️ Database** | MySQL |
| **🐍 Language** | Python |
| **🌱 Environment** | Python virtual environment |

---

## 🔄 Data Pipeline

```text
┌───────────────────────┐
│   Olist Raw CSVs      │
│   9 source datasets   │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Python + Pandas       │
│ Cleaning & Validation │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Processed Analytical  │
│ Data                  │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│       MySQL           │
│ Historical + Live     │
│ Order Data            │
└───────┬─────────┬─────┘
        │         │
        ▼         ▼
┌────────────┐ ┌───────────────┐
│ SQL +      │ │ FastAPI       │
│ Python     │ │ Real-Time API │
│ Analytics  │ │ + Analytics   │
└──────┬─────┘ └───────┬───────┘
       │               │
       └───────┬───────┘
               ▼
      ┌──────────────────┐
      │   Plotly Dash    │
      │ Unified Dashboard│
      └──────────────────┘
```

---

## 🗃️ Dataset

Historical analysis uses the **[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)**.

The dataset contains approximately 100,000 orders from Olist Store and includes information covering orders, products, customers, payments, reviews, sellers, and Brazilian geolocation data.

The project works with nine source datasets:

- Customers
- Geolocation
- Orders
- Order Items
- Order Payments
- Order Reviews
- Products
- Sellers
- Product Category Name Translation

The raw dataset is intentionally excluded from Git because of its size.

Download the dataset from:

**[Download Olist Brazilian E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)**

After downloading and extracting the files, place the nine CSV files locally in:

```text
data/raw/olist/
```

Generated analytical datasets are stored in:

```text
data/processed/
```

Both directories are excluded from repository tracking.

---

## 🗂️ Project Structure

<details>
<summary><strong>Click to expand full folder tree</strong></summary>

```text
ecommerce-analytics-platform/
│
├── api/
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── routes/
│       ├── analytics.py
│       └── orders.py
│
├── dashboard/
│   ├── app.py
│   ├── plotly_theme.py
│   ├── assets/
│   ├── components/
│   └── pages/
│       ├── executive.py
│       ├── customers.py
│       ├── products.py
│       ├── regional.py
│       └── realtime.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│   ├── architecture.png
│   └── screenshots/
│
├── reports/
│   └── data_quality_report.csv
│
├── sql/
│   ├── 01_create_schema.sql
│   ├── 02_sales_analysis.sql
│   ├── 03_advanced_sales_analysis.sql
│   └── 04_realtime_schema.sql
│
├── src/
│   ├── analytics/
│   └── data/
│
├── .gitignore
├── requirements.txt
└── README.md
```

</details>

---

## 🚀 Getting Started

PulseCommerce is designed to be run from the repository root. The raw Olist dataset and generated analytical datasets are intentionally excluded from Git, so a fresh clone requires the dataset preparation steps below before the historical dashboard can load.

### Prerequisites

- **Python 3.x** — [Download Python](https://www.python.org/downloads/)
- **MySQL** — [Download MySQL Community Server](https://dev.mysql.com/downloads/mysql/)
- **Git** — [Download Git](https://git-scm.com/downloads)
- **Olist Brazilian E-Commerce Public Dataset** — [Download from Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

### 1. Clone the repository

Open PowerShell or a terminal and clone the repository:

```bash
git clone https://github.com/JAYSINH6094/ecommerce-analytics-platform.git
cd ecommerce-analytics-platform
```

All commands in the remaining setup steps should be run from this repository root.

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Verify that the virtual environment is active:

```powershell
python -c "import sys; print(sys.executable)"
```

The output should point to:

```text
ecommerce-analytics-platform\.venv\Scripts\python.exe
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure MySQL

Create the required MySQL database and configure the connection values expected by `api/database.py` in your local `.env` file.

Do not commit `.env`.

Database setup scripts are available in:

```text
sql/
```

### 5. Add the Olist dataset

Download the **[Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)** and extract the nine CSV files into:

```text
data/raw/olist/
```

The expected directory is:

```text
data/raw/olist/
├── olist_customers_dataset.csv
├── olist_geolocation_dataset.csv
├── olist_orders_dataset.csv
├── olist_order_items_dataset.csv
├── olist_order_payments_dataset.csv
├── olist_order_reviews_dataset.csv
├── olist_products_dataset.csv
├── olist_sellers_dataset.csv
└── product_category_name_translation.csv
```

The raw dataset is intentionally excluded from Git because of its size.

### 6. Prepare the data

From the repository root, run the data preparation pipeline:

```powershell
python src\prepare_data.py

```
### 7. Generate analytical datasets

Use the analytical workflows under:

```text
src/analytics/
```

to generate the analytical datasets consumed by the dashboard.

The dashboard expects generated files under:

```text
data/processed/
```


## ▶️ Run the Platform

PulseCommerce runs as two application processes: a FastAPI backend and a Plotly Dash dashboard.

### FastAPI Backend

From the repository root:

```powershell
uvicorn api.main:app --reload
```
The backend runs locally and provides real-time order ingestion and analytics endpoints.

Health check:

```text
GET /health
```

You can also open the API documentation at:

```text
http://127.0.0.1:8000/docs
```

### Plotly Dash Dashboard

Keep the FastAPI terminal running and open a **second terminal**.

Navigate to the repository root if necessary:

```powershell
cd ecommerce-analytics-platform
```

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Start the dashboard:

```powershell
python -m dashboard.app
```

The dashboard uses Dash Pages and loads the five views from:

```text
dashboard/pages/
```

The dashboard is typically available at:

```text
http://127.0.0.1:8050/
```

### Recommended Startup Order

For a fresh clone:

```text
Clone repository
      ↓
Create virtual environment
      ↓
Install dependencies
      ↓
Configure MySQL
      ↓
Download Olist dataset
      ↓
Place CSVs in data/raw/olist/
      ↓
Run data preparation workflows
      ↓
Generate analytical datasets
      ↓
Start FastAPI
      ↓
Start Plotly Dash
```

---

## 🔌 API Surface

The backend provides real-time order and analytics functionality.

<details>
<summary><strong>Click to expand API reference</strong></summary>

| Endpoint | Purpose |
| :--- | :--- |
| `POST /orders` | Ingest a real-time order |
| `GET /analytics/today` | Today's real-time analytics |
| `GET /analytics/recent` | Recent order/activity analytics |
| `GET /analytics/category` | Category-level analytics |
| `GET /analytics/state` | State-level analytics |
| `GET /health` | API health check |

</details>

The exact request and response schemas are defined in:

```text
api/schemas.py
```

---

## 🧪 Data Quality

The project includes dedicated data-quality workflows for:

- Missing-value analysis
- Relationship validation
- Data cleaning
- Processed-data validation
- Business-field profiling
- Final analytical validation

The generated report is available at:

```text
reports/data_quality_report.csv
```

---

## 🧹 Repository Hygiene

The repository intentionally excludes local and generated content:

<details>
<summary><strong>What's excluded from version control</strong></summary>

```text
.env
.venv/
.idea/
__pycache__/
data/raw/
data/processed/
```

</details>

This keeps Git focused on application source code, analytics logic, SQL, documentation, reports, and dashboard assets.

---

## 🔮 Future Extensions

Potential future work includes:

- Additional real-time operational metrics
- Customer lifetime-value analysis
- Expanded predictive analytics
- Automated data-quality monitoring
- Additional analytical storytelling views
- Deployment automation

---

## 👤 Author

**Jaysinh Thakor**
Computer Science & Engineering Graduate, Nirma University

GitHub: `JAYSINH6094`

---

<div align="center">

<sub>PulseCommerce Analytics Platform · E-Commerce Analytics with Python, MySQL, FastAPI & Plotly Dash</sub>

</div>