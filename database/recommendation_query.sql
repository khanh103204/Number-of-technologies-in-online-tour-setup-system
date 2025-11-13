SELECT 
    t.id,
    t.name,
    t.type,
    t.price,
    t.min_people,
    t.max_people,
    t.duration_days,
    t.difficulty,
    t.rating_avg,
    (
        (1 - ABS(t.price - 5000000) / 5000000) * 0.4 +
        (CASE 
            WHEN 4 BETWEEN t.min_people AND t.max_people THEN 1 
            ELSE 0.5 
         END) * 0.2 +
        (t.rating_avg / 5) * 0.3 +
        (CASE 
            WHEN t.duration_days <= 5 THEN 1 
            ELSE 0.7 
         END) * 0.1
    ) AS score
FROM tours t
WHERE t.available = TRUE
  AND t.type = 'biển'
  AND t.price <= 5000000 * 1.2
  AND t.max_people >= 4
ORDER BY score DESC
LIMIT 10;
