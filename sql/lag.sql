-- The actual query, using 'pdo_prices' and ordered by most recent date descending
WITH PriceChangeLag AS (
    -- Identify when the price changes compared to the previous day
    SELECT
        date,
        price,
        LAG(price, 1, NULL) OVER (ORDER BY date) AS previous_price,
        -- Flag rows where the price is different from the previous day (start of a new price period)
        CASE
            WHEN price != LAG(price, 1, NULL) OVER (ORDER BY date) THEN 1
            WHEN LAG(price, 1, NULL) OVER (ORDER BY date) IS NULL THEN 1 -- Treat the very first row as a change
            ELSE 0
        END AS price_change_flag
    FROM
        pdo_prices -- Using the specified table name
),
PriceGroup AS (
    -- Assign a unique group ID to each consecutive period of the same price
    SELECT
        date,
        price,
        -- The SUM window function creates a running total of the price_change_flag,
        -- effectively assigning a unique ID to each block of consecutive same-priced days.
        SUM(price_change_flag) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS price_period_id
    FROM
        PriceChangeLag
),
PeriodStats AS (
    -- Calculate stats for each price period: the end date and the count of days
    SELECT
        price,
        price_period_id,
        MAX(date) AS period_end_date,
        COUNT(*) AS days_at_this_price
    FROM
        PriceGroup
    GROUP BY
        price,
        price_period_id
),
RankedPeriods AS (
    -- For each price, rank its periods by end date (most recent first)
    SELECT
        price,
        period_end_date,
        days_at_this_price,
        ROW_NUMBER() OVER (PARTITION BY price ORDER BY period_end_date DESC) as rn
    FROM
        PeriodStats
)
-- Final Selection: Choose the most recent period (rn=1) for each price
SELECT
    period_end_date AS most_recent_date,
    price,
    days_at_this_price
FROM
    RankedPeriods
WHERE
    rn = 1
ORDER BY
    most_recent_date DESC; -- ****** ORDERING UPDATED HERE ******
