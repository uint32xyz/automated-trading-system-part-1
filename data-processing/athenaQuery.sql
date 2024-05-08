
WITH 

last_updated as (
    SELECT *, 
        -- These partitions are the year/month/day/hour we specified in our S3 file name
        -- Each partition is converted to a queryable column in our table
        -- We cast them from integers to strings(VARCHAR), concatenate and convert to timestamp
        CAST(
            CAST(partition_0 AS VARCHAR) || '-' || 
            CAST(partition_1 AS VARCHAR) || '-' || 
            CAST(partition_2 AS VARCHAR) || ' ' || 
            CAST(partition_3 AS VARCHAR) || ':00:00' AS TIMESTAMP
        ) AS date_time
    FROM latest
    -- WHERE symbol = 'ETH' AND name = 'Ethereum' -- specify the token data you want here
),



main AS (
    SELECT DISTINCT
        c1.name as name,
        c1.symbol as symbol,
        c1.cmc_rank,
        c1.num_market_pairs,
        c1.price as price,
        c1.volume_24h as volume,
        c1.volume_change_24h,
        c1.percent_change_24h as percent_change_24h,
        c1.percent_change_7d as percent_change_7d,
        c2.percent_change_7d as y_percentage_change7d, 
        -- Calculate the price change 
        (CAST(c2.price AS DECIMAL(30,15)) - CAST(c1.price AS DECIMAL(30,15))) / CAST(c1.price AS DECIMAL(30,15)) * 100 AS cal_price_change,
        date_parse(c1.timestamp, '%Y-%m-%dT%H:%i:%s') as timestamp
    FROM last_updated c1 
    -- Join where the date is n days ahead 
    INNER JOIN last_updated c2
        ON  c1.partition_0 = c2.partition_0
        AND c1.partition_1 = c2.partition_1  
        AND c1.partition_3 = c2.partition_3  
        AND (date_add('day', 5, c1.date_time)) = c2.date_time
        AND c1.symbol = c2.symbol
        AND c1.name = c2.name
        -- Just filter our some outliers
        AND CAST(c1.percent_change_7d as decimal) <= 1000
        AND CAST(c1.volume_change_24h as decimal) <= 1000
        -- limit to top 1000
        AND c1.cmc_rank <= 1000
), 

classify AS (
SELECT 
    *,
    -- We assign 1 if the price goes up by more than 10% 
    CASE WHEN cal_price_change <= 10 THEN 0 ELSE 1 END as y
FROM main
), 

SELECT * FROM classify

