# AI Service Setup - Quick Reference

## ✅ What's Been Fixed

1. **Import Errors**: All relative imports converted to absolute imports
2. **PyTorch Version**: Updated to 2.2.2 (available version)
3. **Requirements**: Complete requirements.txt with all dependencies

## 🚀 Installation Steps

### Step 1: Install All Dependencies

```bash
cd "d:\Hackfest 2025\Mama-Bhanjas\ai_service"
pip install -r requirements.txt
```

This will install:
- PyTorch 2.2.2
- Transformers (BART models)
- FastAPI & Uvicorn
- Sentence Transformers
- scikit-learn, HDBSCAN, UMAP
- loguru, numpy, pandas
- And all other dependencies

**Note**: Installation may take 5-10 minutes due to large ML models.

### Step 2: Verify Installation

Run from the parent directory:

```bash
cd "d:\Hackfest 2025\Mama-Bhanjas"
python -m ai_service.test_service
```

Or use the Windows batch script:
```bash
cd ai_service
run_tests.bat
```

### Step 3: Start the API Server

```bash
cd "d:\Hackfest 2025\Mama-Bhanjas"
python -m uvicorn ai_service.api:app --reload --host 0.0.0.0 --port 8000
```

Or use the batch script:
```bash
cd ai_service
run_api.bat
```

## 📝 Important Notes

### Running Python Scripts

**Always run from the parent directory** (`Mama-Bhanjas`), not from `ai_service`:

✅ **Correct**:
```bash
cd "d:\Hackfest 2025\Mama-Bhanjas"
python -m ai_service.test_service
python -m ai_service.api
```

❌ **Incorrect**:
```bash
cd "d:\Hackfest 2025\Mama-Bhanjas\ai_service"
python test_service.py  # This will cause import errors
```

### Using in Python Code

```python
import sys
from pathlib import Path

# Add parent directory to path (if running from ai_service folder)
sys.path.insert(0, str(Path.cwd().parent))

# Now you can import
from ai_service.pipelines.classify import ClassificationPipeline
from ai_service.pipelines.summarize import SummarizationPipeline
from ai_service.pipelines.cluster import ClusteringPipeline
```

## 🔍 Testing Individual Components

### Test Classification
```python
from ai_service.pipelines.classify import ClassificationPipeline

classifier = ClassificationPipeline()
result = classifier.process("There is a pothole on Main Street.")
print(result)
```

### Test Summarization
```python
from ai_service.pipelines.summarize import SummarizationPipeline

summarizer = SummarizationPipeline()
result = summarizer.process("Long text here...")
print(result['summary'])
```

### Test Clustering
```python
from ai_service.pipelines.cluster import ClusteringPipeline

clusterer = ClusteringPipeline()
texts = ["Text 1", "Text 2", "Text 3"]
result = clusterer.cluster_kmeans(texts, n_clusters=2)
print(result)
```

## 🌐 API Endpoints

Once the server is running at `http://localhost:8000`:

- **Interactive Docs**: http://localhost:8000/docs
- **Classify**: POST http://localhost:8000/api/classify
- **Summarize**: POST http://localhost:8000/api/summarize
- **Cluster**: POST http://localhost:8000/api/cluster
- **Similarity**: POST http://localhost:8000/api/similarity

## 🐛 Common Issues

### "ModuleNotFoundError: No module named 'ai_service'"
- Make sure you're running from the parent directory
- Or add parent to path: `sys.path.insert(0, str(Path.cwd().parent))`

### "ModuleNotFoundError: No module named 'hdbscan'"
- Run: `pip install hdbscan`

### "ModuleNotFoundError: No module named 'loguru'"
- Run: `pip install -r requirements.txt`

### Models downloading slowly
- First run downloads large models (~1-2GB total)
- Subsequent runs use cached models

## 📦 What's Included

- ✅ Classification (9 categories)
- ✅ Summarization (abstractive)
- ✅ Clustering (HDBSCAN + K-Means)
- ✅ Similarity Search
- ✅ REST API with FastAPI
- ✅ Caching for performance
- ✅ Batch processing
- ✅ Comprehensive tests
