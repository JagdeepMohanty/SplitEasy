# 🚀 EasyXpense - Quick Deployment Reference

## ⚡ ENVIRONMENT VARIABLES (Copy & Paste)

### Render Backend
```
MONGO_URI=mongodb+srv://easyXpense:Jagdeep2607@easyxpense.sfpwthl.mongodb.net/EasyXpense?retryWrites=true&w=majority&appName=EasyXpense
FLASK_ENV=production
PORT=10000
GUNICORN_WORKERS=2
```

### Netlify Frontend
```
REACT_APP_API_URL=https://easyxpense.onrender.com
REACT_APP_NAME=EasyXpense
REACT_APP_VERSION=1.0.0
```

---

## ✅ VERIFICATION COMMANDS

```bash
# Backend health
curl https://easyxpense.onrender.com/health

# Frontend
curl -I https://easyxpense.netlify.app/

# API test
curl https://easyxpense.onrender.com/api/friends
```

---

## 📊 STATUS

✅ Repository cleaned (43 files removed)  
✅ Code pushed to GitHub  
✅ Production-ready  
✅ Free tier optimized  

**Next**: Set environment variables → Deploy → Test
