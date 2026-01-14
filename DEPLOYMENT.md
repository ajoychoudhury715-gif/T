# 🚀 Deployment Guide

Your ALLOTMENT Dashboard is ready for deployment! All code issues have been fixed and tested.

## ✅ Pre-Deployment Checklist
- [x] Code compiles without syntax errors
- [x] Type annotations fixed
- [x] Streamlit app starts successfully
- [x] Changes committed to GitHub

## 📦 Deployment Options

### **Option 1: Streamlit Cloud (Recommended - FREE)**

Streamlit Cloud is the easiest and fastest way to deploy your app with zero infrastructure management.

#### Steps:

1. **Go to Streamlit Cloud**
   - Visit: https://share.streamlit.io/
   - Click "New app"

2. **Connect Your Repository**
   - Repository: `ajoychoudhury715-gif/ALLOTMENT-TDB`
   - Branch: `main`
   - Main file path: `app.py`

3. **Configure Secrets (Optional but Recommended)**
   
   **For Supabase (Recommended):**
   - Click "Advanced settings" → "Secrets"
   - Add your Supabase configuration:
   ```toml
   [supabase]
   url = "https://your-project.supabase.co"
   key = "your-anon-key"
   table = "allotment_data"
   row_id = "main"
   ```

   **Or for Google Sheets:**
   ```toml
   [gsheets]
   spreadsheet_id = "your-spreadsheet-id"
   worksheet_name = "Sheet1"
   
   [gcp_service_account]
   type = "service_account"
   project_id = "your-project-id"
   private_key_id = "your-key-id"
   private_key = "-----BEGIN PRIVATE KEY-----\nYour-Key\n-----END PRIVATE KEY-----\n"
   client_email = "your-service-account@project.iam.gserviceaccount.com"
   client_id = "your-client-id"
   auth_uri = "https://accounts.google.com/o/oauth2/auth"
   token_uri = "https://oauth2.googleapis.com/token"
   auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
   client_x509_cert_url = "your-cert-url"
   ```

4. **Deploy!**
   - Click "Deploy"
   - Wait 2-3 minutes for initial deployment
   - Your app will be live at: `https://your-app-name.streamlit.app`

5. **Access Your App**
   - Share the URL with your team
   - App automatically updates when you push to GitHub!

---

### **Option 2: Local Development**

Run locally for testing or development:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Access at: http://localhost:8501

---

## 🗄️ Data Storage Setup

### **Supabase (Recommended for Production)**

1. **Create Supabase Project**: https://supabase.com
2. **Run SQL Setup**:
```sql
CREATE TABLE allotment_data (
  id TEXT PRIMARY KEY DEFAULT 'main',
  payload JSONB NOT NULL,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Insert initial row
INSERT INTO allotment_data (id, payload)
VALUES ('main', '{"data": [], "meta": {}}'::jsonb);
```

3. **Get Credentials**:
   - Project URL: Settings → API → Project URL
   - Anon Key: Settings → API → Project API keys → anon/public

4. **Add to Streamlit Secrets** (see above)

### **Google Sheets (Alternative)**

1. Create Google Sheet with "Sheet1"
2. Enable Google Sheets API
3. Create Service Account
4. Share sheet with service account email
5. Add credentials to Streamlit secrets

### **Local Excel (Development Only)**

- Place `Putt Allotment.xlsx` in same directory
- Not recommended for cloud deployment

---

## 🔧 Environment Variables

The app automatically detects storage method:
1. Checks for Supabase secrets first (recommended)
2. Falls back to Google Sheets if configured
3. Uses local Excel as last resort

---

## 📊 Monitoring & Maintenance

### **Streamlit Cloud Dashboard**
- View logs: Streamlit Cloud → Your app → Logs
- Monitor usage: Analytics tab
- Reboot app: Menu → Reboot

### **Auto-Updates**
- Push to GitHub `main` branch
- Streamlit Cloud auto-deploys within 1-2 minutes

---

## 🆘 Troubleshooting

### **App Won't Start**
- Check logs in Streamlit Cloud
- Verify secrets are correctly formatted (TOML syntax)
- Ensure all dependencies in requirements.txt

### **Data Not Saving**
- Verify Supabase/Google Sheets credentials
- Check table exists and has correct structure
- Check app logs for error messages

### **Slow Performance**
- Supabase is faster than Google Sheets
- Consider upgrading Streamlit Cloud tier for more resources
- Optimize data with fewer rows if needed

---

## 🎯 Next Steps

1. **Deploy to Streamlit Cloud now!** (takes 5 minutes)
2. Set up Supabase for persistent data
3. Share app URL with your team
4. Monitor usage and feedback

---

## 📞 Support

- Streamlit Docs: https://docs.streamlit.io/
- Supabase Docs: https://supabase.com/docs
- GitHub Issues: Create an issue in your repo

---

**Your app is production-ready! 🎉**

Simply deploy to Streamlit Cloud and you're live!
