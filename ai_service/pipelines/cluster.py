"""
Clustering Pipeline
Groups similar reports together using embeddings and clustering algorithms
"""
from typing import List, Dict, Optional, Tuple
import numpy as np
from loguru import logger
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

# Optional imports
try:
    import hdbscan
    HDBSCAN_AVAILABLE = True
except ImportError:
    HDBSCAN_AVAILABLE = False
    logger.warning("hdbscan not available. HDBSCAN clustering will not work.")

try:
    import umap
    UMAP_AVAILABLE = True
except ImportError:
    UMAP_AVAILABLE = False
    logger.warning("umap-learn not available. UMAP dimensionality reduction will not work.")

from ai_service.utils import TextPreprocessor, cosine_similarity, get_device


class ClusteringPipeline:
    """
    Pipeline for clustering similar reports
    """
    
    def __init__(
        self,
        embedding_model: str = "all-MiniLM-L6-v2",
        device: Optional[str] = None
    ):
        """
        Initialize clustering pipeline
        
        Args:
            embedding_model: Sentence transformer model for embeddings
            device: Device to run model on
        """
        self.device = device or get_device()
        self.preprocessor = TextPreprocessor()
        
        logger.info(f"Loading embedding model: {embedding_model}")
        
        try:
            self.embedding_model = SentenceTransformer(embedding_model)
            if self.device == "cuda":
                self.embedding_model = self.embedding_model.to(self.device)
            logger.info(f"Embedding model loaded successfully on {self.device}")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise
        
        self.embeddings_cache = {}
    
    def generate_embeddings(
        self,
        texts: List[str],
        batch_size: int = 32,
        use_cache: bool = True
    ) -> np.ndarray:
        """
        Generate embeddings for texts
        
        Args:
            texts: List of texts to embed
            batch_size: Batch size for encoding
            use_cache: Whether to use cached embeddings
            
        Returns:
            Numpy array of embeddings
        """
        embeddings = []
        texts_to_encode = []
        indices_to_encode = []
        
        for i, text in enumerate(texts):
            cache_key = hash(text)
            
            if use_cache and cache_key in self.embeddings_cache:
                embeddings.append(self.embeddings_cache[cache_key])
            else:
                texts_to_encode.append(text)
                indices_to_encode.append(i)
                embeddings.append(None)  # Placeholder
        
        # Encode uncached texts
        if texts_to_encode:
            logger.info(f"Generating embeddings for {len(texts_to_encode)} texts")
            
            new_embeddings = self.embedding_model.encode(
                texts_to_encode,
                batch_size=batch_size,
                show_progress_bar=False,
                convert_to_numpy=True
            )
            
            # Cache and insert new embeddings
            for idx, text, embedding in zip(indices_to_encode, texts_to_encode, new_embeddings):
                cache_key = hash(text)
                self.embeddings_cache[cache_key] = embedding
                embeddings[idx] = embedding
        
        return np.array(embeddings)
    
    def cluster_hdbscan(
        self,
        texts: List[str],
        min_cluster_size: int = 5,
        min_samples: int = 3,
        use_umap: bool = True,
        n_components: int = 5
    ) -> Dict[str, any]:
        """
        Cluster texts using HDBSCAN (density-based clustering)
        
        Args:
            texts: List of texts to cluster
            min_cluster_size: Minimum cluster size
            min_samples: Minimum samples for core points
            use_umap: Whether to use UMAP for dimensionality reduction
            n_components: Number of UMAP components
            
        Returns:
            Clustering results
        """
        if not HDBSCAN_AVAILABLE:
            raise ImportError(
                "hdbscan is not installed. Install it with: pip install hdbscan"
            )
        
        logger.info(f"Clustering {len(texts)} texts with HDBSCAN")
        
        # Generate embeddings
        embeddings = self.generate_embeddings(texts)
        
        # Optional dimensionality reduction
        if use_umap and len(texts) > 10:
            if not UMAP_AVAILABLE:
                logger.warning("UMAP not available, skipping dimensionality reduction")
                embeddings_reduced = embeddings
            else:
                logger.info(f"Applying UMAP reduction to {n_components} dimensions")
                reducer = umap.UMAP(
                    n_components=min(n_components, len(texts) - 1),
                    random_state=42
                )
                embeddings_reduced = reducer.fit_transform(embeddings)
        else:
            embeddings_reduced = embeddings
        
        # Cluster with HDBSCAN
        clusterer = hdbscan.HDBSCAN(
            min_cluster_size=min_cluster_size,
            min_samples=min_samples,
            metric='euclidean'
        )
        
        cluster_labels = clusterer.fit_predict(embeddings_reduced)
        
        # Organize results
        clusters = self._organize_clusters(texts, cluster_labels, embeddings)
        
        logger.info(f"Found {len(clusters)} clusters (excluding noise)")
        
        return {
            "clusters": clusters,
            "num_clusters": len(clusters),
            "num_noise_points": sum(1 for label in cluster_labels if label == -1),
            "cluster_labels": cluster_labels.tolist()
        }
    
    def cluster_kmeans(
        self,
        texts: List[str],
        n_clusters: int = 5
    ) -> Dict[str, any]:
        """
        Cluster texts using K-Means
        
        Args:
            texts: List of texts to cluster
            n_clusters: Number of clusters
            
        Returns:
            Clustering results
        """
        logger.info(f"Clustering {len(texts)} texts with K-Means (k={n_clusters})")
        
        # Generate embeddings
        embeddings = self.generate_embeddings(texts)
        
        # Cluster with K-Means
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(embeddings)
        
        # Organize results
        clusters = self._organize_clusters(texts, cluster_labels, embeddings)
        
        logger.info(f"Created {len(clusters)} clusters")
        
        return {
            "clusters": clusters,
            "num_clusters": len(clusters),
            "cluster_labels": cluster_labels.tolist(),
            "inertia": float(kmeans.inertia_)
        }
    
    def _organize_clusters(
        self,
        texts: List[str],
        labels: np.ndarray,
        embeddings: np.ndarray
    ) -> List[Dict[str, any]]:
        """
        Organize clustering results into structured format
        
        Args:
            texts: Original texts
            labels: Cluster labels
            embeddings: Text embeddings
            
        Returns:
            List of cluster dictionaries
        """
        clusters_dict = {}
        
        for i, (text, label) in enumerate(zip(texts, labels)):
            if label == -1:  # Noise point in HDBSCAN
                continue
            
            if label not in clusters_dict:
                clusters_dict[label] = {
                    "cluster_id": int(label),
                    "texts": [],
                    "indices": [],
                    "embeddings": []
                }
            
            clusters_dict[label]["texts"].append(text)
            clusters_dict[label]["indices"].append(i)
            clusters_dict[label]["embeddings"].append(embeddings[i])
        
        # Calculate cluster centroids and representative texts
        clusters = []
        for cluster_data in clusters_dict.values():
            cluster_embeddings = np.array(cluster_data["embeddings"])
            centroid = cluster_embeddings.mean(axis=0)
            
            # Find most representative text (closest to centroid)
            distances = [
                np.linalg.norm(emb - centroid)
                for emb in cluster_embeddings
            ]
            representative_idx = np.argmin(distances)
            
            clusters.append({
                "cluster_id": cluster_data["cluster_id"],
                "size": len(cluster_data["texts"]),
                "texts": cluster_data["texts"],
                "indices": cluster_data["indices"],
                "representative_text": cluster_data["texts"][representative_idx],
                "representative_index": cluster_data["indices"][representative_idx]
            })
        
        # Sort by cluster size
        clusters.sort(key=lambda x: x["size"], reverse=True)
        
        return clusters
    
    def find_similar(
        self,
        query_text: str,
        corpus_texts: List[str],
        top_k: int = 5,
        threshold: float = 0.5
    ) -> List[Dict[str, any]]:
        """
        Find similar texts to a query
        
        Args:
            query_text: Query text
            corpus_texts: List of texts to search
            top_k: Number of similar texts to return
            threshold: Minimum similarity threshold
            
        Returns:
            List of similar texts with scores
        """
        # Generate embeddings
        query_embedding = self.generate_embeddings([query_text])[0]
        corpus_embeddings = self.generate_embeddings(corpus_texts)
        
        # Calculate similarities
        similarities = []
        for i, corpus_embedding in enumerate(corpus_embeddings):
            similarity = cosine_similarity(query_embedding, corpus_embedding)
            if similarity >= threshold:
                similarities.append({
                    "text": corpus_texts[i],
                    "index": i,
                    "similarity": float(similarity)
                })
        
        # Sort by similarity
        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        
        return similarities[:top_k]
