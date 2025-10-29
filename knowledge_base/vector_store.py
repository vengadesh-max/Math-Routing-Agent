import os
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import numpy as np
from config import settings
from .math_dataset import MathDataset

class VectorStore:
    """Vector database for mathematical knowledge base"""
    
    def __init__(self):
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key
        )
        self.embedding_model = SentenceTransformer(settings.embedding_model)
        self.collection_name = settings.collection_name
        self.vector_size = settings.vector_size
        self._initialize_collection()
    
    def _initialize_collection(self):
        """Initialize the Qdrant collection"""
        try:
            # Check if collection exists
            collections = self.client.get_collections()
            collection_names = [col.name for col in collections.collections]
            
            if self.collection_name not in collection_names:
                # Create collection
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.vector_size,
                        distance=Distance.COSINE
                    )
                )
                print(f"Created collection: {self.collection_name}")
            else:
                print(f"Collection {self.collection_name} already exists")
                
        except Exception as e:
            print(f"Error initializing collection: {e}")
            # Fallback to in-memory storage
            self._use_fallback_storage()
    
    def _use_fallback_storage(self):
        """Fallback to in-memory storage if Qdrant is not available"""
        self.collection_name = "fallback_collection"
        self.vectors = {}
        self.metadata = {}
    
    def add_documents(self, documents: List[Dict[str, Any]]):
        """Add documents to the vector store"""
        try:
            points = []
            for i, doc in enumerate(documents):
                # Create embedding
                content = doc.get("content", f"{doc.get('question', '')} {doc.get('explanation', '')}")
                embedding = self.embedding_model.encode(content).tolist()
                
                # Create point
                point = PointStruct(
                    id=i,
                    vector=embedding,
                    payload=doc
                )
                points.append(point)
            
            # Upsert points
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            print(f"Added {len(points)} documents to vector store")
            
        except Exception as e:
            print(f"Error adding documents: {e}")
            # Fallback to in-memory storage
            self._add_to_fallback(documents)
    
    def _add_to_fallback(self, documents: List[Dict[str, Any]]):
        """Add documents to fallback storage"""
        for i, doc in enumerate(documents):
            content = doc.get("content", f"{doc.get('question', '')} {doc.get('explanation', '')}")
            embedding = self.embedding_model.encode(content).tolist()
            self.vectors[i] = embedding
            self.metadata[i] = doc
    
    def search(self, query: str, limit: int = 5, score_threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        try:
            # Create query embedding
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # Search in Qdrant
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                score_threshold=score_threshold
            )
            
            results = []
            for result in search_results:
                results.append({
                    "id": result.id,
                    "score": result.score,
                    "content": result.payload
                })
            
            return results
            
        except Exception as e:
            print(f"Error searching vector store: {e}")
            # Fallback to in-memory search
            return self._search_fallback(query, limit, score_threshold)
    
    def _search_fallback(self, query: str, limit: int, score_threshold: float) -> List[Dict[str, Any]]:
        """Fallback search in memory"""
        if not hasattr(self, 'vectors'):
            return []
        
        query_embedding = self.embedding_model.encode(query).tolist()
        results = []
        
        for doc_id, vector in self.vectors.items():
            # Calculate cosine similarity
            similarity = np.dot(query_embedding, vector) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(vector)
            )
            
            if similarity >= score_threshold:
                results.append({
                    "id": doc_id,
                    "score": float(similarity),
                    "content": self.metadata[doc_id]
                })
        
        # Sort by score and return top results
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]
    
    def populate_knowledge_base(self):
        """Populate the knowledge base with mathematical problems"""
        dataset = MathDataset()
        documents = dataset.to_dict()
        self.add_documents(documents)
        print(f"Knowledge base populated with {len(documents)} mathematical problems")
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection"""
        try:
            collection_info = self.client.get_collection(self.collection_name)
            return {
                "name": collection_info.config.params.vectors.size,
                "vector_size": collection_info.config.params.vectors.size,
                "distance": collection_info.config.params.vectors.distance,
                "points_count": collection_info.points_count
            }
        except Exception as e:
            return {"error": str(e)}

