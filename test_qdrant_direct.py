"""Quick test of Qdrant connection with provided credentials"""
from qdrant_client import QdrantClient

print("Testing Qdrant Cloud connection with provided code...")

try:
    qdrant_client = QdrantClient(
        url="https://b389eee5-b895-4eab-9abb-0fed27c52f29.eu-central-1-0.aws.cloud.qdrant.io:6333", 
        api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.rsRKJaUkbXBFXSCYLVFKQrLFsb8-xYZmammoCIZ664k",
    )
    
    print("✓ Client created successfully")
    
    collections = qdrant_client.get_collections()
    print(f"✓ Connected to Qdrant!")
    print(f"✓ Found {len(collections.collections)} collections:")
    for coll in collections.collections:
        print(f"  - {coll.name}")
        
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
