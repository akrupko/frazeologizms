"""API routes for phraseological data."""
from flask import Blueprint, jsonify, request

from app.extensions import cache, db
from app.models import PhraseologicalEntry

api_bp = Blueprint('api', __name__)


@api_bp.route('/phrases', methods=['GET'])
@cache.cached(timeout=300)
def get_phrases():
    """Get all phrases with optional filtering."""
    category = request.args.get('category')
    limit = request.args.get('limit', 20, type=int)
    offset = request.args.get('offset', 0, type=int)

    query = PhraseologicalEntry.query

    if category:
        query = query.filter_by(category=category)

    total = query.count()
    phrases = query.offset(offset).limit(limit).all()

    return jsonify({
        'phrases': [p.to_dict() for p in phrases],
        'total': total,
        'limit': limit,
        'offset': offset,
    })


@api_bp.route('/phrases/search', methods=['GET'])
def search_phrases():
    """Search for phrases."""
    q = request.args.get('q', '')
    limit = request.args.get('limit', 20, type=int)

    if not q or len(q) < 2:
        return jsonify({'phrases': [], 'error': 'Query must be at least 2 characters'}), 400

    results = PhraseologicalEntry.search(q, limit=limit)

    return jsonify({
        'phrases': [p.to_dict() for p in results],
        'query': q,
    })


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
    """Get all available categories."""
    categories = db.session.query(
        PhraseologicalEntry.category,
        db.func.count(PhraseologicalEntry.id).label('count')
    ).filter(PhraseologicalEntry.category.isnot(None)).group_by(
        PhraseologicalEntry.category
    ).all()

    return jsonify({
        'categories': [
            {'name': cat[0], 'count': cat[1]} for cat in categories
        ]
    })


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
