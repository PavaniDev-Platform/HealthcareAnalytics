/*
PRAGMA table_info(ed_patient_data)
Admission Trends:
    Which months have faced highest emergencies?(not intrested in days here)
    What is main emergency cause based on age group?
    Gender based emergency trends
        --Most common emergecy cause per gender
*/
DROP VIEW IF EXISTS vw_MonthlyERAdmissionTrends;
CREATE VIEW vw_MonthlyERAdmissionTrends
AS
    WITH cteMothlyEmergencyPrepared AS(
        SELECT DISTINCT department,arrival_month,
        COUNT(visit_id) AS emergency_admissions
        FROM ed_patient_data
        GROUP BY department,arrival_month
    ),
    cteMonthyEmergencyRanked AS(
        SELECT department,arrival_month,
        emergency_admissions,
        DENSE_RANK() OVER(
            PARTITION BY department
            ORDER BY emergency_admissions DESC
        ) AS rnk_highest_emergency
        FROM cteMothlyEmergencyPrepared
    )
    SELECT * 
    FROM cteMonthyEmergencyRanked;
    --ORDER BY department ASC,emergency_admissions DESC;
