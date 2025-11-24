# Quick Setup Guide

## Fast Track Setup (about 5-10 minutes)

### 1. Get API Key

1. Go to https://openweathermap.org/api
2. Click "Sign Up" (free tier)
3. Verify email
4. Go to "API keys" tab
5. Copy your API key

### 2. Configure Backend

Create .env file in backend/ directory:

```env
OPENWEATHER_API_KEY=paste_your_key_here
```

That's it. Other settings have defaults.

### 3. Start Backend

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

### 4. Start Frontend

Open new terminal:

```bash
cd frontend

# First time only:
npm install

# Every time:
npm run dev
```

Frontend runs at: http://localhost:5173

## Test It Works

1. Open http://localhost:5173
2. Type "London" in search box
3. Click "Search"
4. You should see air quality data

## Troubleshooting

**"Invalid API key"**
- Check .env file in backend/ folder
- Wait 10-15 minutes after creating key (activation time)
- Restart backend server after adding key

**"City not found"**
- Try major cities: London, Paris, Tokyo, New York
- Check spelling

**Backend won't start**
- Make sure you activated virtual environment
- Check Python version: python --version (need 3.10+)

**Frontend won't start**
- Check Node version: node --version (need 20+)
- Delete node_modules and run npm install again

## What You Need

- Python 3.10+ (https://www.python.org/downloads/)
- Node.js 20+ (https://nodejs.org/)
- Git (https://git-scm.com/)

## Next Steps

After testing locally:

1. Create GitHub repo:
   ```bash
   git init
   git add .
   git commit -m "Air Quality Search Engine"
   git remote add origin https://github.com/yourusername/air-quality.git
   git push -u origin main
   ```

2. Submit:
   - Reply to coding challenge email
   - Don't change subject line
   - Include: GitHub link

## More Info

- Full setup: README.md
- API docs: API_DOCUMENTATION.md

---

Need help? Check the full README for detailed troubleshooting.
