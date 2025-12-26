# D-Brief: Decentralized Disaster Intelligence and Verification Platform

**Status**: Operational  
**License**: MIT  
**Framework**: Next.js 14 | FastAPI | Python 3.11+  
**AI Models**: Fine-tuned HuggingFace Transformers

D-Brief is an AI-powered disaster response and intelligence platform that provides real-time, verified situational awareness during humanitarian crises. The system combines multi-source data ingestion, advanced NLP processing, and a decentralized verification architecture to bridge the gap between field reports and official government data.

---

## 🎯 Key Features

### Multi-Input Report Processing
- **Text Reports**: Direct text input with automatic categorization
- **URL Extraction**: Automatic content extraction from news article URLs
- **PDF Upload**: Process disaster reports from PDF documents
- **Location Detection**: AI-powered location extraction with user override support

### AI-Powered Intelligence Pipeline
- **Fine-Tuned Models**: Custom models trained on Nepal disaster data
  - Classification: `Sachin1224/nepal-disaster-classifier`
  - Summarization: `Sachin1224/nepal-disaster-summarizer`
  - NER: `Sachin1224/nepal-disaster-ner`
  - Verification: `Sachin1224/nepal-disaster-verifier`
- **Smart Text Storage**: Stores AI-generated summaries instead of raw URLs
- **Multi-Factor Verification**: Combines content analysis, source checking, and fact verification
- **Real-Time Processing**: Asynchronous pipeline for fast response times

### Multi-Source Data Aggregation
- **Level 1 (Official)**: BIPAD Portal API for government-confirmed incidents
- **Level 2 (Humanitarian)**: ReliefWeb API for situation reports
- **Level 3 (Seismic)**: USGS API for earthquake monitoring
- **Level 4 (Media)**: NewsData.io for real-time news coverage

### Modern User Interface
- **Dynamic Dashboard**: Built with Next.js 14 and Framer Motion
- **Dark Mode Design**: Glassmorphism aesthetic optimized for operational environments
- **Responsive Layout**: Mobile-first design with Tailwind CSS
- **Real-Time Updates**: Live data refresh and status indicators

---

## 🏗️ Technical Architecture

### System Components

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Frontend      │────▶│   Backend API    │────▶│   AI Service    │
│   (Next.js)     │     │   (FastAPI)      │     │   (FastAPI)     │
│   Port: 3000    │     │   Port: 8001     │     │   Port: 8002    │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │                          │
                               ▼                          ▼
                        ┌──────────────┐         ┌──────────────┐
                        │   SQLite DB  │         │  HF Models   │
                        │  (Reports)   │         │  (4 models)  │
                        └──────────────┘         └──────────────┘
```

### Data Flow

1. **Input Layer**: User submits text/URL/PDF via frontend
2. **Backend Processing**: FastAPI validates and forwards to AI service
3. **AI Pipeline**:
   - Content extraction (URL/PDF → text)
   - Classification (disaster type detection)
   - Summarization (executive summary generation)
   - NER (location and entity extraction)
   - Verification (credibility scoring)
4. **Storage**: Backend stores processed data with AI metadata
5. **Display**: Frontend shows verified reports with AI insights

---

## 🚀 Installation and Setup

### Prerequisites
- **Python**: 3.11 or higher
- **Node.js**: 18 or higher
- **RAM**: Minimum 8GB (16GB recommended for AI models)
- **API Keys**: NewsData.io (optional, for news aggregation)

### 1. Clone Repository
```bash
git clone https://github.com/your-username/D-Brief.git
cd D-Brief
```

### 2. Environment Configuration
Create `.env` file in the root directory:
```env
# AI Service
NEWSDATA_API_KEY=your_newsdata_api_key_here

# Backend
DATABASE_URL=sqlite:///./disaster_local.db
AI_SERVICE_URL=http://localhost:8002

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8001
```

### 3. AI Service Setup
```bash
cd ai_service
pip install -r requirements.txt
python -m ai_service.api
```

**Note**: First run will download ~2GB of AI models from HuggingFace.

### 4. Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

### 5. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 6. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **AI Service**: http://localhost:8002
- **API Docs**: http://localhost:8002/docs

---

## 📡 API Reference

### AI Service Endpoints (Port 8002)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/process/report` | POST | Unified processing (text/URL) |
| `/api/process/upload` | POST | Process PDF documents |
| `/api/classify` | POST | Categorize disaster reports |
| `/api/summarize` | POST | Generate executive summaries |
| `/api/verify/news` | POST | Verify news credibility |
| `/api/realtime/news` | GET | Get cached verified news |
| `/api/fetch/all` | GET | Trigger multi-source data fetch |

### Backend Endpoints (Port 8001)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/reports/` | POST | Submit new disaster report |
| `/reports/` | GET | List all reports |
| `/reports/{id}` | GET | Get specific report |
| `/summaries/` | GET | Get report summaries |
| `/verify/check` | POST | Verify report authenticity |

---

## 💻 Usage Examples

### Submit Text Report
```bash
curl -X POST "http://localhost:8001/reports/" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Severe flooding in Kathmandu valley",
    "location": "Kathmandu",
    "disaster_category": "Flood",
    "source_type": "WEB_USER"
  }'
```

### Submit URL Report
```bash
curl -X POST "http://localhost:8001/reports/" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "https://thehimalayantimes.com/nepal/flood-alert",
    "source_type": "WEB_USER"
  }'
```

### Process PDF via AI Service
```bash
curl -X POST "http://localhost:8002/api/process/upload" \
  -F "file=@disaster_report.pdf"
```

---

## 🧪 Testing

### Verify System Setup (No Model Loading)
```bash
python verify_setup.py
```

### Run Component Tests
```bash
cd ai_service
python test_components.py
```

### Run Integration Tests
```bash
python test_complete_integration.py
```

---

## 📁 Project Structure

```
D-Brief/
├── ai_service/              # AI/ML Service (Port 8002)
│   ├── models/              # Model wrappers
│   │   ├── classifier.py    # Disaster classification
│   │   ├── summarizer.py    # Text summarization
│   │   ├── ner.py          # Named entity recognition
│   │   └── verifier.py     # Credibility verification
│   ├── pipelines/           # Processing pipelines
│   │   ├── processor.py     # Unified processor
│   │   ├── classify.py      # Classification pipeline
│   │   ├── summarize.py     # Summarization pipeline
│   │   ├── ner.py          # NER pipeline
│   │   └── verification.py  # Verification pipeline
│   ├── utils/               # Utilities
│   │   ├── content_extractor.py  # URL/PDF extraction
│   │   └── source_checker.py     # Source validation
│   ├── fetchers/            # Data source integrators
│   │   ├── bipad_client.py
│   │   ├── reliefweb_client.py
│   │   ├── usgs_client.py
│   │   └── news_client.py
│   ├── api.py              # FastAPI application
│   └── requirements.txt     # Python dependencies
│
├── backend/                 # Backend API (Port 8001)
│   ├── app/
│   │   ├── models/         # Database models
│   │   ├── routes/         # API routes
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── main.py        # FastAPI app
│   └── requirements.txt
│
├── frontend/                # Next.js Frontend (Port 3000)
│   ├── src/
│   │   ├── components/     # React components
│   │   │   └── ReportForm.jsx  # Multi-input form
│   │   ├── pages/          # Next.js pages
│   │   ├── services/       # API clients
│   │   └── constants/      # App constants
│   ├── package.json
│   └── tailwind.config.js
│
├── verify_setup.py          # System verification script
└── README.md               # This file
```

---

## 🤖 AI Models

### Fine-Tuned Models (HuggingFace)
All models are fine-tuned on Nepal disaster data for improved accuracy:

- **Classification**: `Sachin1224/nepal-disaster-classifier`
  - Base: DeBERTa-v3-base
  - Categories: Flood, Earthquake, Landslide, Fire, etc.

- **Summarization**: `Sachin1224/nepal-disaster-summarizer`
  - Base: BART-large-cnn
  - Generates concise executive summaries

- **NER**: `Sachin1224/nepal-disaster-ner`
  - Base: BERT-base-cased
  - Extracts locations, organizations, dates

- **Verification**: `Sachin1224/nepal-disaster-verifier`
  - Base: RoBERTa-base
  - Detects fake news and misinformation

### Fallback Models
If fine-tuned models unavailable, system uses:
- `facebook/bart-large-mnli` (classification)
- `facebook/bart-large-cnn` (summarization)
- `dslim/bert-base-NER` (entity extraction)

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Next.js 14, React 18, Tailwind CSS |
| **Animations** | Framer Motion, Lucide Icons |
| **Backend** | FastAPI, Python 3.11, SQLAlchemy |
| **AI/ML** | HuggingFace Transformers, PyTorch, Sentence-Transformers |
| **NLP** | Spacy, NLTK, BeautifulSoup4 |
| **Data Sources** | NewsData.io, BIPAD, ReliefWeb, USGS |
| **Database** | SQLite (dev), PostgreSQL (production ready) |
| **Content Extraction** | PyPDF, BeautifulSoup4, DuckDuckGo Search |

---

## ⚙️ Configuration

### Memory Requirements
- **Minimum**: 8GB RAM
- **Recommended**: 16GB RAM
- **Models Size**: ~2GB total

### Port Configuration
- Frontend: `3000`
- Backend: `8001`
- AI Service: `8002`

### Environment Variables

**AI Service** (`.env`):
```env
NEWSDATA_API_KEY=your_key_here
```

**Backend** (`.env`):
```env
DATABASE_URL=sqlite:///./disaster_local.db
AI_SERVICE_URL=http://localhost:8002
```

**Frontend** (`.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:8001
```

---

## 🐛 Troubleshooting

### Memory Errors
If you encounter "MemoryError" or "paging file too small":
1. Increase Windows virtual memory (8GB+)
2. Close unnecessary applications
3. Deploy to a server with more RAM
4. Disable background tasks in `ai_service/api.py`

### Model Download Issues
If models fail to download:
```bash
# Manual download
python -c "from transformers import AutoModel; AutoModel.from_pretrained('Sachin1224/nepal-disaster-classifier')"
```

### Port Conflicts
If ports are in use:
```bash
# Change ports in respective config files
# AI Service: ai_service/api.py (line 575)
# Backend: Use --port flag with uvicorn
# Frontend: package.json or use PORT=3001 npm run dev
```

### Import Errors
Ensure you're in the correct directory:
```bash
cd D-Brief
python -m ai_service.api  # Not: cd ai_service && python api.py
```

---

## 🤝 Contributing

### Development Guidelines
1. **Code Style**: Follow PEP 8 for Python, ESLint for JavaScript
2. **Type Hints**: Use type annotations in Python code
3. **Logging**: Use `loguru` for AI service, standard logging for backend
4. **Testing**: Add tests for new features
5. **Documentation**: Update README for API changes

### Contribution Process
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

MIT License

Copyright (c) 2025 Team Mama-Bhanjas

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## 🙏 Acknowledgments

- **HuggingFace**: For providing the model hosting and transformers library
- **FastAPI**: For the high-performance API framework
- **Next.js**: For the powerful React framework
- **BIPAD, ReliefWeb, USGS**: For disaster data APIs
- **NewsData.io**: For real-time news aggregation

---

## 📞 Support

For issues, questions, or contributions:
- **GitHub Issues**: [Create an issue](https://github.com/your-username/D-Brief/issues)
- **Documentation**: See `/docs` folder for detailed guides
- **Email**: team@mama-bhanjas.com

---

**Built with ❤️ by Team Mama-Bhanjas for humanitarian disaster response**
