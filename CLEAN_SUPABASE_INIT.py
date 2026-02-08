# ========================================================================
# CLEAN SUPABASE INITIALIZATION - Copy this to replace lines ~6327-6450
# ========================================================================

# Try to connect to Supabase if credentials are available
# PERFORMANCE: Only run full initialization once per session
if SUPABASE_AVAILABLE:
    # Check if already initialized this session
    if st.session_state.get("supabase_init_done"):
        # Quick restore: just reconnect the client from cached config
        if st.session_state.get("supabase_use") and st.session_state.get("sup_url") and st.session_state.get("sup_key"):
            supabase_client = _get_supabase_client(
                st.session_state.get("sup_url"),
                st.session_state.get("sup_key")
            )
            USE_SUPABASE = True
    else:
        # First-time initialization - run all setup
        try:
            sup_url, sup_key, sup_table, sup_row, profile_table = _get_supabase_config_from_secrets_or_env()

            if sup_url and sup_key:
                # Validate URL format
                sup_url = sup_url.strip()
                if not (sup_url.startswith("http://") or sup_url.startswith("https://")):
                    raise ValueError(f"Invalid Supabase URL format: '{sup_url}'. Must start with http:// or https://")
                if ".supabase.co" not in sup_url:
                    st.sidebar.warning(f"⚠️ Unusual Supabase URL: '{sup_url}'. Expected format: https://xxxxx.supabase.co")

                # Get client
                supabase_client = _get_supabase_client(sup_url, sup_key)
                if supabase_client is None:
                    raise RuntimeError("Supabase client unavailable.")

                # Set configuration
                supabase_table_name = sup_table
                supabase_row_id = sup_row
                PROFILE_SUPABASE_TABLE = profile_table

                # Quick connectivity check (only if not done recently)
                if not _supabase_ready_recent():
                    with st.spinner("🔗 Connecting to Supabase..."):
                        _ = supabase_client.table(supabase_table_name).select("id").limit(1).execute()
                    st.session_state.supabase_ready = True
                    st.session_state.supabase_ready_at = time_module.time()
                    st.sidebar.success("✅ Connected to Supabase")

                USE_SUPABASE = True

                # One-time profile seeding
                if not st.session_state.get("supabase_profiles_seeded"):
                    _seed_supabase_profiles_if_needed(supabase_client)
                    st.session_state.supabase_profiles_seeded = True

                # One-time staff refresh
                if not st.session_state.get("supabase_staff_refreshed"):
                    _refresh_staff_options_from_supabase(supabase_client)
                    st.session_state.supabase_staff_refreshed = True

                # Mark initialization as complete and cache config
                st.session_state.supabase_init_done = True
                st.session_state.supabase_use = True
                st.session_state.sup_url = sup_url
                st.session_state.sup_key = sup_key

            else:
                # Not configured - show setup helper
                st.session_state.supabase_init_done = True
                st.session_state.supabase_use = False

                with st.sidebar.expander("✅ Quick setup (Supabase)", expanded=False):
                    st.markdown(
                        "Add these secrets in Streamlit Cloud → Settings → Secrets:\n"
                        "- `supabase_url`\n"
                        "- `supabase_key` (anon key) **or** `supabase_service_role_key` (recommended)\n"
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
                    st.markdown(
                        "If you use the **anon key**, you may need to adjust Row Level Security (RLS). "
                        "Recommended: enable RLS and add policies allowing the single state row (id = 'main'):"
                    )
                    st.code(
                        "alter table tdb_allotment_state enable row level security;\n\n"
                        "create policy \"read main\" on tdb_allotment_state\n"
                        "  for select\n"
                        "  using (id = 'main');\n\n"
                        "create policy \"insert main\" on tdb_allotment_state\n"
                        "  for insert\n"
                        "  with check (id = 'main');\n\n"
                        "create policy \"update main\" on tdb_allotment_state\n"
                        "  for update\n"
                        "  using (id = 'main')\n"
                        "  with check (id = 'main');\n",
                        language="sql",
                    )

        except Exception as e:
            # Handle all initialization errors gracefully
            st.session_state.supabase_ready = False
            st.session_state.supabase_ready_at = 0.0
            st.session_state.supabase_profiles_seeded = False
            st.session_state.supabase_staff_refreshed = False
            st.session_state.supabase_init_done = True
            st.session_state.supabase_use = False
            supabase_client = None
            USE_SUPABASE = False

            # Show user-friendly error message
            error_msg = str(e).lower()

            if "name or service not known" in error_msg or "errno -2" in error_msg:
                st.sidebar.warning(
                    "⚠️ Supabase connection failed (network/DNS error)\n\n"
                    "**Using local Excel file instead** 📁\n\n"
                    "Possible causes:\n"
                    "• Invalid Supabase URL\n"
                    "• Network connectivity issue\n"
                    "• DNS resolution failure"
                )
            elif "rls" in error_msg or "permission" in error_msg:
                st.sidebar.warning(
                    "⚠️ Supabase permission denied\n\n"
                    "**Using local Excel file instead** 📁\n\n"
                    "Tip: If using `supabase_key` (anon key), RLS may block reads/writes. "
                    "Add `supabase_service_role_key` in secrets or disable RLS for the table."
                )
            else:
                # Generic error with diagnostics
                present = {}
                try:
                    if hasattr(st, 'secrets'):
                        interesting = ["supabase_url", "supabase_key", "supabase_service_role_key"]
                        present = {k: (k in st.secrets and bool(str(st.secrets.get(k, '')).strip())) for k in interesting}
                except Exception:
                    pass

                st.sidebar.warning(
                    f"⚠️ Supabase connection failed: {e}\n\n"
                    f"**Using local Excel file instead** 📁"
                    + (f"\n\nCredentials configured: {', '.join([k for k, v in present.items() if v])}" if present else "")
                )

            # Show fallback status
            st.sidebar.info("📁 Local Excel Mode Active\n\nData will be saved to: Putt Allotment.xlsx")
