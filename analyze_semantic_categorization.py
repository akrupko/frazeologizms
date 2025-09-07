#!/usr/bin/env python3
"""
Script to analyze phraseological units and correct categorization based on semantic meaning.
This script focuses on the actual meaning of the complete expression, not individual words.
"""

import json
import re
from collections import defaultdict

def load_phrases():
    """Load phrases from the JSON file."""
    with open('table_phrases.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def analyze_semantic_categorization(data):
    """Analyze and suggest corrections based on semantic meaning."""
    phrases = data['phrases']
    categories = data['categories']
    
    corrections = []
    
    print("🔍 Analyzing semantic categorization...")
    print(f"Total phrases: {len(phrases)}")
    
    # Define semantic categorization rules based on meaning, not keywords
    semantic_rules = {
        'emotions_feelings': {
            'patterns': [
                r'радост|счастлив|весел|смех|улыбк',
                r'грусть|печаль|горе|слез|плач|тоска',
                r'страх|боязн|испуг|ужас|трус',
                r'гнев|злост|ярост|сердит',
                r'любовь|влюбл|страст',
                r'ненавист|враждеб',
                r'волнение|беспокой|тревог',
                r'стыд|срам|позор',
                r'зависть|ревност',
                r'удивление|изумление',
                r'эмоци|чувств|настроение'
            ],
            'meaning_indicators': [
                'эмоциональное состояние',
                'чувство',
                'переживание',
                'настроение',
                'душевное волнение'
            ]
        },
        'body_parts': {
            'patterns': [
                r'голов|башк|череп',
                r'глаз|око|взгляд|взор',
                r'рук|ладон|пальц|кулак',
                r'ног|стоп|пят',
                r'сердц|душ',
                r'язык|рот|губ|зуб',
                r'ухо|слух',
                r'нос|обоняние',
                r'лицо|лик|щек',
                r'спин|плеч|грудь',
                r'живот|желудок',
                r'шея|горло',
                r'волос|борода',
                r'кожа|тело'
            ]
        },
        'animals': {
            'patterns': [
                r'кот|кошк|котен',
                r'собак|пес|щенок',
                r'лошад|конь|кобыл|жеребец',
                r'корова|бык|телен',
                r'волк|волч',
                r'медвед|мишк',
                r'лис|лиц',
                r'заяц|кролик',
                r'мыш|крыс',
                r'птиц|петух|курица|гус|утк|воробей|ворон|орел|сорок',
                r'рыб|карась|щук|окун',
                r'змея|гадюк|уж',
                r'свинь|поросен',
                r'козел|коза|баран|овц',
                r'слон|тигр|лев',
                r'блох|комар|муха'
            ]
        },
        'money_wealth': {
            'meaning_indicators': [
                'богатство',
                'бедность',
                'деньги',
                'материальное положение',
                'нищета',
                'достаток',
                'состояние',
                'финансы',
                'богатый',
                'бедный',
                'нищий'
            ],
            'patterns': [
                r'богат|состоятельн',
                r'беден|нищ|бедност',
                r'деньги|капитал|средства',
                r'золот.*богат|богат.*золот',
                r'грош|копейк|рубл|монет',
                r'клад|сокровищ',
                r'долг|заем|кредит'
            ]
        },
        'work_labor': {
            'meaning_indicators': [
                'работа',
                'труд',
                'деятельность',
                'профессия',
                'ремесло',
                'служба',
                'дело',
                'занятие'
            ],
            'patterns': [
                r'работ|труд|дел',
                r'служб|служить',
                r'ремесл|мастер|кузнец|столяр',
                r'пахать|сеять|косить|жать',
                r'бездельн|лентяй|лениться'
            ]
        },
        'character_behavior': {
            'meaning_indicators': [
                'характер',
                'поведение',
                'нрав',
                'качество личности',
                'черта характера',
                'поступок',
                'манера поведения'
            ],
            'patterns': [
                r'характер|нрав|натур',
                r'добр|зл|хорош|плох',
                r'честн|лжив|обман',
                r'храбр|трусл|смел',
                r'горд|скромн|хвастлив',
                r'жадн|щедр|скупой',
                r'лениво|трудолюбив',
                r'умный|глупый|дурак'
            ]
        },
        'speech_communication': {
            'meaning_indicators': [
                'речь',
                'общение',
                'разговор',
                'слова',
                'язык',
                'беседа',
                'молчание'
            ],
            'patterns': [
                r'говор|сказать|речь',
                r'слов|язык|болтать',
                r'молчать|безмолв',
                r'кричать|шептать',
                r'разговор|беседа|спор',
                r'ругать|хвалить|бранить'
            ]
        },
        'time_age': {
            'meaning_indicators': [
                'время',
                'возраст',
                'период',
                'эпоха',
                'молодость',
                'старость',
                'детство'
            ],
            'patterns': [
                r'время|час|минут',
                r'возраст|лет|год',
                r'молод|стар|детств|юност',
                r'день|ночь|утро|вечер',
                r'сезон|зима|лето|весна|осень'
            ]
        },
        'religion_mythology': {
            'meaning_indicators': [
                'религия',
                'вера',
                'церковь',
                'мифология',
                'древняя легенда',
                'библия',
                'античность'
            ],
            'patterns': [
                r'бог|господь|христос',
                r'черт|дьявол|сатана',
                r'ад|рай|небеса',
                r'ангел|святой|грех',
                r'церков|монастыр|храм',
                r'молитв|служб.*церковн',
                r'библ|еванг',
                r'античн|греческ.*мифолог|римск.*мифолог',
                r'геракл|ахилл|авгиев|олимп',
                r'мифолог|легенд.*древн'
            ]
        },
        'weather_nature': {
            'meaning_indicators': [
                'погода',
                'природа',
                'климат',
                'стихия',
                'природное явление'
            ],
            'patterns': [
                r'дождь|снег|град',
                r'ветер|буря|ураган|вихрь',
                r'солнце|луна|звезд',
                r'туман|облак|тучи',
                r'холод|мороз|жара|тепло',
                r'море|река|озеро|вода',
                r'лес|поле|гора|земля',
                r'погод|климат|стихия'
            ]
        },
        'mind_intelligence': {
            'meaning_indicators': [
                'ум',
                'интеллект',
                'разум',
                'глупость',
                'мышление',
                'память',
                'знание'
            ],
            'patterns': [
                r'ум|умный|умен',
                r'глуп|дурак|дура|глупост',
                r'мудр|мудрост',
                r'разум|рассудок',
                r'память|помнить|забыв',
                r'думать|мысл|соображ',
                r'знать|понимать|учить',
                r'мозг|голов.*ум'
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
        
        # Find the best matching category based on semantic meaning
        best_category = None
        best_score = 0
        
        for category, rules in semantic_rules.items():
            score = 0
            
            # Check meaning indicators (high weight)
            if 'meaning_indicators' in rules:
                for indicator in rules['meaning_indicators']:
                    if indicator in meanings:
                        score += 5
            
            # Check patterns in the full text
            if 'patterns' in rules:
                for pattern in rules['patterns']:
                    if re.search(pattern, full_text):
                        score += 2
            
            # Special case: if phrase is about a physical body part action but meaning is metaphorical
            if category == 'body_parts':
                # Check if the meaning is actually about the body part itself
                body_part_meanings = [
                    'физическое',
                    'анатомия',
                    'телесный',
                    'орган',
                    'часть тела'
                ]
                if not any(bp in meanings for bp in body_part_meanings):
                    # If body part is mentioned but meaning is metaphorical, reduce score
                    if score > 0:
                        score = max(1, score - 3)
            
            if score > best_score:
                best_score = score
                best_category = category
        
        # If we found a better category with good confidence
        if best_category and best_category != current_category and best_score >= 3:
            corrections.append({
                'index': i,
                'phrase': phrase_data['phrase'],
                'current_category': current_category,
                'suggested_category': best_category,
                'score': best_score,
                'meaning': phrase_data.get('meanings', [''])[0] if phrase_data.get('meanings') else '',
                'reason': f'Semantic analysis (score: {best_score})'
            })
    
    return corrections

def apply_semantic_corrections(data, corrections, apply_threshold=5):
    """Apply semantic corrections to the data."""
    phrases = data['phrases']
    
    applied_count = 0
    for correction in corrections:
        if correction['score'] >= apply_threshold:
            phrase_data = phrases[correction['index']]
            old_category = phrase_data['category']
            phrase_data['category'] = correction['suggested_category']
            print(f"✅ '{correction['phrase']}' {old_category} → {correction['suggested_category']} (score: {correction['score']})")
            applied_count += 1
    
    print(f"\n📊 Applied {applied_count} semantic corrections")
    return data

def main():
    """Main function to analyze and fix semantic categorization."""
    print("🔧 Starting semantic categorization analysis...")
    
    # Load data
    data = load_phrases()
    
    # Analyze semantic issues
    corrections = analyze_semantic_categorization(data)
    
    print(f"\n🚨 Found {len(corrections)} potential semantic corrections")
    
    # Show top corrections
    print(f"\n📋 Top 30 semantic corrections:")
    for correction in sorted(corrections, key=lambda x: x['score'], reverse=True)[:30]:
        print(f"  '{correction['phrase']}' - {correction['current_category']} → {correction['suggested_category']} (score: {correction['score']})")
        print(f"     Meaning: {correction['meaning'][:100]}{'...' if len(correction['meaning']) > 100 else ''}")
        print()
    
    # Apply high-confidence corrections
    print(f"\n🔄 Applying high-confidence corrections (score >= 5)...")
    fixed_data = apply_semantic_corrections(data, corrections, apply_threshold=5)
    
    # Save corrected data
    with open('table_phrases_semantic_fixed.json', 'w', encoding='utf-8') as f:
        json.dump(fixed_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Saved semantically corrected data to table_phrases_semantic_fixed.json")
    
    return corrections

if __name__ == "__main__":
    corrections = main()