"""Category service for managing phraseological categories."""
from __future__ import annotations

import os
from typing import Dict, List, Optional

import yaml
from slugify import slugify

from app.extensions import cache, db
from app.models import PhraseologicalEntry


class CategoryService:
    """Service for hydrating categories with metadata and SEO copy."""

    def __init__(self) -> None:
        self.config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'category_config.yaml'
        )
        self._config: Optional[Dict] = None

    @property
    def config(self) -> Dict:
        if self._config is None:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self._config = yaml.safe_load(f) or {}
            else:
                self._config = {}
        return self._config

    def _get_config_categories(self) -> Dict:
        return self.config.get('categories', {})

    def get_category_config(self, category_key: str) -> Optional[Dict]:
        return self._get_config_categories().get(category_key)

    @cache.memoize(timeout=3600)
    def get_db_categories(self) -> List[Dict]:
        categories = db.session.query(
            PhraseologicalEntry.category,
            db.func.count(PhraseologicalEntry.id).label('count')
        ).filter(
            PhraseologicalEntry.category.isnot(None)
        ).group_by(
            PhraseologicalEntry.category
        ).all()

        return [{'name': cat[0], 'count': cat[1]} for cat in categories]

    @cache.memoize(timeout=3600)
    def get_total_phrase_count(self) -> int:
        count = db.session.query(db.func.count(PhraseologicalEntry.id)).scalar()
        return count or 0

    def _enrich_category(
        self,
        category_key: str,
        category_config: Optional[Dict],
        count: int = 0,
    ) -> Dict:
        category_config = category_config or {}

        return {
            'key': category_key,
            'display_name': category_config.get('display_name', category_key.replace('_', ' ').title()),
            'icon': category_config.get('icon', '📚'),
            'slug': category_config.get('slug', slugify(category_key)),
            'count': count,
            'seo': category_config.get('seo', {}),
            'header': category_config.get('header', {}),
            'footer_text': category_config.get('footer_text', ''),
        }

    def _generate_fallback_category(self, category_key: str, count: int) -> Dict:
        display_name = category_key.replace('_', ' ').title()
        slug = slugify(category_key)

        return {
            'key': category_key,
            'display_name': display_name,
            'icon': '📚',
            'slug': slug,
            'count': count,
            'seo': {
                'title': f'Фразеологизмы: {display_name} - русские идиомы онлайн',
                'description': f'{display_name} - фразеологизмы по теме "{display_name}". Изучение русских идиом онлайн.',
                'features_title': f'Особенности изучения фразеологизмов темы "{display_name}"',
                'features_text': f'Фразеологизмы данной категории часто встречаются в заданиях ЕГЭ и ОГЭ по русскому языку. Изучение темы "{display_name}" поможет вам:',
                'footer': 'Начните изучение прямо сейчас и повысьте свои шансы на успешную сдачу экзаменов по русскому языку!',
            },
            'header': {
                'title': '📚 Тренажер фразеологизмов',
                'description': f'Фразеологизмы по теме: {display_name}',
            },
            'footer_text': f'📚 {display_name} - фразеологизмы',
            'count': count,
        }

    @cache.memoize(timeout=3600)
    def get_all_categories_enriched(self) -> List[Dict]:
        db_categories = self.get_db_categories()
        enriched: List[Dict] = []

        for db_cat in db_categories:
            cat_key = db_cat['name']
            cat_config = self.get_category_config(cat_key)

            if cat_config:
                enriched.append(self._enrich_category(cat_key, cat_config, db_cat['count']))
            else:
                enriched.append(self._generate_fallback_category(cat_key, db_cat['count']))

        return sorted(enriched, key=lambda x: x['display_name'])

    @cache.memoize(timeout=600)
    def get_navigation_categories(self) -> List[Dict]:
        categories = []
        general_category = self.get_general_category()
        categories.append({
            'url': '/',
            'display_name': general_category['display_name'],
            'icon': general_category['icon'],
            'count': general_category['count'],
            'slug': general_category['slug'],
            'title': general_category['seo'].get('title', ''),
        })

        for cat in self.get_all_categories_enriched():
            categories.append({
                'url': f'/kategoria/{cat["slug"]}/',
                'display_name': cat['display_name'],
                'icon': cat['icon'],
                'count': cat['count'],
                'slug': cat['slug'],
                'title': cat['seo'].get('title', ''),
            })

        return categories

    def get_general_category(self) -> Dict:
        config = self.get_category_config('general')
        total_phrases = self.get_total_phrase_count()
        return {
            **self._enrich_category('general', config, total_phrases),
            'slug': (config or {}).get('slug', 'vse'),
        }

    def get_category_by_slug(self, slug: str) -> Optional[Dict]:
        general = self.get_general_category()
        normalized_slug = slug.strip('/')
        if general['slug'] == normalized_slug:
            return general

        for cat in self.get_all_categories_enriched():
            if cat['slug'] == normalized_slug:
                return cat
        return None


category_service = CategoryService()
