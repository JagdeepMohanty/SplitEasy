# EasyXpense - Environment Variables

## 🚀 Render (Backend)

Set these environment variables in Render Dashboard:

```
MONGO_URI=mongodb+srv://easyXpense:Jagdeep2607@easyxpense.sfpwthl.mongodb.net/EasyXpense?retryWrites=true&w=majority&appName=EasyXpense

FLASK_ENV=production

PORT=10000

GUNICORN_WORKERS=2
```

**Build Command**: `pip install -r requirements.txt`  
**Start Command**: `gunicorn wsgi:app -c gunicorn.conf.py`  
**Python Version**: 3.11.0

---

## 🌐 Netlify (Frontend)

Set these environment variables in Netlify Dashboard:

```
REACT_APP_API_URL=https://easyxpense.onrender.com

REACT_APP_NAME=EasyXpense

REACT_APP_VERSION=1.0.0
```

**Build Command**: `npm run build`  
**Publish Directory**: `build`  
**Base Directory**: `frontend`

---

## 🗄️ MongoDB Atlas

**Network Access**: Add `0.0.0.0/0` to IP whitelist  
**Database User**: `easyXpense` / `Jagdeep2607`  
**Database Name**: `EasyXpense`  
**Collections**: Auto-created on first use

---

## ✅ Verification

### Backend Health Check
```bash
curl https://easyxpense.onrender.com/health
```
Expected: `{"status": "healthy", "database": "connected"}`

### Frontend
```bash
curl -I https://easyxpense.netlify.app/
```
Expected: `200 OK`

---

## 🔐 Security Notes

- Never commit `.env` files to Git
- All credentials stored in environment variables
- CORS restricted to Netlify origin only
- MongoDB IP whitelist set to allow Render connections
