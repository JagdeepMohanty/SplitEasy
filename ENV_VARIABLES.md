# 🔐 EasyXpense Environment Variables

## Render Backend Environment Variables

Set these in **Render Dashboard → Your Service → Environment**:

```
MONGO_URI=mongodb+srv://easyXpense:Jagdeep2607@easyxpense.sfpwthl.mongodb.net/EasyXpense?retryWrites=true&w=majority&appName=EasyXpense
FLASK_ENV=production
PORT=10000
```

### Variable Details:

**MONGO_URI** (Required)
- Full MongoDB Atlas connection string
- Database name: `EasyXpense`
- Cluster: easyxpense.sfpwthl.mongodb.net
- Credentials included

**FLASK_ENV** (Required)
- Value: `production`
- Controls logging and CORS

**PORT** (Optional)
- Value: `10000`
- Render sets this automatically

---

## Netlify Frontend Environment Variables

Set these in **Netlify Dashboard → Site Settings → Environment Variables**:

```
REACT_APP_API_URL=https://easyxpense.onrender.com
```

### Variable Details:

**REACT_APP_API_URL** (Required)
- Backend API base URL
- Must NOT have trailing slash
- Value: `https://easyxpense.onrender.com`

---

## MongoDB Atlas Configuration

### Network Access
- Go to: **Network Access → IP Whitelist**
- Add: `0.0.0.0/0` (Allow from anywhere)
- Required for Render to connect

### Database Access
- Username: `easyXpense`
- Password: `Jagdeep2607`
- Role: "Read and write to any database"

### Database
- Name: `EasyXpense`
- Collections (auto-created):
  - `friends`
  - `expenses`
  - `settlements`

---

## ✅ Verification

### Test Backend
```bash
curl https://easyxpense.onrender.com/health
```
Expected: `{"status":"healthy","database":"connected"}`

### Test Frontend
Visit: https://easyxpense.netlify.app
Expected: App loads without errors

---

## 🚀 Quick Setup

### Render (Backend)
1. Go to dashboard.render.com
2. Select your service
3. Go to Environment tab
4. Add the 3 variables above
5. Save changes (triggers redeploy)

### Netlify (Frontend)
1. Go to app.netlify.com
2. Select your site
3. Go to Site settings → Environment variables
4. Add REACT_APP_API_URL
5. Trigger redeploy

---

**Status:** ✅ Production Ready
**Last Updated:** 2024
