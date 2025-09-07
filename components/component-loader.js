/**
 * Component Loader for Phrazeologisms Website
 * This script loads common components (navigation, header, footer, etc.)
 * into the current page and handles page-specific customizations.
 */

class ComponentLoader {
    constructor() {
        this.components = {
            navigation: 'components/navigation.html',
            header: 'components/header.html',
            footer: 'components/footer.html',
            'quiz-content': 'components/quiz-content.html',
            'seo-content': 'components/seo-content.html',
            'categories-content': 'components/categories-content.html'
        };
        
        this.pageConfigs = this.getPageConfigs();
        this.currentPage = this.getCurrentPageName();
    }

    /**
     * Load all components and initialize page
     */
    async loadComponents() {
        try {
            // Load navigation first
            await this.loadComponent('navigation', 'navigation-container');
            
            // Load main content components based on page type
            await this.loadComponent('header', 'header-container');
            
            // Special handling for categories page
            if (this.currentPage === 'categories') {
                await this.loadComponent('categories-content', 'categories-container');
                // Create container if it doesn't exist
                const container = document.querySelector('.container');
                if (container && !document.getElementById('categories-container')) {
                    const categoriesDiv = document.createElement('div');
                    categoriesDiv.id = 'categories-container';
                    container.appendChild(categoriesDiv);
                    await this.loadComponent('categories-content', 'categories-container');
                }
            } else {
                await this.loadComponent('quiz-content', 'quiz-container');
            }
            
            await this.loadComponent('footer', 'footer-container');
            
            // Only load SEO content for non-categories pages
            if (this.currentPage !== 'categories') {
                await this.loadComponent('seo-content', 'seo-container');
            }
            
            // Apply page-specific configurations
            this.applyPageConfig();
            
            // Set active navigation item
            this.setActiveNavigation();
            
            // Initialize navigation functionality
            this.initializeNavigation();
            
            // Dispatch event to signal components are loaded
            window.dispatchEvent(new CustomEvent('componentsLoaded'));
            
            console.log('All components loaded successfully');
        } catch (error) {
            console.error('Error loading components:', error);
        }
    }

    /**
     * Load a single component
     */
    async loadComponent(componentName, containerId) {
        try {
            const response = await fetch(this.components[componentName]);
            if (!response.ok) {
                throw new Error(`Failed to load ${componentName}: ${response.statusText}`);
            }
            
            const html = await response.text();
            const container = document.getElementById(containerId);
            
            if (container) {
                container.innerHTML = html;
            } else {
                console.warn(`Container ${containerId} not found for component ${componentName}`);
            }
        } catch (error) {
            console.error(`Error loading component ${componentName}:`, error);
        }
    }

    /**
     * Get current page name from URL
     */
    getCurrentPageName() {
        const path = window.location.pathname;
        const fileName = path.split('/').pop();
        
        if (fileName === 'index.html' || fileName === '') {
            return 'index';
        }
        
        return fileName.replace('.html', '');
    }

    /**
     * Apply page-specific configuration
     */
    applyPageConfig() {
        const config = this.pageConfigs[this.currentPage];
        if (!config) {
            console.warn(`No configuration found for page: ${this.currentPage}`);
            return;
        }

        // Set page title and description
        const titleElement = document.getElementById('page-title');
        const descriptionElement = document.getElementById('page-description');
        const footerElement = document.getElementById('footer-text');

        if (titleElement) titleElement.textContent = config.header.title;
        if (descriptionElement) descriptionElement.textContent = config.header.description;
        if (footerElement) footerElement.textContent = config.footer.text;

        // Set SEO content
        this.setSEOContent(config.seo);
        
        // Set page-specific JavaScript variables
        if (config.category) {
            window.CURRENT_CATEGORY = config.category;
        }
        if (config.categoryName) {
            window.CATEGORY_NAME = config.categoryName;
        }
        if (config.dataFile) {
            window.CATEGORY_DATA_FILE = config.dataFile;
        }
    }

    /**
     * Set SEO content for the page
     */
    setSEOContent(seoConfig) {
        const elements = {
            'seo-title': seoConfig.title,
            'seo-description': seoConfig.description,
            'seo-features-title': seoConfig.featuresTitle,
            'seo-features-text': seoConfig.featuresText,
            'seo-footer': seoConfig.footer
        };

        Object.keys(elements).forEach(id => {
            const element = document.getElementById(id);
            if (element && elements[id]) {
                element.textContent = elements[id];
            }
        });
    }

    /**
     * Set active navigation item
     */
    setActiveNavigation() {
        // Remove active class from all nav links
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => link.classList.remove('active'));

        // Add active class to current page link
        const currentPageLink = document.querySelector(`[data-page="${this.currentPage}"]`);
        if (currentPageLink) {
            currentPageLink.classList.add('active');
        }
    }

    /**
     * Initialize navigation functionality
     */
    initializeNavigation() {
        const sidebar = document.getElementById('sidebar');
        const mobileMenuBtn = document.getElementById('mobile-menu-btn');
        const sidebarClose = document.getElementById('sidebar-close');
        const mainContent = document.getElementById('main-content');

        if (mobileMenuBtn && sidebar && mainContent) {
            // Mobile menu toggle
            mobileMenuBtn.addEventListener('click', () => {
                sidebar.classList.toggle('open');
                mobileMenuBtn.classList.toggle('active');
                
                // Add overlay for mobile
                let overlay = document.querySelector('.sidebar-overlay');
                if (!overlay) {
                    overlay = document.createElement('div');
                    overlay.className = 'sidebar-overlay';
                    document.body.appendChild(overlay);
                    
                    overlay.addEventListener('click', () => {
                        sidebar.classList.remove('open');
                        mobileMenuBtn.classList.remove('active');
                        overlay.classList.remove('active');
                    });
                }
                overlay.classList.toggle('active');
            });

            // Close button
            if (sidebarClose) {
                sidebarClose.addEventListener('click', () => {
                    sidebar.classList.remove('open');
                    mobileMenuBtn.classList.remove('active');
                    const overlay = document.querySelector('.sidebar-overlay');
                    if (overlay) overlay.classList.remove('active');
                });
            }

            // Handle desktop layout
            if (window.innerWidth >= 1024) {
                mainContent.classList.add('shifted');
            }

            // Handle window resize
            window.addEventListener('resize', () => {
                if (window.innerWidth >= 1024) {
                    mainContent.classList.add('shifted');
                    sidebar.classList.remove('open');
                    mobileMenuBtn.classList.remove('active');
                } else {
                    mainContent.classList.remove('shifted');
                }
            });
        }
    }

    /**
     * Page configurations for all pages
     */
    getPageConfigs() {
        return {
            'index': {
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
            },
            'frazeologizmy_emotions': {
                header: {
                    title: '😊 Тренажер фразеологизмов',
                    description: 'Фразеологизмы о эмоциональных состояниях и переживаниях'
                },
                footer: {
                    text: '📚 Эмоции и чувства - фразеологизмы'
                },
                seo: {
                    title: 'Фразеологизмы об эмоциях - русские идиомы о чувствах онлайн',
                    description: 'Эмоции и чувства - фразеологизмы о эмоциональных состояниях и переживаниях. Наш интерактивный тренажер поможет вам изучить фразеологические единицы этой категории.',
                    featuresTitle: 'Особенности изучения фразеологизмов темы "Эмоции и чувства"',
                    featuresText: 'Фразеологизмы данной категории часто встречаются в заданиях ЕГЭ и ОГЭ по русскому языку. Изучение эмоций и чувств поможет вам:',
                    footer: 'Начните изучение прямо сейчас и повысьте свои шансы на успешную сдачу экзаменов по русскому языку! Изучайте фразеологизмы с подробными объяснениями.'
                },
                category: 'emotions_feelings',
                categoryName: 'Эмоции и чувства'
            },
            'frazeologizmy_animals': {
                header: {
                    title: '🐾 Тренажер фразеологизмов',
                    description: 'Фразеологизмы о животных и природных явлениях'
                },
                footer: {
                    text: '📚 Животные и природа - фразеологизмы'
                },
                seo: {
                    title: 'Фразеологизмы о животных - изучение русских идиом с животными онлайн',
                    description: 'Животные и природа - фразеологизмы о животных и природных явлениях. Изучайте русские идиомы о животных.',
                    featuresTitle: 'Особенности изучения фразеологизмов темы "Животные и природа"',
                    featuresText: 'Фразеологизмы данной категории часто встречаются в заданиях ЕГЭ и ОГЭ по русскому языку. Изучение животных и природы поможет вам:',
                    footer: 'Начните изучение прямо сейчас и повысьте свои шансы на успешную сдачу экзаменов по русскому языку!'
                },
                category: 'animals',
                categoryName: 'Животные и природа'
            },
            'frazeologizmy_body-parts': {
                header: {
                    title: '👤 Тренажер фразеологизмов',
                    description: 'Фразеологизмы с частями тела человека'
                },
                footer: {
                    text: '📚 Части тела - фразеологизмы'
                },
                seo: {
                    title: 'Фразеологизмы с частями тела - русские идиомы онлайн тренажер',
                    description: 'Части тела - фразеологизмы с частями тела человека. Изучение русских идиом с головой, руками, глазами.',
                    featuresTitle: 'Особенности изучения фразеологизмов темы "Части тела"',
                    featuresText: 'Фразеологизмы данной категории часто встречаются в заданиях ЕГЭ и ОГЭ по русскому языку. Изучение частей тела поможет вам:',
                    footer: 'Начните изучение прямо сейчас и повысьте свои шансы на успешную сдачу экзаменов по русскому языку!'
                },
                category: 'body_parts',
                categoryName: 'Части тела'
            },
            'frazeologizmy_time': {
                header: {
                    title: '⏰ Тренажер фразеологизмов',
                    description: 'Фразеологизмы о времени и возрастных периодах'
                },
                footer: {
                    text: '📚 Время и возраст - фразеологизмы'
                },
                seo: {
                    title: 'Фразеологизмы о времени - русские идиомы о возрасте онлайн',
                    description: 'Время и возраст - фразеологизмы о временных периодах и возрасте.',
                    featuresTitle: 'Особенности изучения фразеологизмов темы "Время и возраст"',
                    featuresText: 'Фразеологизмы данной категории часто встречаются в заданиях ЕГЭ и ОГЭ по русскому языку. Изучение времени и возраста поможет вам:',
                    footer: 'Начните изучение прямо сейчас и повысьте свои шансы на успешную сдачу экзаменов по русскому языку!'
                },
                category: 'time_age',
                categoryName: 'Время и возраст'
            },
            'frazeologizmy_religion': {
                header: {
                    title: '⛪ Тренажер фразеологизмов',
                    description: 'Религиозные и мифологические фразеологизмы'
                },
                footer: {
                    text: '📚 Религия и мифология - фразеологизмы'
                },
                seo: {
                    title: 'Религиозные фразеологизмы - библейские и мифологические идиомы',
                    description: 'Религия и мифология - фразеологизмы с религиозными и мифологическими мотивами.',
                    featuresTitle: 'Особенности изучения фразеологизмов темы "Религия и мифология"',
                    featuresText: 'Фразеологизмы данной категории часто встречаются в заданиях ЕГЭ и ОГЭ по русскому языку. Изучение религии и мифологии поможет вам:',
                    footer: 'Начните изучение прямо сейчас и повысьте свои шансы на успешную сдачу экзаменов по русскому языку!'
                },
                category: 'religion_mythology',
                categoryName: 'Религия и мифология'
            },
            'frazeologizmy_mind': {
                header: {
                    title: '🧠 Тренажер фразеологизмов',
                    description: 'Фразеологизмы об интеллектуальных способностях'
                },
                footer: {
                    text: '📚 Ум и глупость - фразеологизмы'
                },
                seo: {
                    title: 'Фразеологизмы об уме - русские идиомы об интеллекте и глупости',
                    description: 'Ум и глупость - фразеологизмы об интеллектуальных способностях.',
                    featuresTitle: 'Особенности изучения фразеологизмов темы "Ум и глупость"',
                    featuresText: 'Фразеологизмы данной категории часто встречаются в заданиях ЕГЭ и ОГЭ по русскому языку. Изучение ума и глупости поможет вам:',
                    footer: 'Начните изучение прямо сейчас и повысьте свои шансы на успешную сдачу экзаменов по русскому языку!'
                },
                category: 'mind_intelligence',
                categoryName: 'Ум и глупость'
            },
            'frazeologizmy_work': {
                header: {
                    title: '⚙️ Тренажер фразеологизмов',
                    description: 'Фразеологизмы о трудовой деятельности'
                },
                footer: {
                    text: '📚 Труд и работа - фразеологизмы'
                },
                seo: {
                    title: 'Фразеологизмы о работе - русские идиомы о труде онлайн',
                    description: 'Труд и работа - фразеологизмы о трудовой деятельности.',
                    featuresTitle: 'Особенности изучения фразеологизмов темы "Труд и работа"',
                    featuresText: 'Фразеологизмы данной категории часто встречаются в заданиях ЕГЭ и ОГЭ по русскому языку. Изучение труда и работы поможет вам:',
                    footer: 'Начните изучение прямо сейчас и повысьте свои шансы на успешную сдачу экзаменов по русскому языку!'
                },
                category: 'work_labor',
                categoryName: 'Труд и работа'
            },
            'frazeologizmy_family': {
                header: {
                    title: '👪 Тренажер фразеологизмов',
                    description: 'Фразеологизмы о семейных отношениях'
                },
                footer: {
                    text: '📚 Семья и отношения - фразеологизмы'
                },
                seo: {
                    title: 'Фразеологизмы о семье - русские идиомы о родственных отношениях',
                    description: 'Семья и отношения - фразеологизмы о семейных отношениях.',
                    featuresTitle: 'Особенности изучения фразеологизмов темы "Семья и отношения"',
                    featuresText: 'Фразеологизмы данной категории часто встречаются в заданиях ЕГЭ и ОГЭ по русскому языку. Изучение семьи и отношений поможет вам:',
                    footer: 'Начните изучение прямо сейчас и повысьте свои шансы на успешную сдачу экзаменов по русскому языку!'
                },
                category: 'family_relationships',
                categoryName: 'Семья и отношения'
            },
            'frazeologizmy_house': {
                header: {
                    title: '🏠 Тренажер фразеологизмов',
                    description: 'Фразеологизмы о домашнем быте'
                },
                footer: {
                    text: '📚 Дом и быт - фразеологизмы'
                },
                seo: {
                    title: 'Фразеологизмы о доме - русские идиомы о быте онлайн',
                    description: 'Дом и быт - фразеологизмы о домашнем быте.',
                    featuresTitle: 'Особенности изучения фразеологизмов темы "Дом и быт"',
                    featuresText: 'Фразеологизмы данной категории часто встречаются в заданиях ЕГЭ и ОГЭ по русскому языку. Изучение дома и быта поможет вам:',
                    footer: 'Начните изучение прямо сейчас и повысьте свои шансы на успешную сдачу экзаменов по русскому языку!'
                },
                category: 'house_home',
                categoryName: 'Дом и быт'
            },
            'frazeologizmy_speech': {
                header: {
                    title: '💬 Тренажер фразеологизмов',
                    description: 'Фразеологизмы о речи и коммуникации'
                },
                footer: {
                    text: '📚 Речь и общение - фразеологизмы'
                },
                seo: {
                    title: 'Фразеологизмы о речи - русские идиомы об общении онлайн',
                    description: 'Речь и общение - фразеологизмы о речи и коммуникации.',
                    featuresTitle: 'Особенности изучения фразеологизмов темы "Речь и общение"',
                    featuresText: 'Фразеологизмы данной категории часто встречаются в заданиях ЕГЭ и ОГЭ по русскому языку. Изучение речи и общения поможет вам:',
                    footer: 'Начните изучение прямо сейчас и повысьте свои шансы на успешную сдачу экзаменов по русскому языку!'
                },
                category: 'speech_communication',
                categoryName: 'Речь и общение'
            },
            'frazeologizmy_food': {
                header: {
                    title: '🍽️ Тренажер фразеологизмов',
                    description: 'Фразеологизмы о пище и напитках'
                },
                footer: {
                    text: '📚 Еда и питье - фразеологизмы'
                },
                seo: {
                    title: 'Фразеологизмы о еде - русские идиомы о пище и напитках',
                    description: 'Еда и питье - фразеологизмы о пище и напитках.',
                    featuresTitle: 'Особенности изучения фразеологизмов темы "Еда и питье"',
                    featuresText: 'Фразеологизмы данной категории часто встречаются в заданиях ЕГЭ и ОГЭ по русскому языку. Изучение еды и питья поможет вам:',
                    footer: 'Начните изучение прямо сейчас и повысьте свои шансы на успешную сдачу экзаменов по русскому языку!'
                },
                category: 'food_drink',
                categoryName: 'Еда и питье'
            },
            'frazeologizmy_money': {
                header: {
                    title: '💰 Тренажер фразеологизмов',
                    description: 'Фразеологизмы о материальном достатке'
                },
                footer: {
                    text: '📚 Деньги и богатство - фразеологизмы'
                },
                seo: {
                    title: 'Фразеологизмы о деньгах - русские идиомы о богатстве и бедности',
                    description: 'Деньги и богатство - фразеологизмы о материальном достатке.',
                    featuresTitle: 'Особенности изучения фразеологизмов темы "Деньги и богатство"',
                    featuresText: 'Фразеологизмы данной категории часто встречаются в заданиях ЕГЭ и ОГЭ по русскому языку. Изучение денег и богатства поможет вам:',
                    footer: 'Начните изучение прямо сейчас и повысьте свои шансы на успешную сдачу экзаменов по русскому языку!'
                },
                category: 'money_wealth',
                categoryName: 'Деньги и богатство'
            },
            'frazeologizmy_clothes_appearance': {
                header: {
                    title: '👔 Тренажер фразеологизмов',
                    description: 'Фразеологизмы об одежде и внешнем облике'
                },
                footer: {
                    text: '📚 Одежда и облик - фразеологизмы'
                },
                seo: {
                    title: 'Фразеологизмы об одежде - русские идиомы о внешнем облике',
                    description: 'Одежда и облик - фразеологизмы об одежде и внешнем облике.',
                    featuresTitle: 'Особенности изучения фразеологизмов темы "Одежда и облик"',
                    featuresText: 'Фразеологизмы данной категории часто встречаются в заданиях ЕГЭ и ОГЭ по русскому языку. Изучение одежды и облика поможет вам:',
                    footer: 'Начните изучение прямо сейчас и повысьте свои шансы на успешную сдачу экзаменов по русскому языку!'
                },
                category: 'clothes_appearance',
                categoryName: 'Одежда и облик'
            },
            'categories': {
                header: {
                    title: '📚 Выбор категории',
                    description: 'Выберите тему фразеологизмов для изучения'
                },
                footer: {
                    text: '🎯 Выберите интересующую категорию для изучения'
                },
                seo: {
                    title: 'Выбор категории фразеологизмов - тренажер русского языка',
                    description: 'Выберите категорию фразеологизмов для изучения: эмоции, животные, части тела, семья и другие темы. Интерактивный тренажер для подготовки к ЕГЭ и ОГЭ.',
                    featuresTitle: 'Категории фразеологизмов',
                    featuresText: 'Изучайте фразеологизмы по тематическим группам:',
                    footer: 'Выберите категорию и начните изучение фразеологизмов прямо сейчас!'
                },
                categoryName: 'Выбор категории'
            }
            // Add more page configurations as needed
        };
    }
}

// Initialize component loader when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const loader = new ComponentLoader();
    loader.loadComponents();
});

// Export for use in other scripts if needed
window.ComponentLoader = ComponentLoader;