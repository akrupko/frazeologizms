"""SEO service for generating metadata, structured data, and SEO elements."""
from __future__ import annotations

import os
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin

import yaml
from flask import request, url_for

from app.extensions import cache


class SEOService:
    """Service for managing SEO metadata and structured data."""

    def __init__(self) -> None:
        self.config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'seo_metadata.yaml'
        )
        self._config: Optional[Dict] = None
        self.site_url = os.getenv('SITE_URL', 'https://frazeologizm.ru')

    @property
    def config(self) -> Dict:
        if self._config is None:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self._config = yaml.safe_load(f) or {}
            else:
                self._config = {}
        return self._config

    def _get_absolute_url(self, path: str) -> str:
        """Get absolute URL for a given path."""
        return urljoin(self.site_url, path)

    def _get_current_url(self) -> str:
        """Get current request URL."""
        try:
            return request.url
        except RuntimeError:
            return self.site_url

    def get_home_metadata(self, phrase_count: int = 0) -> Dict[str, Any]:
        """Generate metadata for home page."""
        overrides = self.config.get('pages', {}).get('home', {})
        
        title = overrides.get('title', 'Тренажер фразеологизмов русского языка - изучение онлайн')
        description = overrides.get(
            'description',
            f'Интерактивный тренажер для изучения более {phrase_count} фразеологизмов русского языка. '
            'Подготовка к ЕГЭ и ОГЭ. Онлайн тесты с объяснениями значений и происхождения.'
        )
        
        canonical = self._get_absolute_url('/')
        
        return {
            'title': title,
            'description': description,
            'canonical': canonical,
            'og': {
                'title': title,
                'description': description,
                'url': canonical,
                'type': 'website',
                'image': self._get_absolute_url(url_for('static', filename='images/og-home.jpg')),
            },
            'twitter': {
                'card': 'summary_large_image',
                'title': title,
                'description': description,
                'image': self._get_absolute_url(url_for('static', filename='images/og-home.jpg')),
            }
        }

    def get_category_metadata(self, category: Dict) -> Dict[str, Any]:
        """Generate metadata for category pages."""
        category_slug = category.get('slug', '')
        overrides = self.config.get('pages', {}).get('categories', {}).get(category_slug, {})
        
        title = overrides.get('title', category.get('seo', {}).get('title', f'{category.get("display_name")} - Тренажер фразеологизмов'))
        description = overrides.get('description', category.get('seo', {}).get('description', f'Изучение фразеологизмов по теме "{category.get("display_name")}"'))
        
        canonical = self._get_absolute_url(f'/kategoria/{category_slug}/')
        
        return {
            'title': title,
            'description': description,
            'canonical': canonical,
            'h1': category.get('header', {}).get('title', f'{category.get("icon", "📚")} Тренажер фразеологизмов'),
            'h2': category.get('header', {}).get('description', f'Фразеологизмы по теме: {category.get("display_name")}'),
            'og': {
                'title': title,
                'description': description,
                'url': canonical,
                'type': 'website',
                'image': self._get_absolute_url(url_for('static', filename=f'images/category-{category_slug}.jpg')),
            },
            'twitter': {
                'card': 'summary_large_image',
                'title': title,
                'description': description,
                'image': self._get_absolute_url(url_for('static', filename=f'images/category-{category_slug}.jpg')),
            }
        }

    def get_phrase_metadata(self, phrase: Any, phrase_image: Optional[str] = None) -> Dict[str, Any]:
        """Generate metadata for phrase detail pages."""
        phrase_slug = phrase.slug
        overrides = self.config.get('pages', {}).get('phrases', {}).get(phrase_slug, {})
        
        first_meaning = phrase.meanings[0] if phrase.meanings and len(phrase.meanings) > 0 else 'Значение и происхождение фразеологизма'
        
        title = overrides.get('title', f'{phrase.phrase} - {phrase.category or "Фразеологизм"} | Тренажер фразеологизмов')
        description = overrides.get('description', f'{phrase.phrase}: {first_meaning}. Изучение русских идиом и фразеологических выражений.')
        
        canonical = self._get_absolute_url(f'/frazeologizm/{phrase_slug}/')
        
        # Determine image URL
        image_url = self._get_absolute_url(url_for('static', filename='images/og-phrase.jpg'))
        if phrase_image:
            image_url = self._get_absolute_url(url_for('static', filename=phrase_image))
        
        return {
            'title': title,
            'description': description,
            'canonical': canonical,
            'h1': phrase.phrase,
            'og': {
                'title': title,
                'description': description,
                'url': canonical,
                'type': 'article',
                'image': image_url,
            },
            'twitter': {
                'card': 'summary_large_image',
                'title': title,
                'description': description,
                'image': image_url,
            }
        }

    def get_search_metadata(self, query: str = '') -> Dict[str, Any]:
        """Generate metadata for search pages."""
        if query:
            title = f'Поиск: {query} - Тренажер фразеологизмов'
            description = f'Результаты поиска фразеологизмов по запросу "{query}"'
        else:
            title = 'Поиск фразеологизмов - Тренажер фразеологизмов'
            description = 'Поиск русских фразеологизмов и идиом по ключевым словам'
        
        canonical = self._get_absolute_url('/search')
        
        return {
            'title': title,
            'description': description,
            'canonical': canonical,
            'robots': 'noindex, follow',  # Don't index search result pages
        }

    def get_website_structured_data(self) -> Dict[str, Any]:
        """Generate WebSite JSON-LD structured data with SearchAction."""
        return {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "Тренажер фразеологизмов русского языка",
            "description": "Интерактивный тренажер для изучения фразеологизмов русского языка. Подготовка к ЕГЭ и ОГЭ.",
            "url": self.site_url,
            "potentialAction": {
                "@type": "SearchAction",
                "target": {
                    "@type": "EntryPoint",
                    "urlTemplate": f"{self.site_url}/search?q={{search_term_string}}"
                },
                "query-input": "required name=search_term_string"
            }
        }

    def get_collection_structured_data(self, category: Dict) -> Dict[str, Any]:
        """Generate CollectionPage JSON-LD for category pages."""
        return {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": category.get('display_name', ''),
            "description": category.get('seo', {}).get('description', ''),
            "url": self._get_absolute_url(f'/kategoria/{category.get("slug", "")}/'),
            "numberOfItems": category.get('count', 0),
            "about": {
                "@type": "Thing",
                "name": f"Фразеологизмы: {category.get('display_name', '')}",
                "description": category.get('seo', {}).get('description', '')
            }
        }

    def get_phrase_structured_data(self, phrase: Any, phrase_image: Optional[str] = None) -> List[Dict[str, Any]]:
        """Generate Article and DefinedTerm JSON-LD for phrase detail pages."""
        phrase_url = self._get_absolute_url(f'/frazeologizm/{phrase.slug}/')
        
        # Image URL
        image_url = None
        if phrase_image:
            image_url = self._get_absolute_url(url_for('static', filename=phrase_image))
        
        # Article schema
        article_schema = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": phrase.phrase,
            "description": phrase.meanings[0] if phrase.meanings and len(phrase.meanings) > 0 else '',
            "url": phrase_url,
            "datePublished": phrase.created_at.isoformat() if phrase.created_at else None,
            "dateModified": phrase.updated_at.isoformat() if phrase.updated_at else None,
            "author": {
                "@type": "Organization",
                "name": "Тренажер фразеологизмов"
            }
        }
        
        if image_url:
            article_schema["image"] = image_url
        
        # DefinedTerm schema
        defined_term_schema = {
            "@context": "https://schema.org",
            "@type": "DefinedTerm",
            "name": phrase.phrase,
            "description": '; '.join(phrase.meanings) if phrase.meanings else '',
            "inDefinedTermSet": {
                "@type": "DefinedTermSet",
                "name": f"Фразеологизмы: {phrase.category}" if phrase.category else "Русские фразеологизмы"
            }
        }
        
        if phrase.etymology:
            defined_term_schema["additionalProperty"] = {
                "@type": "PropertyValue",
                "name": "etymology",
                "value": phrase.etymology
            }
        
        if image_url:
            defined_term_schema["image"] = image_url
        
        return [article_schema, defined_term_schema]


seo_service = SEOService()
