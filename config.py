"""
Advanced configuration and utilities for the device support service
"""
import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class QdrantConfig:
    """Configuration for Qdrant"""
    url: str = "http://localhost:6333"
    collection_name: str = "device_solutions"
    vector_size: int = 1536  # OpenAI embedding size


@dataclass
class AgentConfig:
    """Configuration for agents"""
    model: str = "gpt-4"
    temperature: float = 0.3
    max_iterations: int = 10
    verbose: bool = True


class Config:
    """Central configuration management"""
    
    def __init__(self):
        self.qdrant = QdrantConfig(
            url=os.getenv("QDRANT_URL", "http://localhost:6333"),
            collection_name=os.getenv("QDRANT_COLLECTION_NAME", "device_solutions"),
        )
        
        self.agents = AgentConfig(
            model=os.getenv("MODEL", "gpt-4"),
            temperature=float(os.getenv("AGENT_TEMPERATURE", "0.3")),
            verbose=os.getenv("CREWAI_VERBOSE", "true").lower() == "true",
        )
        
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate configuration"""
        if not self.openai_api_key:
            return False, "OPENAI_API_KEY not set"
        return True, None


# Global config instance
config = Config()
