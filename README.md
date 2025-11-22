# Тренажер фразеологизмов русского языка

An interactive web-based trainer for Russian phraseological expressions (фразеологизмы) with 1,200+ phrases organized by thematic categories.

## Technology Stack

- **Backend**: Flask 3.1.2 with SQLAlchemy ORM
- **Database**: MySQL (optimized for Timeweb hosting)
- **Caching**: Flask-Caching (with Redis support for production)
- **Compression**: Flask-Compress for optimized asset delivery
- **Frontend**: Vanilla JavaScript with modular component architecture
- **Database Driver**: PyMySQL for MySQL connectivity

## Project Structure

```
app/
├── __init__.py          # Flask application factory
├── config.py            # Configuration management (environment-based)
├── extensions.py        # Flask extensions initialization
├── models.py            # SQLAlchemy models (PhraseologicalEntry)
├── routes.py            # API routes and main views
├── static/              # Static assets
│   ├── style.css        # Main stylesheet
│   ├── script.js        # Frontend phrase trainer logic
│   ├── navigation.js    # Navigation and sidebar functionality
│   └── component-loader.js  # Dynamic component loading system
└── templates/           # Jinja2 templates
    ├── base.html        # Base template with common layout
    ├── index.html       # Main quiz interface
    ├── categories.html  # Categories listing page
    ├── category.html    # Category-specific page
    └── partials/        # Component HTML partials
        ├── header.html
        ├── navigation.html
        ├── footer.html
        ├── quiz-content.html
        ├── categories-content.html
        └── seo-content.html

run.py                  # Development entry point
wsgi.py                 # Production WSGI entry point
start_server.py         # Simple server launcher
requirements.txt        # Python dependencies
.env.example           # Environment variables template
.gitignore             # Git ignore rules
```

## Quick Start

### Prerequisites

- Python 3.8+
- MySQL database (for production) or SQLite (for development)
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd frazeologizmy
```

2. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. Run the development server:
```bash
flask --app app run
# or
python start_server.py
```

The application will be available at `http://127.0.0.1:5000`

## API Documentation

The application provides a RESTful API for accessing phraseological data. All API endpoints are prefixed with `/api/`.

### Endpoints

#### 1. Get Phrases
```
GET /api/phrases
```

**Parameters:**
- `category` (optional): Filter by category name
- `limit` (optional): Number of phrases to return (default: 20)
- `offset` (optional): Number of phrases to skip (default: 0)
- `random` (optional): Return random phrases if set to 'true'

**Response:**
```json
{
  "phrases": [
    {
      "id": 1,
      "phrase": "бить баклуши",
      "meanings": ["бездельничать, лениться"],
      "etymology": "Старинное выражение...",
      "category": "work",
      "slug": "bit-baklushi"
    }
  ],
  "total": 1200,
  "limit": 20,
  "offset": 0
}
```

**Examples:**
```bash
# Get all phrases (first 20)
GET /api/phrases

# Get phrases from 'work' category
GET /api/phrases?category=work

# Get 10 random phrases
GET /api/phrases?random=true&limit=10

# Get phrases with pagination
GET /api/phrases?limit=50&offset=100
```

#### 2. Search Phrases
```
GET /api/phrases/search
```

**Parameters:**
- `q` (required): Search query (minimum 2 characters)
- `limit` (optional): Number of results to return (default: 20)

**Response:**
```json
{
  "phrases": [
    {
      "id": 1,
      "phrase": "бить баклуши",
      "meanings": ["бездельничать, лениться"],
      "etymology": "Старинное выражение...",
      "category": "work",
      "slug": "bit-baklushi"
    }
  ],
  "query": "баклуши"
}
```

#### 3. Get Categories
```
GET /api/categories
```

**Response:**
```json
{
  "categories": [
    {
      "key": "work",
      "name": "Труд и работа",
      "slug": "trud-i-rabota",
      "count": 45,
      "icon": "⚙️",
      "seo": {
        "title": "Фразеологизмы: Труд и работа",
        "description": "Идиомы о трудовой деятельности..."
      },
      "description": "Идиомы о трудовой деятельности, профессиях и рабочих процессах"
    }
  ]
}
```

#### 4. Autocomplete Search
```
GET /api/search
```

**Parameters:**
- `q` (required): Search query (minimum 2 characters)
- `limit` (optional): Number of results to return (default: 10)

**Response:**
```json
{
  "results": [
    {
      "id": 1,
      "phrase": "бить баклуши",
      "category": "work",
      "slug": "bit-baklushi",
      "meanings": ["бездельничать, лениться"]
    }
  ],
  "query": "бак"
}
```

#### 5. Get Single Phrase
```
GET /api/phrases/<id>
```

**Response:**
```json
{
  "id": 1,
  "phrase": "бить баклуши",
  "meanings": ["бездельничать, лениться"],
  "etymology": "Старинное выражение...",
  "category": "work",
  "slug": "bit-baklushi"
}
```

#### 6. Health Check
```
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "phrases_count": 1200
}
```

### Caching

API endpoints implement caching headers for optimal performance:
- **Phrases endpoint**: 5 minutes (300 seconds)
- **Categories endpoint**: 1 hour (3600 seconds) 
- **Search endpoints**: 3 minutes (180 seconds)
- **Individual phrases**: 1 hour (3600 seconds)

All responses include appropriate `Cache-Control` headers for browser caching.

### Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `400`: Bad request (e.g., search query too short)
- `404`: Resource not found
- `500`: Internal server error

Error responses include descriptive messages:
```json
{
  "error": "Query must be at least 2 characters"
}
```

### JavaScript Integration

The frontend automatically uses these API endpoints. The base API URL is exposed as `window.API_BASE_URL` in all templates.

**Example usage:**
```javascript
// Load phrases for a specific category
const response = await fetch(`${window.API_BASE_URL}/phrases?category=work&limit=50`);
const data = await response.json();

// Search phrases
const searchResponse = await fetch(`${window.API_BASE_URL}/search?q=баклуши`);
const searchData = await searchResponse.json();

// Load categories
const categoriesResponse = await fetch(`${window.API_BASE_URL}/categories`);
const categoriesData = await categoriesResponse.json();
```

## Development

The application uses Flask with SQLAlchemy ORM and supports both MySQL (production) and SQLite (development/testing).

```env
FLASK_ENV=development
DB_HOST=your-db-host.timeweb.com
DB_PORT=3306
DB_NAME=frazes
DB_USER=your-db-user
DB_PASSWORD=your-db-password
```

### 4. Run the Application

#### Option A: Using Flask CLI (recommended for development)

```bash
export FLASK_APP=app
flask run
```

Or using `--app` parameter:

```bash
flask --app app run
```

#### Option B: Using the convenience script

```bash
python start_server.py
```

#### Option C: Using Python directly

```bash
python run.py
```

The application will start on `http://localhost:5000`

## API Endpoints

### Main Routes

- `GET /` - Main quiz interface
- `GET /categories` - Categories listing page
- `GET /category/<category>` - Category-specific page

### API Routes (JSON)

All API endpoints are under `/api`:

#### Phrases

- `GET /api/phrases` - Get phrases with optional filtering
  - Query parameters: `category`, `limit`, `offset`
  - Example: `/api/phrases?category=animals&limit=20&offset=0`

- `GET /api/phrases/search?q=<query>` - Search phrases by text
  - Query parameters: `q` (required, min 2 chars), `limit`

- `GET /api/phrases/<id>` - Get a specific phrase by ID

- `GET /api/phrases/slug/<slug>` - Get a phrase by URL-safe slug

#### Categories

- `GET /api/categories` - Get all available categories with phrase counts

#### Health

- `GET /api/health` - Health check endpoint (includes DB connection status)

## Database Schema

The application connects to the `phraseological_dict` table with the following structure:

```sql
CREATE TABLE phraseological_dict (
    id INT PRIMARY KEY AUTO_INCREMENT,
    phrase VARCHAR(500) NOT NULL UNIQUE INDEX,
    meanings JSON,
    etymology TEXT,
    category VARCHAR(100) INDEX,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## Configuration

### Environment Variables

See `.env.example` for all available configuration options.

#### Key Variables

- `FLASK_ENV` - `development`, `production`, or `testing`
- `FLASK_DEBUG` - Enable/disable debug mode
- `SECRET_KEY` - Flask secret key (must be changed in production)
- `DB_*` - Database credentials
- `CACHE_TYPE` - Cache backend (`simple` for dev, `redis` for production)

### Configuration Files

#### `app/config.py`

Contains three configuration classes:

- `DevelopmentConfig` - Debug enabled, simple caching
- `ProductionConfig` - Debug disabled, requires Redis
- `TestingConfig` - In-memory SQLite database

## Deployment

### Local Development

```bash
python start_server.py
```

### Production with Gunicorn

1. Install gunicorn:

```bash
pip install gunicorn
```

2. Set production environment:

```bash
export FLASK_ENV=production
export CACHE_TYPE=redis  # Requires Redis running
```

3. Run with gunicorn:

```bash
gunicorn --workers 4 --bind 0.0.0.0:8000 wsgi:app
```

### Timeweb Hosting

For Timeweb hosting:

1. Update `.env` with Timeweb MySQL credentials
2. Set `FLASK_ENV=production`
3. Use gunicorn as shown above or configure via Timeweb control panel
4. Ensure Redis is available or switch back to `CACHE_TYPE=simple`

## Caching Configuration

### Development

Uses simple in-memory caching:

```env
CACHE_TYPE=simple
CACHE_DEFAULT_TIMEOUT=300  # 5 minutes
```

### Production

Uses Redis for distributed caching:

```env
CACHE_TYPE=redis
REDIS_URL=redis://localhost:6379/0
CACHE_DEFAULT_TIMEOUT=300
```

Install Redis:

```bash
# macOS
brew install redis

# Ubuntu/Debian
sudo apt-get install redis-server

# Start Redis
redis-server
```

## Static Assets

All static files (CSS, JavaScript) are served from `app/static/`:

- `style.css` - Main stylesheet
- `script.js` - Frontend phrase trainer logic
- `navigation.js` - Navigation and responsive sidebar
- `component-loader.js` - Dynamic component system

Static files are automatically served at `/static/` by Flask.

## Frontend Features

- **Quiz Mode**: Interactive multiple-choice questions for phrases
- **Category Navigation**: Browse phrases by thematic categories
- **Search**: Full-text search across all phrases
- **Etymology Display**: Optional reveal of phrase etymology
- **Responsive Design**: Mobile-friendly interface
- **Component System**: Modular loading of reusable components

## SEO and Performance

The application includes a comprehensive SEO automation suite for optimal search engine visibility and performance.

### SEO Features

#### 1. Metadata Management

All pages automatically generate optimized meta tags:

- **Title tags**: Unique, keyword-optimized titles for each page
- **Meta descriptions**: Compelling descriptions with call-to-action
- **Canonical URLs**: Prevent duplicate content issues
- **Open Graph tags**: Enhanced social media sharing (Facebook, LinkedIn)
- **Twitter Cards**: Rich previews for Twitter shares

Pages with SEO metadata:
- Home page
- All category pages
- All phrase detail pages
- Search pages (noindex)

#### 2. Structured Data (JSON-LD)

Every page includes appropriate Schema.org structured data for rich search results:

**Home Page:**
```json
{
  "@type": "WebSite",
  "potentialAction": {
    "@type": "SearchAction"
  }
}
```

**Category Pages:**
```json
{
  "@type": "CollectionPage",
  "numberOfItems": 150
}
```

**Phrase Detail Pages:**
```json
[
  {
    "@type": "Article",
    "headline": "бить баклуши",
    "datePublished": "...",
    "dateModified": "..."
  },
  {
    "@type": "DefinedTerm",
    "name": "бить баклуши",
    "description": "значение фразеологизма"
  }
]
```

#### 3. Sitemap and Robots

The application dynamically generates SEO-essential files:

**Sitemap (`/sitemap.xml`):**
- Lists all pages: home, categories, and phrase details
- Includes `lastmod` timestamps from the database
- Cached for 1 hour (refreshes when new data is added)
- Proper priority and changefreq settings

**Robots.txt (`/robots.txt`):**
```
User-agent: *
Allow: /
Disallow: /api/
Disallow: /search?
Disallow: /search/text

Sitemap: https://frazeologizm.ru/sitemap.xml
```

#### 4. Custom SEO Metadata

Override default metadata by editing `app/seo_metadata.yaml`:

```yaml
pages:
  home:
    title: "Custom home page title"
    description: "Custom description"
  
  categories:
    my-category-slug:
      title: "Custom category title"
      description: "Custom description"
  
  phrases:
    my-phrase-slug:
      title: "Custom phrase title"
      description: "Custom description"
```

### Performance Optimizations

#### 1. Compression

Flask-Compress automatically gzip-compresses all responses over 500 bytes:
- HTML pages
- JSON API responses
- CSS and JavaScript files

#### 2. Caching

**Browser Caching:**
- Static assets (CSS, JS, images): 1 year (31536000 seconds)
- API responses: 3-60 minutes depending on endpoint
- Page metadata: Cached in Redis/memory

**Server-Side Caching:**
- Category data: 1 hour
- Navigation: 10 minutes
- Sitemap: 1 hour
- API responses: 3-60 minutes

#### 3. CDN and Timeweb Configuration

To enable CDN caching on Timeweb:

1. **Enable caching for static assets:**
   - Configure Timeweb CDN to cache `/static/*` paths
   - Set cache TTL to 1 year for static files

2. **HTML page caching:**
   - Cache home page for 1 hour
   - Cache category pages for 1 hour
   - Cache phrase pages for 1 day
   - Bypass cache for search and API endpoints

3. **Cache invalidation:**
   - Configure cache purge when content is updated
   - Use versioned static file names if needed

**Example Timeweb cache rules:**
```
# Static assets - cache for 1 year
/static/* -> Cache-Control: public, max-age=31536000

# Pages - cache with shorter TTL
/ -> Cache-Control: public, max-age=3600
/kategoria/* -> Cache-Control: public, max-age=3600
/frazeologizm/* -> Cache-Control: public, max-age=86400

# API - short cache
/api/* -> Cache-Control: public, max-age=300

# Dynamic/user-specific - no cache
/search* -> Cache-Control: no-cache
```

### Image Automation

The application automatically serves images for phrase detail pages:

#### Adding Images

1. **Create an image** for a phrase (recommended: WebP format)
2. **Name the file** using the phrase slug: `bit-baklushi.webp`
3. **Upload to** `app/static/images/`

**Example:**
```bash
# For phrase "бить баклуши" (slug: bit-baklushi)
app/static/images/bit-baklushi.webp

# Alternative formats (checked in order)
app/static/images/bit-baklushi.jpg
app/static/images/bit-baklushi.jpeg
app/static/images/bit-baklushi.png
```

The image will automatically:
- Display on the phrase detail page
- Be included in Open Graph meta tags
- Be referenced in JSON-LD structured data
- Have a fallback illustration if missing

#### Image Optimization Tips

1. **Use WebP format** for best compression (60-80% smaller than JPEG)
2. **Recommended size**: 800x600px or 600x600px
3. **Optimize before upload**:
   ```bash
   # Convert to WebP
   cwebp -q 80 input.jpg -o output.webp
   
   # Resize if needed
   convert input.jpg -resize 800x600 output.jpg
   ```
4. **Alt text**: Automatically set to the phrase text

### Advertising Integration

The application includes placeholder divs for ad integration:

#### Ad Slots

**1. Header Banner (Top of page)**
```html
<div class="ad-placeholder ad-header" data-ad-slot="header">
  <!-- Insert your ad code here -->
</div>
```
Recommended size: Leaderboard (728x90) or Large Leaderboard (970x90)

**2. Sidebar (Category menu)**
```html
<div class="ad-placeholder ad-sidebar" data-ad-slot="sidebar">
  <!-- Insert your ad code here -->
</div>
```
Recommended size: Medium Rectangle (300x250)

**3. In-Content (After main content)**
```html
<div class="ad-placeholder ad-content" data-ad-slot="content">
  <!-- Insert your ad code here -->
</div>
```
Recommended size: Large Rectangle (336x280) or Medium Rectangle (300x250)

#### Adding Ad Scripts

**Option 1: Direct injection (templates)**

Edit `app/templates/base.html` and replace placeholder divs:

```html
<div class="ad-placeholder ad-header" data-ad-slot="header">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
  <ins class="adsbygoogle"
       style="display:inline-block;width:728px;height:90px"
       data-ad-client="ca-pub-XXXXXXXXXX"
       data-ad-slot="XXXXXXXXXX"></ins>
  <script>
       (adsbygoogle = window.adsbygoogle || []).push({});
  </script>
</div>
```

**Option 2: JavaScript injection (external script)**

Add ad script to `app/static/ads.js` and include in base template:

```javascript
// app/static/ads.js
document.addEventListener('DOMContentLoaded', function() {
  // Header ad
  const headerAd = document.querySelector('.ad-header');
  if (headerAd) {
    headerAd.innerHTML = '<!-- Your ad code -->';
  }
  
  // Sidebar ad
  const sidebarAd = document.querySelector('.ad-sidebar');
  if (sidebarAd) {
    sidebarAd.innerHTML = '<!-- Your ad code -->';
  }
});
```

Then in `base.html`:
```html
<script src="{{ url_for('static', filename='ads.js') }}"></script>
```

**Option 3: Ad network tags (Google AdSense)**

If using Google AdSense auto ads, simply add the AdSense script to `<head>` in `base.html`:

```html
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"
        data-ad-client="ca-pub-XXXXXXXXXX"></script>
```

### Validating SEO Implementation

#### 1. Test Meta Tags
```bash
curl -I https://frazeologizm.ru/
curl https://frazeologizm.ru/ | grep -E '<meta|<title|<link rel="canonical'
```

#### 2. Test Structured Data
- Use [Google Rich Results Test](https://search.google.com/test/rich-results)
- Paste any page URL to validate JSON-LD schemas

#### 3. Test Sitemap
```bash
curl https://frazeologizm.ru/sitemap.xml
```
Verify it lists all pages with proper lastmod dates.

#### 4. Test Robots.txt
```bash
curl https://frazeologizm.ru/robots.txt
```

#### 5. Performance Testing
```bash
# Test compression
curl -H "Accept-Encoding: gzip" -I https://frazeologizm.ru/

# Test cache headers
curl -I https://frazeologizm.ru/static/style.css
```

### SEO Configuration

Set the base site URL in your `.env` file:

```env
SITE_URL=https://frazeologizm.ru
```

This URL is used for:
- Canonical URLs
- Open Graph URLs
- Sitemap absolute URLs
- Structured data URLs

## Development

### Adding New Routes

Edit `app/routes.py` and add new Blueprint routes:

```python
@main_bp.route('/new-page')
def new_page():
    return render_template('new_page.html')
```

### Creating Models

Edit `app/models.py` and inherit from `db.Model`:

```python
class NewModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
```

### Database Migrations

For future migrations, install Flask-Migrate:

```bash
pip install Flask-Migrate
```

Then create migrations:

```bash
flask db init
flask db migrate -m "Description"
flask db upgrade
```

## Troubleshooting

### Database Connection Error

- Verify MySQL credentials in `.env`
- Ensure MySQL server is running
- Check network connectivity to database host
- Verify `phraseological_dict` table exists

### Static Files Not Loading

- Check that files exist in `app/static/`
- Verify static file folder path in Flask config
- Clear browser cache

### Port Already in Use

Change the port in `.env`:

```env
FLASK_PORT=5001
```

Or kill the process:

```bash
# macOS/Linux
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

## Performance Notes

- Caching is enabled by default (300s TTL)
- Database queries use connection pooling
- Static assets are compressed with gzip
- CSS/JS are served with proper cache headers

## Contributing

1. Create a feature branch
2. Make your changes
3. Test locally with `python start_server.py`
4. Commit with descriptive messages

## License

See LICENSE file for details.

## Support

For issues or questions, refer to the project documentation or contact the development team.
