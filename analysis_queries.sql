-- ============================================================
-- E-Commerce Sales Performance Analysis
-- Author  : Shanmukha Sasank Nandula
-- DB      : PostgreSQL 14+
-- Dataset : ecommerce_sales (50,000 rows)
-- GitHub  : github.com/ShanmukhaSasank
-- ============================================================

-- ── TABLE SETUP ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ecommerce_sales (
    order_id         VARCHAR(20)   PRIMARY KEY,
    order_date       DATE          NOT NULL,
    customer_id      VARCHAR(20)   NOT NULL,
    product_id       VARCHAR(20)   NOT NULL,
    category         VARCHAR(50)   NOT NULL,
    sub_category     VARCHAR(50),
    region           VARCHAR(20)   NOT NULL,
    channel          VARCHAR(30)   NOT NULL,
    customer_segment VARCHAR(20)   NOT NULL,
    payment_method   VARCHAR(20)   NOT NULL,
    unit_price       NUMERIC(12,2),
    quantity         INT,
    discount_pct     NUMERIC(5,2),
    revenue          NUMERIC(14,2) NOT NULL,
    profit           NUMERIC(14,2) NOT NULL,
    is_returned      SMALLINT      DEFAULT 0,
    return_reason    VARCHAR(50),
    shipping_days    INT,
    rating           NUMERIC(3,1)
);

-- Load CSV (update path as needed):
-- COPY ecommerce_sales FROM '/path/to/ecommerce_sales.csv'
-- DELIMITER ',' CSV HEADER;


-- ============================================================
-- QUERY 1: Headline KPI Summary
-- ============================================================
SELECT
    COUNT(*)                                                AS total_orders,
    ROUND(SUM(revenue),        2)                           AS total_revenue,
    ROUND(SUM(profit),         2)                           AS total_profit,
    ROUND(AVG(revenue),        2)                           AS avg_order_value,
    ROUND(SUM(profit) /
          NULLIF(SUM(revenue), 0) * 100, 2)                 AS profit_margin_pct,
    ROUND(AVG(is_returned)     * 100, 2)                    AS return_rate_pct,
    ROUND(AVG(rating),         2)                           AS avg_rating,
    COUNT(DISTINCT customer_id)                             AS unique_customers,
    COUNT(DISTINCT product_id)                              AS unique_products
FROM ecommerce_sales;


-- ============================================================
-- QUERY 2: Revenue & Profit by Category
-- ============================================================
WITH total AS (
    SELECT SUM(revenue) AS grand_total FROM ecommerce_sales
)
SELECT
    category,
    COUNT(*)                                                AS orders,
    ROUND(SUM(revenue), 2)                                  AS total_revenue,
    ROUND(SUM(profit),  2)                                  AS total_profit,
    ROUND(SUM(profit) /
          NULLIF(SUM(revenue), 0) * 100, 1)                 AS profit_margin_pct,
    ROUND(SUM(revenue) / t.grand_total * 100, 1)            AS revenue_share_pct,
    ROUND(AVG(revenue), 2)                                  AS avg_order_value
FROM ecommerce_sales, total t
GROUP BY category, t.grand_total
ORDER BY total_revenue DESC;


-- ============================================================
-- QUERY 3: Monthly Revenue Trend + YoY Growth
-- ============================================================
WITH monthly AS (
    SELECT
        DATE_TRUNC('month', order_date)        AS month_start,
        EXTRACT(YEAR  FROM order_date)::INT    AS yr,
        EXTRACT(MONTH FROM order_date)::INT    AS mo,
        SUM(revenue)                           AS monthly_revenue,
        COUNT(*)                               AS orders
    FROM ecommerce_sales
    GROUP BY 1, 2, 3
),
with_lag AS (
    SELECT *,
        LAG(monthly_revenue)
            OVER (PARTITION BY mo ORDER BY yr) AS prev_yr_revenue
    FROM monthly
)
SELECT
    TO_CHAR(month_start, 'YYYY-MM')                         AS year_month,
    yr,
    mo,
    ROUND(monthly_revenue, 2)                               AS revenue,
    orders,
    ROUND((monthly_revenue - prev_yr_revenue)
          / NULLIF(prev_yr_revenue, 0) * 100, 1)            AS yoy_growth_pct
FROM with_lag
ORDER BY month_start;


-- ============================================================
-- QUERY 4: Seasonal Spike Detection
-- ============================================================
WITH monthly_totals AS (
    SELECT
        EXTRACT(MONTH FROM order_date)::INT    AS month_num,
        TO_CHAR(order_date, 'Month')           AS month_name,
        DATE_TRUNC('month', order_date)        AS month_start,
        SUM(revenue)                           AS monthly_rev
    FROM ecommerce_sales
    GROUP BY 1, 2, 3
),
avg_by_month AS (
    SELECT
        month_num,
        TRIM(month_name)                       AS month_name,
        ROUND(AVG(monthly_rev), 2)             AS avg_monthly_revenue
    FROM monthly_totals
    GROUP BY month_num, month_name
),
ranked AS (
    SELECT *,
        RANK() OVER (ORDER BY avg_monthly_revenue DESC) AS rnk_desc,
        RANK() OVER (ORDER BY avg_monthly_revenue ASC)  AS rnk_asc
    FROM avg_by_month
)
SELECT
    MAX(CASE WHEN rnk_desc = 1 THEN month_name        END) AS peak_month,
    MAX(CASE WHEN rnk_desc = 1 THEN avg_monthly_revenue END) AS peak_avg_revenue,
    MAX(CASE WHEN rnk_asc  = 1 THEN month_name        END) AS trough_month,
    MAX(CASE WHEN rnk_asc  = 1 THEN avg_monthly_revenue END) AS trough_avg_revenue,
    ROUND(
        (MAX(CASE WHEN rnk_desc = 1 THEN avg_monthly_revenue END)
       - MAX(CASE WHEN rnk_asc  = 1 THEN avg_monthly_revenue END))
      / NULLIF(MAX(CASE WHEN rnk_asc = 1
                        THEN avg_monthly_revenue END), 0) * 100, 1
    )                                                       AS seasonal_spike_pct
FROM ranked;


-- ============================================================
-- QUERY 5: Regional Performance
-- ============================================================
SELECT
    region,
    COUNT(*)                                               AS orders,
    ROUND(SUM(revenue),  2)                                AS total_revenue,
    ROUND(SUM(profit),   2)                                AS total_profit,
    ROUND(AVG(revenue),  2)                                AS avg_order_value,
    ROUND(SUM(profit) /
          NULLIF(SUM(revenue), 0) * 100, 1)                AS profit_margin_pct,
    ROUND(AVG(is_returned) * 100, 1)                       AS return_rate_pct
FROM ecommerce_sales
GROUP BY region
ORDER BY total_revenue DESC;


-- ============================================================
-- QUERY 6: Sub-category Drill-down (Top 5 per Category)
-- ============================================================
WITH ranked AS (
    SELECT
        category,
        sub_category,
        ROUND(SUM(revenue), 2)                             AS total_revenue,
        COUNT(*)                                           AS orders,
        ROUND(SUM(profit) /
              NULLIF(SUM(revenue), 0) * 100, 1)            AS margin_pct,
        RANK() OVER (PARTITION BY category
                     ORDER BY SUM(revenue) DESC)           AS rnk
    FROM ecommerce_sales
    GROUP BY category, sub_category
)
SELECT category, sub_category, total_revenue, orders, margin_pct
FROM ranked
WHERE rnk <= 5
ORDER BY category, rnk;


-- ============================================================
-- QUERY 7: Channel & Payment Method Mix
-- ============================================================
SELECT
    channel,
    payment_method,
    COUNT(*)                                               AS orders,
    ROUND(SUM(revenue), 2)                                 AS revenue,
    ROUND(AVG(revenue), 2)                                 AS avg_order_value,
    ROUND(AVG(is_returned) * 100, 1)                       AS return_rate_pct
FROM ecommerce_sales
GROUP BY channel, payment_method
ORDER BY channel, revenue DESC;


-- ============================================================
-- QUERY 8: Customer Segment Analysis
-- ============================================================
SELECT
    customer_segment,
    COUNT(DISTINCT customer_id)                            AS unique_customers,
    COUNT(*)                                               AS total_orders,
    ROUND(SUM(revenue), 2)                                 AS total_revenue,
    ROUND(AVG(revenue), 2)                                 AS avg_order_value,
    ROUND(AVG(is_returned) * 100, 1)                       AS return_rate_pct,
    ROUND(AVG(rating), 2)                                  AS avg_rating
FROM ecommerce_sales
GROUP BY customer_segment
ORDER BY total_revenue DESC;


-- ============================================================
-- QUERY 9: Discount Band Impact on Revenue & Margin
-- ============================================================
SELECT
    CASE
        WHEN discount_pct = 0       THEN '1 - No Discount'
        WHEN discount_pct <= 0.10   THEN '2 - 1% to 10%'
        WHEN discount_pct <= 0.20   THEN '3 - 11% to 20%'
        WHEN discount_pct <= 0.30   THEN '4 - 21% to 30%'
        ELSE                             '5 - 30%+'
    END                                                    AS discount_band,
    COUNT(*)                                               AS orders,
    ROUND(SUM(revenue),  2)                                AS total_revenue,
    ROUND(SUM(profit),   2)                                AS total_profit,
    ROUND(SUM(profit) /
          NULLIF(SUM(revenue), 0) * 100, 1)                AS profit_margin_pct,
    ROUND(AVG(revenue),  2)                                AS avg_order_value
FROM ecommerce_sales
GROUP BY discount_band
ORDER BY discount_band;


-- ============================================================
-- QUERY 10: Product Return Analysis
-- ============================================================
SELECT
    category,
    return_reason,
    COUNT(*)                                               AS returned_orders,
    ROUND(SUM(revenue), 2)                                 AS revenue_at_risk,
    ROUND(COUNT(*) * 100.0
          / SUM(COUNT(*)) OVER (PARTITION BY category), 1) AS pct_of_cat_returns
FROM ecommerce_sales
WHERE is_returned = 1
  AND return_reason IS NOT NULL
  AND return_reason <> ''
GROUP BY category, return_reason
ORDER BY category, returned_orders DESC;


-- ============================================================
-- QUERY 11: Top 10 Revenue-Generating Customers
-- ============================================================
SELECT
    customer_id,
    customer_segment,
    COUNT(*)                                               AS total_orders,
    ROUND(SUM(revenue), 2)                                 AS total_revenue,
    ROUND(AVG(revenue), 2)                                 AS avg_order_value,
    ROUND(AVG(rating),  2)                                 AS avg_rating,
    SUM(is_returned)                                       AS total_returns
FROM ecommerce_sales
GROUP BY customer_id, customer_segment
ORDER BY total_revenue DESC
LIMIT 10;


-- ============================================================
-- QUERY 12: Quarterly Revenue with Running Total
-- ============================================================
SELECT
    TO_CHAR(DATE_TRUNC('quarter', order_date),
            'YYYY-"Q"Q')                                   AS quarter,
    COUNT(*)                                               AS orders,
    ROUND(SUM(revenue), 2)                                 AS quarterly_revenue,
    ROUND(SUM(profit),  2)                                 AS quarterly_profit,
    ROUND(
        SUM(revenue) / NULLIF(
            SUM(SUM(revenue)) OVER (
                PARTITION BY EXTRACT(YEAR FROM order_date)
                ORDER BY DATE_TRUNC('quarter', order_date)
            ), 0) * 100, 1
    )                                                      AS pct_of_year_revenue,
    ROUND(
        SUM(SUM(revenue)) OVER (
            ORDER BY DATE_TRUNC('quarter', order_date)
        ), 2
    )                                                      AS running_total
FROM ecommerce_sales
GROUP BY DATE_TRUNC('quarter', order_date),
         EXTRACT(YEAR FROM order_date)
ORDER BY DATE_TRUNC('quarter', order_date);
