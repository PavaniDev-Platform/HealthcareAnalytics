import pandas as pd
import sys
from pathlib import Path
# Go up one level from 'Dal/' to 'HealthCareAnalysis/' and add it to Python's path
project_root=Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))
# Import your config paths
from core.config import CSV_DIR

#print(CSV_DIR)
from dal.emergency_department_dal import EmergencyDepartmentDAL
#=====================Loading CSV==========================================
dfERPatientData = pd.read_csv(
    CSV_DIR / "ed_patient_data.csv"
)

#Calling database manger to load dataframes into sql tables
db = EmergencyDepartmentDAL()
#Calling load dataframe method by passing dataframe and name of the table to create
db.load_dataframe(dfERPatientData,"ed_patient_data")
print("Emergency Patient Data Loaded")
# 2. Automatically execute all SQL view scripts
db.load_sqlscripts()
print("SQL views initialized successfully!")
