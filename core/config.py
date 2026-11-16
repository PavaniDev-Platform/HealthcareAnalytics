from pathlib import Path

# Go up two levels from core/ to reach the 'Practice/' project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Define your folders cleanly
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "ed_patient_data.db"
CSV_DIR = DATA_DIR / "raw_csvs"  # <--- Lives safely inside your data folder
VISUALS_DIR = PROJECT_ROOT / "visuals" 

# Automatically create data,csv,visuals folders on startup if they don't exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
CSV_DIR.mkdir(parents=True, exist_ok=True)
VISUALS_DIR.mkdir(parents=True, exist_ok=True)
