#!/usr/bin/env python3
"""
Script to analyze and fix categorization issues in table_phrases.json.
This script identifies phrases that are incorrectly categorized and suggests proper categories.
"""

import json
import re
from collections import defaultdict, Counter

def load_phrases():
    """Load phrases from the JSON file."""
    with open('table_phrases.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def analyze_categorization_issues(data):
    """Analyze and identify categorization issues."""
    phrases = data['phrases']
    categories = data['categories']
    
    issues = []
    fixes = []
    
    print("🔍 Analyzing categorization issues...")
    print(f"Total phrases: {len(phrases)}")
    
    # Category distribution
    category_counts = Counter(phrase['category'] for phrase in phrases)
    print(f"\n📊 Current category distribution:")
    for cat, count in category_counts.most_common():
        cat_name = categories.get(cat, {}).get('name', cat)
        print(f"  {cat_name} ({cat}): {count} phrases")
    
    # Define more specific categorization rules based on semantic meaning
    categorization_rules = {
        'emotions_feelings': {
            'keywords': ['радост', 'грусть', 'печаль', 'страх', 'ужас', 'гнев', 'злост', 'ярост', 
                        'счастье', 'горе', 'тоска', 'скука', 'весел', 'смех', 'слезы', 'плач', 
                        'обида', 'зависть', 'ревност', 'любовь', 'ненавист', 'волнение', 'беспокой',
                        'тревог', 'испуг', 'боя', 'опас'],
            'semantic_patterns': [
                r'бояться|страшно|испуг|пугать',
                r'радость|веселье|смех|улыбка',
                r'грусть|печаль|горе|слезы',
                r'гнев|злость|ярость|раздражение'
            ]
        },
        'body_parts': {
            'keywords': ['голова', 'глаз', 'ухо', 'нос', 'рот', 'язык', 'зуб', 'рука', 'нога', 
                        'пальц', 'плечо', 'спина', 'грудь', 'сердце', 'душа', 'живот', 'шея', 
                        'лицо', 'лоб', 'борода', 'волос', 'кожа'],
            'semantic_patterns': [
                r'голов|глаз|рук|ног|сердц|душ',
                r'язык|зуб|нос|ухо|лицо'
            ]
        },
        'animals': {
            'keywords': ['кот', 'собак', 'волк', 'лиса', 'медвед', 'заяц', 'мыш', 'птиц', 'конь', 
                        'лошад', 'корова', 'овц', 'козел', 'баран', 'рыб', 'змея', 'лев', 'тигр', 
                        'слон', 'орел', 'ворон', 'сорок', 'воробей', 'гус', 'утк', 'петух', 'курица',
                        'свинь', 'кобыл', 'жеребец', 'телят', 'блох'],
            'semantic_patterns': [
                r'кот|кошк|котёнок|котенок',
                r'собак|пёс|пес|щенок',
                r'волк|волч',
                r'медвед|мишк',
                r'рыб|карась|щук',
                r'птиц|петух|курица|гус|утк|воробей|ворон|орел',
                r'лошад|конь|кобыл|жеребец|мерин',
                r'корова|бык|телят|телен'
            ]
        },
        'money_wealth': {
            'keywords': ['деньги', 'богат', 'беден', 'золото', 'серебро', 'копейк', 'рубль', 
                        'бедност', 'нищет', 'богатств', 'клад', 'сокровищ', 'монет', 'грош'],
            'semantic_patterns': [
                r'деньги|богат|беден|нищ',
                r'золот|серебр|копейк|рубл|грош',
                r'состояние|богатств|бедност'
            ]
        },
        'work_labor': {
            'keywords': ['работ', 'труд', 'дело', 'служб', 'ремесл', 'мастер', 'артель', 
                        'пахать', 'сеять', 'жать', 'коси', 'молот', 'кузнец', 'столяр', 
                        'плотник', 'швея', 'портной'],
            'semantic_patterns': [
                r'работ|труд|дел|служб',
                r'мастер|ремесл|кузнец|столяр',
                r'пахать|сеять|косить|молотить'
            ]
        },
        'time_age': {
            'keywords': ['время', 'год', 'день', 'ночь', 'утро', 'вечер', 'час', 'минут', 
                        'секунд', 'возраст', 'молод', 'стар', 'детств', 'юность', 'зрелост', 'старост'],
            'semantic_patterns': [
                r'время|час|минут|секунд',
                r'день|ночь|утро|вечер',
                r'год|месяц|неделя',
                r'возраст|молод|стар|детств|юност|старост'
            ]
        },
        'speech_communication': {
            'keywords': ['говорить', 'сказать', 'слово', 'речь', 'язык', 'молчать', 'кричать', 
                        'шептать', 'болтать', 'рассказ', 'беседа', 'разговор', 'спор', 'ссора'],
            'semantic_patterns': [
                r'говор|сказать|слов|речь',
                r'молчать|шептать|кричать|болтать',
                r'разговор|беседа|спор|ссора'
            ]
        },
        'character_behavior': {
            'keywords': ['характер', 'нрав', 'поведение', 'добрый', 'злой', 'хороший', 'плохой', 
                        'честный', 'лживый', 'храбрый', 'трусливый', 'гордый', 'скромный', 
                        'жадный', 'щедрый', 'ленивый', 'трудолюбив'],
            'semantic_patterns': [
                r'характер|нрав|поведение',
                r'добр|зл|хорош|плох',
                r'честн|лжив|храбр|трусл',
                r'горд|скромн|жадн|щедр'
            ]
        }
    }
    
    # Analyze each phrase
    for i, phrase_data in enumerate(phrases):
        phrase = phrase_data['phrase'].lower()
        meanings = ' '.join(phrase_data.get('meanings', [])).lower()
        etymology = phrase_data.get('etymology', '').lower()
        current_category = phrase_data['category']
        
        # Combine all text for analysis
        full_text = f"{phrase} {meanings} {etymology}"
        
        # Find the best matching category
        best_category = None
        best_score = 0
        
        for category, rules in categorization_rules.items():
            score = 0
            
            # Check keyword matches
            for keyword in rules['keywords']:
                if keyword in full_text:
                    score += 2
            
            # Check semantic pattern matches
            for pattern in rules['semantic_patterns']:
                if re.search(pattern, full_text):
                    score += 3
            
            if score > best_score:
                best_score = score
                best_category = category
        
        # If we found a better category and current one is wrong
        if best_category and best_category != current_category and best_score >= 2:
            issues.append({
                'index': i,
                'phrase': phrase_data['phrase'],
                'current_category': current_category,
                'suggested_category': best_category,
                'score': best_score,
                'meanings': phrase_data.get('meanings', [])
            })
    
    return issues, categorization_rules

def manual_fixes():
    """Return a list of manual fixes for specific phrases."""
    return {
        # Animals that are incorrectly categorized
        'братья наши меньшие': 'animals',
        'биться как рыба об лед': 'animals', 
        'Васька слушает, да ест': 'animals',
        'вернёмся к нашим баранам': 'animals',
        'волк в овечьей шкуре': 'animals',
        'вставать с петухами': 'animals',
        'голодный как волк': 'animals',
        'дойная корова': 'animals',
        'делать из мухи слона': 'animals',
        'как с гуся вода': 'animals',
        'кот в мешке': 'animals',
        'кот валяка': 'animals',
        'кот наплакал': 'animals',
        'ловить рыбу в мутной воде': 'animals',
        'ложиться спать с курами': 'animals',
        'чувствовать себя как рыба в воде': 'animals',
        'ёшкин кот': 'animals',
        
        # Money/economics related
        'грош цена': 'money_wealth',
        'гроша ломаного не стоит': 'money_wealth',
        
        # Speech/communication
        'крылатые слова': 'speech_communication',
        
        # Religion/mythology  
        'терновый венец': 'religion_mythology',
        'разрубить гордиев узел': 'religion_mythology',
        
        # Time/weather
        'ждать у моря погоды': 'weather_nature',
        'жив, курилка!': 'general',
        
        # Incorrectly categorized as animals
        'в центре внимания': 'general',
        'лезть вперёд батьки в пекло': 'general',
        'непреклонное правило': 'general',
        'нечист на руку': 'character_behavior',
    }

def apply_fixes(data, issues, manual_fix_dict):
    """Apply the categorization fixes to the data."""
    phrases = data['phrases']
    
    # Apply manual fixes first
    manual_fixes_applied = 0
    for phrase_data in phrases:
        phrase = phrase_data['phrase']
        if phrase in manual_fix_dict:
            old_category = phrase_data['category']
            phrase_data['category'] = manual_fix_dict[phrase]
            print(f"Manual fix: '{phrase}' {old_category} → {manual_fix_dict[phrase]}")
            manual_fixes_applied += 1
    
    # Apply algorithmic fixes for high-confidence cases
    algorithmic_fixes_applied = 0
    for issue in issues:
        if issue['score'] >= 5:  # High confidence threshold
            phrase_data = phrases[issue['index']]
            old_category = phrase_data['category']
            phrase_data['category'] = issue['suggested_category']
            print(f"Auto fix: '{issue['phrase']}' {old_category} → {issue['suggested_category']} (score: {issue['score']})")
            algorithmic_fixes_applied += 1
    
    print(f"\n✅ Applied {manual_fixes_applied} manual fixes")
    print(f"✅ Applied {algorithmic_fixes_applied} algorithmic fixes")
    
    return data

def main():
    """Main function to analyze and fix categorization issues."""
    print("🔧 Starting categorization analysis and fixes...")
    
    # Load data
    data = load_phrases()
    
    # Analyze issues
    issues, rules = analyze_categorization_issues(data)
    
    print(f"\n🚨 Found {len(issues)} potential categorization issues")
    
    # Show top issues
    print(f"\n📋 Top 20 categorization issues:")
    for issue in sorted(issues, key=lambda x: x['score'], reverse=True)[:20]:
        print(f"  '{issue['phrase']}' - {issue['current_category']} → {issue['suggested_category']} (score: {issue['score']})")
        print(f"     Meaning: {issue['meanings'][0] if issue['meanings'] else 'No meaning'}")
    
    # Get manual fixes
    manual_fix_dict = manual_fixes()
    
    # Apply fixes
    fixed_data = apply_fixes(data, issues, manual_fix_dict)
    
    # Save fixed data
    with open('table_phrases_fixed.json', 'w', encoding='utf-8') as f:
        json.dump(fixed_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Saved fixed data to table_phrases_fixed.json")
    
    # Final statistics
    category_counts = Counter(phrase['category'] for phrase in fixed_data['phrases'])
    print(f"\n📊 Updated category distribution:")
    for cat, count in category_counts.most_common():
        cat_name = fixed_data['categories'].get(cat, {}).get('name', cat)
        print(f"  {cat_name} ({cat}): {count} phrases")

if __name__ == "__main__":
    main()