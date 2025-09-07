#!/usr/bin/env python3
"""
Simple script to convert all HTML pages to use modular components.
This replaces the content between <body> and </body> with modular containers.
"""

import os
import re
from pathlib import Path

def get_modular_body_content():
    """Return the modular body content template"""
    return '''    <!-- Navigation will be loaded here -->
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
    <script src="navigation.js"></script>'''

def convert_html_to_modular(file_path):
    """Convert an HTML file to use modular components"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace everything between <body> and </body> with modular content
        pattern = r'(<body>)(.*?)(</body>)'
        replacement = r'\1\n' + get_modular_body_content() + '\n\3'
        
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        # Write back the updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Converted {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error converting {file_path}: {e}")
        return False

def main():
    """Convert all frazeologizmy_*.html files to modular system"""
    print("🔄 Converting HTML pages to modular component system...")
    
    # Find all frazeologizmy_*.html files
    pattern = "frazeologizmy_*.html"
    html_files = list(Path('.').glob(pattern))
    
    if not html_files:
        print("No frazeologizmy_*.html files found")
        return
    
    converted = 0
    for file_path in html_files:
        if convert_html_to_modular(file_path):
            converted += 1
    
    print(f"\n✅ Successfully converted {converted}/{len(html_files)} files!")
    print("\n🎉 Modular component system is now active!")
    print("\nNext steps:")
    print("1. Test the pages in your browser")
    print("2. Upload the updated files to your live website")
    print("3. Now you can edit menu/header/footer in components/ folder!")

if __name__ == "__main__":
    main()