# Immigration Client CRM - MERN Stack Version

A full-stack MERN (MongoDB, Express, React, Node.js) application for immigration attorneys to manage client cases. This version demonstrates a modern JavaScript-based tech stack with separate frontend and backend.

## Tech Stack

- **Frontend**: React 18 with Vite
- **Backend**: Node.js with Express
- **Database**: MongoDB with Mongoose ODM
- **Styling**: CSS3 (modern responsive design)
- **State Management**: React Hooks (useState, useEffect)
- **HTTP Client**: Axios

## Features

- **CRUD Operations**: Create, Read, Update, and Delete immigration client records
- **Client Management**: Track personal information, visa types, case status, and important dates
- **RESTful API**: Fully featured REST API with proper HTTP methods
- **Responsive UI**: Modern, mobile-friendly interface
- **Form Validation**: Client-side and server-side validation
- **Case Tracking**: Monitor filing dates, priority dates, and case statuses
- **Visa Types**: Support for H-1B, L-1, O-1, EB-1/2/3, F-1, Green Card, Citizenship, Asylum, and more
- **Real-time Updates**: Automatic UI updates after CRUD operations

## Prerequisites

- Node.js 18.x or higher
- npm or yarn
- MongoDB (local installation or MongoDB Atlas account)

## Project Structure

```
immigration-crm-mern/
├── client/                    # React frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── ClientList.jsx
│   │   │   ├── ClientDetail.jsx
│   │   │   ├── ClientForm.jsx
│   │   │   └── Navbar.jsx
│   │   ├── services/         # API services
│   │   │   └── api.js
│   │   ├── App.jsx           # Main app component
│   │   ├── App.css           # Styles
│   │   └── main.jsx          # Entry point
│   ├── package.json
│   └── vite.config.js
├── server/                   # Express backend
│   ├── models/
│   │   └── Client.js         # Mongoose schema
│   ├── routes/
│   │   └── clients.js        # API routes
│   ├── config/
│   │   └── db.js             # Database connection
│   ├── server.js             # Express server
│   └── package.json
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## Installation & Setup

### 1. Clone or navigate to the project directory

```bash
cd immigration-crm-mern
```

### 2. Set up MongoDB

**Option A: Local MongoDB**
- Install MongoDB Community Edition from https://www.mongodb.com/try/download/community
- Start MongoDB service:
  ```bash
  # macOS (with Homebrew)
  brew services start mongodb-community

  # Linux
  sudo systemctl start mongod

  # Windows
  # MongoDB should start automatically or use Services manager
  ```

**Option B: MongoDB Atlas (Cloud)**
- Create a free account at https://www.mongodb.com/cloud/atlas
- Create a cluster and get your connection string
- Whitelist your IP address
- Create a database user

### 3. Configure Environment Variables

Create a `.env` file in the `server/` directory:

```env
PORT=5000
MONGODB_URI=mongodb://localhost:27017/immigration_crm
# Or for MongoDB Atlas:
# MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/immigration_crm
```

### 4. Install Backend Dependencies

```bash
cd server
npm install
```

### 5. Install Frontend Dependencies

```bash
cd ../client
npm install
```

## Running the Application

You'll need to run both the backend and frontend servers.

### Terminal 1: Start the Backend Server

```bash
cd server
npm start
```

The API server will run on http://localhost:5000

### Terminal 2: Start the Frontend Development Server

```bash
cd client
npm run dev
```

The React app will run on http://localhost:5173

### Access the Application

Open your browser and navigate to http://localhost:5173

## API Endpoints

The backend provides the following RESTful API endpoints:

- `GET /api/clients` - Get all clients
- `GET /api/clients/:id` - Get a specific client
- `POST /api/clients` - Create a new client
- `PUT /api/clients/:id` - Update a client
- `DELETE /api/clients/:id` - Delete a client

## Data Model

The `Client` schema (MongoDB/Mongoose):

```javascript
{
  firstName: String (required),
  lastName: String (required),
  email: String (required, validated),
  phone: String,
  caseNumber: String (required, unique),
  visaType: String (enum, required),
  currentStatus: String (enum, default: 'INITIAL_CONSULTATION'),
  countryOfOrigin: String (required),
  filingDate: Date,
  priorityDate: Date,
  notes: String,
  createdAt: Date (auto),
  updatedAt: Date (auto)
}
```

**Visa Types**:
- H1B, L1, O1, EB1, EB2, EB3, F1, GREEN_CARD, CITIZENSHIP, ASYLUM, OTHER

**Status Options**:
- INITIAL_CONSULTATION, DOCUMENTS_GATHERING, APPLICATION_PREP, FILED, RFE, APPROVED, DENIED, WITHDRAWN

## Development

### Backend Development

The backend uses:
- **Express** for routing and middleware
- **Mongoose** for MongoDB object modeling
- **CORS** for cross-origin requests
- **dotenv** for environment variables

Key files:
- `server.js` - Express app configuration
- `models/Client.js` - Mongoose schema
- `routes/clients.js` - API route handlers
- `config/db.js` - Database connection

### Frontend Development

The frontend uses:
- **React** with functional components and hooks
- **Vite** for fast development and building
- **Axios** for HTTP requests
- **React Router** for navigation (if implemented)

Key files:
- `App.jsx` - Main application component
- `components/` - Reusable React components
- `services/api.js` - API client configuration

## Building for Production

### Build the Frontend

```bash
cd client
npm run build
```

This creates optimized production files in `client/dist/`

### Serve the Production Build

You can configure the Express server to serve the React build:

```javascript
// In server/server.js
const path = require('path');

// Serve static files from React app
app.use(express.static(path.join(__dirname, '../client/dist')));

// Catch-all handler for React routing
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../client/dist/index.html'));
});
```

Then run only the backend server, which will serve both API and frontend.

## Testing

### Manual Testing

1. **Create a client**: Click "Add New Client" and fill out the form
2. **View clients**: Check the client list on the homepage
3. **View details**: Click on a client to see full details
4. **Update client**: Use the edit button to modify client information
5. **Delete client**: Use the delete button (with confirmation)

### Using API Testing Tools

Test the API directly with Postman, Insomnia, or curl:

```bash
# Get all clients
curl http://localhost:5000/api/clients

# Create a client
curl -X POST http://localhost:5000/api/clients \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com",
    "caseNumber": "CASE-2025-001",
    "visaType": "H1B",
    "countryOfOrigin": "India"
  }'
```

## Environment Variables

### Server (.env)

- `PORT` - Server port (default: 5000)
- `MONGODB_URI` - MongoDB connection string
- `NODE_ENV` - Environment (development/production)

### Client

The frontend uses Vite's environment variable system. Prefix variables with `VITE_`:

```env
VITE_API_URL=http://localhost:5000/api
```

## Troubleshooting

### MongoDB Connection Issues

- Verify MongoDB is running: `mongosh` (or `mongo`)
- Check connection string in `.env`
- For Atlas: verify IP whitelist and credentials

### Port Already in Use

If port 5000 or 5173 is taken:
- Change `PORT` in server `.env`
- Update proxy in `client/vite.config.js`

### CORS Errors

- Ensure backend CORS is configured for frontend origin
- Check that API URLs in frontend match backend

### Module Not Found

```bash
# Reinstall dependencies
cd server && rm -rf node_modules && npm install
cd ../client && rm -rf node_modules && npm install
```

## Deployment

### Backend Deployment (Heroku, Railway, Render)

1. Ensure `package.json` has start script
2. Set environment variables
3. Connect MongoDB Atlas
4. Deploy from Git repository

### Frontend Deployment (Vercel, Netlify)

1. Build the frontend: `npm run build`
2. Deploy the `dist/` folder
3. Set environment variables for API URL
4. Configure redirects for SPA routing

## Known Issues & Deviations

- No authentication/authorization implemented (suitable for internal use)
- Form validation is basic (could be enhanced with libraries like Formik or React Hook Form)
- No pagination on client list (all clients loaded at once)
- No search/filter functionality yet
- Error handling could be more robust

## Future Enhancements

- User authentication (JWT-based)
- Document upload and storage (AWS S3, Cloudinary)
- Email notifications for status changes
- Advanced search and filtering
- Data export (PDF, CSV)
- Case timeline and activity log
- Multi-user support with roles

## License

This project is for educational purposes.
