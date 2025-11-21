"""Web routes for serving dynamic category pages."""
from flask import Blueprint, render_template, abort, send_from_directory, request, redirect, url_for
import os
from app.services.categories import category_service
from app.services.slug import slug_service
from app.services.search import search_service
from app.models import PhraseologicalEntry

web_bp = Blueprint('web', __name__)


@web_bp.route('/')
def home():
    general_category = category_service.get_general_category()
    categories = category_service.get_navigation_categories()

    return render_template(
        'home.html',
        category=general_category,
        categories=categories,
        is_home=True,
    )


@web_bp.route('/kategoria/<category_slug>/')
def category_page(category_slug):
    category = category_service.get_category_by_slug(category_slug)
    if not category:
        abort(404)

    categories = category_service.get_navigation_categories()

    return render_template(
        'category.html',
        category=category,
        categories=categories,
        is_home=False,
    )


@web_bp.route('/frazeologizm/<phrase_slug>/')
def phrase_detail(phrase_slug):
    """Phrase detail page."""
    phrase = slug_service.get_phrase_by_slug(phrase_slug)
    if not phrase:
        abort(404)
    
    categories = category_service.get_navigation_categories()
    
    # Get related phrases from same category
    related_phrases = []
    if phrase.category:
        related_phrases = PhraseologicalEntry.query.filter(
            PhraseologicalEntry.category == phrase.category,
            PhraseologicalEntry.id != phrase.id
        ).limit(5).all()
    
    # Check for image files
    image_extensions = ['webp', 'jpg', 'jpeg', 'png']
    phrase_image = None
    for ext in image_extensions:
        image_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            'static', 'images', f'{phrase_slug}.{ext}'
        )
        if os.path.exists(image_path):
            phrase_image = f'images/{phrase_slug}.{ext}'
            break
    
    return render_template(
        'phrase_detail.html',
        phrase=phrase,
        categories=categories,
        related_phrases=related_phrases,
        phrase_image=phrase_image,
        breadcrumbs=[
            {'url': '/', 'title': 'Главная'},
            {'url': f'/kategoria/{phrase.category}/' if phrase.category else None, 'title': phrase.category or 'Без категории'},
            {'url': None, 'title': phrase.phrase}
        ]
    )


@web_bp.route('/search')
def search():
    """Standard search page."""
    query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    categories = category_service.get_navigation_categories()
    
    results = []
    total = 0
    pagination = None
    
    if query and len(query) >= 2:
        offset = (page - 1) * per_page
        results, total = search_service.search_phrases(
            query, 
            limit=per_page, 
            offset=offset
        )
        
        # Simple pagination
        has_next = offset + per_page < total
        has_prev = page > 1
        pagination = {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page,
            'has_next': has_next,
            'has_prev': has_prev,
            'next_num': page + 1 if has_next else None,
            'prev_num': page - 1 if has_prev else None,
        }
    
    return render_template(
        'search.html',
        query=query,
        results=results,
        categories=categories,
        pagination=pagination,
        breadcrumbs=[
            {'url': '/', 'title': 'Главная'},
            {'url': None, 'title': 'Поиск'}
        ]
    )


@web_bp.route('/search/text', methods=['GET', 'POST'])
def search_in_text():
    """Search for phrases within submitted text."""
    text = ''
    matches = []
    
    if request.method == 'POST':
        text = request.form.get('text', '').strip()
    else:
        text = request.args.get('text', '').strip()
    
    categories = category_service.get_navigation_categories()
    
    if text:
        matches = search_service.search_in_text(text)
    
    return render_template(
        'search_text.html',
        text=text,
        matches=matches,
        categories=categories,
        breadcrumbs=[
            {'url': '/', 'title': 'Главная'},
            {'url': None, 'title': 'Поиск в тексте'}
        ]
    )
