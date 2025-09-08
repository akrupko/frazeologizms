# Технологический стек и зависимости

## Обзор

Проект фразеологизмы использует современный, лёгкий технологический стек, разработанный для доставки образовательного контента и эффективности обслуживания. Архитектура делает акцент на генерации статических сайтов для производительности, одновременно предоставляя динамические интерактивные функции через клиентский JavaScript.

## Основные технологии

### Бэкенд технологии

#### Python 3.9+
**Основной бэкенд язык для обработки данных и генерации сайта**

- **Требования к версии**: Python >= 3.9
- **Использование**: Конвейер обработки данных, движок категоризации, генерация статических сайтов
- **Ключевые особенности**: Подсказки типов, f-строки, классы данных для надёжной обработки данных

#### Flask 3.1.2
**Веб-сервер разработки и шаблонизатор**

- **Назначение**: Локальный сервер разработки через `start_server.py`
- **Особенности**: Лёгкий WSGI-фреймворк приложений
- **Использование**: Тестирование в разработке, не для продакшена
- **Спутник**: Werkzeug 3.1.3 (WSGI тулкит)

#### Jinja2 3.1.4
**Движок шаблонов для генерации HTML**

- **Интеграция**: Встроен в Flask для отображения шаблонов
- **Использование**: Динамическая генерация HTML в `generate_pages.py`
- **Особенности**: Наследование шаблонов, макросы, фильтры

### Data Processing Libraries

#### pandas 2.2.3
**Data manipulation and analysis**

- **Usage**: Processing large datasets of phraseological units
- **Features**: DataFrame operations, data cleaning, transformation
- **Performance**: Efficient handling of 10,000+ phrase records

#### numpy 2.1.3
**Numerical computing foundation**

- **Dependency**: Required by pandas for mathematical operations
- **Usage**: Array operations, statistical calculations
- **Integration**: Seamless with pandas for data analysis

#### BeautifulSoup4 4.12.3
**HTML/XML parsing for web scraping**

- **Usage**: Data extraction in `table_scraper.py`
- **Features**: Robust HTML parsing, CSS selectors
- **Reliability**: Handles malformed HTML gracefully

### Database & Storage

#### JSON-Based Storage
**Primary data format**

- **Main File**: `table_phrases.json` (377.9KB)
- **Structure**: Hierarchical JSON with categories and phrases
- **Advantages**: Human-readable, version-controllable, lightweight
- **Backup Versions**: Multiple JSON variants for data integrity

#### PostgreSQL Support (Optional)
**Future database integration**

- **Driver**: psycopg2-binary 2.9.10
- **Status**: Prepared for future database migration
- **Current Use**: Not actively implemented

### Frontend Technologies

#### HTML5
**Modern semantic markup**

- **Structure**: Component-based HTML fragments
- **SEO**: Semantic tags for search engine optimization
- **Accessibility**: ARIA attributes and proper heading hierarchy

#### CSS3
**Modern styling and responsive design**

- **Framework**: Custom CSS with modern features
- **Design**: Responsive layout with Flexbox and Grid
- **Typography**: Inter font family for readability
- **Colors**: Semantic color scheme (blue primary, green success, red error)

#### Vanilla JavaScript
**Client-side interactivity**

- **Philosophy**: No external framework dependencies
- **Features**: ES6+ syntax, async/await, modules
- **Components**: Dynamic component loading system
- **Quiz System**: Interactive learning functionality

## Development Dependencies

### JupyterLab 4.2.6
**Data exploration and analysis**

- **Usage**: Data analysis, visualization, prototyping
- **Integration**: Python kernel for interactive development
- **Features**: Notebook interface, data visualization

### Additional Libraries
**Supporting utilities**

- **matplotlib**: Data visualization (if needed)
- **pygame**: Potentially unused - candidate for removal
- **Various utilities**: String processing, file handling

## Architecture Patterns

### Static Site Generation
**JAMstack Architecture**

- **JavaScript**: Client-side interactivity
- **APIs**: JSON data files as API
- **Markup**: Pre-generated HTML pages

### Component-Based Design
**Modular Frontend Architecture**

- **Pattern**: Reusable HTML components
- **Loading**: Dynamic component injection
- **Maintenance**: Single-point updates

### Data Pipeline Pattern
**ETL (Extract, Transform, Load)**

- **Extract**: Web scraping from external sources
- **Transform**: Categorization and semantic analysis
- **Load**: Static HTML generation

## Development Environment

### Required Tools

#### Python Environment
```bash
# Python 3.9 or higher
python --version

# Virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

#### Development Server
```bash
# Start local development server
python start_server.py

# Access at http://localhost:5000
```

### Optional Tools

#### Code Editor
- **VS Code**: Recommended with Python and HTML extensions
- **PyCharm**: Full IDE with integrated debugging
- **Sublime Text**: Lightweight alternative

#### Version Control
- **Git**: Required for project versioning
- **GitHub**: Remote repository hosting

## Deployment Architecture

### Static Hosting
**Production deployment options**

- **GitHub Pages**: Free static hosting
- **Netlify**: Advanced static hosting with CI/CD
- **Vercel**: Modern static site hosting
- **Traditional Web Hosting**: Any HTTP server

### Build Process
**Static site generation**

1. **Data Processing**: Run Python scripts
2. **Page Generation**: Create HTML files
3. **Asset Optimization**: Minimize CSS/JS
4. **Deployment**: Upload to static host

## Performance Characteristics

### Load Times
- **Static HTML**: Near-instantaneous loading
- **Component Loading**: Minimal JavaScript overhead
- **Data Size**: Optimized JSON for quick parsing

### Resource Usage
- **Memory**: Low memory footprint
- **CPU**: Minimal client-side processing
- **Bandwidth**: Efficient static asset delivery

### Scalability
- **CDN-Ready**: Easy distribution via content delivery networks
- **Caching**: Browser and server-side caching friendly
- **Mobile Performance**: Optimized for mobile devices

## Security Considerations

### Client-Side Security
- **XSS Prevention**: Input sanitization in JavaScript
- **HTTPS**: Secure transport in production
- **Content Security Policy**: Protection against malicious scripts

### Data Integrity
- **Version Control**: Git-based change tracking
- **Backup Strategy**: Multiple JSON file versions
- **Validation**: Automated data consistency checks

## Version Compatibility

### Python Compatibility
- **Minimum**: Python 3.9
- **Recommended**: Python 3.11+
- **Tested**: Python 3.9-3.12

### Browser Support
- **Modern Browsers**: Chrome, Firefox, Safari, Edge
- **Mobile Browsers**: iOS Safari, Chrome Mobile
- **Minimum Standards**: ES6+ support required

### Dependency Updates
- **Regular Updates**: Security patches and bug fixes
- **Breaking Changes**: Careful version pinning
- **Testing**: Comprehensive testing before updates

## Known Issues & Limitations

### Current Issues
- **Encoding**: `requirements.txt` may have UTF-8 BOM issues
- **Dependency Bloat**: Some unused packages (pygame, matplotlib)
- **Manual Workflow**: Script execution requires specific order

### Technical Debt
- **Error Handling**: Limited error recovery in scripts
- **Testing**: No automated test suite
- **Documentation**: Some script documentation incomplete

### Future Improvements
- **Containerization**: Docker for consistent environments
- **CI/CD Pipeline**: Automated testing and deployment
- **TypeScript**: Type safety for JavaScript components
- **Test Coverage**: Comprehensive automated testing

---

*This technology stack documentation reflects the current state of the project. For updates and changes, monitor the requirements.txt file and project changelog.*