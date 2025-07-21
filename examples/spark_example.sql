/*
@title: Spark SQL Example
@description: Demonstrating SQL dialect annotation with Spark
@version: 2.1.0
@status: active
@author: Analytics Team
@sqlDialect: spark
@relatedDependency: hdfs://data-lake/schemas/patient_schema.json
*/

-- Spark SQL specific syntax with window functions
WITH patient_metrics AS (
    SELECT 
        patient_id,
        visit_date,
        diagnosis_code,
        lag(visit_date, 1) OVER (
            PARTITION BY patient_id 
            ORDER BY visit_date
        ) as prev_visit_date,
        datediff(visit_date, lag(visit_date, 1) OVER (
            PARTITION BY patient_id 
            ORDER BY visit_date
        )) as days_between_visits
    FROM patient_visits
    WHERE visit_date >= current_date() - INTERVAL 1 YEAR
)
SELECT 
    patient_id,
    count(*) as visit_count,
    avg(days_between_visits) as avg_days_between_visits,
    collect_list(diagnosis_code) as diagnosis_codes
FROM patient_metrics
GROUP BY patient_id
HAVING count(*) > 2;
