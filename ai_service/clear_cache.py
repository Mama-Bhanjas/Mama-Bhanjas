"""
Clear Hugging Face cache to free up disk space
"""
import os
import shutil
from pathlib import Path
from loguru import logger

def get_cache_size(cache_dir: Path) -> float:
    """Get total size of cache directory in MB"""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(cache_dir):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.exists(filepath):
                    total_size += os.path.getsize(filepath)
    except Exception as e:
        logger.warning(f"Error calculating cache size: {e}")
    return total_size / (1024 * 1024)  # Convert to MB

def clear_huggingface_cache():
    """Clear Hugging Face model cache"""
    cache_dir = Path.home() / ".cache" / "huggingface"
    
    if not cache_dir.exists():
        logger.info("No Hugging Face cache found")
        return
    
    # Get cache size before clearing
    cache_size_mb = get_cache_size(cache_dir)
    logger.info(f"Current cache size: {cache_size_mb:.2f} MB")
    
    try:
        # Remove the cache directory
        shutil.rmtree(cache_dir)
        logger.info(f"Successfully cleared {cache_size_mb:.2f} MB from Hugging Face cache")
        logger.info("Models will be re-downloaded on next use")
    except Exception as e:
        logger.error(f"Failed to clear cache: {e}")
        raise

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("Clearing Hugging Face Cache")
    logger.info("=" * 60)
    clear_huggingface_cache()
    logger.info("Cache cleared successfully!")
