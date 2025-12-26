# 🚀 QUICK START GUIDE

## Prerequisites
- Python 3.8+
- Node.js 16+
- NewsData.io API key (get from https://newsdata.io)

## Setup (First Time Only)

### 1. Install Dependencies
```bash
# Backend + AI Service
pip install -r requirements.txt

# Frontend
cd frontend
npm install
cd ..
```

### 2. Configure Environment
Create `.env` in project root:
```env
NEWSDATA_API_KEY=your_actual_api_key_here
DATABASE_URL=sqlite:///./disaster_local.db
AI_SERVICE_URL=http://127.0.0.1:8002
```

Create `frontend/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Running the Application

### Option 1: Manual (3 Terminals)

**Terminal 1 - AI Service:**
```bash
python -m ai_service.api
```
Wait for "Application startup complete" message.

**Terminal 2 - Backend:**
```bash
$env:DATABASE_URL="sqlite:///./disaster_local.db"
$env:AI_SERVICE_URL="http://127.0.0.1:8002"
python -m uvicorn backend.app.main:app --port 8000 --reload
```
Wait for "Application startup complete" message.

**Terminal 3 - Frontend:**
```bash
cd frontend
npm run dev
```
Wait for "Ready" message.

### Option 2: Verify System
After starting all services, run:
```bash
python verify_system.py
```

This will check if all services are running correctly.

## Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **AI Service**: http://localhost:8002
- **API Docs**: http://localhost:8000/docs

## Using the Application

### Submit a Report
1. Go to http://localhost:3000
2. Click "Report Incident"
3. Choose input mode (Text, URL, or PDF)
4. Fill in details:
   - Your report text/URL/file
   - Category (optional - AI will detect)
   - Location (optional - AI will extract)
   - Your name (optional - defaults to "Anonymous")
5. Click "Submit Report"
6. AI will process it and show results

### View Reports
1. Go to http://localhost:3000
2. See all reports on the dashboard
3. Each card shows:
   - Disaster category
   - Verification status
   - AI-generated summary
   - Confidence score
   - Location
   - Who submitted it

### View Verified News
1. Click "Verified News" in navigation
2. See AI-verified news from multiple sources
3. Filter by category
4. Search by location or keyword

## Testing

### Quick Test
```bash
python test_complete_integration.py
```

### Comprehensive Test
```bash
python backend_comprehensive_test.py
```

## Troubleshooting

### "Failed to fetch reports" error
- Make sure Backend is running on port 8000
- Check `frontend/.env.local` has correct API URL
- Verify CORS is enabled in backend

### AI Service not responding
- Check if port 8002 is available
- Verify models are downloading (first run takes time)
- Check `NEWSDATA_API_KEY` is set correctly

### Frontend shows no data
- Check browser console for errors
- Verify Backend is accessible at http://localhost:8000
- Run `python verify_system.py` to check all services

## Important Notes

- **First AI Service startup** takes 2-3 minutes (downloading models)
- **TEST_MODE is enabled** - only fetches 5 news articles for faster testing
- **Database** is SQLite, stored in `disaster_local.db`
- **Anonymous submissions** are allowed (name field is optional)

## Production Deployment

To disable TEST_MODE for production:
1. Edit `ai_service/api.py`
2. Find lines with `test_mode=True`
3. Change to `test_mode=False`
4. Restart AI Service

See `TEST_MODE_README.md` for details.

## Need Help?

1. Check `COMPLETE_INTEGRATION_SUMMARY.md` for full documentation
2. Run `python verify_system.py` to diagnose issues
3. Check terminal logs for error messages

---

**Ready to go!** 🎉

Start all three services and visit http://localhost:3000
