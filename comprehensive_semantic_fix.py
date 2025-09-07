#!/usr/bin/env python3
"""
Comprehensive Semantic Categorization Analyzer and Fixer
This script analyzes all phraseological units and corrects categorization based on semantic meaning.
Follows semantic-first categorization principles - the complete expression's meaning determines its category.
"""

import json
import re
from collections import defaultdict, Counter

def load_phrases():
    """Load phrases from the JSON file."""
    with open('table_phrases.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def analyze_comprehensive_semantic_categorization(data):
    """Comprehensive analysis and correction based on semantic meaning."""
    phrases = data['phrases']
    categories = data['categories']
    
    corrections = []
    
    print("🔍 Starting comprehensive semantic categorization analysis...")
    print(f"Total phrases: {len(phrases)}")
    
    # Enhanced semantic categorization rules based on complete expression meanings
    semantic_rules = {
        'emotions_feelings': {
            'meaning_patterns': [
                r'радост|счастлив|весел|смех|улыбк|довольн',
                r'грусть|печаль|горе|слез|плач|тоска|унын',
                r'страх|боязн|испуг|ужас|трус|пугат',
                r'гнев|злост|ярост|сердит|раздражен',
                r'любовь|влюбл|страст|нежност',
                r'ненавист|враждеб|презрен',
                r'волнение|беспокой|тревог|нервн',
                r'стыд|срам|позор|смущен',
                r'зависть|ревност',
                r'удивление|изумлен|поражен',
                r'эмоциональн|чувств|настроение|переживан'
            ],
            'description_indicators': [
                'эмоциональное состояние', 'чувство', 'переживание', 'настроение',
                'душевное волнение', 'эмоция', 'сильно переживать', 'испытывать чувство'
            ]
        },
        
        'money_wealth': {
            'meaning_patterns': [
                r'богат|состоятельн|зажиточн',
                r'беден|нищ|бедност|нужда',
                r'деньги|капитал|средства|финанс',
                r'золот.*богат|богат.*золот',
                r'грош|копейк|рубл|монет|валют',
                r'клад|сокровищ|богатств',
                r'долг|заем|кредит|займ',
                r'дорог|дешев|цена|стоимост',
                r'экономи|трати|расход|доход'
            ],
            'description_indicators': [
                'богатство', 'бедность', 'деньги', 'материальное положение',
                'нищета', 'достаток', 'состояние', 'финансы', 'материальный',
                'о богатых', 'о бедных', 'материальные блага'
            ]
        },
        
        'work_labor': {
            'meaning_patterns': [
                r'работ|труд|трудит|деятельност',
                r'служб|служить|должност',
                r'ремесл|мастер|профессия',
                r'пахать|сеять|косить|жать',
                r'бездельн|лентяй|лениться|безделье',
                r'усили|стараться|напряжен',
                r'результат|достижен|успех.*дел',
                r'выполня|исполня|завершать'
            ],
            'description_indicators': [
                'работа', 'труд', 'деятельность', 'профессия', 'ремесло',
                'служба', 'дело', 'занятие', 'усилия', 'старание',
                'о работе', 'трудовая деятельность', 'профессиональная деятельность'
            ]
        },
        
        'character_behavior': {
            'meaning_patterns': [
                r'характер|нрав|натур|темперамент',
                r'добр|зл|хорош|плох|милосерд',
                r'честн|лжив|обман|правдив',
                r'храбр|трусл|смел|отважн',
                r'горд|скромн|хвастлив|самолюб',
                r'жадн|щедр|скупой|расточительн',
                r'лениво|трудолюбив|активн',
                r'поведение|поступок|манер|привычк'
            ],
            'description_indicators': [
                'характер', 'поведение', 'нрав', 'качество личности',
                'черта характера', 'поступок', 'манера поведения',
                'о человеке', 'личностные качества', 'моральные качества'
            ]
        },
        
        'speech_communication': {
            'meaning_patterns': [
                r'говор|сказать|речь|беседа',
                r'слов|язык|болтать|разговар',
                r'молчать|безмолв|тишина',
                r'кричать|шептать|орать',
                r'спор|ссора|ругать|бранить',
                r'хвалить|одобрять|критиков',
                r'общение|коммуникац|диалог'
            ],
            'description_indicators': [
                'речь', 'общение', 'разговор', 'слова', 'язык',
                'беседа', 'молчание', 'говорить', 'сказать',
                'о речи', 'о словах', 'о разговоре'
            ]
        },
        
        'time_age': {
            'meaning_patterns': [
                r'время|час|минут|секунд',
                r'возраст|лет|год|столет',
                r'молод|стар|детств|юност|зрелост',
                r'день|ночь|утро|вечер',
                r'сезон|зима|лето|весна|осень',
                r'период|эпоха|века|тысячелет',
                r'рано|поздно|своевременн|несвоевременн',
                r'долго|быстро|медленно.*времен'
            ],
            'description_indicators': [
                'время', 'возраст', 'период', 'эпоха', 'молодость',
                'старость', 'детство', 'о времени', 'временной',
                'возрастной', 'жизненный период'
            ]
        },
        
        'mind_intelligence': {
            'meaning_patterns': [
                r'ум|умный|умен|мудр',
                r'глуп|дурак|дура|глупост|тупой',
                r'разум|рассудок|интеллект',
                r'память|помнить|забыв|вспомина',
                r'думать|мысл|соображ|понима',
                r'знать|учить|образован|наук',
                r'мозг|голов.*ум|сообразительн'
            ],
            'description_indicators': [
                'ум', 'интеллект', 'разум', 'глупость', 'мышление',
                'память', 'знание', 'о глупом', 'об умном',
                'интеллектуальные способности', 'умственные способности'
            ]
        },
        
        'food_drink': {
            'meaning_patterns': [
                r'есть|пить|еда|питье|кушать',
                r'хлеб|мясо|молоко|каша|суп',
                r'вода|вино|пиво|чай|кофе',
                r'голод|сыт|аппетит|вкус',
                r'обед|ужин|завтрак|трапез',
                r'кухня|стол.*еда|блюдо',
                r'напиток|угощен|застолье'
            ],
            'description_indicators': [
                'еда', 'питье', 'пища', 'напитки', 'о еде',
                'о питье', 'кулинария', 'застолье', 'о рюмке',
                'о напитке', 'пищевой', 'питейный'
            ]
        },
        
        'body_parts': {
            'meaning_patterns': [
                # Only if actually about physical body parts, not metaphorical
                r'физическ.*тел|анатоми|телесн',
                r'орган.*тел|часть.*тел',
                r'болезн.*тел|здоровье.*тел'
            ],
            'description_indicators': [
                'физическое', 'анатомия', 'телесный', 'орган',
                'часть тела', 'о теле', 'физиология'
            ],
            # Special handling: if body part mentioned but meaning is metaphorical, don't categorize here
            'avoid_if_metaphorical': True
        },
        
        'animals': {
            'meaning_patterns': [
                # Only if actually about animals as living creatures
                r'животн|зверь|скот|фауна',
                r'поведение.*животн|повадки.*животн',
                r'охота|звероло|животновод'
            ],
            'description_indicators': [
                'животные', 'звери', 'о животных', 'зоология',
                'животный мир', 'фауна'
            ],
            # Special handling: if animal mentioned but meaning is metaphorical, don't categorize here
            'avoid_if_metaphorical': True
        },
        
        'quantity_measure': {
            'meaning_patterns': [
                r'много|мало|количеств|числ',
                r'больш|маленьк|огромн|крошечн',
                r'размер|мера|величин|объем',
                r'длинн|коротк|высок|низк',
                r'широк|узк|толст|тонк',
                r'вес|легк|тяжел'
            ],
            'description_indicators': [
                'количество', 'размер', 'мера', 'много', 'мало',
                'большой', 'маленький', 'о количестве', 'о размере'
            ]
        },
        
        'general': {
            'description_indicators': [
                'общее выражение', 'разное', 'различное'
            ],
            # General category for expressions that don't fit specific categories
            'is_fallback': True
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
        category_scores = {}
        
        for category, rules in semantic_rules.items():
            score = 0
            
            # Skip fallback categories in initial scoring
            if rules.get('is_fallback'):
                continue
            
            # Check description indicators (highest weight) - these are in the meaning text
            if 'description_indicators' in rules:
                for indicator in rules['description_indicators']:
                    if indicator in meanings:
                        score += 10  # High weight for semantic meaning indicators
            
            # Check meaning patterns in the meanings text (high weight)
            if 'meaning_patterns' in rules:
                for pattern in rules['meaning_patterns']:
                    if re.search(pattern, meanings):
                        score += 5  # Medium-high weight for meaning patterns
            
            # Special handling for body_parts and animals - avoid if metaphorical
            if category in ['body_parts', 'animals'] and rules.get('avoid_if_metaphorical'):
                # Check if it's actually about the physical aspect
                physical_indicators = [
                    'физически', 'анатомия', 'буквально', 'настоящий',
                    'реальный', 'живое', 'биология'
                ]
                is_physical = any(indicator in full_text for indicator in physical_indicators)
                
                # If no physical indicators but score > 0, it's likely metaphorical
                if score > 0 and not is_physical:
                    # Check if there are strong semantic indicators for other categories
                    has_other_semantic = False
                    for other_cat, other_rules in semantic_rules.items():
                        if other_cat != category and 'description_indicators' in other_rules:
                            for other_indicator in other_rules['description_indicators']:
                                if other_indicator in meanings:
                                    has_other_semantic = True
                                    break
                    
                    if has_other_semantic:
                        score = max(1, score - 8)  # Reduce score significantly for metaphorical usage
            
            category_scores[category] = score
            
            if score > best_score:
                best_score = score
                best_category = category
        
        # Special cases and validation
        
        # 1. Time-related phrases should stay in time_age if they're about time duration
        if current_category == 'time_age':
            time_indicators = ['время', 'период', 'долго', 'быстро', 'рано', 'поздно', 'временной']
            if any(indicator in meanings for indicator in time_indicators):
                # Keep in time_age if it's genuinely about time
                continue
        
        # 2. Work-related phrases about effort vs results
        effort_result_patterns = [
            r'усили.*результат|результат.*усили',
            r'труд.*польз|польз.*труд',
            r'работ.*выгод|выгод.*работ',
            r'стараться.*толк|толк.*стараться',
            r'дело.*стоит|стоит.*дело'
        ]
        for pattern in effort_result_patterns:
            if re.search(pattern, meanings):
                if best_category != 'work_labor':
                    best_category = 'work_labor'
                    best_score = 8
                    break
        
        # 3. Money/wealth related expressions
        wealth_patterns = [
            r'богат.*детей|детей.*богат',
            r'материальн.*положен|положен.*материальн',
            r'деньги.*тратить|тратить.*деньги'
        ]
        for pattern in wealth_patterns:
            if re.search(pattern, meanings):
                if best_category != 'money_wealth':
                    best_category = 'money_wealth'
                    best_score = 8
                    break
        
        # If we found a significantly better category
        if best_category and best_category != current_category and best_score >= 5:
            corrections.append({
                'index': i,
                'phrase': phrase_data['phrase'],
                'current_category': current_category,
                'suggested_category': best_category,
                'score': best_score,
                'meaning': phrase_data.get('meanings', [''])[0] if phrase_data.get('meanings') else '',
                'reason': f'Semantic analysis (score: {best_score})',
                'category_scores': category_scores
            })
    
    return corrections

def apply_semantic_corrections(data, corrections, apply_threshold=5):
    """Apply semantic corrections to the data."""
    phrases = data['phrases']
    
    applied_count = 0
    skipped_count = 0
    
    print(f"\n🔄 Applying corrections with confidence score >= {apply_threshold}...")
    
    for correction in corrections:
        if correction['score'] >= apply_threshold:
            phrase_data = phrases[correction['index']]
            old_category = phrase_data['category']
            phrase_data['category'] = correction['suggested_category']
            
            print(f"✅ '{correction['phrase'][:50]}{'...' if len(correction['phrase']) > 50 else ''}' ")
            print(f"   {old_category} → {correction['suggested_category']} (score: {correction['score']})")
            print(f"   Meaning: {correction['meaning'][:80]}{'...' if len(correction['meaning']) > 80 else ''}")
            print()
            
            applied_count += 1
        else:
            skipped_count += 1
    
    print(f"📊 Applied {applied_count} corrections, skipped {skipped_count} low-confidence suggestions")
    return data

def main():
    """Main function to analyze and fix comprehensive semantic categorization."""
    print("🔧 Starting comprehensive semantic categorization analysis...")
    
    # Load data
    data = load_phrases()
    
    # Analyze semantic issues
    corrections = analyze_comprehensive_semantic_categorization(data)
    
    print(f"\n🚨 Found {len(corrections)} potential semantic corrections")
    
    # Show statistics by category
    current_categories = Counter([c['current_category'] for c in corrections])
    suggested_categories = Counter([c['suggested_category'] for c in corrections])
    
    print(f"\n📈 Categories with most issues:")
    for cat, count in current_categories.most_common(10):
        print(f"  {cat}: {count} phrases need correction")
    
    print(f"\n📈 Most suggested target categories:")
    for cat, count in suggested_categories.most_common(10):
        print(f"  {cat}: {count} phrases should move here")
    
    # Show top corrections by confidence
    print(f"\n📋 Top 20 high-confidence corrections:")
    for correction in sorted(corrections, key=lambda x: x['score'], reverse=True)[:20]:
        print(f"  '{correction['phrase'][:40]}{'...' if len(correction['phrase']) > 40 else ''}' ")
        print(f"    {correction['current_category']} → {correction['suggested_category']} (score: {correction['score']})")
        print(f"    {correction['meaning'][:60]}{'...' if len(correction['meaning']) > 60 else ''}")
        print()
    
    # Apply high-confidence corrections
    print(f"\n🔄 Applying high-confidence corrections (score >= 5)...")
    fixed_data = apply_semantic_corrections(data, corrections, apply_threshold=5)
    
    # Save corrected data
    with open('table_phrases.json', 'w', encoding='utf-8') as f:
        json.dump(fixed_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Applied corrections to table_phrases.json")
    
    # Also save a backup with all suggestions for review
    with open('semantic_corrections_report.json', 'w', encoding='utf-8') as f:
        json.dump({
            'applied_corrections': [c for c in corrections if c['score'] >= 5],
            'suggested_corrections': [c for c in corrections if c['score'] < 5],
            'statistics': {
                'total_corrections': len(corrections),
                'applied': len([c for c in corrections if c['score'] >= 5]),
                'suggested': len([c for c in corrections if c['score'] < 5]),
                'categories_with_issues': dict(current_categories),
                'target_categories': dict(suggested_categories)
            }
        }, f, ensure_ascii=False, indent=2)
    
    print(f"📋 Detailed report saved to semantic_corrections_report.json")
    
    return corrections

if __name__ == "__main__":
    corrections = main()