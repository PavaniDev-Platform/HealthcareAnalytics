class EmergencyDepartmentAnalyzer:
     def __init__(self, objDatabaseManager):
            self.objERDatabaseManager = objDatabaseManager

     def fetchData(self):
         strQuery="SELECT * FROM ed_patient_data"
         dfEDPatientData=self.objERDatabaseManager.run_query(strQuery)
         return dfEDPatientData
     #================================Emergency Department Executive Overview================================
     def getEDExecutiveOverview(self):
          strQuery="SELECT * FROM vw_ExecutiveEROverview"
          dfEDExecutiveOverview=self.objERDatabaseManager.run_query(strQuery)
          return dfEDExecutiveOverview

     #=============================================================================================================
     
     #==================================#Emergency Department Operation Overview===================================
     def getEDOperationOverview(self):
           strQuery="SELECT * FROM vw_OperationEROverview"
           dfEDOperationOverview=self.objERDatabaseManager.run_query(strQuery)
           return dfEDOperationOverview
     def getMonthlyEDAdmissionTrends(self):
          strQuery="SELECT * FROM vw_MonthlyERAdmissionTrends"
          dfEDMonthlyEDAdmissionTrends=self.objERDatabaseManager.run_query(strQuery)
          return dfEDMonthlyEDAdmissionTrends
     #==============================================================================================================

     #======================================== #Emergency Department Demographic Overview=============================
     def getChiefComplaintPerAgeGroup(self):
          strQuery="SELECT * FROM vw_ChiefComplaintPerAgeGroup"
          dfChiefComplaintPerAgeGrp=self.objERDatabaseManager.run_query(strQuery)
          return dfChiefComplaintPerAgeGrp
     def getEDDemographicOverviewByAge(self):
          strQuery="SELECT * FROM vw_DemographicsByAgeEROverview"
          dfDemographicOverviewByAge=self.objERDatabaseManager.run_query(strQuery)
          return dfDemographicOverviewByAge
     def getChiefComplaintPerGender(self):
          strQuery="SELECT * FROM vw_ChiefComplaintPerGender"
          dfChiefComplaintPerGender=self.objERDatabaseManager.run_query(strQuery)
          return dfChiefComplaintPerGender
     def getEDDemographicOverviewByGender(self):
          strQuery="SELECT * FROM vw_DemographicsByGenderEROverview"
          dfDemographicOverviewByGender=self.objERDatabaseManager.run_query(strQuery)
          return dfDemographicOverviewByGender
     #===================================================================================================================

     #=============================================Emergency Insurance Trend Overview====================================
     def getEDInsuranceOverview(self):
          strQuery="""SELECT 
                    department,
                    insurance_type,
                    COUNT(visit_id) as total_admissions,
                    ROUND(AVG(wait_time_doctor_min),2) as avg_wait_time,
                    SUM(billed_amount_usd) as total_deptrevenue,
                    ROUND((100.0* SUM(readmitted_30d)/COUNT(visit_id)),2) AS rate_of_readmission_30d,
                    ROUND(AVG(satisfaction_score),2) AS avg_satisfaction_score
                    FROM ed_patient_data
                    GROUP BY department, insurance_type;"""
          dfInsuranceOverview=self.objERDatabaseManager.run_query(strQuery)
          return dfInsuranceOverview
     #======================================================================================================================

     #===================================================Emergency Quality Care Overview===================================
     def getReadmissionRatePerDiagnosis(self):
          strQuery=""" SELECT chief_complaint,
                       ROUND((100.0* SUM(readmitted_30d)/COUNT(visit_id)),2) AS rate_of_readmission_30d
                       FROM ed_patient_data
                       GROUP BY chief_complaint"""
          dfReadmissionPerDiagnosis=self.objERDatabaseManager.run_query(strQuery)
          return dfReadmissionPerDiagnosis
     def getReadmissionRateByInsuranceType(self):
          strQuery="""SELECT insurance_type,
                      ROUND((100.0* SUM(readmitted_30d)/COUNT(visit_id)),2) AS rate_of_readmission_30d
                      FROM ed_patient_data
                      GROUP BY insurance_type"""
          dfReadmissionRateByInsuranceType=self.objERDatabaseManager.run_query(strQuery)
          return dfReadmissionRateByInsuranceType
     
