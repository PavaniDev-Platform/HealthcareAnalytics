/*
    Demographic Overview By Age Group:
        ---Admissions
        ---Satisfaction
        ---Readmission 
        ---Chief Complaint
    SELECT * FROM vw_ChiefComplaintPerAgeGroup
    SELECT * FROM vw_DemographicsByAgeEROverview
*/
DROP VIEW IF EXISTS vw_DemographicsByAgeEROverview;
CREATE VIEW vw_DemographicsByAgeEROverview
AS
   WITH cteCriticalEmergencyByAgePrepared AS (
    SELECT 
        department, 
        patient_age,
        COUNT(visit_id) AS critical_admissions,
        SUM(readmitted_30d) AS critical_readmission_30d,
        SUM(satisfaction_score) AS critical_satisfaction_score
    FROM ed_patient_data
    WHERE triage_level IN (1, 2)
    GROUP BY patient_age, department
), 
cteGeneralEmergencyBYAgePrepared AS (
    SELECT 
        department, 
        patient_age,
        COUNT(visit_id) AS number_0f_admissions,
        SUM(readmitted_30d) AS readmission_30d,
        SUM(satisfaction_score) AS satisfaction_score
    FROM ed_patient_data
    WHERE triage_level IN (3, 4, 5)
    GROUP BY patient_age, department
)        
SELECT 
    gen.department, 
    gen.patient_age,
    gen.number_0f_admissions,
    COALESCE(cr.critical_admissions, 0) AS critical_admissions,
    gen.readmission_30d,
    COALESCE(cr.critical_readmission_30d, 0) AS critical_readmission_30d,
    gen.satisfaction_score,
    COALESCE(cr.critical_satisfaction_score, 0) AS critical_satisfaction_score 
FROM cteGeneralEmergencyBYAgePrepared gen
LEFT JOIN cteCriticalEmergencyByAgePrepared cr
    ON gen.department = cr.department 
    AND gen.patient_age = cr.patient_age;