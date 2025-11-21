"""Search service for phraseological entries."""
from __future__ import annotations

import re
from typing import List, Dict, Tuple
from unicodedata import normalize

from app.extensions import cache, db
from app.models import PhraseologicalEntry


class SearchService:
    """Service for searching phraseological entries."""

    @staticmethod
    def normalize_text(text: str) -> str:
        """Normalize text for comparison (remove punctuation, lowercase, etc.)."""
        # Remove punctuation and normalize Unicode
        text = normalize('NFKD', text.lower())
        # Remove all non-word characters except spaces
        text = re.sub(r'[^\w\s]', ' ', text)
        # Normalize multiple spaces
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    @staticmethod
    def extract_phrases_from_text(text: str, min_length: int = 2) -> List[str]:
        """Extract potential phrases from text for matching."""
        # Split into words and create n-grams
        words = text.split()
        phrases = []
        
        # Add individual words
        phrases.extend([word for word in words if len(word) >= min_length])
        
        # Add 2-3 word phrases
        for i in range(len(words) - 1):
            phrase = f"{words[i]} {words[i+1]}"
            if len(phrase) >= min_length * 2:
                phrases.append(phrase)
                
        for i in range(len(words) - 2):
            phrase = f"{words[i]} {words[i+1]} {words[i+2]}"
            if len(phrase) >= min_length * 3:
                phrases.append(phrase)
                
        return phrases

    def search_phrases(
        self, 
        query: str, 
        limit: int = 20, 
        offset: int = 0,
        search_fields: List[str] = None
    ) -> Tuple[List[PhraseologicalEntry], int]:
        """Search phrases by query with ranking."""
        if not query or len(query.strip()) < 2:
            return [], 0

        query = query.strip()
        search_fields = search_fields or ['phrase', 'meanings', 'etymology']
        
        # Build base query
        base_query = PhraseologicalEntry.query
        
        # Add search conditions for each field
        conditions = []
        for field in search_fields:
            if field == 'phrase':
                conditions.append(PhraseologicalEntry.phrase.ilike(f'%{query}%'))
            elif field == 'meanings':
                # Search in JSON meanings array
                conditions.append(db.cast(PhraseologicalEntry.meanings, db.Text).ilike(f'%{query}%'))
            elif field == 'etymology':
                conditions.append(PhraseologicalEntry.etymology.ilike(f'%{query}%'))
        
        # Apply conditions with OR
        from sqlalchemy import or_
        base_query = base_query.filter(or_(*conditions))
        
        # Count total results
        total = base_query.count()
        
        # Apply ranking and pagination
        # Prioritize exact phrase matches, then partial matches
        results = base_query.order_by(
            # Exact phrase match first
            PhraseologicalEntry.phrase.ilike(f'%{query}%').desc(),
            # Then by phrase length (shorter phrases first)
            db.func.length(PhraseologicalEntry.phrase).asc(),
            # Then alphabetically
            PhraseologicalEntry.phrase.asc()
        ).offset(offset).limit(limit).all()
        
        return results, total

    def search_in_text(
        self, 
        text: str, 
        min_phrase_length: int = 2
    ) -> List[Dict]:
        """Search for phrases within arbitrary text."""
        if not text or len(text.strip()) < min_phrase_length:
            return []
        
        # Normalize input text
        normalized_text = self.normalize_text(text)
        
        # Get all phrases from database
        all_phrases = PhraseologicalEntry.query.all()
        
        matches = []
        
        for phrase in all_phrases:
            normalized_phrase = self.normalize_text(phrase.phrase)
            
            # Check if phrase exists in text
            if normalized_phrase in normalized_text:
                # Count occurrences
                count = normalized_text.count(normalized_phrase)
                
                matches.append({
                    'phrase': phrase,
                    'count': count,
                    'normalized_phrase': normalized_phrase,
                    'match_positions': self._find_match_positions(normalized_text, normalized_phrase)
                })
        
        # Sort by count (descending) then phrase length (ascending)
        matches.sort(key=lambda x: (-x['count'], len(x['phrase'].phrase)))
        
        return matches

    def _find_match_positions(self, text: str, pattern: str) -> List[int]:
        """Find all starting positions of pattern in text."""
        positions = []
        start = 0
        while True:
            pos = text.find(pattern, start)
            if pos == -1:
                break
            positions.append(pos)
            start = pos + 1
        return positions

    @cache.memoize(timeout=300)
    def get_popular_searches(self, limit: int = 10) -> List[str]:
        """Get popular search terms (could be enhanced with analytics)."""
        # For now, return some common phraseological terms
        return [
            "быть",
            "дело",
            "рука",
            "голова",
            "сердце",
            "время",
            "день",
            "дом",
            "вода",
            "огонь"
        ]

    def highlight_matches(self, text: str, query: str) -> str:
        """Highlight query matches in text."""
        if not query:
            return text
        
        # Create case-insensitive pattern
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        return pattern.sub(f'<mark>{query}</mark>', text)


search_service = SearchService()