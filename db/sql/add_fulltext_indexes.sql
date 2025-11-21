-- SQL script to add fulltext indexes for improved search performance
-- Run this script manually on your MySQL database if needed

-- Create fulltext index for phrase column
-- Note: Requires InnoDB engine and MySQL 5.6+ or MariaDB 10.0+
ALTER TABLE phraseological_dict ADD FULLTEXT(phrase);

-- Create fulltext index for meanings column (JSON cast to text)
-- This might need adjustments based on your MySQL version
-- ALTER TABLE phraseological_dict ADD FULLTEXT(CAST(meanings AS CHAR));

-- Create fulltext index for etymology column
ALTER TABLE phraseological_dict ADD FULLTEXT(etymology);

-- Combined fulltext index for better search performance
ALTER TABLE phraseological_dict ADD FULLTEXT search_index(phrase, etymology);

-- Alternative: If you want to include meanings, you might need to create a generated column
-- ALTER TABLE phraseological_dict ADD COLUMN meanings_text TEXT 
-- GENERATED ALWAYS AS (JSON_UNQUOTE(JSON_EXTRACT(meanings, '$[0]'))) STORED;
-- ALTER TABLE phraseological_dict ADD FULLTEXT(phrase, meanings_text, etymology);

-- Regular indexes for better performance on common queries
CREATE INDEX idx_phrase_category ON phraseological_dict(category);
CREATE INDEX idx_phrase_created_at ON phraseological_dict(created_at);
CREATE INDEX idx_phrase_updated_at ON phraseological_dict(updated_at);

-- For slug-based lookups (if you add a slug column in the future)
-- ALTER TABLE phraseological_dict ADD COLUMN slug VARCHAR(255) GENERATED ALWAYS AS (LOWER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(phrase, ' ', '-'), ',', ''), '.', ''), '!', ''), '?', ''))) STORED;
-- CREATE INDEX idx_phrase_slug ON phraseological_dict(slug);