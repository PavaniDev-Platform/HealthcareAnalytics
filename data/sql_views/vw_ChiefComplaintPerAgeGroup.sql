--What is main emergency cause based on age group?
--PRAGMA table_info(ed_patient_data)
DROP VIEW IF EXISTS vw_ChiefComplaintPerAgeGroup;
CREATE VIEW vw_ChiefComplaintPerAgeGroup
AS
    WITH cteEmergencyComplaintsPrepared AS(
        SELECT department,
        COUNT(visit_id) AS number_0f_admissions,
        patient_age
        FROM ed_patient_data
        GROUP BY patient_age,department
    ),
    CteEmergencyComplaintsRanked AS(
        SELECT department,
        number_0f_admissions,
        patient_age,
        DENSE_RANK() OVER(
            PARTITION BY patient_age
            ORDER BY number_0f_admissions DESC
        ) AS rnk_emergency_complaint
        FROM cteEmergencyComplaintsPrepared
    )
    SELECT * FROM CteEmergencyComplaintsRanked;
   


