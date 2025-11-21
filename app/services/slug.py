"""Slug service for mapping phrase slugs to IDs with caching."""
from __future__ import annotations

from typing import Dict, Optional

from app.extensions import cache, db
from app.models import PhraseologicalEntry


class SlugService:
    """Service for managing phrase slug to ID mappings with caching."""

    @cache.memoize(timeout=3600)
    def get_slug_to_id_mapping(self) -> Dict[str, int]:
        """Get all phrase slug to ID mappings."""
        phrases = PhraseologicalEntry.query.all()
        return {phrase.slug: phrase.id for phrase in phrases}

    def get_id_by_slug(self, slug: str) -> Optional[int]:
        """Get phrase ID by slug, using cache first."""
        mapping = self.get_slug_to_id_mapping()
        return mapping.get(slug)

    def get_phrase_by_slug(self, slug: str) -> Optional[PhraseologicalEntry]:
        """Get phrase by slug, using cache first."""
        phrase_id = self.get_id_by_slug(slug)
        if phrase_id:
            return PhraseologicalEntry.query.get(phrase_id)
        return None

    def clear_cache(self) -> None:
        """Clear the slug mapping cache."""
        cache.delete_memoized(self.get_slug_to_id_mapping)

    def refresh_for_phrase(self, phrase: PhraseologicalEntry) -> None:
        """Refresh cache for a specific phrase (useful after insert/update)."""
        self.clear_cache()


slug_service = SlugService()