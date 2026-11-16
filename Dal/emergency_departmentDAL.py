import pandas as pd
import sqlite3
import sys
from pathlib import Path
# Go up one level from 'Dal/' to 'HealthCareAnalysis/' and add it to Python's path
project_root=Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))
# Import your config paths
from core.config import DB_PATH

class EmergencyDepartmentDAL:
    '''Used to load data into dataframes and manage SQLite connection'''
    def __init__(self, db_name="ed_patient_data.db"):
        print(f"-> Connected to Central Database at: {DB_PATH}")
        self.conn = sqlite3.connect(DB_PATH,check_same_thread=False)

    def load_dataframe(self, df, table_name):
        df.to_sql(
            table_name,
            self.conn,
            if_exists="replace",
            index=False
        )

    def run_query(self, query):
        return pd.read_sql(
            query,
            self.conn
        )


     
