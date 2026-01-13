# EasyXpense - Expense Splitting Application

A modern, no-authentication expense splitting application built with React.js frontend and Python Flask backend, designed for Indian Rupee (INR) transactions.

## 🌟 Features

- **💰 Expense Splitting**: Easily split expenses among friends
- **📊 Debt Tracking**: See who owes what and how much
- **💳 Payment Reminders**: Track outstanding debts
- **📱 Payment History**: Complete log of expenses and settlements
- **🇮🇳 INR Currency**: Native Indian Rupee support with proper formatting
- **🚫 No Authentication**: Direct access without login/registration
- **📱 Responsive Design**: Works perfectly on mobile and desktop

## 🏗️ Project Structure

```
/
├── frontend/                # React.js application
│   ├── public/
│   │   ├── _redirects      # Netlify SPA routing
│   │   └── index.html
│   ├── src/
│   │   ├── components/     # Reusable components (Navbar, Footer)
│   │   ├── pages/          # Page components
│   │   │   ├── Home.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── AddExpense.jsx
│   │   │   ├── Friends.jsx
│   │   │   ├── DebtTracker.jsx
│   │   │   └── PaymentHistory.jsx
│   │   ├── services/       # API integration
│   │   ├── utils/          # Currency & calculation utilities
│   │   ├── styles/         # CSS styles
│   │   ├── App.jsx
│   │   └── index.js
│   ├── package.json
│   └── .env.example
│
├── backend/                 # Flask application
│   ├── app/
│   │   ├── routes/          # API endpoints
│   │   ├── models/          # Database models
│   │   ├── middleware/      # Custom middleware
│   │   └── __init__.py
│   ├── run.py
│   ├── requirements.txt
│   └── .env.example
│
├── .gitignore
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm
- Python 3.8+
- MongoDB Atlas account

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your MongoDB URI and JWT secret
   ```

5. **Start backend:**
   ```bash
   python run.py
   ```
   Backend runs on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with backend URL if needed
   ```

4. **Start frontend:**
   ```bash
   npm start
   ```
   Frontend runs on `http://localhost:3000`

## 🔧 Environment Configuration

### Backend (.env)
```env
MONGO_URI=mongodb+srv://<user>:<password>@cluster.mongodb.net/easyxpense
JWT_SECRET=your-secure-secret-key
FLASK_ENV=production
PORT=5000
```

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:5000
REACT_APP_NAME=EasyXpense
REACT_APP_VERSION=1.0.0
```

## 📱 Application Pages

### 🏠 **Home**
- Welcome page with feature overview
- How it works section
- Quick access to main features

### 📊 **Dashboard**
- Expense summary and statistics
- Recent expenses overview
- Debt summary with friends
- Quick action buttons

### 💰 **Add Expense**
- Create new shared expenses
- Select payer and participants
- Automatic split calculation
- INR amount validation

### 👥 **Friends**
- Add new friends by name and email
- View all friends list
- Friend management

### 📈 **Debt Tracker**
- Complete debt overview
- See who owes what
- Settle debts functionality
- Net balance calculations

### 📋 **Payment History**
- All expenses history
- Settlement records
- Filterable by type
- Date-wise organization

## 🛠️ Tech Stack

### Frontend
- **React 18** - Modern React with hooks
- **React Router DOM** - Client-side routing
- **Axios** - HTTP client for API calls
- **Create React App** - Standard React setup

### Backend
- **Python Flask** - Lightweight web framework
- **PyMongo** - MongoDB driver
- **JWT** - Token authentication
- **bcrypt** - Password hashing

### Database
- **MongoDB Atlas** - Cloud-hosted MongoDB

## 🌐 API Endpoints

### Expenses
- `GET /api/expenses` - Get all expenses
- `POST /api/expenses` - Create new expense

### Debts
- `GET /api/debts` - Get debt summary

### Settlements
- `GET /api/settlements` - Get settlement history
- `POST /api/settlements` - Create new settlement

### Friends
- `GET /api/friends` - Get all friends
- `POST /api/friends` - Add new friend

## 💰 Currency Features

- **INR Formatting**: Proper Indian Rupee display with ₹ symbol
- **Decimal Precision**: Accurate to paise (0.01 INR)
- **Input Validation**: Prevents invalid amounts
- **Split Calculations**: Automatic per-person amount calculation
- **Indian Number Format**: Uses en-IN locale formatting

## 🚀 Production Deployment

### Frontend (Netlify)
1. Connect GitHub repository to Netlify
2. Set build command: `npm run build`
3. Set publish directory: `build`
4. Set environment variable: `REACT_APP_API_URL`

### Backend (Render/Heroku)
1. Connect GitHub repository
2. Set environment variables
3. Deploy with: `gunicorn run:app`

## 📋 Backend API Requirements

The frontend expects these API endpoints to be available:

```javascript
// Expenses API
GET /api/expenses
POST /api/expenses
Body: { description, amount, payer, participants[] }

// Debts API  
GET /api/debts
Response: [{ friendId, friendName, amount }]

// Settlements API
GET /api/settlements
POST /api/settlements
Body: { fromUserId, toUserId, amount }

// Friends API
GET /api/friends
POST /api/friends
Body: { name, email }
```

## 🔍 Key Features

### No Authentication Required
- Direct access to all features
- No login/registration process
- Simplified user experience

### Responsive Design
- Mobile-first approach
- Touch-friendly interface
- Adaptive layouts for all screen sizes

### Professional UI
- Clean, modern design
- Consistent color scheme
- Intuitive navigation
- Loading states and error handling

### INR-Focused
- Native Indian Rupee support
- Proper currency formatting
- Paise-level precision
- Indian number formatting

## 🐛 Troubleshooting

### Common Issues

1. **API Connection Error**
   - Verify `REACT_APP_API_URL` in frontend `.env`
   - Ensure backend is running on correct port
   - Check CORS configuration

2. **Build Errors**
   - Run `npm install` to ensure all dependencies
   - Check for any missing environment variables
   - Verify all imports are correct

3. **Deployment Issues**
   - Ensure `_redirects` file exists for Netlify
   - Set correct environment variables in hosting platform
   - Check build logs for specific errors

## 📄 License

This project is for educational and portfolio purposes.

---

**Made with ❤️ for expense splitting in India** 🇮🇳