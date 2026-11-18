DROP VIEW IF EXISTS vw_PhysicianEffeciancyOverview;
CREATE VIEW vw_PhysicianEffeciancyOverview
AS
    WITH ctePhysiciansGeneralEmergency AS(
        SELECT DISTINCT 
        attending_physician,
        ROUND(AVG(wait_time_doctor_min),2) As physician_wait_time,
        ROUND(AVG(satisfaction_score),2) As physician_satisfaction_score,
        ROUND(100.0 * SUM(readmitted_30d)/COUNT(visit_id),2) AS readmission_rate_30d,
        COUNT(visit_id) AS patient_volume
        FROM ed_patient_data
        WHERE triage_level IN (3, 4, 5)
        GROUP BY attending_physician
    ),
    ctePhysiciansCriticalEmergency AS(
        SELECT DISTINCT 
        attending_physician,
        ROUND(AVG(wait_time_doctor_min),2) As physician_critical_wait_time,
        ROUND(AVG(satisfaction_score),2) As physician_critical_satisfaction_score,
        ROUND(100.0 * SUM(readmitted_30d)/COUNT(visit_id),2) AS critical_readmission_rate_30d,
        COUNT(visit_id) AS critical_patient_volume
        FROM ed_patient_data
        WHERE triage_level IN (1,2)
        GROUP BY attending_physician
    )
    SELECT 
        ge.attending_physician,
        ge.physician_wait_time,
        cr.physician_critical_wait_time,
        ge.physician_satisfaction_score,
        cr.physician_critical_satisfaction_score,
        ge.readmission_rate_30d,
        cr.critical_readmission_rate_30d,
        ge.patient_volume,
        cr.critical_patient_volume
    FROM ctePhysiciansGeneralEmergency ge
    JOIN ctePhysiciansCriticalEmergency cr
    ON ge.attending_physician=cr.attending_physician;
