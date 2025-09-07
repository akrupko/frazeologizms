#!/usr/bin/env python3
"""
Script to add category information directly to the existing table_phrases.json file.
This modifies the original file by adding a 'category' field to each phrase object.
"""

import json
import os
from collections import defaultdict

def add_categories_to_table_phrases():
    """Add category information to each phrase in table_phrases.json."""
    
    # Load the original table_phrases.json
    if not os.path.exists('table_phrases.json'):
        print("Error: table_phrases.json not found!")
        return False
    
    with open('table_phrases.json', 'r', encoding='utf-8') as f:
        phrases = json.load(f)
    
    print(f"Loaded {len(phrases)} phrases from table_phrases.json")
    
    # Define thematic categories with keywords for classification
    categories = {
        'animals': {
            'name': 'Животные и природа',
            'description': 'Фразеологизмы с животными, птицами и природными явлениями',
            'keywords': ['кот', 'собак', 'волк', 'лиса', 'медвед', 'заяц', 'мыш', 'птиц', 'конь', 'лошад', 'корова', 'овц', 'козел', 'баран', 'рыб', 'змея', 'лев', 'тигр', 'слон', 'орел', 'ворон', 'сорок', 'воробей', 'гус', 'утк', 'петух', 'курица']
        },
        'body_parts': {
            'name': 'Части тела',
            'description': 'Фразеологизмы с частями тела человека',
            'keywords': ['голова', 'глаз', 'ухо', 'нос', 'рот', 'язык', 'зуб', 'рука', 'нога', 'пальц', 'плечо', 'спина', 'грудь', 'сердце', 'душа', 'живот', 'шея', 'лицо', 'лоб', 'борода', 'волос', 'кожа']
        },
        'religion_mythology': {
            'name': 'Религия и мифология',
            'description': 'Фразеологизмы с религиозными и мифологическими мотивами',
            'keywords': ['бог', 'черт', 'дьявол', 'ад', 'рай', 'ангел', 'душа', 'грех', 'молитв', 'церков', 'святой', 'божий', 'господь', 'христос', 'библия', 'античн', 'греческ', 'мифолог', 'легенда', 'авгиев', 'ахиллес']
        },
        'work_labor': {
            'name': 'Труд и работа',
            'description': 'Фразеологизмы о работе, труде и профессиональной деятельности',
            'keywords': ['работ', 'труд', 'дело', 'служб', 'ремесл', 'мастер', 'артель', 'пахать', 'сеять', 'жать', 'коси', 'молот', 'кузнец', 'столяр', 'плотник', 'швея', 'портной']
        },
        'money_wealth': {
            'name': 'Деньги и богатство',
            'description': 'Фразеологизмы о деньгах, богатстве и бедности',
            'keywords': ['деньги', 'богат', 'беден', 'золото', 'серебро', 'копейк', 'рубль', 'бедност', 'нищет', 'богатств', 'клад', 'сокровищ', 'монет', 'бюджет', 'долг', 'заем', 'кредит']
        },
        'family_relationships': {
            'name': 'Семья и отношения',
            'description': 'Фразеологизмы о семейных отношениях и родственных связях',
            'keywords': ['мать', 'отец', 'сын', 'дочь', 'брат', 'сестра', 'дед', 'бабушк', 'внук', 'муж', 'жена', 'семья', 'род', 'детей', 'ребенок', 'супруг', 'свадьб', 'женить', 'замуж']
        },
        'time_age': {
            'name': 'Время и возраст',
            'description': 'Фразеологизмы о времени, возрасте и жизненных периодах',
            'keywords': ['время', 'год', 'день', 'ночь', 'утро', 'вечер', 'час', 'минут', 'секунд', 'возраст', 'молод', 'стар', 'детств', 'юность', 'зрелост', 'старост', 'век', 'эпох', 'сезон', 'месяц', 'неделя']
        },
        'emotions_feelings': {
            'name': 'Эмоции и чувства',
            'description': 'Фразеологизмы о эмоциональных состояниях и переживаниях',
            'keywords': ['любовь', 'ненавист', 'радост', 'грусть', 'печаль', 'страх', 'ужас', 'гнев', 'злост', 'ярост', 'счастье', 'горе', 'тоска', 'скука', 'весел', 'смех', 'слезы', 'плач', 'обида', 'зависть', 'ревност']
        },
        'mind_intelligence': {
            'name': 'Ум и глупость',
            'description': 'Фразеологизмы об интеллектуальных способностях',
            'keywords': ['ум', 'глупост', 'дурак', 'дура', 'мудр', 'мозг', 'разум', 'рассудок', 'память', 'забыв', 'помнить', 'думать', 'соображ', 'понима', 'знать', 'учить', 'образован']
        },
        'speech_communication': {
            'name': 'Речь и общение',
            'description': 'Фразеологизмы о речи, общении и языке',
            'keywords': ['говорить', 'сказать', 'слово', 'речь', 'язык', 'молчать', 'кричать', 'шептать', 'болтать', 'рассказ', 'беседа', 'разговор', 'спор', 'ссора', 'ругать', 'хвалить', 'обещать']
        },
        'food_drink': {
            'name': 'Еда и питье',
            'description': 'Фразеологизмы о пище и напитках',
            'keywords': ['есть', 'пить', 'хлеб', 'мясо', 'молоко', 'вода', 'вино', 'пиво', 'чай', 'кофе', 'сахар', 'соль', 'масло', 'каша', 'суп', 'блюдо', 'кухня', 'стол', 'обед', 'ужин', 'завтрак', 'голод', 'сыт']
        },
        'house_home': {
            'name': 'Дом и быт',
            'description': 'Фразеологизмы о доме, жилище и повседневной жизни',
            'keywords': ['дом', 'изба', 'хата', 'квартира', 'комната', 'кухня', 'двор', 'сад', 'огород', 'крыша', 'стена', 'дверь', 'окно', 'стол', 'стул', 'кровать', 'печь', 'очаг', 'быт', 'хозяйств']
        },
        'war_conflict': {
            'name': 'Война и конфликты',
            'description': 'Фразеологизмы о военных действиях и конфликтах',
            'keywords': ['война', 'битва', 'бой', 'сражение', 'враг', 'друг', 'солдат', 'офицер', 'генерал', 'армия', 'полк', 'оружие', 'меч', 'копье', 'пушка', 'ружье', 'победа', 'поражение', 'мир', 'драка', 'ссора']
        },
        'weather_nature': {
            'name': 'Погода и природа',
            'description': 'Фразеологизмы о погодных явлениях и природе',
            'keywords': ['дождь', 'снег', 'ветер', 'буря', 'гроза', 'туман', 'солнце', 'луна', 'звезд', 'небо', 'земля', 'море', 'река', 'лес', 'поле', 'гора', 'холод', 'тепло', 'жара', 'мороз', 'лето', 'зима', 'весна', 'осень']
        },
        'transport_travel': {
            'name': 'Транспорт и путешествия',
            'description': 'Фразеологизмы о передвижении и путешествиях',
            'keywords': ['дорога', 'путь', 'ехать', 'идти', 'бежать', 'лететь', 'плыть', 'корабль', 'лодка', 'телега', 'сани', 'лошадь', 'воз', 'путешеств', 'поездка', 'прогулка']
        },
        'character_behavior': {
            'name': 'Характер и поведение',
            'description': 'Фразеологизмы о человеческом характере и поведении',
            'keywords': ['характер', 'нрав', 'поведение', 'добрый', 'злой', 'хороший', 'плохой', 'честный', 'лживый', 'храбрый', 'трусливый', 'гордый', 'скромный', 'жадный', 'щедрый', 'ленивый', 'трудолюбив']
        },
        'health_disease': {
            'name': 'Здоровье и болезни',
            'description': 'Фразеологизмы о здоровье и недугах',
            'keywords': ['здоровье', 'болезнь', 'больной', 'здоровый', 'лечить', 'врач', 'лекарство', 'боль', 'рана', 'язва', 'лихорадка', 'кашель', 'чума', 'смерть', 'умереть']
        },
        'quantity_measure': {
            'name': 'Количество и мера',
            'description': 'Фразеологизмы о количестве, размере и мере',
            'keywords': ['много', 'мало', 'больш', 'маленьк', 'огромн', 'крошечн', 'длинн', 'коротк', 'широк', 'узк', 'высок', 'низк', 'глубок', 'мелк', 'толст', 'тонк', 'размер', 'мера']
        },
        'colors_light': {
            'name': 'Цвета и свет',
            'description': 'Фразеологизмы с цветами и световыми явлениями',
            'keywords': ['белый', 'черный', 'красный', 'синий', 'зеленый', 'желтый', 'серый', 'розовый', 'фиолетов', 'свет', 'тьма', 'темнота', 'яркий', 'тусклый', 'блеск', 'сиять']
        },
        'luck_fortune': {
            'name': 'Удача и судьба',
            'description': 'Фразеологизмы о везении, невезении и судьбе',
            'keywords': ['удача', 'везение', 'судьба', 'рок', 'счастье', 'несчастье', 'участь', 'доля', 'жребий', 'случай', 'везти', 'фортуна', 'звезда']
        }
    }
    
    # Add category information to each phrase
    categorized_count = 0
    category_stats = defaultdict(int)
    
    for phrase_data in phrases:
        phrase = phrase_data['phrase'].lower()
        meanings = ' '.join(phrase_data.get('meanings', [])).lower()
        etymology = phrase_data.get('etymology', '').lower()
        
        full_text = f"{phrase} {meanings} {etymology}"
        
        # Find matching category
        assigned_category = 'general'  # Default category
        
        for category_key, category_info in categories.items():
            for keyword in category_info['keywords']:
                if keyword in full_text:
                    assigned_category = category_key
                    break
            if assigned_category != 'general':
                break
        
        # Add category to phrase data
        phrase_data['category'] = assigned_category
        category_stats[assigned_category] += 1
        
        if assigned_category != 'general':
            categorized_count += 1
    
    # Add category metadata to the structure
    result_data = {
        'categories': {**categories, 'general': {
            'name': 'Общие выражения',
            'description': 'Различные фразеологизмы общего характера',
            'keywords': []
        }},
        'phrases': phrases,
        'stats': {
            'total_phrases': len(phrases),
            'categorized_phrases': categorized_count,
            'general_phrases': len(phrases) - categorized_count,
            'total_categories': len(categories) + 1
        }
    }
    
    # Create backup of original file
    backup_filename = 'table_phrases_backup.json'
    with open(backup_filename, 'w', encoding='utf-8') as f:
        json.dump(phrases, f, ensure_ascii=False, indent=2)
    print(f"Created backup: {backup_filename}")
    
    # Save updated file
    with open('table_phrases.json', 'w', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Successfully updated table_phrases.json!")
    print(f"📊 Statistics:")
    print(f"  - Total phrases: {len(phrases)}")
    print(f"  - Categorized: {categorized_count}")
    print(f"  - General: {len(phrases) - categorized_count}")
    print(f"  - Categories: {len(categories) + 1}")
    
    print(f"\n📈 Category distribution:")
    for category, count in sorted(category_stats.items(), key=lambda x: x[1], reverse=True):
        category_name = categories.get(category, {}).get('name', category)
        if category == 'general':
            category_name = 'Общие выражения'
        print(f"  - {category_name}: {count} phrases")
    
    return True

if __name__ == "__main__":
    print("🔄 Adding category information to table_phrases.json...")
    success = add_categories_to_table_phrases()
    
    if success:
        print("\n🎉 Task completed successfully!")
        print("📝 Note: Original file backed up as table_phrases_backup.json")
        print("💡 The updated table_phrases.json now includes category information for each phrase.")
    else:
        print("\n❌ Task failed!")