-- Run this SQL in Supabase SQL Editor (your project dashboard)
-- Copy and paste the entire content, then click "Run"

-- Note: tdb_allotment_state and profiles already exist from previous integration

-- Create new tables for duties and attendance
CREATE TABLE IF NOT EXISTS assistant_attendance (
  id uuid primary key default gen_random_uuid(),
  date text,
  assistant text,
  punch_in text,
  punch_out text,
  created_at timestamptz default now()
);

CREATE TABLE IF NOT EXISTS duties_master (
  id uuid primary key default gen_random_uuid(),
  title text,
  frequency text,
  default_minutes int,
  op text,
  active boolean default true,
  created_at timestamptz default now()
);

CREATE TABLE IF NOT EXISTS duty_assignments (
  id uuid primary key default gen_random_uuid(),
  duty_id text,
  assistant text,
  op text,
  est_minutes int,
  active boolean default true,
  created_at timestamptz default now()
);

CREATE TABLE IF NOT EXISTS duty_runs (
  id uuid primary key default gen_random_uuid(),
  date text,
  assistant text,
  duty_id text,
  status text,
  started_at text,
  due_at text,
  ended_at text,
  est_minutes int,
  op text,
  created_at timestamptz default now()
);

CREATE TABLE IF NOT EXISTS patients (
  id uuid primary key default gen_random_uuid(),
  name text,
  created_at timestamptz default now()
);

-- Optional: Enable RLS if you want security policies
-- ALTER TABLE assistant_attendance ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE duties_master ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE duty_assignments ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE duty_runs ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE patients ENABLE ROW LEVEL SECURITY;

-- Grant public access (for development)
-- GRANT ALL ON assistant_attendance TO anon, authenticated, service_role;
-- GRANT ALL ON duties_master TO anon, authenticated, service_role;
-- GRANT ALL ON duty_assignments TO anon, authenticated, service_role;
-- GRANT ALL ON duty_runs TO anon, authenticated, service_role;
-- GRANT ALL ON patients TO anon, authenticated, service_role;
