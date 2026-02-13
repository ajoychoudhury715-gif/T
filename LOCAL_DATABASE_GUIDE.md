# 📁 Local Database Guide - The Dental Bond App

## ✅ Quick Start - Use Local Excel Files (ENABLED!)

Your app now uses **local Excel files** instead of cloud storage. No internet required!

---

## 📂 How It Works

### **Storage Location:**
```
c:\Users\arian\Desktop\MY APPS\T\T\
├── Putt Allotment.xlsx          ← Main schedule data
├── app.py                        ← Your application
└── [other files]
```

### **What Gets Stored:**
- ✅ **Patient schedules** - All appointments and allocations
- ✅ **Assistant attendance** - Punch in/out records
- ✅ **Profiles** - Doctor and assistant information
- ✅ **Time blocks** - Assistant availability
- ✅ **Duty assignments** - Task assignments
- ✅ **Metadata** - Save versions, timestamps

---

## 🚀 Using Local Storage

### **1. First Launch:**
When you run the app:
```bash
streamlit run app.py
```

The app will:
1. ✅ Check for Supabase (disabled)
2. ✅ **Use local Excel file** (enabled!)
3. ✅ Create `Putt Allotment.xlsx` if it doesn't exist

You'll see in the sidebar:
```
📁 Using local Excel file: Putt Allotment.xlsx
```

### **2. Making Changes:**
- Add/edit patients → Saves to Excel
- Update schedules → Saves to Excel
- Attendance punch → Saves to Excel
- **All changes persist** in the local file

### **3. Data Persistence:**
- ✅ Survives app restarts
- ✅ Works offline (no internet needed)
- ✅ Instant saves (no API calls)
- ✅ Fast loading (local file access)

---

## 💾 Backup & Restore

### **Manual Backup:**
```bash
# Create a backup
copy "Putt Allotment.xlsx" "Putt Allotment_backup_2024-01-15.xlsx"
```

### **Automated Backup Script:**
Create `backup.bat`:
```batch
@echo off
set TIMESTAMP=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%
copy "Putt Allotment.xlsx" "backups\Putt_Allotment_%TIMESTAMP%.xlsx"
echo Backup created: Putt_Allotment_%TIMESTAMP%.xlsx
```

### **Restore from Backup:**
```bash
# Restore a backup
copy "Putt Allotment_backup_2024-01-15.xlsx" "Putt Allotment.xlsx"
```

---

## 🔄 Switching Between Storage Types

### **Current Setup (Local Only):**
```python
USE_SUPABASE = False
FORCE_SUPABASE = False
```

### **Enable Supabase (Cloud):**
```python
# In app.py line 143-144
USE_SUPABASE = False
FORCE_SUPABASE = True  # ← Change this to True

# Then configure secrets (see below)
```

**Supabase Secrets Configuration:**
```toml
# In .streamlit/secrets.toml
supabase_url = "https://your-project.supabase.co"
supabase_service_role_key = "your-service-role-key"
```

---

## 🗄️ Option 2: Use SQLite (Local SQL Database)

Want a real database instead of Excel? Here's how to add SQLite:

### **Advantages:**
- ✅ Faster than Excel
- ✅ Better for large datasets
- ✅ SQL queries
- ✅ ACID transactions
- ✅ No size limits

### **Quick Implementation:**

**1. Install SQLite (already in Python):**
```bash
# SQLite3 is built into Python - no installation needed!
```

**2. Add this code to app.py:**
```python
import sqlite3
import pandas as pd

# SQLite Configuration
SQLITE_DB_PATH = "dental_bond.db"

def init_sqlite_db():
    """Initialize SQLite database with tables."""
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()

    # Create main schedule table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedule (
            id TEXT PRIMARY KEY,
            patient_id TEXT,
            patient_name TEXT,
            in_time TEXT,
            out_time TEXT,
            procedure TEXT,
            doctor TEXT,
            first_assistant TEXT,
            second_assistant TEXT,
            third_assistant TEXT,
            case_paper TEXT,
            op TEXT,
            suction TEXT,
            cleaning TEXT,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create attendance table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            assistant TEXT,
            punch_in TEXT,
            punch_out TEXT
        )
    ''')

    conn.commit()
    conn.close()

def load_data_from_sqlite():
    """Load schedule data from SQLite."""
    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        df = pd.read_sql_query("SELECT * FROM schedule", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error loading from SQLite: {e}")
        return pd.DataFrame()

def save_data_to_sqlite(df):
    """Save schedule data to SQLite."""
    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        df.to_sql('schedule', conn, if_exists='replace', index=False)
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error saving to SQLite: {e}")
        return False

# Initialize DB on startup
if not os.path.exists(SQLITE_DB_PATH):
    init_sqlite_db()
    st.success("✅ SQLite database created!")
```

---

## 🗄️ Option 3: Use PostgreSQL Locally

For advanced users who want a production-grade database:

### **Install PostgreSQL:**
```bash
# Download from: https://www.postgresql.org/download/windows/
# Or use Docker:
docker run --name dental-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres
```

### **Install Python Driver:**
```bash
pip install psycopg2-binary
```

### **Configuration:**
```python
import psycopg2
from psycopg2 import pool

# PostgreSQL Configuration
PG_CONNECTION_POOL = psycopg2.pool.SimpleConnectionPool(
    1, 20,
    host="localhost",
    database="dental_bond",
    user="postgres",
    password="your_password",
    port=5432
)

def load_data_from_postgres():
    conn = PG_CONNECTION_POOL.getconn()
    df = pd.read_sql_query("SELECT * FROM schedule", conn)
    PG_CONNECTION_POOL.putconn(conn)
    return df
```

---

## 📊 Performance Comparison

| Storage Type | Speed | Capacity | Complexity | Offline |
|--------------|-------|----------|------------|---------|
| **Excel** | ⚡ Fast | 1M rows | ✅ Simple | ✅ Yes |
| **SQLite** | ⚡⚡ Faster | Unlimited | ✅ Simple | ✅ Yes |
| **PostgreSQL** | ⚡⚡⚡ Fastest | Unlimited | ⚠️ Complex | ✅ Yes |
| **Supabase** | 🌐 Network | Unlimited | ⚠️ Complex | ❌ No |

---

## 🔧 Troubleshooting

### **"File not found" Error:**
```python
# The app creates it automatically, but if issues persist:
import openpyxl
wb = openpyxl.Workbook()
wb.save("Putt Allotment.xlsx")
```

### **"Permission denied" Error:**
- Close Excel if the file is open
- Check folder permissions
- Run as administrator if needed

### **Data not saving:**
- Check if auto-save is enabled in the app
- Verify file is not read-only
- Check disk space

### **Slow performance:**
- Excel: Good for < 10,000 rows
- Switch to SQLite for > 10,000 rows
- Use PostgreSQL for > 100,000 rows

---

## 📦 Data Export/Import

### **Export to CSV:**
```python
df = pd.read_excel("Putt Allotment.xlsx")
df.to_csv("backup.csv", index=False)
```

### **Import from CSV:**
```python
df = pd.read_csv("backup.csv")
df.to_excel("Putt Allotment.xlsx", index=False)
```

---

## ✅ Current Status

Your app is now configured for:
- ✅ **Local storage enabled**
- ✅ **No cloud dependencies**
- ✅ **Offline capable**
- ✅ **Fast and reliable**
- ✅ **Data stays on your computer**

**File location:**
```
c:\Users\arian\Desktop\MY APPS\T\T\Putt Allotment.xlsx
```

---

## 🎯 Recommendations

**For your use case (Dental clinic):**
- ✅ **Start with Excel** (simple, works great)
- ⚠️ **Upgrade to SQLite** if you have > 5,000 appointments
- ⚠️ **Use PostgreSQL** only if you need multi-user concurrent access
- 🌐 **Keep Supabase as backup** for cloud sync if needed

**Best practice:**
```
Local Excel (primary) + Cloud backup (Supabase)
```

This gives you:
- ⚡ Fast local performance
- ☁️ Cloud backup for safety
- 🔄 Sync capability when needed
