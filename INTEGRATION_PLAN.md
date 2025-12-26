# System Integration Status & Implementation Plan

## 1. Current Integration Status
The **Backend** (`port 8000`) and **AI Service** (`port 8002`) are currently integrated for **AI Processing tasks only**. The **Real-time News (Fetchers)** component is currently **isolated**.

| Component | Functionality | Status | Integration Method |
| :--- | :--- | :--- | :--- |
| **Unified Processor** | Classification, NER, Summarization | ✅ **Integrated** | `backend.services.ai_pipeline.process_report()` calls `POST /api/process/report` |
| **Verifier** | Fake News & Fact Checking | ✅ **Integrated** | `backend.services.ai_pipeline` calls `/api/verify/*` endpoints |
| **Real-time News** | Aggregating Nepal Disaster News | ❌ **Not Integrated** | The Backend has no awareness of the `/api/realtime/news` endpoint. The Frontend likely has to call AI Service directly or isn't using it yet. |

## 2. Integration Goal
To create a clean, unified architecture where the **Backend** acts as the single API Gateway for the Frontend. The Backend will proxy news requests to the AI Service, ensuring consistent security and domain logic.

**Target Architecture:**
`Frontend` -> `Backend (Port 8000)` -> `AI Service (Port 8002)`

## 3. Implementation Plan

### Step 1: Update AI Client Wrapper
Modify `backend/app/services/ai_pipeline.py` to include a method for fetching the cached news.
- **Action**: Add `get_realtime_news()` method.
- **Details**: It will perform a `GET` request to `${AI_SERVICE_URL}/api/realtime/news`.

### Step 2: Create News Router
Create a new route in the Backend to expose this data.
- **File**: `backend/app/routes/news.py`
- **Endpoint**: `GET /news/realtime`
- **Logic**: Call `ai_pipeline.get_realtime_news()` and return the JSON response.

### Step 3: Register Router
Register the new router in the main application entry point.
- **File**: `backend/app/main.py`
- **Action**: Add `app.include_router(news.router, prefix="/news", tags=["news"])`

### Step 4: Verification
- Verify that `http://localhost:8000/news/realtime` returns the same data as `http://localhost:8002/api/realtime/news`.
