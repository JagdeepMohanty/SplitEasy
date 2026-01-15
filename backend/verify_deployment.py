#!/usr/bin/env python3
"""
Deployment verification script for EasyXpense backend
Run this to verify MongoDB connection and environment setup
"""
import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient

def verify_environment():
    """Verify all required environment variables"""
    print("=" * 50)
    print("ENVIRONMENT VERIFICATION")
    print("=" * 50)
    
    load_dotenv()
    
    required_vars = ['MONGO_URI']
    optional_vars = ['FLASK_ENV', 'PORT']
    
    all_good = True
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Mask sensitive data
            if 'URI' in var or 'SECRET' in var:
                display_value = value[:20] + '...' if len(value) > 20 else '***'
            else:
                display_value = value
            print(f"✓ {var}: {display_value}")
        else:
            print(f"✗ {var}: NOT SET (REQUIRED)")
            all_good = False
    
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            print(f"✓ {var}: {value}")
        else:
            print(f"○ {var}: Not set (optional)")
    
    return all_good

def verify_mongodb():
    """Verify MongoDB connection"""
    print("\n" + "=" * 50)
    print("MONGODB CONNECTION TEST")
    print("=" * 50)
    
    mongo_uri = os.getenv('MONGO_URI')
    if not mongo_uri:
        print("✗ MONGO_URI not set")
        return False
    
    try:
        print("Connecting to MongoDB...")
        client = MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=10000
        )
        
        # Test connection
        db = client.get_default_database()
        db.command('ping')
        
        print(f"✓ Connected to database: {db.name}")
        
        # List collections
        collections = db.list_collection_names()
        print(f"✓ Collections: {collections if collections else 'None (will be created on first insert)'}")
        
        # Test insert
        print("\nTesting insert operation...")
        test_collection = db.test_verification
        result = test_collection.insert_one({'test': 'verification', 'timestamp': 'now'})
        print(f"✓ Insert successful. ID: {result.inserted_id}")
        
        # Clean up
        test_collection.delete_one({'_id': result.inserted_id})
        print("✓ Cleanup successful")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"✗ MongoDB connection failed: {e}")
        return False

def main():
    """Main verification function"""
    print("\n🚀 EasyXpense Backend Deployment Verification\n")
    
    env_ok = verify_environment()
    mongo_ok = verify_mongodb()
    
    print("\n" + "=" * 50)
    print("VERIFICATION SUMMARY")
    print("=" * 50)
    
    if env_ok and mongo_ok:
        print("✓ All checks passed! Backend is ready for deployment.")
        sys.exit(0)
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == '__main__':
    main()
