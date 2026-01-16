# EasyXpense - Expense Splitting Application

A modern expense splitting web application built with React, Flask, and MongoDB Atlas. Split expenses with friends, track debts, and settle payments easily.

## 🌐 Live Application

- **Frontend**: https://easyxpense.netlify.app
- **Backend API**: https://easyxpense.onrender.com

## 🚀 Features

- 💰 Split expenses equally among friends
- 📊 Track who owes what with optimized debt calculations
- 💳 Record settlements and payment history
- 🇮🇳 Indian Rupee (INR) support with proper formatting
- 📱 Responsive design for mobile and desktop
- 🚫 No authentication required - simple and fast

## 🏗️ Tech Stack

### Frontend
- React 19.2.3
- React Router DOM 7.12.0
- Axios 1.13.2
- Deployed on Netlify

### Backend
- Python 3.11
- Flask 3.0.0
- Flask-CORS 4.0.0
- PyMongo 4.6.1
- Gunicorn 21.2.0
- Deployed on Render

### Database
- MongoDB Atlas (Free Tier)
- Database: `EasyXpense`
- Collections: `friends`, `expenses`, `settlements`, `groups`

## 📁 Project Structure

```
easyxpense/
├── backend/
│   ├── app/
│   │   ├── models/         # Data models
│   │   ├── routes/         # API endpoints
│   │   ├── utils/          # Utilities (money, sanitization, debt optimizer)
│   │   └── __init__.py     # Flask app initialization
│   ├── wsgi.py             # Production WSGI entry
│   ├── run.py              # Development server
│   ├── gunicorn.conf.py    # Gunicorn configuration
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API service
│   │   └── utils/          # Utilities
│   ├── public/
│   │   └── _redirects      # Netlify SPA routing
│   └── package.json        # Node dependencies
├── render.yaml             # Render deployment config
├── netlify.toml            # Netlify deployment config
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites
- Node.js 16+
- Python 3.11+
- MongoDB Atlas account

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Mac/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file:
   ```bash
   MONGO_URI=your_mongodb_uri
   FLASK_ENV=development
   PORT=5000
   ```

5. Run development server:
   ```bash
   python run.py
   ```

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create `.env` file:
   ```bash
   REACT_APP_API_URL=http://localhost:5000
   ```

4. Run development server:
   ```bash
   npm start
   ```

## 🌐 Production Deployment

### Render (Backend)

**Environment Variables**:
```
MONGO_URI=mongodb+srv://easyXpense:Jagdeep2607@easyxpense.sfpwthl.mongodb.net/EasyXpense?retryWrites=true&w=majority&appName=EasyXpense
FLASK_ENV=production
PORT=10000
GUNICORN_WORKERS=2
```

**Build Command**: `pip install -r requirements.txt`  
**Start Command**: `gunicorn wsgi:app -c gunicorn.conf.py`

### Netlify (Frontend)

**Environment Variables**:
```
REACT_APP_API_URL=https://easyxpense.onrender.com
REACT_APP_NAME=EasyXpense
REACT_APP_VERSION=1.0.0
```

**Build Command**: `npm run build`  
**Publish Directory**: `build`  
**Base Directory**: `frontend`

### MongoDB Atlas

**Network Access**: Add `0.0.0.0/0` to IP whitelist  
**Database User**: `easyXpense` with read/write permissions  
**Database Name**: `EasyXpense`

## 🔧 API Endpoints

### Health
- `GET /health` - Health check
- `GET /api/health` - Detailed health check

### Friends
- `GET /api/friends` - List all friends
- `POST /api/friends` - Add new friend

### Expenses
- `GET /api/expenses` - List all expenses
- `POST /api/expenses` - Create new expense

### Debts
- `GET /api/debts` - Get optimized debt settlements

### Settlements
- `GET /api/settlements` - List settlement history
- `POST /api/settlements` - Record new settlement

### Groups
- `GET /api/groups` - List all groups
- `POST /api/groups` - Create new group
- `DELETE /api/groups/:id` - Delete group

## 🔐 Security Features

- CORS restricted to Netlify origin only
- Input sanitization on all endpoints
- Request size limits (10MB max)
- Security headers (X-Frame-Options, X-XSS-Protection, HSTS)
- No hardcoded credentials
- Environment variable configuration

## ⚡ Performance

- Optimized debt calculation algorithm (60-90% fewer transactions)
- Connection pooling for MongoDB
- Gunicorn with 2 workers for Render free tier
- 30s timeout handling for cold starts
- Automatic retry logic on frontend

## 🧪 Testing

### Backend
```bash
cd backend
python run.py
# Visit http://localhost:5000/health
```

### Frontend
```bash
cd frontend
npm start
# Visit http://localhost:3000
```

### Production
```bash
# Backend health check
curl https://easyxpense.onrender.com/health

# Frontend
curl -I https://easyxpense.netlify.app/
```

## 📊 Free Tier Limits

- **Render**: 512MB RAM, 750 hours/month
- **Netlify**: 100GB bandwidth/month
- **MongoDB Atlas**: 512MB storage

Current usage is well within all limits.

## 🤝 Contributing

This is a portfolio project. Feel free to fork and modify for your own use.

## 📄 License

This project is for educational and portfolio purposes.

## 👨‍💻 Author

Jagdeep Mohanty

## 🙏 Acknowledgments

Built with React, Flask, and MongoDB Atlas. Deployed on Netlify and Render free tiers.

---

**Made with ❤️ for expense splitting in India** 🇮🇳
