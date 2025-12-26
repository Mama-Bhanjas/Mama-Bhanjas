# TEST MODE Configuration

## Current Status
**TEST_MODE is ENABLED** - The system will fetch and process only **5 news articles** instead of all available articles.

## Why This Exists
During development and testing, processing all news articles can take 5-10 minutes because each article goes through:
- Classification
- Summarization  
- Named Entity Recognition (NER)
- Verification

Limiting to 5 articles reduces startup time to ~1-2 minutes.

## How to Disable for Production

### Option 1: In `ai_service/api.py`
Find these two locations and change `test_mode=True` to `test_mode=False`:

**Location 1 - Background Refresh Task (line ~528):**
```python
# Change this:
fetcher = MultiSourceFetcher(news_api_key=key, test_mode=True)

# To this:
fetcher = MultiSourceFetcher(news_api_key=key, test_mode=False)
```

**Location 2 - Manual Fetch Endpoint (line ~503):**
```python
# Change this:
fetcher = MultiSourceFetcher(news_api_key=key, test_mode=True)

# To this:
fetcher = MultiSourceFetcher(news_api_key=key, test_mode=False)
```

### Option 2: Environment Variable (Recommended for Production)
Add this to your `.env` file:
```env
TEST_MODE=false
```

Then update the code to read from environment:
```python
test_mode = os.getenv("TEST_MODE", "true").lower() == "true"
fetcher = MultiSourceFetcher(news_api_key=key, test_mode=test_mode)
```

## What Happens When Disabled
- The system will fetch ALL available news articles from NewsData.io (typically 20-50 articles)
- Each article will be processed through the full AI pipeline
- First startup will take 5-10 minutes
- Subsequent requests will be instant (served from cache)
- Background refresh runs once every 24 hours
