-- @title: Clinical Decision Support Library
-- @name: ClinicalDecisionSupport  
-- @description: Advanced clinical decision support queries with multiple dependencies
-- @version: 4.2.0
-- @status: active
-- @author: Clinical Informatics Team
-- @publisher: Regional Medical Center
-- @purpose: Support evidence-based clinical decision making
-- @date: 2024-07-21
-- @experimental: false

/*
@copyright: 2024 Regional Medical Center. All rights reserved.
@jurisdiction: US
@approvalDate: 2024-05-15
@lastReviewDate: 2024-07-18
@relatedDependency: Library/patient-risk-assessment
@relatedDependency: Library/medication-interactions
@relatedDependency: ValueSet/clinical-conditions
@relatedDependency: CodeSystem/lab-results
*/

-- @query_name: high_risk_patient_identification
-- @relatedDependency: Questionnaire/patient-assessment
-- @relatedDependency: Library/comorbidity-scoring
-- @performance_tier: high
-- @cache_duration: 15_minutes
-- @param: min_age integer
-- @param: risk_threshold integer

WITH risk_factors AS (
    SELECT 
        patient_id,
        age,
        diabetes_flag,
        hypertension_flag,
        heart_disease_flag,
        CASE 
            WHEN age > 65 THEN 2
            WHEN age > :min_age THEN 1
            ELSE 0
        END as age_risk_score
    FROM patient_demographics pd
    JOIN patient_conditions pc ON pd.patient_id = pc.patient_id
    WHERE age >= :min_age
),

-- @relatedDependency: ValueSet/critical-lab-values
-- @relatedDependency: Library/lab-interpretation-rules
lab_risk_indicators AS (
    SELECT 
        patient_id,
        MAX(CASE WHEN test_name = 'HbA1c' AND result_value > 9.0 THEN 3 ELSE 0 END) as diabetes_risk,
        MAX(CASE WHEN test_name = 'BP_SYSTOLIC' AND result_value > 160 THEN 2 ELSE 0 END) as bp_risk,
        MAX(CASE WHEN test_name = 'CHOLESTEROL' AND result_value > 240 THEN 1 ELSE 0 END) as cholesterol_risk
    FROM lab_results
    WHERE test_date >= DATE_SUB(CURRENT_DATE, INTERVAL 6 MONTH)
    GROUP BY patient_id
)

-- @output_format: clinical_alert
-- @relatedDependency: StructureDefinition/clinical-alert
SELECT 
    rf.patient_id,
    pd.first_name,
    pd.last_name,
    rf.age,
    (rf.age_risk_score + 
     COALESCE(lri.diabetes_risk, 0) + 
     COALESCE(lri.bp_risk, 0) + 
     COALESCE(lri.cholesterol_risk, 0)) as total_risk_score,
    CASE 
        WHEN (rf.age_risk_score + COALESCE(lri.diabetes_risk, 0) + 
              COALESCE(lri.bp_risk, 0) + COALESCE(lri.cholesterol_risk, 0)) >= :risk_threshold 
        THEN 'HIGH'
        WHEN (rf.age_risk_score + COALESCE(lri.diabetes_risk, 0) + 
              COALESCE(lri.bp_risk, 0) + COALESCE(lri.cholesterol_risk, 0)) >= 3 
        THEN 'MEDIUM'
        ELSE 'LOW'
    END as risk_category
FROM risk_factors rf
JOIN patient_demographics pd ON rf.patient_id = pd.patient_id
LEFT JOIN lab_risk_indicators lri ON rf.patient_id = lri.patient_id
WHERE rf.age_risk_score > 0 OR lri.diabetes_risk > 0 OR lri.bp_risk > 0 OR lri.cholesterol_risk > 0
ORDER BY total_risk_score DESC;

/*
@query_name: medication_interaction_check
@security_level: PHI
@relatedDependency: Library/drug-interaction-rules
@relatedDependency: ValueSet/high-risk-medications
@relatedDependency: CodeSystem/medication-codes
@audit_required: true
@param: patient_id string
@param: include_inactive boolean
*/

-- Check for potentially dangerous drug interactions
SELECT DISTINCT
    pm1.patient_id,
    pm1.medication_name as medication_1,
    pm2.medication_name as medication_2,
    dir.interaction_severity,
    dir.clinical_significance,
    dir.recommended_action
FROM patient_medications pm1
JOIN patient_medications pm2 ON pm1.patient_id = pm2.patient_id 
    AND pm1.medication_id < pm2.medication_id  -- Avoid duplicate pairs
JOIN drug_interaction_rules dir ON (
    (dir.drug_1_code = pm1.medication_code AND dir.drug_2_code = pm2.medication_code) OR
    (dir.drug_1_code = pm2.medication_code AND dir.drug_2_code = pm1.medication_code)
)
WHERE pm1.status = 'ACTIVE' 
    AND pm2.status = 'ACTIVE'
    AND dir.interaction_severity IN ('HIGH', 'CRITICAL')
    AND pm1.patient_id = :patient_id;  -- Parameter for specific patient
