# Temporary file with fixed Supabase initialization code
# This replaces lines 6327-6407 approximately

# Try to connect to Supabase if credentials are available
# PERFORMANCE: Only run full initialization on first load
if SUPABASE_AVAILABLE:
    # Check if already initialized
    if st.session_state.get("supabase_init_done"):
        # Quick restore from session
        if st.session_state.get("supabase_use"):
            sup_url = st.session_state.get("sup_url")
            sup_key = st.session_state.get("sup_key")
            if sup_url and sup_key:
                supabase_client = _get_supabase_client(sup_url, sup_key)
                USE_SUPABASE = True
    else:
        # First-time initialization
        try:
            sup_url, sup_key, sup_table, sup_row, profile_table = _get_supabase_config_from_secrets_or_env()
            if sup_url and sup_key:
                # Validate URL format
                sup_url = sup_url.strip()
                if not (sup_url.startswith("http://") or sup_url.startswith("https://")):
                    raise ValueError(f"Invalid Supabase URL format: '{sup_url}'. Must start with http:// or https://")
                if not ".supabase.co" in sup_url:
                    st.sidebar.warning(f"⚠️ Unusual Supabase URL: '{sup_url}'. Expected format: https://xxxxx.supabase.co")

                supabase_client = _get_supabase_client(sup_url, sup_key)
                if supabase_client is None:
                    raise RuntimeError("Supabase client unavailable.")
                supabase_table_name = sup_table
                supabase_row_id = sup_row
                PROFILE_SUPABASE_TABLE = profile_table
                # Quick connectivity check
                if not _supabase_ready_recent():
                    with st.spinner("Connecting to Supabase..."):
                        _ = supabase_client.table(supabase_table_name).select("id").limit(1).execute()
                    st.session_state.supabase_ready = True
                    st.session_state.supabase_ready_at = time_module.time()
                    st.sidebar.success("Connected to Supabase")
                USE_SUPABASE = True
                if not st.session_state.get("supabase_profiles_seeded"):
                    _seed_supabase_profiles_if_needed(supabase_client)
                    st.session_state.supabase_profiles_seeded = True
                if not st.session_state.get("supabase_staff_refreshed"):
                    _refresh_staff_options_from_supabase(supabase_client)
                    st.session_state.supabase_staff_refreshed = True
                # Store config in session
                st.session_state.supabase_init_done = True
                st.session_state.supabase_use = True
                st.session_state.sup_url = sup_url
                st.session_state.sup_key = sup_key
            else:
                # Not configured
                st.session_state.supabase_init_done = True
                st.session_state.supabase_use = False
                with st.sidebar.expander("✅ Quick setup (Supabase)", expanded=False):
                    st.markdown(
                        "Add these secrets in Streamlit Cloud → Settings → Secrets:\n"
                        "- `supabase_url`\n"
                        "- `supabase_key` (anon key) **or** `supabase_service_role_key` (recommended for server-side apps)\n"
                        "\nThen create the table in Supabase (SQL Editor):"
                    )
                    st.code(
                        "create table if not exists tdb_allotment_state (\n"
                        "  id text primary key,\n"
                        "  payload jsonb not null,\n"
                        "  updated_at timestamptz not null default now()\n"
                        ");\n",
                        language="sql",
                    )
        except Exception as e:
            # Safe diagnostics
            st.session_state.supabase_ready = False
            st.session_state.supabase_init_done = True
            st.session_state.supabase_use = False
            supabase_client = None
            USE_SUPABASE = False

            # Show user-friendly error
            error_msg = str(e).lower()
            if "name or service not known" in error_msg or "errno -2" in error_msg:
                st.sidebar.warning(
                    "⚠️ Supabase connection failed (network/DNS error)\n\n"
                    "**Using local Excel file instead** 📁"
                )
            else:
                st.sidebar.warning(
                    f"⚠️ Supabase connection failed\n\n"
                    f"**Using local Excel file instead** 📁"
                )
