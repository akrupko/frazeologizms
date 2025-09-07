#!/usr/bin/env python3
"""
Table-focused scraper that extracts ALL phraseological units from the three-column Wiktionary table.
This scraper was used to generate table_phrases.json.
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin

class TablePhraseologismScraper:
    """Scraper specifically for the three-column table on Wiktionary."""
    
    def __init__(self):
        self.base_url = "https://ru.wiktionary.org"
        self.target_url = (
            "https://ru.wiktionary.org/wiki/"
            "%D0%9F%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5:"
            "%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D1%84%D1%80%D0%B0%D0%B7%D0%B5%D0%BE"
            "%D0%BB%D0%BE%D0%B3%D0%B8%D0%B7%D0%BC%D0%BE%D0%B2_%D1%80%D1%83%D1%81%D1%81%D0%BA"
            "%D0%BE%D0%B3%D0%BE_%D1%8F%D0%B7%D1%8B%D0%BA%D0%B0"
        )
        
        self.headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/120.0.0.0 Safari/537.36'
            ),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
        }
        
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.phrases_data = []
    
    def get_page_content(self, url, retries=3):
        """Fetch page content with retry logic."""
        for attempt in range(retries):
            try:
                print(f"Fetching page (attempt {attempt + 1}/{retries})")
                response = self.session.get(url, timeout=20)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                return soup
                
            except requests.RequestException as e:
                print(f"Request failed: {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
                    
        return None
    
    def extract_from_table(self, soup):
        """Extract phraseological units from the three-column table."""
        print("Looking for the three-column table...")
        
        # Find content area
        content_div = soup.find('div', {'id': 'mw-content-text'})
        if not content_div:
            content_div = soup.find('div', {'class': 'mw-parser-output'})
        
        if not content_div:
            print("No content area found")
            return []
        
        phrases = []
        
        # Look for tables
        tables = content_div.find_all('table')
        print(f"Found {len(tables)} tables")
        
        for table_idx, table in enumerate(tables):
            print(f"\nProcessing table {table_idx + 1}...")
            
            # Look for table rows
            rows = table.find_all('tr')
            print(f"  Found {len(rows)} rows")
            
            for row_idx, row in enumerate(rows):
                cells = row.find_all(['td', 'th'])
                
                if len(cells) >= 3:  # Three-column table
                    # Extract data from columns
                    col1 = cells[0].get_text().strip()  # Phrase
                    col2 = cells[1].get_text().strip()  # Meaning  
                    col3 = cells[2].get_text().strip()  # Etymology/Origin
                    
                    # Clean and validate the phrase
                    phrase = self.clean_phrase(col1)
                    meaning = self.clean_meaning(col2)
                    etymology = self.clean_etymology(col3)
                    
                    if phrase and self.is_valid_phrase(phrase):
                        # Look for link to individual page
                        phrase_link = ""
                        link_element = cells[0].find('a', href=True)
                        if link_element:
                            href = link_element.get('href', '')
                            if href.startswith('/wiki/'):
                                phrase_link = urljoin(self.base_url, href)
                        
                        phrase_data = {
                            'phrase': phrase,
                            'meanings': [meaning] if meaning else ["Значение требует уточнения"],
                            'etymology': etymology,
                            'source_url': phrase_link or self.target_url
                        }
                        
                        phrases.append(phrase_data)
                        print(f"  ✓ Extracted: {phrase}")
                        if meaning:
                            print(f"    Meaning: {meaning[:80]}...")
                        if etymology:
                            print(f"    Etymology: {etymology[:80]}...")
                
                elif len(cells) >= 2:  # Two-column format
                    col1 = cells[0].get_text().strip()
                    col2 = cells[1].get_text().strip()
                    
                    phrase = self.clean_phrase(col1)
                    meaning = self.clean_meaning(col2)
                    
                    if phrase and self.is_valid_phrase(phrase):
                        phrase_link = ""
                        link_element = cells[0].find('a', href=True)
                        if link_element:
                            href = link_element.get('href', '')
                            if href.startswith('/wiki/'):
                                phrase_link = urljoin(self.base_url, href)
                        
                        phrase_data = {
                            'phrase': phrase,
                            'meanings': [meaning] if meaning else ["Значение требует уточнения"],
                            'etymology': "",
                            'source_url': phrase_link or self.target_url
                        }
                        
                        phrases.append(phrase_data)
                        print(f"  ✓ Extracted: {phrase}")
        
        # Also look for list-based content
        self.extract_from_lists(content_div, phrases)
        
        return phrases
    
    def extract_from_lists(self, content_div, phrases):
        """Extract from list structures as backup."""
        print("\nLooking for list-based content...")
        
        # Get existing phrases to avoid duplicates
        existing_phrases = {p['phrase'] for p in phrases}
        
        # Look for definition lists (dl, dt, dd)
        for dl in content_div.find_all('dl'):
            dt_elements = dl.find_all('dt')
            dd_elements = dl.find_all('dd')
            
            for dt, dd in zip(dt_elements, dd_elements):
                phrase = self.clean_phrase(dt.get_text().strip())
                meaning = self.clean_meaning(dd.get_text().strip())
                
                if (phrase and self.is_valid_phrase(phrase) and 
                    phrase not in existing_phrases):
                    
                    phrase_data = {
                        'phrase': phrase,
                        'meanings': [meaning] if meaning else ["Значение требует уточнения"],
                        'etymology': "",
                        'source_url': self.target_url
                    }
                    
                    phrases.append(phrase_data)
                    existing_phrases.add(phrase)
                    print(f"  ✓ From list: {phrase}")
        
        # Look for ordered and unordered lists
        for list_element in content_div.find_all(['ol', 'ul']):
            for li in list_element.find_all('li'):
                text = li.get_text().strip()
                
                # Try to parse phrase and meaning from the text
                if ' — ' in text or ' - ' in text:
                    parts = re.split(r' — | - ', text, 1)
                    if len(parts) == 2:
                        phrase = self.clean_phrase(parts[0])
                        meaning = self.clean_meaning(parts[1])
                        
                        if (phrase and self.is_valid_phrase(phrase) and 
                            phrase not in existing_phrases):
                            
                            phrase_data = {
                                'phrase': phrase,
                                'meanings': [meaning] if meaning else ["Значение требует уточнения"],
                                'etymology': "",
                                'source_url': self.target_url
                            }
                            
                            phrases.append(phrase_data)
                            existing_phrases.add(phrase)
                            print(f"  ✓ From list: {phrase}")
                
                # Also extract just the phrase if it's a link
                else:
                    phrase = self.clean_phrase(text)
                    if (phrase and self.is_valid_phrase(phrase) and 
                        phrase not in existing_phrases):
                        
                        phrase_data = {
                            'phrase': phrase,
                            'meanings': ["Значение требует уточнения"],
                            'etymology': "",
                            'source_url': self.target_url
                        }
                        
                        phrases.append(phrase_data)
                        existing_phrases.add(phrase)
                        print(f"  ✓ From list: {phrase}")
    
    def clean_phrase(self, text):
        """Clean phrase text."""
        if not text:
            return ""
        
        # Remove common prefixes and clean up
        text = re.sub(r'^\d+\.\s*', '', text)  # Remove numbering
        text = re.sub(r'^[•–—]\s*', '', text)   # Remove bullets
        text = re.sub(r'\[.*?\]', '', text)     # Remove brackets
        text = re.sub(r'\s+', ' ', text)        # Normalize whitespace
        text = text.strip()
        
        return text
    
    def clean_meaning(self, text):
        """Clean meaning text."""
        if not text:
            return ""
        
        # Remove common artifacts
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        # Skip if too short or looks like metadata
        if (len(text) < 5 or
            text.lower().startswith(('см.', 'ср.', 'http', 'www')) or
            text in ['—', '-', '–']):
            return ""
        
        return text
    
    def clean_etymology(self, text):
        """Clean etymology text."""
        if not text:
            return ""
        
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        if (len(text) < 5 or
            text.lower().startswith(('см.', 'ср.', 'http', 'www')) or
            text in ['—', '-', '–']):
            return ""
        
        return text
    
    def is_valid_phrase(self, phrase):
        """Check if phrase is a valid phraseological unit."""
        if not phrase or len(phrase) < 3:
            return False
        
        # Skip obviously invalid entries
        invalid_patterns = [
            r'^\d+$',  # Just numbers
            r'^[A-Za-z]+$',  # Only Latin letters
            r'^[^а-яё]+$',  # No Cyrillic letters
            r'^(см\.|ср\.|http|www)',  # References
        ]
        
        for pattern in invalid_patterns:
            if re.match(pattern, phrase.lower()):
                return False
        
        return True
    
    def scrape_table_phrases(self):
        """Main scraping method for table-based content."""
        print("Starting table-based phraseological units scraping...")
        
        # Get the main page
        soup = self.get_page_content(self.target_url)
        if not soup:
            print("Failed to fetch main page")
            return []
        
        print("Successfully fetched main page")
        
        # Extract from table
        phrases = self.extract_from_table(soup)
        
        print(f"\nExtraction complete!")
        print(f"Total phrases extracted: {len(phrases)}")
        
        return phrases

def main():
    """Main function."""
    scraper = TablePhraseologismScraper()
    
    try:
        # Scrape phrases from table
        phrases = scraper.scrape_table_phrases()
        
        if phrases:
            # Sort alphabetically
            phrases.sort(key=lambda x: x['phrase'].lower())
            
            # Save results
            with open('table_phrases.json', 'w', encoding='utf-8') as f:
                json.dump(phrases, f, ensure_ascii=False, indent=2)
            
            print(f"\n✅ Table extraction complete!")
            print(f"📊 Total phrases: {len(phrases)}")
            print(f"💾 Results saved to table_phrases.json")
            
            # Show sample
            print(f"\n📝 Sample phrases:")
            for i, phrase in enumerate(phrases[:10], 1):
                print(f"{i}. {phrase['phrase']}")
                if phrase['meanings'][0] != "Значение требует уточнения":
                    print(f"   {phrase['meanings'][0][:60]}...")
        else:
            print("No phrases extracted from table")
            
    except KeyboardInterrupt:
        print("\nScraping interrupted")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()