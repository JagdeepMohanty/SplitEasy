# SplitEasy - Expense Splitting Application

A modern expense splitting application built with React frontend and Python Flask backend, designed for Indian Rupee (INR) transactions.

## 🏗️ Project Structure

```
/
├── frontend/                # React.js application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── contexts/        # React contexts (Auth)
│   │   ├── pages/           # Page components
│   │   ├── services/        # API service layer
│   │   └── utils/           # Utility functions
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── backend/                 # Flask application
│   ├── app/
│   │   ├── routes/          # API route handlers
│   │   ├── models/          # Database models
│   │   ├── middleware/      # Custom middleware
│   │   ├── utils/           # Utility functions
│   │   └── __init__.py      # Flask app factory
│   ├── run.py               # Application entry point
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Environment variables template
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

2. **Create and activate virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your MongoDB URI and JWT secret
   ```

5. **Start the backend server:**
   ```bash
   python run.py
   ```
   Backend will run on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure environment (optional):**
   ```bash
   cp .env.example .env
   # Edit .env if needed (default API URL is http://localhost:5000)
   ```

4. **Start development server:**
   ```bash
   npm run dev
   ```
   Frontend will run on `http://localhost:5173`

## 🔧 Environment Configuration

### Backend (.env)
```env
# MongoDB Connection
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/spliteasy?retryWrites=true&w=majority

# JWT Secret (Generate a secure random string for production)
JWT_SECRET=your-super-secure-jwt-secret-key-change-this-in-production

# Frontend URL for CORS
CLIENT_URL=http://localhost:5173

# Server Configuration
PORT=5000
FLASK_ENV=development
FLASK_DEBUG=True
```

### Frontend (.env)
```env
# API Base URL (Backend URL)
VITE_API_URL=http://localhost:5000

# App Configuration
VITE_APP_NAME=SplitEasy
VITE_APP_VERSION=1.0.0
```

## 🌟 Features

- **🔐 Secure Authentication**: JWT-based user authentication with bcrypt password hashing
- **👥 Friend Management**: Add and manage friends by email
- **💰 Expense Tracking**: Create and track shared expenses in Indian Rupees (₹)
- **📊 Debt Calculation**: Automatic debt calculation and tracking between friends
- **💳 Settlement System**: Record payments to settle debts
- **🇮🇳 INR Currency**: Native Indian Rupee support with proper formatting
- **📱 Responsive Design**: Mobile-friendly interface
- **🛡️ Input Validation**: Comprehensive validation on both frontend and backend

## 🔒 Security Features

- JWT token-based authentication
- Password hashing with bcrypt
- Input validation and sanitization
- CORS configuration for secure cross-origin requests
- Environment variable protection
- SQL injection prevention with MongoDB

## 📱 How to Use

1. **Register/Login**: Create a new account or login with existing credentials
2. **Add Friends**: Add friends by their email addresses
3. **Create Expenses**: Add shared expenses with selected participants
4. **Track Debts**: View who owes what in the debt tracker
5. **Settle Up**: Record payments to settle debts between friends

## 🚀 Production Deployment

### Backend Deployment
```bash
# Install production dependencies
pip install -r requirements.txt

# Set production environment variables
export FLASK_ENV=production
export FLASK_DEBUG=False

# Run with Gunicorn
gunicorn wsgi:app --bind 0.0.0.0:5000
```

### Frontend Deployment
```bash
# Build for production
npm run build

# Serve the dist folder with any static file server
# Example with serve:
npx serve -s dist -l 3000
```

## 📊 API Endpoints

### Authentication
- `POST /api/users/register` - User registration
- `POST /api/users/login` - User login
- `GET /api/users/me` - Get current user profile

### Friends Management
- `GET /api/friends` - Get user's friends list
- `POST /api/friends/add` - Add a friend by email

### Expense Management
- `GET /api/expenses` - Get user's expenses
- `POST /api/expenses` - Create a new expense

### Settlements
- `GET /api/settlements` - Get user's settlements
- `POST /api/settlements` - Create a new settlement

### Debt Tracking
- `GET /api/debts` - Get debt summary with all friends

### System
- `GET /api/health` - Health check endpoint

## 💰 Currency Handling

- All amounts stored as precise decimal values in the database
- INR currency symbol (₹) displayed throughout the UI
- Proper rounding to paise (0.01 INR) precision
- Indian number formatting support
- Input validation for reasonable amount limits

## 🛠️ Tech Stack

### Frontend
- **React 18** - Modern React with hooks
- **React Router** - Client-side routing
- **Axios** - HTTP client for API calls
- **Vite** - Fast build tool and dev server

### Backend
- **Python Flask** - Lightweight web framework
- **PyMongo** - MongoDB driver for Python
- **JWT** - JSON Web Token authentication
- **bcrypt** - Password hashing
- **Flask-CORS** - Cross-origin resource sharing

### Database
- **MongoDB Atlas** - Cloud-hosted MongoDB

## 🧪 Development

### Running Tests
```bash
# Backend tests (if implemented)
cd backend
python -m pytest

# Frontend tests (if implemented)
cd frontend
npm test
```

### Code Quality
- Follow PEP 8 for Python code
- Use ESLint and Prettier for JavaScript/React code
- Implement proper error handling
- Add comprehensive logging

## 🐛 Troubleshooting

### Common Issues

1. **MongoDB Connection Error**
   - Verify MongoDB URI in `.env` file
   - Check network connectivity
   - Ensure MongoDB Atlas IP whitelist includes your IP

2. **CORS Errors**
   - Verify `CLIENT_URL` in backend `.env` matches frontend URL
   - Check if both servers are running

3. **Authentication Issues**
   - Verify JWT secret is set in backend `.env`
   - Check if token is being sent in request headers

4. **Port Conflicts**
   - Backend default: 5000
   - Frontend default: 5173
   - Change ports in respective configuration files if needed

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify all environment variables are properly configured
3. Check application logs for detailed error messages
4. Ensure all dependencies are installed correctly

## 📄 License

This project is for educational and portfolio purposes.

---

**Made with ❤️ for expense splitting in India** 🇮🇳