-- Refactored and smaller query for DuckDB
WITH GroupIdentifier AS (
    -- Create a unique identifier for each consecutive block of the same price.
    -- The difference between a general row number and a row number partitioned by price
    -- remains constant within each consecutive block.
    SELECT
        date,
        price,
        ROW_NUMBER() OVER (ORDER BY date) - ROW_NUMBER() OVER (PARTITION BY price ORDER BY date) AS grp
    FROM
        pdo_prices -- Using the specified table name
),
PeriodStats AS (
    -- Calculate stats for each identified price period (block)
    SELECT
        price,
      -- grp, -- Grouping identifier, not needed in final output
        MAX(date) AS period_end_date,
        COUNT(*) AS days_at_this_price
    FROM
        GroupIdentifier
    GROUP BY
        price,
        grp -- Group by price and the block identifier
)
-- Final Selection using QUALIFY
SELECT
    period_end_date AS most_recent_date,
    price,
    days_at_this_price
FROM
    PeriodStats
-- QUALIFY filters the results of a window function *after* aggregation.
-- Here, we keep only the latest period (highest period_end_date) for each price.
QUALIFY ROW_NUMBER() OVER (PARTITION BY price ORDER BY period_end_date DESC) = 1
ORDER BY
    most_recent_date DESC; -- Final ordering as requested
