# ALLOTMENT DASHBOARD - The Dental Bond

A **Streamlit-based real-time scheduling dashboard** for managing dental allotments and procedures.

## Features

✨ **Real-time Scheduling**
- Live updates with auto-refresh every 60 seconds
- Status tracking (WAITING, ARRIVED, ON GOING, CANCELLED)
- Doctor and staff assignments
- Operation theater management
- 🔔 **15-minute reminder notifications** before patient appointments

🎨 **Premium UI Design**
- Beautiful gradient interfaces
- Smooth animations and transitions
- Professional table styling
- Responsive layout
- Loading screen with animated spinner

☁️ **Cloud-Ready**
- **Supabase (Postgres) integration** for persistent cloud storage (recommended)
- Works on Streamlit Cloud without data loss
- Falls back to local Excel file for development
- Real-time sync across all users

📊 **Data Management**
- Excel integration (local development)
- Live data editing
- Automatic save functionality
- Change detection with notifications
- Toast notifications for status updates

🧩 **Assistant Allocation + Time Blocking**
- Automatic assistant allocation by department (PROSTHO/Endo) based on time overlap and availability
- Manual override supported (auto-allocation can be configured to fill only empty slots)
- **Time blocks** for assistants (backend work, lunch, training) are persisted:
   - **Supabase**: stored in the same `payload.meta` JSON as the schedule
   - **Excel**: stored in a separate sheet named `Meta`

## Deployment Options

### Option 1: Streamlit Cloud (Recommended for Production)

#### Supabase (Recommended)

1. **Create a Supabase project**
   - Go to https://supabase.com and create a new project
   - In the Supabase dashboard → **SQL Editor**, run:

```sql
create table if not exists tdb_allotment_state (
  id text primary key,
  payload jsonb not null,
  updated_at timestamptz not null default now()
);
```

2. **Deploy to Streamlit Cloud**
   - Go to https://share.streamlit.io and deploy this repo
   - In app settings → **Secrets**, add:

```toml
supabase_url = "https://YOUR_PROJECT_REF.supabase.co"
supabase_key = "YOUR_SUPABASE_ANON_KEY"

# Optional (recommended): avoids Row Level Security (RLS) blocking reads/writes
# supabase_service_role_key = "YOUR_SUPABASE_SERVICE_ROLE_KEY"

# Optional overrides:
# supabase_table = "tdb_allotment_state"
# supabase_row_id = "main"
```

The app will store the whole schedule in a single row (`id = "main"`) as JSON.

##### Supabase RLS (if using `supabase_key` anon key)

If Row Level Security (RLS) is enabled and you use the **anon key**, you must allow your app to read/write the single state row.
In Supabase → **SQL Editor**, run:

```sql
alter table tdb_allotment_state enable row level security;

create policy "read main" on tdb_allotment_state
   for select
   using (id = 'main');

create policy "insert main" on tdb_allotment_state
   for insert
   with check (id = 'main');

create policy "update main" on tdb_allotment_state
   for update
   using (id = 'main')
   with check (id = 'main');
```

If you don’t want to manage RLS policies, use `supabase_service_role_key` in Streamlit Secrets (server-side) instead.

##### (Optional) Patient Master List (Supabase)

If you have a patient database (id + name) and want the app to show a patient list while searching, create a `patients` table in Supabase:

```sql
create table if not exists patients (
   id text primary key,
   name text not null
);

create index if not exists patients_name_idx on patients (name);
```

Secrets (only needed if you used different names):

```toml
# Optional: patient list table/columns
# supabase_patients_table = "patients"
# supabase_patients_id_col = "id"
# supabase_patients_name_col = "name"
```

### Option 2: Local Development

1. **Clone the repository**
```bash
git clone https://github.com/ajoychoudhury715-gif/ALLOTMENT-TDB.git
cd ALLOTMENT-TDB
```

2. **Create a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Add your Excel file**
- Place `Putt Allotment.xlsx` in the project root directory
- Required sheet: "Sheet1"
- Required columns: Patient Name, In Time, Out Time, Procedure, DR., OP, FIRST, SECOND, Third, CASE PAPER, SUCTION, CLEANING, STATUS

## Running the App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Project Structure

```
ALLOTMENT-TDB/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
├── README.md                       # Project documentation
├── Putt Allotment.xlsx            # Excel data file
├── The Dental Bond LOGO_page-0001.jpg  # Company logo
└── .github/                        # GitHub configurations
```

## Dependencies

- **streamlit**: Web framework
- **pandas**: Data manipulation
- **openpyxl**: Excel handling
- **streamlit-autorefresh**: Auto-refresh functionality

See `requirements.txt` for full list.

## Features Overview

### Dashboard Sections
1. **Header** - Logo, title, and real-time date/time display
2. **Full Today's Schedule** - Comprehensive table with all procedures
3. **Status Tracking** - Color-coded status indicators
4. **Data Editing** - Inline editing with instant saves

### Status Colors
- 🔵 **WAITING** - Patient waiting for procedure
- 🟢 **ON GOING** - Procedure in progress
- 🟡 **ARRIVED** - Patient has arrived
- 🔴 **CANCELLED** - Procedure cancelled

### Time Format
- Input: HH:MM (12-hour with AM/PM)
- Storage: Decimal format in Excel (9.30 = 09:30)

## Configuration

### Color Theme
Edit the `COLORS` dictionary in `app.py` to customize:
- Background colors
- Text colors
- Accent colors
- Status indicators

### Auto-Refresh Interval
Change the interval in the `st_autorefresh()` call:
```python
st_autorefresh(interval=60000, debounce=True, key="autorefresh")  # 60 seconds
```

## Usage Tips

1. **Adding Patients** - Click "➕ Add Patient" button
2. **Saving Changes** - Click "💾 Save" button (changes auto-save after edits)
3. **Status Updates** - Use dropdown in STATUS column
4. **Real-time Updates** - Dashboard refreshes automatically every 60 seconds

## Troubleshooting

### Excel File Not Found
- Ensure `Putt Allotment.xlsx` is in the same directory as `app.py`
- Check that the filename matches exactly (case-sensitive)

### Missing Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Auto-refresh Not Working
Install the missing package:
```bash
pip install streamlit-autorefresh
```

## Development

### Code Structure
- **Imports & Config** - Lines 1-30
- **Color Customization** - Lines 26-36
- **CSS Styling** - Lines 45-430
- **Header Section** - Lines 440-490
- **Data Loading** - Lines 500-570
- **Data Processing** - Lines 580-700
- **UI Components** - Lines 800+

### Adding Features
1. Create a new function in the appropriate section
2. Update the CSS if adding new UI elements
3. Test with sample data
4. Document changes in this README

## Contributing

1. Create a feature branch (`git checkout -b feature/amazing-feature`)
2. Commit changes (`git commit -m 'Add amazing feature'`)
3. Push to branch (`git push origin feature/amazing-feature`)
4. Open a Pull Request

## License

This project is proprietary software for The Dental Bond.

## Support

For issues or questions, please contact the development team.

## Version History

### v1.0.0 (Current)
- Initial release
- Premium UI design
- Real-time scheduling
- Excel integration
- Auto-refresh functionality

---

**Made with ❤️ for The Dental Bond**
