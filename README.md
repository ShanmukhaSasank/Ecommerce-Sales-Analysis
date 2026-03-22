# 🛒 E-Commerce Sales Performance Analysis

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-PostgreSQL-336791?logo=postgresql&logoColor=white)
![PowerBI](https://img.shields.io/badge/Power%20BI-4%20Page%20Dashboard-F2C811?logo=powerbi&logoColor=black)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)
![Records](https://img.shields.io/badge/Dataset-50%2C000%20Records-brightgreen)
![Status](https://img.shields.io/badge/Status-Complete-success)

---

## 📌 Overview

This project analyzes the sales performance of an e-commerce business across **2 years (January 2023 – December 2024)** to uncover revenue trends, category performance, regional distribution, channel effectiveness, and customer behavior. The goal is to support data-driven business decisions by combining Python EDA, SQL analytics, and an interactive Power BI dashboard.

---

## 🎯 Business Objectives

- Measure overall revenue, profit, and order performance across 50,000 transactions
- Identify the top revenue-generating and highest-margin product categories
- Detect seasonal trends and quantify the revenue spike during peak months
- Compare regional and channel performance to guide investment decisions
- Analyze customer segment behavior — spending patterns, return rates, and AOV
- Assess the impact of discounts on profit margins across discount bands

---

## 🗃️ Dataset

- **Source:** Synthetically generated e-commerce transactions (Indian market context)
- **Records:** 50,000 orders across 11,821 unique customers and 800 products
- **Period:** January 2023 – December 2024
- **Features include:** order date, category, sub-category, region, channel, customer segment, payment method, unit price, quantity, discount, revenue, profit, return status, shipping days, and customer rating

---

## 🛠️ Tools & Technologies

- **Python** (Pandas, NumPy, Matplotlib, Seaborn) for data cleaning, feature engineering, and EDA
- **PostgreSQL** for analytical SQL queries using CTEs, window functions, and business KPI calculations
- **Power BI Desktop** for interactive 4-page dashboard with 16 DAX measures and time intelligence
- **Power Query (M)** for data transformation and calculated column generation inside Power BI

---

## ⚙️ Project Workflow

1. Dataset generation with realistic seasonal patterns, discount bands, and customer segmentation
2. Data cleaning and feature engineering in Python — added Year, Month, Quarter, Year-Month, and Discount Band columns
3. Exploratory data analysis with 7 charts covering category, regional, channel, seasonal, and discount insights
4. Business-driven SQL analysis with 12 PostgreSQL queries calculating churn metrics, seasonal spikes, YoY growth, and revenue rankings
5. Power BI data model setup — `_Measures` table, `DateTable` with time intelligence, and relationship between order date and date table
6. 4-page Power BI dashboard built with 20+ visuals, dark theme, DAX measures, and formatted Indian currency values

---

## 📊 Dashboard Structure

### 📄 Page 1: Overview Dashboard
- Total Revenue, Total Profit, Total Orders, and Avg Order Value KPI cards
- Monthly Revenue Line Chart showing the full 2-year trend with clear Q4 spike
- Revenue vs Profit Clustered Bar Chart grouped by quarter
- Orders by Discount Band Donut Chart

### 📄 Page 2: Category Analysis
- Revenue by Category horizontal bar chart — Electronics dominates at 68%
- Profit Margin by Category vertical bar chart — Books leads at 54%
- Category Revenue Share donut chart
- Full Category Performance Matrix with data bars on revenue column

### 📄 Page 3: Regional Performance
- Total Revenue, Top Region, and Avg Order Value KPI cards
- Revenue by Region horizontal bar chart — East leads
- Regional Revenue Share donut chart
- Regional Matrix table with Revenue, Profit, Orders, AOV, and Margin %

### 📄 Page 4: Channel & Customer Segment
- Total Revenue, Mobile App Revenue, Return Rate, and Avg Order Value KPI cards
- Revenue by Channel horizontal bar — Mobile App is #1 at ₹41.8 Crore
- Revenue by Customer Segment vertical bar — Returning customers lead
- Payment Method Mix donut chart
- Return Rate by Customer Segment bar chart

---

## 💡 Key Insights

- **Electronics drives 68% of revenue** but carries the lowest margin (31.5%) — high-margin categories like Books (54%) are under-leveraged
- **Seasonal spike of 84.3%** between February (trough) and December (peak) — inventory and marketing must scale up by September every year
- **Mobile App is the #1 channel** with ₹41.8 Crore and 40% of all orders — app-first investment has the highest ROI
- **New customers spend the most per order** (AOV ₹21,859) while Returning customers generate the most total revenue (₹36.3 Crore)
- **Discounts do not erode margins** — profit margin stays at ~35.5% across all discount bands from 0% to 30%
- **Return rate is consistently ~12%** across all segments — representing ₹12.4 Crore in returned revenue annually, a key area for operational improvement

---

## ✅ Recommendations

- Increase marketing spend and inventory for Electronics in Q3 to capture Q4 demand
- Promote high-margin categories like Books and Beauty through targeted campaigns
- Invest in Mobile App UX improvements and app-exclusive offers to grow the leading channel
- Launch early-tenure loyalty programs targeting New customers to convert them into Returning customers
- Introduce a returns reduction initiative — reducing return rate by 2% recovers ~₹2 Crore annually
- Use discount campaigns freely as they do not hurt margins, especially in slower months (Jan–Mar)

---

## 📈 Outcome

This project demonstrates a complete end-to-end analytics workflow — from raw data generation and Python EDA to advanced SQL analysis and an executive-level Power BI dashboard — combining technical depth with clear business storytelling to support strategic decision-making for an e-commerce business.

---

## 👤 Author

**Shanmukha Sasank Nandula**
Data Analyst — Python · SQL · Power BI

- 🔗 LinkedIn: [linkedin.com/in/sasank-nandula](https://linkedin.com/in/sasank-nandula)
- 💻 GitHub: [github.com/ShanmukhaSasank](https://github.com/ShanmukhaSasank)
- 📧 Email: nandulashanmu123@gmail.com
