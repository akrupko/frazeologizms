# Development Environment

## Overview

This guide provides comprehensive instructions for setting up and maintaining the frazeologizms development environment. The project uses a Python-based processing pipeline with a static frontend, designed for educational content delivery and ease of maintenance.

## Prerequisites

### System Requirements

#### Operating System
- **Windows 10/11** (primary development environment)
- **macOS 10.15+** (supported)
- **Linux Ubuntu 18.04+** (supported)

#### Required Software
- **Python 3.9+** (recommended: Python 3.11)
- **Git** for version control
- **Web Browser** (Chrome, Firefox, Safari, Edge)
- **Text Editor/IDE** (VS Code recommended)

### Hardware Requirements
- **RAM**: Minimum 4GB, recommended 8GB+
- **Storage**: 2GB free space for project and dependencies
- **Network**: Internet connection for package installation

## Initial Setup

### 1. Repository Setup

#### Clone the Repository
```bash
# Clone the project
git clone https://github.com/your-username/frazeologizms.git
cd frazeologizms

# Verify project structure
ls -la
```

#### Project Structure Verification
```
frazeologizms/
├── components/                 # HTML components
├── wiki/                      # Project documentation
├── *.py                      # Python processing scripts
├── *.html                    # Static HTML pages
├── *.js                      # JavaScript files
├── *.css                     # Stylesheets
├── table_phrases.json        # Main data file
├── requirements.txt          # Python dependencies
└── README.md                 # Project overview
```

### 2. Python Environment Setup

#### Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Verify activation
which python  # Should show venv path
```

#### Install Dependencies
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

### 3. Dependency Overview

#### Core Dependencies
```txt
Flask==3.1.2                 # Development server
Jinja2==3.1.4                # Template engine
pandas==2.2.3                # Data processing
numpy==2.1.3                 # Numerical computing
beautifulsoup4==4.12.3       # Web scraping
psycopg2-binary==2.9.10      # PostgreSQL support (future)
```

#### Development Dependencies
```txt
jupyterlab==4.2.6            # Data analysis
matplotlib==3.x              # Visualization (optional)
requests==2.x                # HTTP requests
lxml==4.x                    # XML/HTML processing
```

## Development Workflow

### Standard Development Process

#### 1. Data Processing Pipeline
```bash
# Run processing scripts in sequence
python table_scraper.py          # Extract data from sources
python categorize_phrases.py     # Initial categorization
python fix_categorization.py     # Apply correction rules
python comprehensive_semantic_fix.py  # Semantic analysis
python add_categories_to_table.py     # Category integration
python restructure_data.py       # Data optimization
```

#### 2. Static Site Generation
```bash
# Generate HTML pages
python generate_pages.py

# Verify generated files
ls frazeologizmy_*.html
```

#### 3. Local Development Server
```bash
# Start development server
python start_server.py

# Access the application
# Open browser to: http://localhost:5000
```

### Development Scripts

#### `start_server.py` - Development Server
```python
from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

**Features:**
- **Hot Reload**: Automatic restart on file changes
- **Static Serving**: Serves all project files
- **Debug Mode**: Detailed error messages
- **Network Access**: Available on local network

#### Development Server Usage
```bash
# Basic server start
python start_server.py

# Custom configuration
export FLASK_ENV=development
export FLASK_DEBUG=1
python start_server.py

# Alternative ports
FLASK_RUN_PORT=8000 python start_server.py
```

## Code Quality & Standards

### Python Code Standards

#### PEP 8 Compliance
```python
# Example: Proper Python formatting
import json
import re
from collections import defaultdict
from typing import Dict, List, Optional

class SemanticAnalyzer:
    """Semantic analysis for phraseological categorization."""
    
    def __init__(self, data_file: str) -> None:
        self.data_file = data_file
        self.phrases: List[Dict] = []
        self.categories: Dict = {}
    
    def load_data(self) -> None:
        """Load phrases from JSON file."""
        with open(self.data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.phrases = data.get('phrases', [])
        self.categories = data.get('categories', {})
```

#### Type Hints
```python
from typing import Dict, List, Optional, Tuple, Union

def categorize_phrase(
    phrase: str, 
    meanings: List[str], 
    categories: Dict[str, Dict]
) -> Optional[str]:
    """Categorize phrase based on semantic analysis."""
    pass
```

### JavaScript Standards

#### ES6+ Modern JavaScript
```javascript
// Use modern JavaScript features
class PhraseologyTrainer {
  constructor() {
    this.phrases = [];
    this.currentQuestion = null;
  }
  
  async loadPhrases() {
    try {
      const response = await fetch('table_phrases.json');
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Loading error:', error);
      throw error;
    }
  }
  
  // Use arrow functions for callbacks
  setupEventListeners() {
    document.getElementById('next-button')
      .addEventListener('click', () => this.nextQuestion());
  }
}
```

#### Code Organization
```javascript
// Modular organization
const QuizManager = {
  // Public methods
  init() { /* ... */ },
  start() { /* ... */ },
  
  // Private methods (use underscore prefix)
  _loadData() { /* ... */ },
  _validateInput() { /* ... */ }
};
```

### HTML/CSS Standards

#### Semantic HTML
```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Specific Page Title - Фразеологизмы</title>
</head>
<body>
  <header role="banner">
    <h1>Site Title</h1>
    <nav role="navigation">
      <!-- Navigation content -->
    </nav>
  </header>
  
  <main role="main">
    <!-- Main content -->
  </main>
  
  <footer role="contentinfo">
    <!-- Footer content -->
  </footer>
</body>
</html>
```

#### CSS Organization
```css
/* Use CSS custom properties */
:root {
  --primary-color: #3498db;
  --success-color: #27ae60;
  --error-color: #e74c3c;
  --font-family: 'Inter', sans-serif;
}

/* Mobile-first responsive design */
.container {
  width: 100%;
  padding: 1rem;
}

@media (min-width: 768px) {
  .container {
    max-width: 750px;
    margin: 0 auto;
  }
}
```

## Testing & Quality Assurance

### Manual Testing Checklist

#### Functionality Testing
- [ ] All category pages load correctly
- [ ] Quiz functionality works across categories
- [ ] Navigation menu functions properly
- [ ] Progress tracking displays accurately
- [ ] Etymology display shows correctly
- [ ] Error handling works as expected

#### Cross-Browser Testing
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile browsers (iOS Safari, Chrome Mobile)

#### Responsive Design Testing
```bash
# Use browser dev tools to test:
# - Mobile: 320px - 768px
# - Tablet: 768px - 1024px
# - Desktop: 1024px+
```

#### Performance Testing
- [ ] Page load times < 2 seconds
- [ ] JavaScript execution < 100ms
- [ ] JSON data loading < 500ms
- [ ] Component loading smooth

### Data Quality Testing

#### Script Validation
```bash
# Test data processing pipeline
python -m pytest test_categorization.py  # If tests exist
python categorize_phrases.py --validate   # Validation mode
python fix_categorization.py --dry-run    # Test without changes
```

#### Data Integrity Checks
```python
# Example validation script
def validate_data_integrity():
    with open('table_phrases.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    phrases = data['phrases']
    categories = data['categories']
    
    # Check all phrases have valid categories
    valid_categories = set(categories.keys())
    for phrase in phrases:
        assert phrase['category'] in valid_categories
    
    # Check required fields
    for phrase in phrases:
        assert 'phrase' in phrase
        assert 'meanings' in phrase
        assert 'category' in phrase
    
    print("Data validation passed!")
```

## Debugging & Troubleshooting

### Common Issues

#### Python Environment Issues
```bash
# Issue: ModuleNotFoundError
# Solution: Verify virtual environment activation
which python
pip list

# Issue: Permission errors
# Solution: Use virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

#### Data Processing Issues
```bash
# Issue: Encoding errors
# Solution: Ensure UTF-8 encoding
python -c "import locale; print(locale.getpreferredencoding())"

# Issue: JSON parsing errors
# Solution: Validate JSON syntax
python -m json.tool table_phrases.json > /dev/null
```

#### Frontend Issues
```javascript
// Issue: Component loading failures
// Solution: Check browser console for errors
console.error('Component loading failed:', error);

// Issue: Quiz not starting
// Solution: Verify data loading
fetch('table_phrases.json')
  .then(response => response.json())
  .then(data => console.log('Data loaded:', data))
  .catch(error => console.error('Data loading failed:', error));
```

### Debugging Tools

#### Browser Development Tools
```javascript
// Enable verbose logging
localStorage.setItem('debug', 'true');

// Monitor quiz state
window.debugQuiz = {
  phrases: trainer.phrases,
  currentQuestion: trainer.currentQuestion,
  stats: {
    correct: trainer.correctAnswers,
    total: trainer.totalQuestions
  }
};
```

#### Python Debugging
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def debug_categorization():
    logger.debug("Starting categorization process")
    # ... rest of function
```

## Performance Optimization

### Development Performance

#### Python Script Optimization
```python
# Use pandas for large data processing
import pandas as pd

def process_large_dataset():
    df = pd.read_json('table_phrases.json')
    # Vectorized operations are faster
    df['category_valid'] = df['category'].isin(valid_categories)
    return df
```

#### Frontend Optimization
```javascript
// Lazy loading for large datasets
async function loadCategoryData(category) {
  if (!this.categoryCache[category]) {
    const data = await fetch(`data/${category}.json`);
    this.categoryCache[category] = await data.json();
  }
  return this.categoryCache[category];
}
```

### Memory Management
```python
# Generator for large file processing
def process_phrases_generator(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for phrase in data['phrases']:
            yield phrase

# Process without loading all into memory
for phrase in process_phrases_generator('table_phrases.json'):
    process_phrase(phrase)
```

## Deployment Preparation

### Pre-deployment Checklist
- [ ] All Python scripts run without errors
- [ ] Static pages generate correctly
- [ ] All components load properly
- [ ] Data integrity validated
- [ ] Performance benchmarks met
- [ ] Cross-browser testing completed

### Build Process
```bash
# Complete build sequence
./build.sh  # If build script exists

# Or manual build:
python categorize_phrases.py
python fix_categorization.py
python comprehensive_semantic_fix.py
python generate_pages.py

# Verify build
ls *.html
du -sh table_phrases.json
```

### Environment Variables
```bash
# Development
export FLASK_ENV=development
export FLASK_DEBUG=1

# Production
export FLASK_ENV=production
export FLASK_DEBUG=0
```

## IDE Configuration

### VS Code Settings
```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "html.format.indentInnerHtml": true,
  "css.validate": true,
  "javascript.validate.enable": true
}
```

### Recommended VS Code Extensions
- **Python**: Official Python extension
- **HTML CSS Support**: Enhanced HTML/CSS support
- **Live Server**: Development server for frontend
- **JSON Tools**: JSON formatting and validation
- **GitLens**: Enhanced Git integration

## Version Control Workflow

### Git Best Practices
```bash
# Feature development
git checkout -b feature/new-categorization
git add .
git commit -m "Add semantic categorization improvements"
git push origin feature/new-categorization

# Code review and merge
git checkout main
git pull origin main
git merge feature/new-categorization
```

### Commit Message Format
```
type(scope): description

Types: feat, fix, docs, style, refactor, test, chore
Scope: categorization, quiz, frontend, data, etc.

Examples:
feat(categorization): add semantic analysis engine
fix(quiz): resolve answer selection bug
docs(wiki): update development setup guide
```

## Continuous Integration

### Automated Checks
```yaml
# Example GitHub Actions workflow
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run data validation
      run: python validate_data.py
    - name: Generate pages
      run: python generate_pages.py
```

---

*This development environment guide ensures consistent setup and workflow across all contributors to the frazeologizms project.*