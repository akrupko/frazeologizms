"""Services package."""
from app.services.categories import CategoryService, category_service
from app.services.seo import SEOService, seo_service

__all__ = ['CategoryService', 'category_service', 'SEOService', 'seo_service']
