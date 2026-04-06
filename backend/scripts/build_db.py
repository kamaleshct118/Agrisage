import sqlite3
import pandas as pd
import os

def setup_database(db_path):
    # Precise paths to the specific datasets you provided
    npk_csv = 'data/raw/npk-dataset.csv'
    yield_csv = 'data/raw/crop_yield.csv'
    
    print(f"Connecting to unified SQLite database at {db_path}...")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    
    # 1. Process NPK Dataset -> npk_data table
    if os.path.exists(npk_csv):
        print("Loading NPK Data...")
        df_npk = pd.read_csv(npk_csv)
        df_npk.columns = [col.strip().replace(' ', '_') for col in df_npk.columns]
        df_npk.to_sql('npk_data', conn, if_exists='replace', index=False)
        print(f"Successfully loaded {len(df_npk)} rows into 'npk_data' table.")
    else:
        print(f"Error: Could not find {npk_csv}")
        
    # 2. Process Crop Yield Dataset -> crop_production table
    if os.path.exists(yield_csv):
        print("Loading Crop Yield Data...")
        df_yield = pd.read_csv(yield_csv)
        df_yield.columns = [col.strip().replace(' ', '_') for col in df_yield.columns]
        df_yield.to_sql('crop_production', conn, if_exists='replace', index=False)
        print(f"Successfully loaded {len(df_yield)} rows into 'crop_production' table.")
    else:
        print(f"Error: Could not find {yield_csv}")
        
    conn.close()
    print("Database 'agri.db' setup complete with Multiple Tables (npk_data, crop_production).")

if __name__ == "__main__":
    db_path = 'data/processed/agri.db'
    setup_database(db_path)
