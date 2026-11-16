/*
 PRAGMA table_info(ed_patient_data)
 SELECT * FROM vw_OperationEROverview
 Which departments are the busiest?
      --Departments attending highest number of critical emergency(triage_level=critical or 1)
    Which departments are understaffed or over staffed?
     ---Patients attended single doctor
    Average Length of stay of patients in each emergency department

*/
DROP VIEW IF EXISTS vw_OperationEROverview;
CREATE VIEW vw_OperationEROverview
AS
    -- 1. Critical cases (Triage 1 & 2)
    WITH cteCriticalEmergencyPrepared AS (
        SELECT department,
        COUNT(DISTINCT attending_physician) AS criticalcare_physicians,
        COUNT(patient_id) AS number_of_critical_admissions,
        ROUND(AVG(wait_time_triage_min), 2) AS avg_critical_wait_time_triage_min,
        ROUND(AVG(length_of_stay_hrs), 2) AS avg_critical_length_of_stay_hrs,
        ROUND(AVG(satisfaction_score), 2) AS critical_satisfaction_score
        FROM ed_patient_data
        WHERE triage_level IN (1, 2)
        GROUP BY department
    ),
    -- 2. General cases (Triage 3, 4, & 5)
    cteGeneralEmergencyPrepared AS (
        SELECT department,
        COUNT(DISTINCT attending_physician) AS general_physicians,
        COUNT(patient_id) AS number_of_admissions,
        ROUND(AVG(length_of_stay_hrs), 2) AS avg_length_of_stay_hrs,
        ROUND(AVG(wait_time_triage_min), 2) AS avg_wait_time_triage_min,
        ROUND(AVG(satisfaction_score), 2) AS satisfaction
        FROM ed_patient_data
        WHERE triage_level IN (3, 4, 5)
        GROUP BY department 
    ),
    -- 3. Overall metrics across ALL triage levels (1 through 5)
    cteOverallEmergencyPrepared AS (
        SELECT department,
        COUNT(patient_id) AS total_admissions,
        ROUND(AVG(wait_time_triage_min), 2) AS total_avg_wait_time_triage_min,
        ROUND(AVG(satisfaction_score), 2) AS total_avg_satisfaction_score
        FROM ed_patient_data
        WHERE triage_level BETWEEN 1 AND 5
        GROUP BY department
    )
    SELECT 
        PD.department,
        -- Physician counts
        PD.general_physicians,
        Tr.criticalcare_physicians,
        
        -- Admissions breakdown & Overall total
        PD.number_of_admissions,
        Tr.number_of_critical_admissions,
        O.total_admissions,
        
        -- Wait times breakdown & Overall average
        PD.avg_wait_time_triage_min,
        Tr.avg_critical_wait_time_triage_min,
        O.total_avg_wait_time_triage_min,
        
        -- Length of stay
        PD.avg_length_of_stay_hrs,
        Tr.avg_critical_length_of_stay_hrs,
        
        -- Satisfaction breakdown & Overall average
        PD.satisfaction,
        Tr.critical_satisfaction_score,
        O.total_avg_satisfaction_score
        
    FROM cteGeneralEmergencyPrepared PD
    JOIN cteCriticalEmergencyPrepared Tr 
        ON PD.department = Tr.department
    JOIN cteOverallEmergencyPrepared O 
        ON PD.department = O.department;
