"""
Detailed Qdrant Cloud diagnostic to identify the 400 Bad Request issue
"""
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME")

print("=" * 70)
print("🔍 Detailed Qdrant Diagnostic")
print("=" * 70)

try:
    print("\n1️⃣ Creating client...")
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        check_compatibility=False,
        timeout=10
    )
    print("   ✓ Client created")
    
    print("\n2️⃣ Getting collections...")
    collections_response = client.get_collections()
    print(f"   ✓ Got response: {type(collections_response)}")
    print(f"   ✓ Number of collections: {len(collections_response.collections)}")
    
    if collections_response.collections:
        print(f"\n   Available collections:")
        for coll in collections_response.collections:
            print(f"     - Name: {coll.name}")
            print(f"       Points count: {coll.points_count}")
    
    print(f"\n3️⃣ Looking for '{COLLECTION_NAME}' collection...")
    collection_names = [c.name for c in collections_response.collections]
    
    if COLLECTION_NAME in collection_names:
        print(f"   ✓ Collection '{COLLECTION_NAME}' exists")
        
        print(f"\n4️⃣ Getting collection info...")
        coll_info = client.get_collection(COLLECTION_NAME)
        print(f"   ✓ Points count: {coll_info.points_count}")
        print(f"   ✓ Vectors config: {coll_info.config.vectors}")
        
    else:
        print(f"   ✗ Collection '{COLLECTION_NAME}' NOT found")
        print(f"   Available: {collection_names}")
        
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)

