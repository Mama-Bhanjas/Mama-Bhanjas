# AI Service - Installation & Setup Guide

Machine Learning service for report classification, summarization, and clustering.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd "d:\Hackfest 2025\Mama-Bhanjas\ai_service"
pip install -r requirements.txt
```

**Note**: The installation may take several minutes as it downloads large ML models.

### 2. Run Tests

To verify everything is working:

**Option A - Using the batch script (Windows):**
```bash
run_tests.bat
```

**Option B - Using Python directly:**
```bash
cd "d:\Hackfest 2025\Mama-Bhanjas"
python -m ai_service.test_service
```

### 3. Start the API Server

**Option A - Using the batch script (Windows):**
```bash
run_api.bat
```

**Option B - Using Python directly:**
```bash
cd "d:\Hackfest 2025\Mama-Bhanjas"
python -m uvicorn ai_service.api:app --reload --host 0.0.0.0 --port 8000
```

Then visit:
- API: `http://localhost:8000`
- Interactive Docs: `http://localhost:8000/docs`
- Alternative Docs: `http://localhost:8000/redoc`

## 📋 Features

- **Text Classification**: Categorize reports into predefined categories using zero-shot classification
- **Text Summarization**: Generate concise summaries using state-of-the-art transformer models
- **Text Clustering**: Group similar reports using embeddings and clustering algorithms
- **Similarity Search**: Find similar reports based on semantic similarity

## 🔧 Usage Examples

### Using the API

#### Classify Text
```bash
curl -X POST "http://localhost:8000/api/classify" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"There is a broken streetlight on Oak Avenue\", \"top_k\": 3}"
```

#### Summarize Text
```bash
curl -X POST "http://localhost:8000/api/summarize" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Your long text here...\", \"max_length\": 150}"
```

#### Cluster Texts
```bash
curl -X POST "http://localhost:8000/api/cluster" \
  -H "Content-Type: application/json" \
  -d "{\"texts\": [\"Text 1\", \"Text 2\", \"Text 3\"], \"method\": \"kmeans\", \"n_clusters\": 2}"
```

### Using Python Directly

```python
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path.cwd().parent))

from ai_service.pipelines.classify import ClassificationPipeline
from ai_service.pipelines.summarize import SummarizationPipeline
from ai_service.pipelines.cluster import ClusteringPipeline

# Classification
classifier = ClassificationPipeline()
result = classifier.process("There is a pothole on Main Street.")
print(f"Category: {result['category']}")

# Summarization
summarizer = SummarizationPipeline()
result = summarizer.process("Long text to summarize...")
print(f"Summary: {result['summary']}")

# Clustering
clusterer = ClusteringPipeline()
texts = ["Report 1...", "Report 2...", "Report 3..."]
result = clusterer.cluster_kmeans(texts, n_clusters=2)
print(f"Found {result['num_clusters']} clusters")
```

## 📁 Project Structure

```
ai_service/
├── models/              # ML model wrappers
│   ├── classifier.py    # Category classification
│   └── summarizer.py    # Text summarization
├── pipelines/           # End-to-end pipelines
│   ├── classify.py      # Classification pipeline
│   ├── summarize.py     # Summarization pipeline
│   └── cluster.py       # Clustering pipeline
├── api.py              # FastAPI endpoints
├── utils.py            # Utility functions
├── test_service.py     # Test suite
├── requirements.txt    # Dependencies
├── run_tests.bat       # Windows test runner
└── run_api.bat         # Windows API runner
```

## 🎯 Default Categories

The classifier uses these default categories:
- Infrastructure
- Public Safety
- Environment
- Transportation
- Health & Sanitation
- Education
- Utilities
- Community Services
- Other

## 🤖 Models Used

- **Classification**: `facebook/bart-large-mnli` (zero-shot classification)
- **Summarization**: `facebook/bart-large-cnn` (abstractive summarization)
- **Embeddings**: `all-MiniLM-L6-v2` (sentence transformers)

## ⚙️ Configuration

- Models automatically use GPU if available, otherwise CPU
- Logs are stored in `logs/` directory with daily rotation
- Cache is enabled by default for faster repeated predictions

## 🐛 Troubleshooting

### Import Errors
If you get import errors, make sure you're running from the parent directory:
```bash
cd "d:\Hackfest 2025\Mama-Bhanjas"
python -m ai_service.test_service
```

### Missing Dependencies
If you get "ModuleNotFoundError", install missing packages:
```bash
pip install <package-name>
```

### CUDA/GPU Issues
If you have GPU issues, the models will automatically fall back to CPU. To force CPU:
```python
pipeline = ClassificationPipeline(device="cpu")
```

## 📝 API Endpoints

### Classification
- `POST /api/classify` - Classify a single text
- `POST /api/classify/batch` - Classify multiple texts

### Summarization
- `POST /api/summarize` - Summarize a single text
- `POST /api/summarize/batch` - Summarize multiple texts

### Clustering
- `POST /api/cluster` - Cluster similar texts
- `POST /api/similarity` - Find similar texts to a query

### Health
- `GET /health` - Health check
- `GET /` - API information

## 📄 License

MIT
