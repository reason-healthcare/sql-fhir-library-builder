/*
@title: PostgreSQL 15 Advanced Features
@description: Demonstrating PostgreSQL-specific features with version 15
@version: 2.0.0
@status: active
@author: Database Team
@sqlDialect: postgres
@dialectVersion: 15.4
*/

-- PostgreSQL 15.4 specific query using advanced features
-- @relatedDependency: Library/patient-base-tables

-- Using PostgreSQL 15+ MERGE statement (SQL standard)
WITH patient_updates AS (
    SELECT patient_id, updated_demographics
    FROM staging.patient_changes
    WHERE processed_date = CURRENT_DATE
)
SELECT 
    p.patient_id,
    p.first_name,
    p.last_name,
    -- JSON operations (PostgreSQL specialty)
    p.metadata->>'provider_id' as provider_id,
    JSONB_PATH_EXISTS(p.metadata, '$.allergies[*] ? (@.severity == "severe")') as has_severe_allergies,
    -- Window function with RANGE
    AVG(p.age) OVER (
        ORDER BY p.birth_date 
        RANGE BETWEEN INTERVAL '5 years' PRECEDING 
                  AND INTERVAL '5 years' FOLLOWING
    ) as age_cohort_average
FROM patients p
LEFT JOIN patient_updates pu ON p.patient_id = pu.patient_id
WHERE p.active = true
ORDER BY p.patient_id;
