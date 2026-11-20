-- SELECT * FROM vw_InsuranceEROverview
DROP VIEW IF EXISTS vw_InsuranceEROverview;
CREATE VIEW vw_InsuranceEROverview
AS
    SELECT 
        department,
        insurance_type,
        COUNT(visit_id) as total_admissions,
        ROUND(AVG(wait_time_triage_min + wait_time_doctor_min),2)  As avg_doortodoc_wait_time,
        SUM(billed_amount_usd) as total_deptrevenue,
        ROUND((100.0* SUM(readmitted_30d)/COUNT(visit_id)),2) AS rate_of_readmission_30d,
        ROUND(AVG(satisfaction_score),2) AS avg_satisfaction_score
        FROM ed_patient_data
        GROUP BY department, insurance_type;