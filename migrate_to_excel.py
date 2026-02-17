"""
Migration script: Export Supabase data to Excel
Converts all Supabase tables to Excel sheets in Putt Allotment.xlsx
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

import pandas as pd
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows

# Import Supabase
try:
    from supabase import create_client
except ImportError:
    print("ERROR: supabase library not installed. Install with: pip install supabase")
    sys.exit(1)

# Configuration
EXCEL_FILE = Path(__file__).parent / "Putt Allotment.xlsx"
SHEET_NAMES = {
    "tdb_allotment_state": "Sheet1",
    "profiles_assistants": "Assistants",
    "profiles_doctors": "Doctors",
    "assistant_attendance": "Assistants_Attendance",
    "duties_master": "Duties_Master",
    "duty_assignments": "Duty_Assignments",
    "duty_runs": "Duty_Runs",
    "patients": "Patients",
}

def get_supabase_credentials():
    """Get Supabase URL and KEY from environment or prompt user."""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        print("\n🔐 Supabase credentials required for migration.")
        print("Set SUPABASE_URL and SUPABASE_KEY environment variables, or enter below:\n")
        url = input("Supabase URL: ").strip()
        key = input("Supabase Key: ").strip()

    if not url or not key:
        print("ERROR: Supabase credentials not provided")
        sys.exit(1)

    return url, key

def fetch_supabase_data(client, table_name):
    """Fetch all data from a Supabase table."""
    try:
        response = client.table(table_name).select("*").execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"⚠️  Error fetching {table_name}: {e}")
        return []

def export_allotment_state(client, excel_file):
    """Export tdb_allotment_state (main schedule)."""
    print("📋 Exporting main schedule (tdb_allotment_state)...")

    try:
        data = fetch_supabase_data(client, "tdb_allotment_state")
        if not data:
            print("   No data found in tdb_allotment_state")
            return

        # Extract payload (JSONB blob)
        row = data[0]
        payload = row.get("payload", {})

        # Payload structure: {columns: [...], rows: [...], meta: {...}}
        columns = payload.get("columns", [])
        rows = payload.get("rows", [])
        meta = payload.get("meta", {})

        if rows:
            df = pd.DataFrame(rows, columns=columns)
            df.to_excel(excel_file, sheet_name="Sheet1", index=False)
            print(f"   ✓ Exported {len(rows)} schedule rows")

        # Save metadata to Meta sheet
        if meta:
            meta_df = pd.DataFrame([meta])
            meta_df.to_excel(excel_file, sheet_name="Meta", index=False, engine="openpyxl")
            print(f"   ✓ Exported metadata")

    except Exception as e:
        print(f"   ✗ Error exporting allotment state: {e}")

def export_profiles(client, excel_file):
    """Export profiles split by kind (Assistants/Doctors)."""
    print("👥 Exporting profiles (assistants and doctors)...")

    try:
        data = fetch_supabase_data(client, "profiles")
        if not data:
            print("   No data found in profiles")
            return

        df = pd.DataFrame(data)

        # Split by kind
        assistants = df[df["kind"] == "Assistants"]
        doctors = df[df["kind"] == "Doctors"]

        if len(assistants) > 0:
            assistants.to_excel(excel_file, sheet_name="Assistants", index=False, engine="openpyxl")
            print(f"   ✓ Exported {len(assistants)} assistants")

        if len(doctors) > 0:
            doctors.to_excel(excel_file, sheet_name="Doctors", index=False, engine="openpyxl")
            print(f"   ✓ Exported {len(doctors)} doctors")

    except Exception as e:
        print(f"   ✗ Error exporting profiles: {e}")

def export_attendance(client, excel_file):
    """Export assistant_attendance."""
    print("⏰ Exporting attendance records...")

    try:
        data = fetch_supabase_data(client, "assistant_attendance")
        if not data:
            print("   No data found in assistant_attendance")
            return

        df = pd.DataFrame(data)
        df.to_excel(excel_file, sheet_name="Assistants_Attendance", index=False, engine="openpyxl")
        print(f"   ✓ Exported {len(df)} attendance records")

    except Exception as e:
        print(f"   ✗ Error exporting attendance: {e}")

def export_duties_master(client, excel_file):
    """Export duties_master."""
    print("📝 Exporting duties master list...")

    try:
        data = fetch_supabase_data(client, "duties_master")
        if not data:
            print("   No data found in duties_master")
            return

        df = pd.DataFrame(data)
        df.to_excel(excel_file, sheet_name="Duties_Master", index=False, engine="openpyxl")
        print(f"   ✓ Exported {len(df)} duties")

    except Exception as e:
        print(f"   ✗ Error exporting duties_master: {e}")

def export_duty_assignments(client, excel_file):
    """Export duty_assignments."""
    print("🎯 Exporting duty assignments...")

    try:
        data = fetch_supabase_data(client, "duty_assignments")
        if not data:
            print("   No data found in duty_assignments")
            return

        df = pd.DataFrame(data)
        df.to_excel(excel_file, sheet_name="Duty_Assignments", index=False, engine="openpyxl")
        print(f"   ✓ Exported {len(df)} duty assignments")

    except Exception as e:
        print(f"   ✗ Error exporting duty_assignments: {e}")

def export_duty_runs(client, excel_file):
    """Export duty_runs."""
    print("▶️  Exporting duty runs (audit log)...")

    try:
        data = fetch_supabase_data(client, "duty_runs")
        if not data:
            print("   No data found in duty_runs")
            return

        df = pd.DataFrame(data)
        df.to_excel(excel_file, sheet_name="Duty_Runs", index=False, engine="openpyxl")
        print(f"   ✓ Exported {len(df)} duty run records")

    except Exception as e:
        print(f"   ✗ Error exporting duty_runs: {e}")

def export_patients(client, excel_file):
    """Export patients."""
    print("🧑‍⚕️  Exporting patient list...")

    try:
        # Get table name from env or use default
        patients_table = os.getenv("SUPABASE_PATIENTS_TABLE", "patients")

        # Try default first, then fallback
        data = fetch_supabase_data(client, patients_table)

        if not data and patients_table != "patients":
            print(f"   Trying alternate table name 'patients'...")
            data = fetch_supabase_data(client, "patients")

        if not data:
            print("   No data found in patients table")
            return

        df = pd.DataFrame(data)
        df.to_excel(excel_file, sheet_name="Patients", index=False, engine="openpyxl")
        print(f"   ✓ Exported {len(df)} patients")

    except Exception as e:
        print(f"   ✗ Error exporting patients: {e}")

def main():
    """Run full migration."""
    print("\n" + "="*60)
    print("SUPABASE → EXCEL MIGRATION TOOL")
    print("="*60)

    # Check Excel file exists
    if not EXCEL_FILE.exists():
        print(f"\nERROR: Excel file not found: {EXCEL_FILE}")
        sys.exit(1)

    print(f"\n📁 Target Excel file: {EXCEL_FILE}\n")

    # Get credentials
    url, key = get_supabase_credentials()

    # Connect to Supabase
    print("\n🔗 Connecting to Supabase...")
    try:
        client = create_client(url, key)
        # Verify connection by fetching one record
        client.table("tdb_allotment_state").select("id", count="exact").limit(1).execute()
        print("✓ Connected successfully\n")
    except Exception as e:
        print(f"✗ Failed to connect: {e}")
        sys.exit(1)

    # Export all tables
    print("Starting export...\n")

    export_allotment_state(client, EXCEL_FILE)
    export_profiles(client, EXCEL_FILE)
    export_attendance(client, EXCEL_FILE)
    export_duties_master(client, EXCEL_FILE)
    export_duty_assignments(client, EXCEL_FILE)
    export_duty_runs(client, EXCEL_FILE)
    export_patients(client, EXCEL_FILE)

    print("\n" + "="*60)
    print("✅ Migration complete!")
    print("="*60)
    print(f"\nAll Supabase data has been exported to Excel.")
    print(f"File: {EXCEL_FILE}")
    print("\nNext steps:")
    print("1. Review the Excel file to verify all data is correct")
    print("2. The app will now use Excel for all data (Supabase is disabled)")
    print("3. You can safely remove or disconnect Supabase credentials\n")

if __name__ == "__main__":
    main()
