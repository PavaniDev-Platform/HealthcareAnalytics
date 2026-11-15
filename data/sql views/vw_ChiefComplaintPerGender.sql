/*
    Gender based emergency trends
        Most common emergecy cause per gender
        PRAGMA table_info(ed_patient_data)
*/
DROP VIEW IF EXISTS vw_ChiefComplaintPerGender;
CREATE VIEW vw_ChiefComplaintPerGender
AS
    WITH cteEmergencyComplaintsPrepared AS(
        SELECT chief_complaint,
        COUNT(chief_complaint) AS number_0f_admissions,
        patient_gender
        FROM ed_patient_data
        GROUP BY patient_gender,chief_complaint
    ),
    CteEmergencyComplaintsRanked AS(
        SELECT chief_complaint,
        number_0f_admissions,
        patient_gender,
        DENSE_RANK() OVER(
            PARTITION BY patient_gender
            ORDER BY number_0f_admissions DESC
        ) AS rnk_emergency_complaint
        FROM cteEmergencyComplaintsPrepared
    )
    SELECT * FROM CteEmergencyComplaintsRanked;