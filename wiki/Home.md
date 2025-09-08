# Frazeologizms - Russian Phraseological Units Learning Platform

Welcome to the **Frazeologizms** project wiki! This is an interactive learning platform dedicated to Russian phraseological units (idioms, expressions, and proverbs).

## 📚 What is Frazeologizms?

The **frazeologizms** project is a comprehensive educational platform that provides:
- **Interactive Learning**: Explore Russian idioms with definitions, meanings, and etymologies
- **Semantic Categorization**: Phrases organized into meaningful thematic groups
- **Quiz System**: Test your knowledge with interactive exercises
- **Exam Preparation**: Targeted practice for Russian language exams (EGE/OGÉ)
- **Cultural Insights**: Understand Russian culture through idiomatic expressions

## 🏗️ Architecture Overview

The platform uses a hybrid architecture combining:
- **Frontend**: Static website with dynamic JavaScript components
- **Backend**: Python-based data processing pipeline
- **Data Layer**: JSON-based storage with semantic categorization

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Data Layer    │    │ Processing Layer │    │Presentation Layer│
│                 │    │                  │    │                 │
│ • JSON Files    │───▶│ • Python Scripts │───▶│ • Static HTML   │
│ • Categories    │    │ • Categorization │    │ • JavaScript    │
│ • Corrections   │    │ • Validation     │    │ • CSS Styling   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

1. **Clone the repository**
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Run data processing**: Execute Python scripts in sequence
4. **Generate pages**: `python generate_pages.py`
5. **Start local server**: `python start_server.py`
6. **Open browser**: Navigate to `http://localhost:5000`

## 📖 Documentation Structure

### Core Documentation
- **[Project Overview](Project-Overview.md)** - Detailed project information
- **[Technology Stack](Technology-Stack.md)** - Dependencies and tools
- **[System Architecture](System-Architecture.md)** - Technical architecture details

### Data & Processing
- **[Data Architecture](Data-Architecture.md)** - Data model and structure
- **[Categorization System](Categorization-System.md)** - Semantic classification engine
- **[Data Processing Pipeline](Data-Processing-Pipeline.md)** - Automated processing workflow

### Frontend Development
- **[Frontend Architecture](Frontend-Architecture.md)** - Component-based design
- **[Quiz Functionality](Quiz-Functionality.md)** - Interactive learning system
- **[Navigation System](Navigation-System.md)** - Site navigation and components

### Backend Systems
- **[Backend Processing](Backend-Processing.md)** - Python processing scripts
- **[Semantic Correction System](Semantic-Correction-System.md)** - Advanced categorization
- **[Static Site Generation](Static-Site-Generation.md)** - Page generation system

### Development & Maintenance
- **[Development Environment](Development-Environment.md)** - Setup and workflow
- **[User Guide](User-Guide.md)** - Platform usage instructions
- **[API Documentation](API-Documentation.md)** - Integration interfaces
- **[Maintenance Guide](Maintenance-Guide.md)** - Updates and management

## 🎯 Key Features

### 📊 Interactive Quiz System
- Non-repeating question selection
- Immediate feedback with explanations
- Progress tracking and statistics
- Etymology display for learning context

### 🏷️ Semantic Categorization
- **20+ thematic categories**: Animals, emotions, work, time, etc.
- **Advanced classification**: Based on complete phrase meanings
- **Automatic correction**: AI-powered semantic validation
- **Flexible organization**: Easy browsing and discovery

### 🛠️ Automated Processing
- **Data extraction**: Web scraping from external sources
- **Quality validation**: Automated error detection and correction
- **Page generation**: Static HTML creation for all categories
- **SEO optimization**: Search engine friendly structure

## 👥 Target Users

- **Language Learners**: Students studying Russian idioms
- **Exam Candidates**: EGE/OGÉ preparation
- **Linguists**: Researchers studying phraseology
- **Educators**: Teachers of Russian language and culture

## 🔧 Technology Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python 3.9+
- **Data**: JSON-based storage
- **Processing**: pandas, BeautifulSoup, regex
- **Server**: Flask (development)
- **Build**: Static site generation

## 📈 Project Statistics

- **10,000+** Russian phraseological units
- **20+** semantic categories
- **401** categorization corrections applied
- **100%** automated processing pipeline
- **SEO-optimized** static pages

## 🤝 Contributing

See our [Development Environment](Development-Environment.md) guide for setup instructions and [Maintenance Guide](Maintenance-Guide.md) for contribution guidelines.

## 📄 License

This project is designed for educational purposes and Russian language learning.

---

*Last updated: December 2024*