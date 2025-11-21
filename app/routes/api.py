"""API routes for phraseological data."""
from flask import Blueprint, jsonify, request, make_response
from sqlalchemy import func
import random

from app.extensions import cache, db
from app.models import PhraseologicalEntry
from app.services.categories import category_service

api_bp = Blueprint('api', __name__)


@api_bp.route('/phrases', methods=['GET'])
@cache.cached(timeout=300, query_string=True)
def get_phrases():
    """Get all phrases with optional filtering for trainer compatibility."""
    category = request.args.get('category')
    limit = request.args.get('limit', type=int)
    offset = request.args.get('offset', 0, type=int)
    random_flag = request.args.get('random', 'false').lower() == 'true'

    query = PhraseologicalEntry.query

    if category:
        query = query.filter_by(category=category)

    total = query.count()
    
    # Handle random ordering
    if random_flag:
        phrases = query.order_by(func.random()).limit(limit or 20).all()
    else:
        phrases = query.offset(offset).limit(limit or 20).all()

    # Create response with Cache-Control headers
    response = make_response(jsonify({
        'phrases': [p.to_dict() for p in phrases],
        'total': total,
        'limit': limit or 20,
        'offset': offset,
    }))
    
    # Set cache headers for trainer compatibility
    response.cache_control.max_age = 300
    response.cache_control.public = True
    
    return response


@api_bp.route('/phrases/search', methods=['GET'])
@cache.cached(timeout=180, query_string=True)
def search_phrases():
    """Search for phrases with autocomplete support."""
    q = request.args.get('q', '')
    limit = request.args.get('limit', 20, type=int)

    if not q or len(q) < 2:
        return jsonify({'phrases': [], 'error': 'Query must be at least 2 characters'}), 400

    results = PhraseologicalEntry.search(q, limit=limit)

    # Create response with Cache-Control headers
    response = make_response(jsonify({
        'phrases': [p.to_dict() for p in results],
        'query': q,
    }))
    
    # Set cache headers for autocomplete
    response.cache_control.max_age = 180
    response.cache_control.public = True
    
    return response


@api_bp.route('/phrases/<int:phrase_id>', methods=['GET'])
@cache.cached(timeout=3600)
def get_phrase(phrase_id):
    """Get a single phrase by ID."""
    phrase = PhraseologicalEntry.query.get_or_404(phrase_id)
    return jsonify(phrase.to_dict())


@api_bp.route('/phrases/slug/<slug>', methods=['GET'])
@cache.cached(timeout=3600)
def get_phrase_by_slug(slug):
    """Get a phrase by its slug."""
    # Since slugs are generated from the phrase, we need to search
    phrases = PhraseologicalEntry.query.all()
    for phrase in phrases:
        if phrase.slug == slug:
            return jsonify(phrase.to_dict())
    return jsonify({'error': 'Phrase not found'}), 404


@api_bp.route('/categories', methods=['GET'])
@cache.cached(timeout=3600)
def get_categories():
    """Get all available categories with enriched metadata for trainer."""
    # Get enriched categories from the category service
    enriched_categories = category_service.get_all_categories_enriched()
    
    # Transform to match expected structure for trainer
    categories_data = []
    for cat in enriched_categories:
        categories_data.append({
            'key': cat['key'],
            'name': cat['display_name'],
            'slug': cat['slug'],
            'count': cat['count'],
            'icon': cat['icon'],
            'seo': cat.get('seo', {}),
            'description': cat.get('seo', {}).get('description', ''),
        })

    # Create response with Cache-Control headers
    response = make_response(jsonify({
        'categories': categories_data,
    }))
    
    # Set cache headers for categories (changes rarely)
    response.cache_control.max_age = 3600
    response.cache_control.public = True
    
    return response


@api_bp.route('/search', methods=['GET'])
@cache.cached(timeout=180, query_string=True)
def search_autocomplete():
    """Search endpoint for autocomplete functionality."""
    q = request.args.get('q', '')
    limit = request.args.get('limit', 10, type=int)

    if not q or len(q) < 2:
        return jsonify({'results': [], 'error': 'Query must be at least 2 characters'}), 400

    # Search in phrases and meanings
    results = PhraseologicalEntry.search(q, limit=limit)
    
    # Format for autocomplete
    autocomplete_results = []
    for phrase in results:
        autocomplete_results.append({
            'id': phrase.id,
            'phrase': phrase.phrase,
            'category': phrase.category,
            'slug': phrase.slug,
            'meanings': phrase.meanings or [],
        })

    # Create response with Cache-Control headers
    response = make_response(jsonify({
        'results': autocomplete_results,
        'query': q,
    }))
    
    # Set cache headers for autocomplete
    response.cache_control.max_age = 180
    response.cache_control.public = True
    
    return response


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        count = PhraseologicalEntry.query.count()
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'phrases_count': count,
        })
    except Exception as exc:  # pragma: no cover - defensive logging
        return jsonify({
            'status': 'unhealthy',
            'error': str(exc),
        }), 500
