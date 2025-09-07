#!/usr/bin/env python3
"""
Script to update existing HTML pages to use the modular component system.
This will backup the old files and create new modular versions.
"""

import os
import shutil
import re
from pathlib import Path

# Page configurations for component loader
PAGE_CONFIGS = {
    'frazeologizmy_animals': {
        'title': '🐾 Тренажер фразеологизмов',
        'description': 'Фразеологизмы о животных и природных явлениях',
        'footer': '📚 Животные и природа - фразеологизмы',
        'seo_title': 'Фразеологизмы о животных - изучение русских идиом с животными онлайн',
        'page_title': 'Фразеологизмы о животных - изучение русских идиом с животными онлайн',
        'meta_description': 'Изучайте фразеологизмы с животными и природными явлениями. Русские идиомы о животных для подготовки к экзаменам.'
    },
    'frazeologizmy_body-parts': {
        'title': '👤 Тренажер фразеологизмов',
        'description': 'Фразеологизмы с частями тела человека',
        'footer': '📚 Части тела - фразеологизмы',
        'seo_title': 'Фразеологизмы с частями тела - русские идиомы онлайн тренажер',
        'page_title': 'Фразеологизмы с частями тела - русские идиомы онлайн тренажер',
        'meta_description': 'Фразеологизмы с частями тела человека. Изучение русских идиом с головой, руками, глазами. Подготовка к экзаменам.'
    },
    'frazeologizmy_time': {
        'title': '⏰ Тренажер фразеологизмов',
        'description': 'Фразеологизмы о времени и возрастных периодах',
        'footer': '📚 Время и возраст - фразеологизмы',
        'seo_title': 'Фразеологизмы о времени - русские идиомы о возрасте онлайн',
        'page_title': 'Фразеологизмы о времени - русские идиомы о возрасте онлайн',
        'meta_description': 'Фразеологизмы о времени и возрасте. Изучение русских идиом о жизненных периодах и времени.'
    },
    'frazeologizmy_religion': {
        'title': '⛪ Тренажер фразеологизмов',
        'description': 'Религиозные и мифологические фразеологизмы',
        'footer': '📚 Религия и мифология - фразеологизмы',
        'seo_title': 'Религиозные фразеологизмы - библейские и мифологические идиомы',
        'page_title': 'Религиозные фразеологизмы - библейские и мифологические идиомы',
        'meta_description': 'Фразеологизмы с религиозными и мифологическими мотивами. Библейские выражения и античные идиомы в русском языке.'
    },
    'frazeologizmy_mind': {
        'title': '🧠 Тренажер фразеологизмов',
        'description': 'Фразеологизмы об интеллектуальных способностях',
        'footer': '📚 Ум и глупость - фразеологизмы',
        'seo_title': 'Фразеологизмы об уме - русские идиомы об интеллекте и глупости',
        'page_title': 'Фразеологизмы об уме - русские идиомы об интеллекте и глупости',
        'meta_description': 'Фразеологизмы об уме и глупости. Русские идиомы об интеллектуальных способностях и мудрости.'
    },
    'frazeologizmy_work': {
        'title': '⚙️ Тренажер фразеологизмов',
        'description': 'Фразеологизмы о трудовой деятельности',
        'footer': '📚 Труд и работа - фразеологизмы',
        'seo_title': 'Фразеологизмы о работе - русские идиомы о труде онлайн',
        'page_title': 'Фразеологизмы о работе - русские идиомы о труде онлайн',
        'meta_description': 'Фразеологизмы о труде и работе. Изучение русских идиом о профессиональной деятельности и трудовых процессах.'
    },
    'frazeologizmy_family': {
        'title': '👪 Тренажер фразеологизмов',
        'description': 'Фразеологизмы о семейных отношениях',
        'footer': '📚 Семья и отношения - фразеологизмы',
        'seo_title': 'Фразеологизмы о семье - русские идиомы о родственных отношениях',
        'page_title': 'Фразеологизмы о семье - русские идиомы о родственных отношениях',
        'meta_description': 'Семейные фразеологизмы и идиомы о родственных отношениях. Изучение русских выражений о семье онлайн.'
    },
    'frazeologizmy_house': {
        'title': '🏠 Тренажер фразеологизмов',
        'description': 'Фразеологизмы о домашнем быте',
        'footer': '📚 Дом и быт - фразеологизмы',
        'seo_title': 'Фразеологизмы о доме - русские идиомы о быте онлайн',
        'page_title': 'Фразеологизмы о доме - русские идиомы о быте онлайн',
        'meta_description': 'Фразеологизмы о доме и быте. Изучение русских идиом о жилище и повседневной жизни.'
    },
    'frazeologizmy_speech': {
        'title': '💬 Тренажер фразеологизмов',
        'description': 'Фразеологизмы о речи и коммуникации',
        'footer': '📚 Речь и общение - фразеологизмы',
        'seo_title': 'Фразеологизмы о речи - русские идиомы об общении онлайн',
        'page_title': 'Фразеологизмы о речи - русские идиомы об общении онлайн',
        'meta_description': 'Фразеологизмы о речи и общении. Изучение русских идиом о языке, разговоре и коммуникации.'
    },
    'frazeologizmy_food': {
        'title': '🍽️ Тренажер фразеологизмов',
        'description': 'Фразеологизмы о пище и напитках',
        'footer': '📚 Еда и питье - фразеологизмы',
        'seo_title': 'Фразеологизмы о еде - русские идиомы о пище и напитках',
        'page_title': 'Фразеологизмы о еде - русские идиомы о пище и напитках',
        'meta_description': 'Фразеологизмы о еде и питье. Русские идиомы о пище, напитках и кулинарии.'
    },
    'frazeologizmy_money': {
        'title': '💰 Тренажер фразеологизмов',
        'description': 'Фразеологизмы о материальном достатке',
        'footer': '📚 Деньги и богатство - фразеологизмы',
        'seo_title': 'Фразеологизмы о деньгах - русские идиомы о богатстве и бедности',
        'page_title': 'Фразеологизмы о деньгах - русские идиомы о богатстве и бедности',
        'meta_description': 'Фразеологизмы о деньгах и богатстве. Русские идиомы о материальном достатке и бедности.'
    },
    'frazeologizmy_emotions': {
        'title': '😊 Тренажер фразеологизмов',
        'description': 'Фразеологизмы о эмоциональных состояниях и переживаниях',
        'footer': '📚 Эмоции и чувства - фразеологизмы',
        'seo_title': 'Фразеологизмы об эмоциях - русские идиомы о чувствах онлайн',
        'page_title': 'Фразеологизмы об эмоциях - русские идиомы о чувствах онлайн',
        'meta_description': 'Изучайте фразеологизмы об эмоциях и чувствах. Русские идиомы о радости, грусти, любви, страхе. Тренажер для подготовки к экзаменам.'
    }
}

def get_modular_page_template(page_name, config):
    """Generate the modular HTML template for a page"""
    template = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="format-detection" content="telephone=no">
    <title>{config['page_title']}</title>
    <meta name="description" content="{config['meta_description']}">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- Navigation will be loaded here -->
    <div id="navigation-container"></div>
    
    <!-- Main Content -->
    <div class="main-content" id="main-content">
        <div class="container">
            <!-- Header will be loaded here -->
            <div id="header-container"></div>

            <!-- Quiz content will be loaded here -->
            <div id="quiz-container"></div>

            <!-- Footer will be loaded here -->
            <div id="footer-container"></div>

            <!-- SEO Content will be loaded here -->
            <div id="seo-container"></div>
        </div>
    </div>

    <!-- Load component loader first, then other scripts -->
    <script src="components/component-loader.js"></script>
    <script src="script.js"></script>
    <script src="navigation.js"></script>
</body>
</html>"""
    return template

def backup_existing_files():
    """Backup existing HTML files"""
    backup_dir = Path('backup_old_html')
    backup_dir.mkdir(exist_ok=True)
    
    html_files = list(Path('.').glob('frazeologizmy_*.html')) + [Path('index.html')]
    
    for file in html_files:
        if file.exists():
            backup_path = backup_dir / file.name
            shutil.copy2(file, backup_path)
            print(f"Backed up {file.name} to {backup_path}")

def update_component_loader_configs():
    """Update component-loader.js with all page configurations"""
    
    # Generate JavaScript config object
    js_configs = []
    
    # Add index page config
    js_configs.append("""            'index': {
                header: {
                    title: '🏠 Тренажер фразеологизмов',
                    description: 'Изучение всех фразеологизмов русского языка по разным темам'
                },
                footer: {
                    text: '📚 Все фразеологизмы - более 1280 выражений'
                },
                seo: {
                    title: 'Тренажер фразеологизмов русского языка - изучение онлайн',
                    description: 'Все фразеологизмы - комплексное изучение русских идиом и выражений. Наш интерактивный тренажер поможет вам изучить более 1280 фразеологических единиц различной тематики и успешно подготовиться к экзаменам по русскому языку.',
                    featuresTitle: 'Особенности изучения фразеологизмов на нашем сайте',
                    featuresText: 'Фразеологизмы различных категорий часто встречаются в заданиях ЕГЭ и ОГЭ по русскому языку. Изучение всех фразеологизмов поможет вам:',
                    footer: 'Начните изучение прямо сейчас и повысьте свои шансы на успешную сдачу экзаменов по русскому языку! Наша база содержит более 1280 фразеологизмов с подробными объяснениями и историей происхождения.'
                },
                category: 'general',
                categoryName: 'Все фразеологизмы'
            }""")
    
    # Add thematic page configs
    for page_name, config in PAGE_CONFIGS.items():
        category_name = config['title'].split('Тренажер фразеологизмов')[0].strip()
        
        js_config = f"""            '{page_name}': {{
                header: {{
                    title: '{config['title']}',
                    description: '{config['description']}'
                }},
                footer: {{
                    text: '{config['footer']}'
                }},
                seo: {{
                    title: '{config['seo_title']}',
                    description: '{config['description']} - фразеологизмы данной тематики. Наш интерактивный тренажер поможет вам изучить фразеологические единицы этой категории и успешно подготовиться к экзаменам по русскому языку.',
                    featuresTitle: 'Особенности изучения фразеологизмов темы "{category_name}"',
                    featuresText: 'Фразеологизмы данной категории часто встречаются в заданиях ЕГЭ и ОГЭ по русскому языку. Изучение {category_name.lower()} поможет вам:',
                    footer: 'Начните изучение прямо сейчас и повысьте свои шансы на успешную сдачу экзаменов по русскому языку! Изучайте фразеологизмы с подробными объяснениями и историей происхождения.'
                }},
                categoryName: '{category_name}'
            }}"""
        
        js_configs.append(js_config)
    
    # Read the current component-loader.js
    loader_path = Path('components/component-loader.js')
    if loader_path.exists():
        with open(loader_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the getPageConfigs method
        new_configs = ',\\n'.join(js_configs)
        
        pattern = r'(getPageConfigs\(\) \{\\s*return \{)(.*?)(\s*\};\\s*\})'
        replacement = f'\\1\\n{new_configs}\\n        \\3'
        
        updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        with open(loader_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("Updated component-loader.js with all page configurations")

def create_modular_pages():
    """Create new modular versions of all pages"""
    
    # Create modular index.html
    index_config = {
        'page_title': 'Тренажер фразеологизмов русского языка - изучение онлайн',
        'meta_description': 'Интерактивный тренажер для изучения всех фразеологизмов русского языка. Подготовка к ЕГЭ и ОГЭ по русскому языку. Онлайн тесты с объяснениями значений и происхождения.'
    }
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(get_modular_page_template('index', index_config))
    print("Created modular index.html")
    
    # Create modular thematic pages
    for page_name, config in PAGE_CONFIGS.items():
        filename = f"{page_name}.html"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(get_modular_page_template(page_name, config))
        
        print(f"Created modular {filename}")

def main():
    """Main function to update all pages to modular system"""
    print("Starting conversion to modular component system...")
    
    # 1. Backup existing files
    print("\\n1. Backing up existing HTML files...")
    backup_existing_files()
    
    # 2. Update component loader configurations
    print("\\n2. Updating component loader configurations...")
    update_component_loader_configs()
    
    # 3. Create new modular pages
    print("\\n3. Creating modular pages...")
    create_modular_pages()
    
    print("\\n✅ Conversion completed successfully!")
    print("\\nNext steps:")
    print("1. Test the modular pages in your browser")
    print("2. Upload the new files to your live website:")
    print("   - All HTML files")
    print("   - The components/ directory")
    print("   - Updated style.css (if needed)")
    print("3. The old HTML files are backed up in backup_old_html/ directory")

if __name__ == "__main__":
    main()

# Execute the conversion
main()