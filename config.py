import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Keys
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    tavily_api_key: str = os.getenv("TAVILY_API_KEY", "")
    qdrant_url: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_api_key: Optional[str] = os.getenv("QDRANT_API_KEY")
    mcp_server_url: str = os.getenv("MCP_SERVER_URL", "http://localhost:3000")
    
    # Model Configuration
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    llm_model: str = "gemini-2.5-flash"
    
    # Vector Database Configuration
    collection_name: str = "math_knowledge_base"
    vector_size: int = 384
    
    # Guardrails Configuration
    max_input_length: int = 1000
    max_output_length: int = 2000
    allowed_topics: list = ["mathematics", "algebra", "calculus", "geometry", "statistics", "trigonometry"]
    
    class Config:
        env_file = ".env"

settings = Settings()
