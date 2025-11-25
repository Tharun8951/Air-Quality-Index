# Quick Setup Guide

## Fast Track Setup (2 methods available)

### Method 1: Docker (Recommended - 3 minutes)

This is the easiest way. Everything runs in containers.

#### Step 1: Get API Key (2 minutes)

1. Go to https://openweathermap.org/api
2. Click "Sign Up" (free tier)
3. Verify email
4. Go to "API keys" tab
5. Copy your API key

#### Step 2: Configure Backend (1 minute)

Create `backend/.env` file:

```env
OPENWEATHER_API_KEY=paste_your_key_here
```

That's it for configuration!

#### Step 3: Run Everything (1 command)

**Windows/Linux:**
```bash
python run.py
```

**Mac/Linux (alternative):**
```bash
chmod +x run.sh
./run.sh
```

This automatically:
- Starts Redis
- Starts Django backend
- Starts React frontend
- Runs database migrations

Access:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000

To stop: Press `Ctrl+C`

---

### Method 2: Manual Setup (5-10 minutes)

If you prefer not to use Docker or want to develop locally.

#### 1. Get API Key (2 minutes)

Same as Method 1 above.

#### 2. Configure Backend (1 minute)

Create `backend/.env` file:

```env
OPENWEATHER_API_KEY=paste_your_key_here
```

#### 3. Start Backend (2 minutes)

```bash
cd backend

# First time only:
python -m venv venv
.\venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
python manage.py migrate

# Every time:
.\venv\Scripts\activate
python manage.py runserver
```

Backend runs at: http://localhost:8000

#### 4. Start Frontend (2 minutes)

Open new terminal:

```bash
cd frontend

# First time only:
npm install

# Every time:
npm run dev
```

Frontend runs at: http://localhost:5173

---

## Test It Works

1. Open http://localhost:5173
2. Type "London" in search box
3. Click "Search"
4. You should see air quality data with pollutants, WHO guidelines, and forecast

---

## Troubleshooting

**"Invalid API key"**
- Check backend/.env file exists and has correct key
- Wait 10-15 minutes after creating key (activation time)
- Restart backend/containers after adding key

**"City not found"**
- Try major cities: London, Paris, Tokyo, New York
- Check spelling

**Docker: Port already in use**
- Stop other services using ports 8000, 5173, or 6379
- Or use: docker compose down

**Manual Setup: Backend won't start**
- Make sure you activated virtual environment
- Check Python version: python --version (need 3.10+)

**Manual Setup: Frontend won't start**
- Check Node version: node --version (need 20+)
- Delete node_modules and run npm install again

---

## What You Need

**For Docker Method:**
- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Python 3.10+ (to run run.py script)
- OpenWeatherMap API key

**For Manual Method:**
- Python 3.10+ (https://www.python.org/downloads/)
- Node.js 20+ (https://nodejs.org/)
- Git (https://git-scm.com/)
- OpenWeatherMap API key

---

## Docker Commands (Method 1 only)

```bash
# Start all services
docker compose up

# Start in background
docker compose up -d

# Stop all services
docker compose down

# View logs
docker compose logs

# Rebuild after code changes
docker compose up --build
```

---

## Next Steps

After testing locally:

1. **Make changes** to code
2. **Test** in browser
3. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Your message"
   git push
   ```

---

## More Info

- Full documentation: README.md
- API endpoints: API_DOCUMENTATION.md
- Environment setup: .env.example

---

Need help? Check the full README for detailed troubleshooting.
