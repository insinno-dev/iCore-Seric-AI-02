"""
RAG Service for Problem-Solving using Qdrant Vector Database
"""
import os
import sys
from dotenv import load_dotenv
from typing import List
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from voyageai import Client as VoyageClient

# Fix Windows encoding issues (only for non-Streamlit environments)
if sys.platform == "win32" and hasattr(sys.stdout, 'buffer'):
    try:
        import io
        if not isinstance(sys.stdout, io.TextIOWrapper) or sys.stdout.encoding.lower() != 'utf-8':
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
    except Exception:
        # If we can't wrap stdout, just continue - might be in Streamlit
        pass

# Always load environment variables first
load_dotenv()


class RAGService:
    """Service for managing and querying solutions from Qdrant"""

    def __init__(self, qdrant_url: str = "http://localhost:6333", collection_name: str = "device_solutions", api_key: str = None):
        """
        Initialize RAG Service
        
        Args:
            qdrant_url: URL to Qdrant server
            collection_name: Name of the collection in Qdrant
            api_key: Optional API key for Qdrant cloud
        """
        # Clean up inputs (strip whitespace)
        qdrant_url = qdrant_url.strip() if qdrant_url else qdrant_url
        collection_name = collection_name.strip() if collection_name else collection_name
        api_key = api_key.strip() if api_key else api_key
        
        # Create Qdrant client with optional API key
        # For Qdrant Cloud, disable compatibility check which can cause issues
        try:
            # Use ASCII-safe output
            url_safe = qdrant_url.encode('ascii', errors='replace').decode('ascii')
            coll_safe = collection_name.encode('ascii', errors='replace').decode('ascii')
            key_display = f"{'*' * 10}...{api_key[-10:]}" if api_key else "None"
            
            print(f"Connecting to Qdrant:")
            print(f"  URL: {url_safe}")
            print(f"  Collection: {coll_safe}")
            print(f"  API Key: {key_display}")
            
            if api_key:
                self.client = QdrantClient(
                    url=qdrant_url,
                    api_key=api_key,
                    check_compatibility=False,
                    timeout=10
                )
            else:
                self.client = QdrantClient(
                    url=qdrant_url,
                    check_compatibility=False,
                    timeout=10
                )
            
            # Test connection
            self.client.get_collections()
            print(f"✓ Connected to Qdrant successfully")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Qdrant: {str(e)}")
        
        self.collection_name = collection_name
        self.voyage_client = VoyageClient(api_key=os.getenv("VOYAGE_API_KEY"))
        self.model = "voyage-3-large"
        self.vector_size = 1024  # Voyage AI 3 Large embedding size
        
        # Initialize collection if it doesn't exist
        self._initialize_collection()

    def _initialize_collection(self):
        """Check if collection exists, don't try to create it"""
        try:
            coll_info = self.client.get_collection(self.collection_name)
            print(f"✓ Collection '{self.collection_name}' exists with {coll_info.points_count if hasattr(coll_info, 'points_count') else '?'} points")
        except Exception as e:
            print(f"⚠ Warning: Collection '{self.collection_name}' check failed: {e}")
            print("  The collection may not exist or may be inaccessible")

    def add_solution(self, device_type: str, problem: str, solution: str, manual_reference: str = None):
        """
        Add a solution to the knowledge base
        
        Args:
            device_type: Type of device (e.g., "Laptop", "Router")
            problem: Problem description
            solution: Solution/fix description
            manual_reference: Reference to manual or documentation
        """
        # Create embedding for the problem
        text = f"{device_type}: {problem}"
        embedding = self.voyage_client.embed([text], model=self.model).embeddings[0]
        
        # Create document ID
        doc_id = hash(text) % (10 ** 8)
        
        # Prepare metadata
        metadata = {
            "device_type": device_type,
            "problem": problem,
            "solution": solution,
            "manual_reference": manual_reference or "",
        }
        
        # Add to Qdrant
        point = PointStruct(
            id=doc_id,
            vector=embedding,
            payload=metadata
        )
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=[point]
        )
        print(f"Added solution for {device_type}: {problem}")

    def search_solutions(self, device_type: str, problem_description: str, limit: int = 3) -> List[dict]:
        """
        Search for similar solutions in the knowledge base
        
        Args:
            device_type: Type of device
            problem_description: Detailed problem description
            limit: Number of results to return
            
        Returns:
            List of relevant solutions
        """
        # Create embedding for the search query
        text = f"{device_type}: {problem_description}"
        query_embedding = self.voyage_client.embed([text], model=self.model).embeddings[0]
        
        # Search in Qdrant
        search_results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit,
        )
        
        # Extract and format results
        solutions = []
        for result in search_results:
            solutions.append({
                "score": result.score,
                "device_type": result.payload.get("device_type"),
                "problem": result.payload.get("problem"),
                "solution": result.payload.get("solution"),
                "manual_reference": result.payload.get("manual_reference"),
            })
        
        return solutions

    def get_collection_stats(self) -> dict:
        """Get statistics about the collection"""
        try:
            collection_info = self.client.get_collection(self.collection_name)
            return {
                "collection_name": self.collection_name,
                "vectors_count": collection_info.points_count,
                "vector_size": self.vector_size,
            }
        except Exception as e:
            return {"error": str(e)}

    def add_sample_solutions(self):
        """Add sample solutions to the knowledge base"""
        sample_data = [
            {
                "device_type": "Laptop",
                "problem": "Laptop won't turn on, no power response",
                "solution": "Check power adapter connection, try force reset by holding power button for 30 seconds. If still not responsive, check battery connection.",
                "manual_reference": "Laptop Service Manual v2.1 - Section 3.1",
            },
            {
                "device_type": "Laptop",
                "problem": "Screen is black but laptop is running",
                "solution": "Try external monitor to test display output. Check brightness controls. Update graphics drivers. Restart in safe mode.",
                "manual_reference": "Troubleshooting Guide - Display Issues",
            },
            {
                "device_type": "Router",
                "problem": "No internet connection, router lights are off",
                "solution": "Check power cable and outlet. Verify the power button is ON. Check if power supply indicator light is on.",
                "manual_reference": "Router Setup Guide v3.0",
            },
            {
                "device_type": "Router",
                "problem": "WiFi network not visible",
                "solution": "Restart router by unplugging for 30 seconds. Check if WiFi is enabled using the WiFi button. Factory reset if needed.",
                "manual_reference": "Wireless Configuration - Section 2",
            },
            {
                "device_type": "Printer",
                "problem": "Printer not printing, offline status",
                "solution": "Check USB or network connection. Clear print queue. Restart printer and computer. Update printer drivers.",
                "manual_reference": "Printer Troubleshooting - Common Issues",
            },
        ]
        
        for data in sample_data:
            self.add_solution(**data)
