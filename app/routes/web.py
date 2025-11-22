"""Web routes for serving dynamic category pages."""
from flask import Blueprint, render_template, abort, send_from_directory, request, redirect, url_for
import os
from app.services.categories import category_service
from app.services.slug import slug_service
from app.services.search import search_service
from app.services.seo import seo_service
from app.models import PhraseologicalEntry

web_bp = Blueprint('web', __name__)


@web_bp.route('/')
def home():
    general_category = category_service.get_general_category()
    categories = category_service.get_navigation_categories()
    
    # SEO metadata
    phrase_count = category_service.get_total_phrase_count()
    seo_meta = seo_service.get_home_metadata(phrase_count)
    structured_data = seo_service.get_website_structured_data()

    return render_template(
        'home.html',
        category=general_category,
        categories=categories,
        is_home=True,
        seo_meta=seo_meta,
        structured_data=structured_data,
    )


@web_bp.route('/kategoria/<category_slug>/')
def category_page(category_slug):
    category = category_service.get_category_by_slug(category_slug)
    if not category:
        abort(404)

    categories = category_service.get_navigation_categories()
    
    # SEO metadata
    seo_meta = seo_service.get_category_metadata(category)
    structured_data = seo_service.get_collection_structured_data(category)

    return render_template(
        'category.html',
        category=category,
        categories=categories,
        is_home=False,
        seo_meta=seo_meta,
        structured_data=structured_data,
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
    
    # SEO metadata
    seo_meta = seo_service.get_phrase_metadata(phrase, phrase_image)
    structured_data = seo_service.get_phrase_structured_data(phrase, phrase_image)
    
    return render_template(
        'phrase_detail.html',
        phrase=phrase,
        categories=categories,
        related_phrases=related_phrases,
        phrase_image=phrase_image,
        seo_meta=seo_meta,
        structured_data=structured_data,
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
    
    # SEO metadata
    seo_meta = seo_service.get_search_metadata(query)
    
    return render_template(
        'search.html',
        query=query,
        results=results,
        categories=categories,
        pagination=pagination,
        seo_meta=seo_meta,
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
    
    # SEO metadata
    seo_meta = {
        'title': 'Поиск фразеологизмов в тексте - Тренажер фразеологизмов',
        'description': 'Найдите все фразеологизмы в вашем тексте. Инструмент для анализа текста на наличие русских идиом.',
        'canonical': seo_service._get_absolute_url('/search/text'),
        'robots': 'noindex, follow',
    }
    
    return render_template(
        'search_text.html',
        text=text,
        matches=matches,
        categories=categories,
        seo_meta=seo_meta,
        breadcrumbs=[
            {'url': '/', 'title': 'Главная'},
            {'url': None, 'title': 'Поиск в тексте'}
        ]
    )


@web_bp.route('/sitemap.xml')
def sitemap():
    """Generate dynamic sitemap.xml."""
    from flask import Response, make_response
    from app.extensions import cache
    from datetime import datetime
    
    @cache.memoize(timeout=3600)
    def generate_sitemap():
        """Generate sitemap content with caching."""
        site_url = os.getenv('SITE_URL', 'https://frazeologizm.ru')
        
        urls = []
        
        # Home page
        urls.append({
            'loc': site_url + '/',
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'changefreq': 'daily',
            'priority': '1.0'
        })
        
        # Category pages
        categories = category_service.get_all_categories_enriched()
        for cat in categories:
            urls.append({
                'loc': site_url + f'/kategoria/{cat["slug"]}/',
                'lastmod': datetime.now().strftime('%Y-%m-%d'),
                'changefreq': 'weekly',
                'priority': '0.8'
            })
        
        # Phrase detail pages
        phrases = PhraseologicalEntry.query.all()
        for phrase in phrases:
            lastmod = phrase.updated_at.strftime('%Y-%m-%d') if phrase.updated_at else datetime.now().strftime('%Y-%m-%d')
            urls.append({
                'loc': site_url + f'/frazeologizm/{phrase.slug}/',
                'lastmod': lastmod,
                'changefreq': 'monthly',
                'priority': '0.6'
            })
        
        # Generate XML
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        
        for url in urls:
            xml += '  <url>\n'
            xml += f'    <loc>{url["loc"]}</loc>\n'
            xml += f'    <lastmod>{url["lastmod"]}</lastmod>\n'
            xml += f'    <changefreq>{url["changefreq"]}</changefreq>\n'
            xml += f'    <priority>{url["priority"]}</priority>\n'
            xml += '  </url>\n'
        
        xml += '</urlset>'
        
        return xml
    
    sitemap_xml = generate_sitemap()
    response = make_response(sitemap_xml)
    response.headers['Content-Type'] = 'application/xml; charset=utf-8'
    return response


@web_bp.route('/robots.txt')
def robots():
    """Generate robots.txt file."""
    from flask import Response
    
    site_url = os.getenv('SITE_URL', 'https://frazeologizm.ru')
    
    robots_txt = f"""User-agent: *
Allow: /
Disallow: /api/
Disallow: /search?
Disallow: /search/text

Sitemap: {site_url}/sitemap.xml
"""
    
    response = Response(robots_txt, mimetype='text/plain')
    response.headers['Cache-Control'] = 'public, max-age=86400'
    return response
