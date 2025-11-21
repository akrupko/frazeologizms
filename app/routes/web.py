"""Web routes for serving dynamic category pages."""
from flask import Blueprint, render_template, abort, send_from_directory
import os
from app.services.categories import category_service

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


@web_bp.route('/table_phrases.json')
def table_phrases_data():
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    return send_from_directory(project_root, 'table_phrases.json')
