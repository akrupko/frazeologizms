#!/usr/bin/env python3
"""
Script to restructure phraseological units data from multiple category files 
into a single file with category information included in each phrase object.
"""

import json
import os
from pathlib import Path

def restructure_to_single_file():
    """Restructure data from multiple category files to single file with categories."""
    
    # Load the original phrases
    with open('table_phrases.json', 'r', encoding='utf-8') as f:
        original_phrases = json.load(f)
    
    print(f"Loaded {len(original_phrases)} original phrases")
    
    # Load categorized data
    categories_file = 'categorized_phrases.json'
    if not os.path.exists(categories_file):
        print(f"Error: {categories_file} not found. Run categorize_phrases.py first.")
        return
    
    with open(categories_file, 'r', encoding='utf-8') as f:
        categorized_data = json.load(f)
    
    print(f"Loaded {len(categorized_data)} categories")
    
    # Create mapping of phrases to categories
    phrase_to_category = {}
    categories_info = {}
    
    for category_key, category_data in categorized_data.items():
        # Store category info
        categories_info[category_key] = {
            'name': category_data['name'],
            'description': category_data['description'],
            'count': len(category_data['phrases'])
        }
        
        # Map each phrase to its category
        for phrase_data in category_data['phrases']:
            phrase_text = phrase_data['phrase']
            phrase_to_category[phrase_text] = category_key
    
    # Add category information to original phrases
    phrases_with_categories = []
    categorized_count = 0
    
    for phrase_data in original_phrases:
        # Create new phrase object with category
        new_phrase = phrase_data.copy()
        
        # Find category for this phrase
        phrase_text = phrase_data['phrase']
        category = phrase_to_category.get(phrase_text, 'general')
        
        new_phrase['category'] = category
        phrases_with_categories.append(new_phrase)
        
        if category != 'general':
            categorized_count += 1
    
    # Create the final structure
    result = {
        'categories': categories_info,
        'phrases': phrases_with_categories,
        'stats': {
            'total_phrases': len(phrases_with_categories),
            'categorized_phrases': categorized_count,
            'uncategorized_phrases': len(phrases_with_categories) - categorized_count,
            'total_categories': len(categories_info)
        }
    }
    
    # Save the restructured data
    output_file = 'phrases_with_categories.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Restructuring complete!")
    print(f"📊 Statistics:")
    print(f"  - Total phrases: {result['stats']['total_phrases']}")
    print(f"  - Categorized: {result['stats']['categorized_phrases']}")
    print(f"  - Uncategorized: {result['stats']['uncategorized_phrases']}")
    print(f"  - Categories: {result['stats']['total_categories']}")
    print(f"💾 Saved to: {output_file}")
    
    # Show category distribution
    print(f"\n📈 Category distribution:")
    category_counts = {}
    for phrase in phrases_with_categories:
        cat = phrase['category']
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        category_name = categories_info.get(category, {}).get('name', category)
        print(f"  - {category_name}: {count} phrases")
    
    return result

def clean_old_files():
    """Clean up individual category JSON files that are no longer needed."""
    
    # List of category files to remove
    category_files = [
        'animals_phrases.json',
        'body_parts_phrases.json',
        'religion_mythology_phrases.json',
        'work_labor_phrases.json',
        'money_wealth_phrases.json',
        'family_relationships_phrases.json',
        'time_age_phrases.json',
        'emotions_feelings_phrases.json',
        'mind_intelligence_phrases.json',
        'speech_communication_phrases.json',
        'appearance_beauty_phrases.json',
        'food_drink_phrases.json',
        'war_conflict_phrases.json',
        'house_home_phrases.json',
        'weather_nature_phrases.json',
        'transport_travel_phrases.json',
        'clothes_appearance_phrases.json',
        'luck_fortune_phrases.json',
        'education_knowledge_phrases.json',
        'love_romance_phrases.json',
        'quantity_measure_phrases.json',
        'colors_light_phrases.json',
        'games_entertainment_phrases.json',
        'health_disease_phrases.json',
        'social_status_phrases.json',
        'business_trade_phrases.json',
        'character_behavior_phrases.json',
        'ancient_historical_phrases.json',
        'literary_cultural_phrases.json',
        'general_phrases.json'
    ]
    
    removed_count = 0
    for file_name in category_files:
        if os.path.exists(file_name):
            os.remove(file_name)
            removed_count += 1
            print(f"🗑️ Removed: {file_name}")
    
    print(f"\n🧹 Cleanup complete! Removed {removed_count} old category files.")

if __name__ == "__main__":
    print("🔄 Restructuring phraseological units data...")
    result = restructure_to_single_file()
    
    if result:
        print(f"\n❓ Clean up old category JSON files? (y/n): ", end="")
        choice = input().lower().strip()
        
        if choice in ['y', 'yes', 'да']:
            clean_old_files()
        else:
            print("Old files kept. You can clean them up manually if needed.")