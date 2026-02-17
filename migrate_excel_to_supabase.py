#!/usr/bin/env python3
"""
Migration script: Copy Excel data to Supabase tables
Run this ONCE after creating the Supabase tables
"""

import os
import sys
import pandas as pd
from pathlib import Path

# Get Supabase credentials
try:
    from supabase import create_client
except ImportError:
    print("ERROR: supabase library not installed. Install with: pip install supabase")
    sys.exit(1)

# Supabase configuration
SUPABASE_URL = "https://iulgvbjkqcrwwnrwjolh.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml1bGd2YmprcWNyd3ducndqb2xoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjQyNDM1NSwiZXhwIjoyMDgyMDAwMzU1fQ.PlilHFvaHxCTCdXHQILJ07enCTwTarOphYILnO9RIwU"

# Excel file path
EXCEL_FILE = Path(__file__).parent / "Putt Allotment.xlsx"

# Sheet names
SHEET_NAMES = {
    "Assistants_Attendance": "assistant_attendance",
    "Duties_Master": "duties_master",
    "Duty_Assignments": "duty_assignments",
    "Duty_Runs": "duty_runs",
    "Patients": "patients",
}

def migrate_table(sb_client, excel_sheet: str, sb_table: str):
    """Migrate one table from Excel to Supabase."""
    try:
        print(f"\n📋 Migrating {excel_sheet} → {sb_table}...")

        # Read Excel sheet
        df = pd.read_excel(EXCEL_FILE, sheet_name=excel_sheet, engine="openpyxl")

        if df.empty:
            print(f"   ⚠️  No data in {excel_sheet}, skipping")
            return

        print(f"   ✓ Read {len(df)} rows from Excel")

        # Convert DataFrame to records
        records = df.where(pd.notna(df), None).to_dict("records")

        # Upsert to Supabase
        if records:
            response = sb_client.table(sb_table).upsert(records).execute()
            print(f"   ✅ Upserted {len(records)} records to {sb_table}")
        else:
            print(f"   ⚠️  No records to upsert")

    except Exception as e:
        print(f"   ❌ Error migrating {excel_sheet}: {e}")


def main():
    print("=" * 60)
    print("EXCEL → SUPABASE MIGRATION")
    print("=" * 60)

    # Check Excel file exists
    if not EXCEL_FILE.exists():
        print(f"\n❌ ERROR: Excel file not found: {EXCEL_FILE}")
        sys.exit(1)

    print(f"\n📁 Excel file: {EXCEL_FILE}")

    # Connect to Supabase
    print("\n🔗 Connecting to Supabase...")
    try:
        sb_client = create_client(SUPABASE_URL, SUPABASE_KEY)
        # Test connection
        sb_client.table("patients").select("id", count="exact").limit(1).execute()
        print("✓ Connected to Supabase")
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        sys.exit(1)

    # Migrate each table
    for excel_sheet, sb_table in SHEET_NAMES.items():
        migrate_table(sb_client, excel_sheet, sb_table)

    print("\n" + "=" * 60)
    print("✅ MIGRATION COMPLETE!")
    print("=" * 60)
    print("\nYour Excel data has been copied to Supabase.")
    print("The app will now load data from Supabase.")
    print("\nNext: Restart the app with: streamlit run app.py --server.port 8501")


if __name__ == "__main__":
    main()
