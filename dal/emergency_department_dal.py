import pandas as pd
import sqlite3
import sys
from pathlib import Path
# Go up one level from 'Dal/' to 'HealthCareAnalysis/' and add it to Python's path
project_root=Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))
# Import your config paths
from core.config import DB_PATH,SQL_DIR

class EmergencyDepartmentDAL:
    '''Used to load data into dataframes and manage SQLite connection'''
    def __init__(self):
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
    def load_sqlscripts(self):
        for sql_file in sorted(SQL_DIR.glob("*.sql")):
            with open(sql_file, "r", encoding="utf-8") as f:
                view_sql = f.read()
            self.conn.executescript(view_sql)
            print(f"Created view from: {sql_file.name}")
    def close(self):
        if self.conn:
            self.conn.close()    
       


     
