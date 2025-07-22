/*
@title: Trivial SQL on FHIR Example
@description: Demonstrating converting SQL to FHIR Library with basic annotations 
@version: 4.2.0
@status: active
@author: Clinical Informatics Team
@publisher: Regional Medical Center
*/

-- @relatedDependency: https://sql-on-fhir.org/ig/StructureDefinition/ViewDefinition/PatientDemographics
-- @relatedDependency: https://sql-on-fhir.org/ig/StructureDefinition/ViewDefinition/PatientAddresses
-- @param: city string
WITH RankedAddresses AS (
    SELECT 
        pd.*,
        pa.*,
        ROW_NUMBER() OVER (PARTITION BY pd.patient_id ORDER BY pa.address_id) AS address_rank
    FROM 
        patient_demographics pd
    JOIN 
        patient_addresses pa ON pd.patient_id = pa.patient_id
    WHERE 
        pd.age > 18
        AND pa.city = :city
)
