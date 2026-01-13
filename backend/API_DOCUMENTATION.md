# EasyXpense Backend API Documentation

## Base URL
- **Production**: `https://easyxpense-backend.onrender.com`
- **Development**: `http://localhost:5000`

## API Endpoints

### Health Check
- **GET** `/api/health` - Health check endpoint
- **GET** `/api/` - Root endpoint

### Friends Management
- **GET** `/api/friends` - Get all friends
- **POST** `/api/friends` - Add a new friend

#### POST /api/friends
```json
{
  "name": "John Doe",
  "email": "john@example.com"
}
```

### Expenses Management
- **GET** `/api/expenses` - Get all expenses
- **POST** `/api/expenses` - Create a new expense

#### POST /api/expenses
```json
{
  "description": "Dinner at restaurant",
  "amount": 1200.50,
  "payer": "John Doe",
  "participants": ["John Doe", "Jane Smith", "Bob Wilson"]
}
```

### Debt Tracking
- **GET** `/api/debts` - Get debt summary between all friends

#### Response Format
```json
[
  {
    "debtor": "Jane Smith",
    "creditor": "John Doe", 
    "amount": 400.25
  }
]
```

### Settlements (Payment History)
- **GET** `/api/settlements` - Get payment history
- **POST** `/api/settlements` - Record a payment

#### POST /api/settlements
```json
{
  "fromUser": "Jane Smith",
  "toUser": "John Doe",
  "amount": 400.00
}
```

## Data Validation

### Amount Validation
- Must be positive number
- Maximum: ₹10,00,000 (10 lakh INR)
- Precision: 2 decimal places (paise)
- Currency: INR

### String Validation
- Names: Max 100 characters
- Descriptions: Max 200 characters
- Emails: Valid email format, max 254 characters

### Business Rules
- Payer must be included in participants
- Cannot settle with yourself
- Duplicate friends (by email) not allowed
- Maximum 50 participants per expense

## Error Responses

All errors return JSON with `error` field:

```json
{
  "error": "Description of the error"
}
```

### HTTP Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation error)
- `404` - Not Found
- `405` - Method Not Allowed
- `500` - Internal Server Error
- `503` - Service Unavailable (database issues)

## Database Collections

### friends
```json
{
  "_id": "ObjectId",
  "name": "string",
  "email": "string",
  "created_at": "datetime"
}
```

### expenses
```json
{
  "_id": "ObjectId",
  "description": "string",
  "amount": "number",
  "payer": "string",
  "participants": ["string"],
  "date": "datetime",
  "currency": "INR"
}
```

### settlements
```json
{
  "_id": "ObjectId",
  "fromUser": "string",
  "toUser": "string", 
  "amount": "number",
  "date": "datetime",
  "currency": "INR"
}
```

## Environment Variables

Required environment variables:

```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/easyxpense
FLASK_ENV=production
PORT=5000
```

## CORS Configuration

Allowed origins:
- `https://easyxpense.netlify.app` (production)
- `http://localhost:3000` (development)
- `http://localhost:5173` (development)

## Deployment

### Render Deployment
- Uses `wsgi.py` as entry point
- Gunicorn with 2 workers, 120s timeout
- Automatic deployment from GitHub main branch

### Local Development
```bash
cd backend
pip install -r requirements.txt
python run.py
```

## Performance Features

- MongoDB indexes on date, payer, and participants
- Connection pooling with 5s timeout
- Efficient debt calculation algorithm
- Proper error logging and monitoring