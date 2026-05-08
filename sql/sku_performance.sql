-- SKU performance with placement correlation
-- Run in Looker Studio or psql

SELECT
    s.sku_id,
    s.sku_name,
    s.category,
    SUM(d.units_sold)                                         AS total_units,
    SUM(d.revenue)                                            AS total_revenue,
    AVG(d.sell_through_rate)                                  AS avg_sell_through,
    AVG(d.days_of_supply)                                     AS avg_days_supply,
    p.shelf_location,
    p.placement_type,                                         -- endcap / eye_level / bottom
    SUM(d.revenue) / NULLIF(SUM(d.shelf_sqft), 0)            AS revenue_per_sqft,
    LAG(SUM(d.revenue), 7) OVER (
        PARTITION BY s.sku_id ORDER BY d.date
    )                                                         AS revenue_7d_ago,
    (SUM(d.revenue) - LAG(SUM(d.revenue), 7) OVER (
        PARTITION BY s.sku_id ORDER BY d.date
    )) / NULLIF(LAG(SUM(d.revenue), 7) OVER (
        PARTITION BY s.sku_id ORDER BY d.date
    ), 0) * 100                                               AS wow_pct_change

FROM sku_daily d
JOIN skus s          ON s.sku_id = d.sku_id
JOIN placements p    ON p.sku_id = d.sku_id AND p.date = d.date

WHERE d.date >= CURRENT_DATE - INTERVAL '30 days'

GROUP BY s.sku_id, s.sku_name, s.category, p.shelf_location, p.placement_type, d.date
ORDER BY total_revenue DESC;
