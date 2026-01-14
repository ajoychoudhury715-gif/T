create table if not exists profiles (
  id text primary key,
  kind text not null,
  name text not null,
  department text,
  contact_email text,
  contact_phone text,
  status text,
  weekly_off text,
  pref_first text,
  pref_second text,
  pref_third text,
  created_at timestamptz,
  updated_at timestamptz,
  created_by text,
  updated_by text
);
