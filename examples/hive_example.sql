/*
@title: Hive SQL Example
@description: Demonstrating SQL dialect annotation with Hive
@version: 1.0.0
@status: draft
@author: Data Engineering Team
@sqlDialect: hive
*/

-- This is a Hive-specific query using HiveQL syntax
-- @relatedDependency: https://sql-on-fhir.org/ig/StructureDefinition/ViewDefinition/PatientDemographics
SELECT 
    patient_id,
    age,
    CASE 
        WHEN age < 18 THEN 'Minor'
        WHEN age BETWEEN 18 AND 65 THEN 'Adult'
        ELSE 'Senior'
    END as age_group,
    regexp_extract(phone, '\\d{3}-(\\d{3})-(\\d{4})', 0) as formatted_phone
FROM patient_demographics
WHERE 
    year = 2024
    AND month = 12
DISTRIBUTE BY patient_id
SORT BY age DESC;
