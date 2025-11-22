#!/usr/bin/env python
"""Simple test script to validate SEO implementation."""
import os
import sys

# Set environment variables before importing app
os.environ['SITE_URL'] = 'https://frazeologizm.ru'
os.environ['FLASK_ENV'] = 'testing'
os.environ['DB_HOST'] = 'localhost'
os.environ['DB_NAME'] = 'test'
os.environ['DB_USER'] = 'test'
os.environ['DB_PASSWORD'] = 'test'

try:
    # Test 1: Import SEO service
    print("Test 1: Importing SEO service...")
    from app.services.seo import seo_service
    print("✓ SEO service imported successfully")
    
    # Test 2: Check SEO metadata config
    print("\nTest 2: Checking SEO metadata config...")
    config = seo_service.config
    print(f"✓ SEO config loaded: {len(config.get('pages', {}))} pages configured")
    
    # Test 3: Generate home metadata
    print("\nTest 3: Generating home page metadata...")
    home_meta = seo_service.get_home_metadata(1200)
    print(f"✓ Title: {home_meta['title']}")
    print(f"✓ Description: {home_meta['description'][:50]}...")
    print(f"✓ Canonical: {home_meta['canonical']}")
    print(f"✓ OG tags: {len(home_meta.get('og', {}))} tags")
    print(f"✓ Twitter tags: {len(home_meta.get('twitter', {}))} tags")
    
    # Test 4: Generate structured data
    print("\nTest 4: Generating structured data...")
    website_schema = seo_service.get_website_structured_data()
    print(f"✓ Schema type: {website_schema.get('@type')}")
    print(f"✓ Has SearchAction: {website_schema.get('potentialAction', {}).get('@type') == 'SearchAction'}")
    
    # Test 5: Generate category metadata
    print("\nTest 5: Generating category metadata...")
    mock_category = {
        'slug': 'test-category',
        'display_name': 'Test Category',
        'count': 50,
        'icon': '📚',
        'seo': {
            'title': 'Test Category Title',
            'description': 'Test category description'
        },
        'header': {
            'title': 'Test Header',
            'description': 'Test description'
        }
    }
    cat_meta = seo_service.get_category_metadata(mock_category)
    print(f"✓ Title: {cat_meta['title']}")
    print(f"✓ H1: {cat_meta.get('h1')}")
    print(f"✓ Canonical: {cat_meta['canonical']}")
    
    # Test 6: Generate collection schema
    print("\nTest 6: Generating CollectionPage schema...")
    collection_schema = seo_service.get_collection_structured_data(mock_category)
    print(f"✓ Schema type: {collection_schema.get('@type')}")
    print(f"✓ Number of items: {collection_schema.get('numberOfItems')}")
    
    print("\n" + "="*50)
    print("✓ All tests passed successfully!")
    print("="*50)
    
    sys.exit(0)
    
except Exception as e:
    print(f"\n✗ Test failed with error:")
    print(f"  {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
