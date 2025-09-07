#!/usr/bin/env python3
"""
Generate thematic pages for phraseological units trainer.
Creates individual HTML pages for each category with proper SEO optimization.
"""

import json
import os
from datetime import datetime

def generate_thematic_pages():
    """Generate HTML pages for each thematic category."""
    
    # Load restructured data
    with open('phrases_with_categories.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    categories = data['categories']
    phrases = data['phrases']
    
    print(f"Generating pages for {len(categories)} categories...")
    
    # Category mappings for file names and SEO
    category_mappings = {
        'general': {
            'filename': 'index.html',
            'title': 'Все фразеологизмы',
            'icon': '🏠',
            'seo_title': 'Тренажер фразеологизмов русского языка - изучение онлайн',
            'seo_description': 'Интерактивный тренажер для изучения всех фразеологизмов русского языка. Подготовка к ЕГЭ и ОГЭ по русскому языку. Онлайн тесты с объяснениями значений и происхождения.'
        },
        'animals': {
            'filename': 'animals.html',
            'title': 'Животные и природа', 
            'icon': '🐾',
            'seo_title': 'Фразеологизмы о животных - изучение русских идиом с животными онлайн',
            'seo_description': 'Изучайте фразеологизмы с животными и природными явлениями. Русские идиомы о животных для подготовки к ЕГЭ и ОГЭ. Интерактивные тесты с объяснениями.'
        },
        'body_parts': {
            'filename': 'body-parts.html',
            'title': 'Части тела',
            'icon': '👤',
            'seo_title': 'Фразеологизмы с частями тела - русские идиомы онлайн тренажер',
            'seo_description': 'Фразеологизмы с частями тела человека. Изучение русских идиом с головой, руками, глазами. Подготовка к экзаменам по русскому языку.'
        },
        'religion_mythology': {
            'filename': 'religion.html',
            'title': 'Религия и мифология',
            'icon': '⛪',
            'seo_title': 'Религиозные фразеологизмы - библейские и мифологические идиомы',
            'seo_description': 'Фразеологизмы с религиозными и мифологическими мотивами. Библейские выражения и античные идиомы в русском языке.'
        },
        'emotions_feelings': {
            'filename': 'emotions.html',
            'title': 'Эмоции и чувства',
            'icon': '😊',
            'seo_title': 'Фразеологизмы об эмоциях - русские идиомы о чувствах онлайн',
            'seo_description': 'Изучайте фразеологизмы об эмоциях и чувствах. Русские идиомы о радости, грусти, любви, страхе. Тренажер для подготовки к экзаменам.'
        },
        'work_labor': {
            'filename': 'work.html',
            'title': 'Труд и работа',
            'icon': '⚙️',
            'seo_title': 'Фразеологизмы о работе - русские идиомы о труде онлайн',
            'seo_description': 'Фразеологизмы о труде и работе. Изучение русских идиом о профессиональной деятельности и трудовых процессах.'
        },
        'family_relationships': {
            'filename': 'family.html',
            'title': 'Семья и отношения',
            'icon': '👪',
            'seo_title': 'Фразеологизмы о семье - русские идиомы о родственных отношениях',
            'seo_description': 'Семейные фразеологизмы и идиомы о родственных отношениях. Изучение русских выражений о семье онлайн.'
        },
        'mind_intelligence': {
            'filename': 'mind.html',
            'title': 'Ум и глупость',
            'icon': '🧠',
            'seo_title': 'Фразеологизмы об уме - русские идиомы об интеллекте и глупости',
            'seo_description': 'Фразеологизмы об уме и глупости. Русские идиомы об интеллектуальных способностях и мудрости.'
        },
        'speech_communication': {
            'filename': 'speech.html',
            'title': 'Речь и общение',
            'icon': '💬',
            'seo_title': 'Фразеологизмы о речи - русские идиомы об общении онлайн',
            'seo_description': 'Фразеологизмы о речи и общении. Изучение русских идиом о языке, разговоре и коммуникации.'
        },
        'money_wealth': {
            'filename': 'money.html',
            'title': 'Деньги и богатство',
            'icon': '💰',
            'seo_title': 'Фразеологизмы о деньгах - русские идиомы о богатстве и бедности',
            'seo_description': 'Фразеологизмы о деньгах и богатстве. Русские идиомы о материальном достатке и бедности.'
        },
        'time_age': {
            'filename': 'time.html',
            'title': 'Время и возраст',
            'icon': '⏰',
            'seo_title': 'Фразеологизмы о времени - русские идиомы о возрасте онлайн',
            'seo_description': 'Фразеологизмы о времени и возрасте. Изучение русских идиом о жизненных периодах и времени.'
        },
        'food_drink': {
            'filename': 'food.html',
            'title': 'Еда и питье',
            'icon': '🍽️',
            'seo_title': 'Фразеологизмы о еде - русские идиомы о пище и напитках',
            'seo_description': 'Фразеологизмы о еде и питье. Русские идиомы о пище, напитках и кулинарии.'
        },
        'house_home': {
            'filename': 'house.html',
            'title': 'Дом и быт',
            'icon': '🏠',
            'seo_title': 'Фразеологизмы о доме - русские идиомы о быте онлайн',
            'seo_description': 'Фразеологизмы о доме и быте. Изучение русских идиом о жилище и повседневной жизни.'
        },
        'education_knowledge': {
            'filename': 'education.html',
            'title': 'Образование и знания',
            'icon': '📚',
            'seo_title': 'Фразеологизмы об образовании - русские идиомы о знаниях онлайн',
            'seo_description': 'Фразеологизмы об образовании и знаниях. Русские идиомы об обучении и познании.'
        },
        'character_behavior': {
            'filename': 'character.html',
            'title': 'Характер и поведение',
            'icon': '🎭',
            'seo_title': 'Фразеологизмы о характере - русские идиомы о поведении онлайн',
            'seo_description': 'Фразеологизмы о характере и поведении. Изучение русских идиом о человеческих качествах.'
        },
        'ancient_historical': {
            'filename': 'historical.html',
            'title': 'Исторические и античные',
            'icon': '🏛️',
            'seo_title': 'Исторические фразеологизмы - античные русские идиомы онлайн',
            'seo_description': 'Исторические и античные фразеологизмы. Изучение русских идиом с древними корнями и историческим происхождением.'
        }
    }
    
    # Generate navigation HTML
    def generate_navigation(current_category):
        nav_html = f'''    <!-- Navigation Sidebar -->
    <nav class="sidebar" id="sidebar">
        <div class="sidebar-header">
            <h3>📚 Темы фразеологизмов</h3>
            <button class="sidebar-close" id="sidebar-close">&times;</button>
        </div>
        <div class="sidebar-content">'''
        
        for cat_key, cat_data in categories.items():
            if cat_key in category_mappings:
                mapping = category_mappings[cat_key]
                active_class = ' active' if cat_key == current_category else ''
                nav_html += f'''
            <a href="{mapping['filename']}" class="nav-link{active_class}" 
               title="{mapping['seo_title']}"
               alt="{mapping['seo_description'][:100]}...">
                {mapping['icon']} {mapping['title']}
            </a>'''
        
        nav_html += '''
            <div class="sidebar-footer">
                <small>🎓 Подготовка к ЕГЭ и ОГЭ</small>
            </div>
        </div>
    </nav>'''
        
        return nav_html
    
    # Generate page template
    def generate_page_template(category_key, category_data):
        mapping = category_mappings.get(category_key, {
            'filename': f'{category_key}.html',
            'title': category_data['name'],
            'icon': category_data.get('icon', '📖'),
            'seo_title': f"{category_data['name']} фразеологизмы",
            'seo_description': category_data['description']
        })
        
        # Count phrases in this category
        category_phrase_count = category_data['count']
        
        html_content = f'''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="format-detection" content="telephone=no">
    <title>{mapping['seo_title']}</title>
    <meta name="description" content="{mapping['seo_description']}">
    <link rel="stylesheet" href="style.css">
</head>
<body>
{generate_navigation(category_key)}
    
    <!-- Mobile Menu Button -->
    <button class="mobile-menu-btn" id="mobile-menu-btn">
        <span></span>
        <span></span>
        <span></span>
    </button>
    
    <!-- Main Content -->
    <div class="main-content" id="main-content">
    <div class="container">
        <header>
            <h1>{mapping['icon']} Тренажер фразеологизмов</h1>
            <p>{category_data['description']}</p>
        </header>

        <div class="game-container">
            <div class="stats">
                <div class="stat-item">
                    <span class="stat-label">Правильных ответов:</span>
                    <span id="correct-count" class="stat-value">0</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Всего вопросов:</span>
                    <span id="total-count" class="stat-value">0</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Точность:</span>
                    <span id="accuracy" class="stat-value">0%</span>
                </div>
            </div>

            <div class="quiz-section">
                <div id="loading" class="loading">
                    <div class="spinner"></div>
                    <p>Загружаем фразеологизмы...</p>
                </div>

                <div id="quiz-content" class="quiz-content" style="display: none;">
                    <div class="question-section">
                        <h2>Что означает фразеологизм:</h2>
                        <div id="phrase" class="phrase"></div>
                    </div>

                    <div class="answers-section">
                        <h3>Выберите правильное значение:</h3>
                        <div id="answer-options" class="answer-options">
                            <!-- Answer buttons will be inserted here -->
                        </div>
                    </div>

                    <div id="feedback" class="feedback" style="display: none;">
                        <div id="feedback-message" class="feedback-message"></div>
                        <div id="correct-answer" class="correct-answer"></div>
                        <button id="next-button" class="next-button">Следующий вопрос</button>
                    </div>
                </div>

                <div id="error-message" class="error-message" style="display: none;">
                    <h3>❌ Ошибка загрузки</h3>
                    <p>Не удалось загрузить базу фразеологизмов.</p>
                    <button onclick="location.reload()" class="retry-button">Попробовать снова</button>
                </div>
            </div>

            <div class="controls">
                <button id="restart-button" class="control-button" style="display: none;">🔄 Начать заново</button>
                <button id="show-etymology" class="control-button" style="display: none;">📚 Показать происхождение</button>
            </div>

            <div id="etymology-info" class="etymology-info" style="display: none;">
                <h4>📖 Происхождение:</h4>
                <p id="etymology-text"></p>
            </div>
        </div>

        <footer>
            <p>📚 {category_data['name']} - {category_phrase_count} фразеологизмов</p>
        </footer>

        <!-- SEO Content Section -->
        <section class="seo-content">
            <div class="seo-text">
                <h2>{mapping['seo_title']}</h2>
                
                <p><strong>{category_data['name']}</strong> - {category_data['description'].lower()}. Наш интерактивный тренажер поможет вам изучить {category_phrase_count} фразеологических единиц этой тематики и успешно подготовиться к экзаменам по русскому языку.</p>
                
                <h3>Особенности изучения фразеологизмов темы "{category_data['name']}"</h3>
                <p>Фразеологизмы данной категории часто встречаются в заданиях ЕГЭ и ОГЭ по русскому языку. Изучение {category_data['name'].lower()} поможет вам:</p>
                
                <ul class="seo-list">
                    <li>🎯 Подготовиться к заданиям ЕГЭ и ОГЭ по фразеологии</li>
                    <li>📖 Изучить происхождение и этимологию фразеологических единиц</li>
                    <li>💡 Запомнить значения популярных русских идиом</li>
                    <li>🏆 Успешно выступить на олимпиадах по русскому языку</li>
                    <li>📝 Улучшить письменную и устную речь</li>
                </ul>
                
                <p class="seo-footer">Начните изучение прямо сейчас и повысьте свои шансы на успешную сдачу экзаменов по русскому языку! Наша база содержит {category_phrase_count} фразеологизмов с подробными объяснениями и историей происхождения.</p>
            </div>
        </section>
    </div>
    </div>

    <script>
        // Set the category for filtering
        window.CURRENT_CATEGORY = '{category_key}';
        window.CATEGORY_NAME = '{category_data["name"]}';
    </script>
    <script src="script.js"></script>
    <script src="navigation.js"></script>
</body>
</html>'''
        
        return html_content
    
    # Generate pages for each category
    pages_created = 0
    for category_key, category_data in categories.items():
        if category_data['count'] >= 5:  # Only create pages with enough content
            # Generate page
            html_content = generate_page_template(category_key, category_data)
            
            # Get filename
            filename = category_mappings.get(category_key, {}).get('filename', f'{category_key}.html')
            
            # Write page file
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"Created page: {filename} ({category_data['count']} phrases)")
            pages_created += 1
    
    print(f"\n✅ Generated {pages_created} thematic pages!")
    print(f"📊 Total categories with sufficient content: {pages_created}")
    
    return pages_created

if __name__ == "__main__":
    generate_thematic_pages()