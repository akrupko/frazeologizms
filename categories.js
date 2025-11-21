/**
 * Categories Page JavaScript
 * Populates the categories grid with available phraseological themes from API
 */

class CategoriesPage {
    constructor() {
        this.categories = [];
        this.init();
    }

    init() {
        // Wait for components to be loaded
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                // Wait for components to load before rendering
                window.addEventListener('componentsLoaded', () => this.loadCategories());
            });
        } else {
            // Check if components are already loaded
            if (document.getElementById('categories-grid')) {
                this.loadCategories();
            } else {
                // Wait for components to load
                window.addEventListener('componentsLoaded', () => this.loadCategories());
            }
        }
    }

    async loadCategories() {
        try {
            console.log('Loading categories from API...');
            
            const response = await fetch(`${window.API_BASE_URL}/categories`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status} - ${response.statusText}`);
            }
            
            const data = await response.json();
            this.categories = data.categories || [];
            
            console.log(`Loaded ${this.categories.length} categories`);
            
            if (this.categories.length === 0) {
                throw new Error('No categories found');
            }
            
            this.render();
            
        } catch (error) {
            console.error('Error loading categories:', error);
            this.showError(error);
        }
    }

    getCategoriesData() {
        return this.categories;
    }

    render() {
        const grid = document.getElementById('categories-grid');
        if (!grid) {
            console.error('Categories grid element not found');
            return;
        }

        // Clear existing content
        grid.innerHTML = '';

        // Create category cards
        this.categories.forEach(category => {
            const card = this.createCategoryCard(category);
            grid.appendChild(card);
        });

        // Add event listeners
        this.setupEventListeners();
    }

    createCategoryCard(category) {
        const card = document.createElement('div');
        card.className = 'category-card';
        
        // Determine difficulty level based on count (heuristic)
        const level = this.getDifficultyLevel(category.count);
        
        // Assign color based on category key or use a default
        const color = this.getCategoryColor(category.key);
        
        // Format count display
        const countText = this.formatCount(category.count);
        
        card.innerHTML = `
            <div class="category-icon" style="background-color: ${color}20; color: ${color};">
                ${category.icon || '📚'}
            </div>
            <div class="category-content">
                <h3 class="category-title">${category.name || category.key}</h3>
                <p class="category-description">${category.description || `Фразеологизмы на тему "${category.name || category.key}"`}</p>
                <div class="category-meta">
                    <span class="category-count">${countText}</span>
                    <span class="category-level">${level}</span>
                </div>
            </div>
        `;

        // Make card clickable
        card.addEventListener('click', () => {
            window.location.href = `/kategoria/${category.slug}/`;
        });

        return card;
    }

    getDifficultyLevel(count) {
        if (count < 15) return 'Легкий';
        if (count < 30) return 'Средний';
        return 'Сложный';
    }

    getCategoryColor(key) {
        // Assign colors based on category key for consistency
        const colorMap = {
            'emotions': '#f59e0b',
            'animals': '#10b981',
            'body-parts': '#3b82f6',
            'time': '#8b5cf6',
            'family': '#ef4444',
            'work': '#f97316',
            'mind': '#06b6d4',
            'money': '#84cc16',
            'house': '#a855f7',
            'food': '#ec4899',
            'speech': '#14b8a6',
            'religion': '#f43f5e',
            'clothes_appearance': '#6366f1',
            'appearance_beauty': '#ec4899',
            'games_entertainment': '#8b5cf6',
            'luck_fortune': '#10b981',
            'quantity_measure': '#f59e0b',
            'transport_travel': '#0ea5e9',
            'weather_nature': '#22c55e',
            'war_conflict': '#dc2626',
        };
        
        return colorMap[key] || '#6b7280';
    }

    formatCount(count) {
        if (count >= 50) {
            return `${count}+ выражений`;
        } else if (count % 10 === 1 && count !== 11) {
            return `${count} выражение`;
        } else if ([2, 3, 4].includes(count % 10) && ![12, 13, 14].includes(count % 100)) {
            return `${count} выражения`;
        } else {
            return `${count} выражений`;
        }
    }

    setupEventListeners() {
        // Add hover effects and other interactions
        const cards = document.querySelectorAll('.category-card');
        cards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-2px)';
                card.style.boxShadow = '0 8px 25px rgba(0, 0, 0, 0.15)';
            });

            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0)';
                card.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.1)';
            });
        });
    }

    showError(error) {
        const grid = document.getElementById('categories-grid');
        if (grid) {
            grid.innerHTML = `
                <div class="error-message">
                    <h3>Ошибка загрузки категорий</h3>
                    <p>Не удалось загрузить категории с сервера. Пожалуйста, попробуйте обновить страницу.</p>
                    <button onclick="location.reload()" class="retry-button">Попробовать снова</button>
                </div>
            `;
        }
    }
}

// Initialize the categories page
const categoriesPage = new CategoriesPage();