DROP VIEW  IF EXISTS vw_ExecutiveEROverview;
CREATE  VIEW vw_ExecutiveEROverview
AS
    SELECT department,COUNT(visit_id) AS total_admissions,
    ROUND(AVG(wait_time_doctor_min),2) AS avg_wait_time_doctor_min,
    ROUND(AVG(satisfaction_score),2) AS avg_satisfaction_score,
    ROUND((100.0*SUM(readmitted_30d)/COUNT(visit_id)),2) AS readmission_rate_30d,
    ROUND(SUM(billed_amount_usd),2) AS total_deptrevenue
    FROM ed_patient_data
    GROUP BY department;

