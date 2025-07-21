/*
@title: PostgreSQL Analytics Query
@description: Using PostgreSQL-specific features for patient analytics
@version: 1.3.2
@status: active
@author: Database Analytics Team
@publisher: Regional Medical Center
@sqlDialect: postgres
@relatedDependency: Library/patient-demographics
@relatedDependency: Library/encounter-summaries
*/

-- PostgreSQL-specific query using advanced features
WITH RECURSIVE patient_hierarchy AS (
    -- Base case: top-level patients
    SELECT 
        patient_id,
        primary_care_provider_id,
        1 as level,
        ARRAY[patient_id] as path
    FROM patients 
    WHERE primary_care_provider_id IS NULL
    
    UNION ALL
    
    -- Recursive case: patients under other providers
    SELECT 
        p.patient_id,
        p.primary_care_provider_id,
        ph.level + 1,
        ph.path || p.patient_id
    FROM patients p
    INNER JOIN patient_hierarchy ph 
        ON p.primary_care_provider_id = ph.patient_id
    WHERE NOT (p.patient_id = ANY(ph.path))  -- Prevent cycles
),
aggregated_stats AS (
    SELECT 
        ph.patient_id,
        ph.level,
        count(*) OVER (PARTITION BY ph.level) as patients_at_level,
        jsonb_agg(
            jsonb_build_object(
                'encounter_id', e.encounter_id,
                'encounter_date', e.encounter_date,
                'diagnosis_codes', e.diagnosis_codes::jsonb
            )
        ) as encounters_json,
        -- PostgreSQL-specific window function with FILTER
        count(*) FILTER (WHERE e.encounter_date >= NOW() - INTERVAL '30 days') 
            OVER (PARTITION BY ph.patient_id) as recent_encounters
    FROM patient_hierarchy ph
    LEFT JOIN encounters e ON ph.patient_id = e.patient_id
    GROUP BY ph.patient_id, ph.level, e.encounter_id, e.encounter_date, e.diagnosis_codes
)
SELECT 
    patient_id,
    level,
    patients_at_level,
    encounters_json,
    recent_encounters,
    -- PostgreSQL array functions
    array_length(path, 1) as hierarchy_depth,
    -- PostgreSQL-specific date functions
    EXTRACT(EPOCH FROM NOW() - created_at)::int as seconds_since_creation
FROM aggregated_stats
WHERE encounters_json IS NOT NULL
ORDER BY level, patient_id
LIMIT 1000;
