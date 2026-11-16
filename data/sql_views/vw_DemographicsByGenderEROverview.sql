-- SQLite
/*
    Demographic Overview By Gender:
        ---Admissions
        ---Satisfaction
        ---Readmission 
        ---Chief Complaint
        SELECT * FROM vw_DemographicsByGenderEROverview
*/
DROP VIEW IF EXISTS vw_DemographicsByGenderEROverview;
CREATE VIEW vw_DemographicsByGenderEROverview
AS
    WITH cteChiefComplaintPerAgeGender AS(
        SELECT chief_complaint,patient_gender,
        number_0f_admissions AS  chief_complaint_admissions
        FROM vw_ChiefComplaintPerGender
        WHERE rnk_emergency_complaint=1
    )
    SELECT PD.patient_gender,
    COUNT(DISTINCT visit_id) AS number_of_admissions,
    CC.chief_complaint_admissions ,
    ROUND((100.0* SUM(PD.readmitted_30d)/COUNT(PD.visit_id)),2) AS rate_of_readmission_30d,
    ROUND(AVG(PD.satisfaction_score),2) AS avg_satisfaction_score,
    CC.chief_complaint AS chief_complaint
    FROM ed_patient_data PD
    JOIN cteChiefComplaintPerAgeGender AS CC
    ON PD.patient_gender=CC.patient_gender
    GROUP BY PD.patient_gender;