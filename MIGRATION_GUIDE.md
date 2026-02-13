# Migration Guide: Google Sheets to Supabase

If you're currently using Google Sheets with this application, this guide will help you migrate to Supabase or local Excel files.

## Why Migrate?

Google Sheets support has been removed to:
- Simplify the codebase and reduce maintenance
- Improve performance with Supabase's faster API
- Reduce dependencies and security concerns
- Focus on a single cloud provider

## Migration Options

You have two options:

### Option 1: Migrate to Supabase (Recommended for Production)

**Best for:** Cloud deployment, team collaboration, automatic backups

### Option 2: Use Local Excel Files

**Best for:** Local development, testing, offline use

---

## Option 1: Migrate to Supabase

### Step 1: Export Your Data from Google Sheets

1. Open your Google Sheet
2. Go to **File** → **Download** → **Microsoft Excel (.xlsx)**
3. Save the file as `export.xlsx`

### Step 2: Create a Supabase Project

1. Go to [https://supabase.com](https://supabase.com)
2. Sign up for a free account (if you don't have one)
3. Click **New Project**
4. Choose your organization
5. Fill in:
   - **Name:** `dental-bond-app` (or your preferred name)
   - **Database Password:** Choose a strong password (save this!)
   - **Region:** Choose closest to your location
6. Click **Create new project** (takes ~2 minutes)

### Step 3: Set Up Database Tables

1. In your Supabase project, go to **SQL Editor**
2. Click **New Query**
3. Copy and paste this SQL:

```sql
-- Main state table for schedule data
CREATE TABLE IF NOT EXISTS tdb_allotment_state (
  id TEXT PRIMARY KEY,
  payload JSONB NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Profiles table for assistants and doctors
CREATE TABLE IF NOT EXISTS profiles (
  id TEXT PRIMARY KEY,
  kind TEXT NOT NULL,
  name TEXT NOT NULL,
  department TEXT,
  contact_email TEXT,
  contact_phone TEXT,
  status TEXT,
  weekly_off TEXT,
  pref_first TEXT,
  pref_second TEXT,
  pref_third TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  created_by TEXT,
  updated_by TEXT
);

-- Attendance tracking table
CREATE TABLE IF NOT EXISTS assistant_attendance (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  date TEXT NOT NULL,
  assistant TEXT NOT NULL,
  punch_in TEXT,
  punch_out TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(date, assistant)
);

-- Insert initial state row
INSERT INTO tdb_allotment_state (id, payload)
VALUES ('main', '{"columns": [], "rows": [], "meta": {}}'::jsonb)
ON CONFLICT (id) DO NOTHING;
```

4. Click **Run** (or press Ctrl/Cmd + Enter)
5. You should see "Success. No rows returned" - this is correct!

### Step 4: Get Your Supabase Credentials

1. Go to **Project Settings** (gear icon in sidebar)
2. Click **API** in the left menu
3. Copy these two values:
   - **Project URL** (looks like: `https://xxxxx.supabase.co`)
   - **service_role key** (in the "Project API keys" section - **not** the anon key!)

### Step 5: Configure Streamlit Secrets

If deploying to **Streamlit Cloud:**

1. Go to your app on Streamlit Cloud
2. Click **Settings** → **Secrets**
3. Add this configuration (replace with your actual values):

```toml
supabase_url = "https://your-project-id.supabase.co"
supabase_service_role_key = "your-service-role-key-here"
```

If running **locally:**

1. Create a file at `.streamlit/secrets.toml` in your project directory
2. Add the same configuration as above

### Step 6: Import Your Data (Optional)

If you want to import your Google Sheets data into Supabase:

**Method 1: Using the App (Easiest)**

1. Start the app with Supabase configured
2. Go to **Admin/Settings** → **Profiles**
3. Add your assistants and doctors manually
4. Go to the main schedule view
5. Manually re-create your schedule data

**Method 2: Using Excel Import (Advanced)**

1. Keep your exported `export.xlsx` file as `Putt Allotment.xlsx`
2. Temporarily remove Supabase secrets
3. Run the app - it will load from the Excel file
4. Re-add Supabase secrets
5. Restart the app - it will now save to Supabase

### Step 7: Verify the Migration

1. Start/restart your app
2. Check the sidebar - you should see "🔗 Connected to Supabase"
3. Create a test entry in the schedule
4. Refresh the page - your data should persist
5. Check your Supabase dashboard → **Table Editor** → `tdb_allotment_state` to see the data

---

## Option 2: Use Local Excel Files

If you prefer to use local Excel files instead of cloud storage:

### Step 1: Export from Google Sheets

1. Open your Google Sheet
2. Go to **File** → **Download** → **Microsoft Excel (.xlsx)**
3. Save as `Putt Allotment.xlsx` in your project directory

### Step 2: Remove Cloud Secrets

- If using Streamlit Cloud: Remove all Supabase secrets
- If running locally: Delete `.streamlit/secrets.toml` or remove Supabase config

### Step 3: Run the App

1. The app will automatically detect the Excel file
2. You'll see "📁 Using local Excel file" in the sidebar
3. All changes will be saved to the Excel file

**Note:** Local Excel files are not recommended for cloud deployment as the file system is temporary.

---

## Troubleshooting

### "Supabase connection failed"

- **Check URL format:** Must be `https://xxxxx.supabase.co`
- **Verify service role key:** Make sure you're using the service_role key, not the anon key
- **Check network:** Ensure you can access supabase.com from your deployment environment

### "Permission denied" or "RLS policy"

- Make sure you're using the **service_role key** (bypasses RLS)
- If using anon key, you'll need to set up Row Level Security policies

### Data not appearing after migration

- Check Supabase dashboard → **Table Editor** → `tdb_allotment_state`
- Verify the payload column contains your data
- Check browser console and app logs for errors

### App is slow

- Supabase is generally faster than Google Sheets
- Check your internet connection
- Consider upgrading Supabase plan if on heavy usage

---

## Rollback (If Needed)

If you need to temporarily go back to the previous version with Google Sheets support:

```bash
git checkout <previous-commit-hash>
```

However, the old version will not receive updates or bug fixes.

---

## Benefits of Supabase

- ✅ **Faster** - Sub-100ms queries vs Google Sheets API latency
- ✅ **More reliable** - 99.9% uptime SLA
- ✅ **Better security** - Row-level security, encryption at rest
- ✅ **Free tier** - 500MB database, 50MB file storage, 2GB bandwidth
- ✅ **Scalable** - Can handle much larger datasets
- ✅ **Real-time** - Built-in real-time subscriptions (future feature)
- ✅ **PostgreSQL** - Full SQL database with powerful queries

---

## Need Help?

- **Supabase Docs:** https://supabase.com/docs
- **Supabase Discord:** https://discord.supabase.com
- **GitHub Issues:** Create an issue in your repository

---

## Migration Checklist

- [ ] Export data from Google Sheets
- [ ] Create Supabase project
- [ ] Run SQL setup script
- [ ] Get Supabase URL and service_role key
- [ ] Update Streamlit secrets
- [ ] Test connection (should see "🔗 Connected to Supabase")
- [ ] Import/re-create your data
- [ ] Verify data persists across page refreshes
- [ ] Update team members with new deployment
- [ ] Remove old Google Sheets credentials

**Your migration is complete! 🎉**
