/*
@title: Hive SQL with Version Example
@description: Demonstrating SQL dialect with version annotation
@version: 1.0.0
@status: draft
@author: Data Engineering Team
@sqlDialect: hive
@dialectVersion: 3.1.2
*/

-- This is a Hive-specific query using HiveQL syntax with version 3.1.2 features
-- @relatedDependency: https://sql-on-fhir.org/ig/StructureDefinition/ViewDefinition/PatientDemographics
SELECT 
    patient_id,
    age,
    CASE 
        WHEN age < 18 THEN 'Minor'
        WHEN age BETWEEN 18 AND 65 THEN 'Adult'
        ELSE 'Senior'
    END as age_group,
    -- Using Hive 3.1+ features
    MAP('key1', value1, 'key2', value2) as metadata_map,
    ARRAY_CONTAINS(diagnosis_codes, 'I50.9') as has_heart_failure
FROM patient_demographics
WHERE 
    year = 2024
    AND month = 12
DISTRIBUTE BY patient_id
SORT BY age DESC;
