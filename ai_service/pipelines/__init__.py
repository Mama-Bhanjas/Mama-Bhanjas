"""
Pipelines package
"""
from .classify import ClassificationPipeline
from .summarize import SummarizationPipeline
from .cluster import ClusteringPipeline

__all__ = ['ClassificationPipeline', 'SummarizationPipeline', 'ClusteringPipeline']
