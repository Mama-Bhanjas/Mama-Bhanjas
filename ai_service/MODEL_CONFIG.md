# AI Service Model Configuration

This document describes the model choices and alternatives for the AI service.

## Current Models (Space-Efficient)

### Classification Model
- **Current**: `MoritzLaurer/deberta-v3-base-zeroshot-v1.1-all-33`
- **Size**: ~500MB
- **Type**: Zero-shot classification
- **Advantages**: Excellent performance, supports custom categories

### Summarization Model
- **Current**: `sshleifer/distilbart-cnn-12-6`
- **Size**: ~300MB
- **Type**: Distilled BART for summarization
- **Advantages**: Fast, efficient, good quality summaries

## Alternative Models (If Still Low on Space)

### Ultra-Lightweight Classification
If you still encounter disk space issues, you can use even smaller models:

```python
# In classifier.py, change model_name to:
model_name = "cross-encoder/ms-marco-MiniLM-L-6-v2"  # ~90MB
```

### Ultra-Lightweight Summarization
```python
# In summarizer.py, change model_name to:
model_name = "sshleifer/distilbart-xsum-12-6"  # ~300MB
# OR even smaller:
model_name = "google/pegasus-xsum"  # ~570MB but better quality
```

## Previous Models (Too Large)

These models were causing disk space issues:
- ❌ `facebook/bart-large-mnli` - 1.63GB
- ❌ `facebook/bart-large-cnn` - 1.63GB

## Disk Space Management

### Clear Cache
Run this command to clear the Hugging Face cache:
```bash
python -m ai_service.clear_cache
```

### Check Disk Space
Before running tests, ensure you have at least **2GB** of free disk space for model downloads and caching.

### Cache Location
Models are cached in: `C:\Users\Lenovo\.cache\huggingface\`

## Performance Comparison

| Model Type | Model Name | Size | Quality | Speed |
|------------|-----------|------|---------|-------|
| Classification (Large) | facebook/bart-large-mnli | 1.6GB | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Classification (Current) | MoritzLaurer/deberta-v3-base | 500MB | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Classification (Tiny) | cross-encoder/ms-marco-MiniLM | 90MB | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Summarization (Large) | facebook/bart-large-cnn | 1.6GB | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Summarization (Current) | sshleifer/distilbart-cnn-12-6 | 300MB | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
