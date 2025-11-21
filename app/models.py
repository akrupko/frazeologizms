"""SQLAlchemy models for the application."""
from slugify import slugify
from app.extensions import db


class PhraseologicalEntry(db.Model):
    """Model for phraseological expressions from the phraseological_dict table."""
    
    __tablename__ = 'phraseological_dict'
    
    id = db.Column(db.Integer, primary_key=True)
    phrase = db.Column(db.String(500), nullable=False, unique=True, index=True)
    meanings = db.Column(db.JSON, nullable=True)
    etymology = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(100), nullable=True, index=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    def __repr__(self):
        return f'<PhraseologicalEntry {self.phrase}>'
    
    @property
    def slug(self):
        """Generate a URL-safe slug from the phrase."""
        return slugify(self.phrase)
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'phrase': self.phrase,
            'meanings': self.meanings or [],
            'etymology': self.etymology,
            'category': self.category,
            'slug': self.slug,
        }
    
    @classmethod
    def get_by_category(cls, category, limit=None, offset=0):
        """Get entries by category."""
        query = cls.query.filter_by(category=category).offset(offset)
        if limit:
            query = query.limit(limit)
        return query.all()
    
    @classmethod
    def search(cls, query_text, limit=20):
        """Search for entries by phrase or meaning."""
        return cls.query.filter(
            cls.phrase.ilike(f'%{query_text}%')
        ).limit(limit).all()
