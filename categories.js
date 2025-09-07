/**
 * Categories Page JavaScript
 * Populates the categories grid with available phraseological themes
 */

class CategoriesPage {
    constructor() {
        this.categories = this.getCategoriesData();
        this.init();
    }

    init() {
        // Wait for components to be loaded
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                // Wait for components to load before rendering
                window.addEventListener('componentsLoaded', () => this.render());
            });
        } else {
            // Check if components are already loaded
            if (document.getElementById('categories-grid')) {
                this.render();
            } else {
                // Wait for components to load
                window.addEventListener('componentsLoaded', () => this.render());
            }
        }
    }

    getCategoriesData() {
        return [
            {
                id: 'frazeologizmy_emotions',
                icon: '😊',
                title: 'Эмоции и чувства',
                description: 'Фразеологизмы о радости, грусти, любви, страхе и других эмоциональных состояниях',
                count: '22 выражения',
                level: 'Средний',
                color: '#f59e0b',
                examples: ['на седьмом небе', 'душа в пятки ушла', 'сердце екнуло']
            },
            {
                id: 'frazeologizmy_animals',
                icon: '🐾',
                title: 'Животные и природа', 
                description: 'Идиомы с животными, птицами и природными явлениями',
                count: '45+ выражений',
                level: 'Легкий',
                color: '#10b981',
                examples: ['медведь на ухо наступил', 'заячья душа', 'волки сыты']
            },
            {
                id: 'frazeologizmy_body-parts',
                icon: '👤',
                title: 'Части тела',
                description: 'Фразеологизмы с упоминанием головы, рук, глаз и других частей тела',
                count: '38+ выражений',
                level: 'Средний',
                color: '#3b82f6',
                examples: ['голова идет кругом', 'рука об руку', 'глаза разбежались']
            },
            {
                id: 'frazeologizmy_time',
                icon: '⏰',
                title: 'Время и возраст',
                description: 'Выражения о времени, возрасте и жизненных периодах',
                count: '25+ выражений', 
                level: 'Средний',
                color: '#8b5cf6',
                examples: ['время летит', 'на старости лет', 'с младых ногтей']
            },
            {
                id: 'frazeologizmy_family',
                icon: '👪',
                title: 'Семья и отношения',
                description: 'Фразеологизмы о семейных связях и межличностных отношениях',
                count: '28+ выражений',
                level: 'Легкий',
                color: '#ef4444',
                examples: ['кровь от крови', 'седьмая вода на киселе', 'как за каменной стеной']
            },
            {
                id: 'frazeologizmy_work',
                icon: '⚙️',
                title: 'Труд и работа',
                description: 'Идиомы о трудовой деятельности, профессиях и рабочих процессах',
                count: '32+ выражений',
                level: 'Средний',
                color: '#f97316',
                examples: ['засучить рукава', 'работать спустя рукава', 'дело мастера боится']
            },
            {
                id: 'frazeologizmy_mind',
                icon: '🧠',
                title: 'Ум и глупость',
                description: 'Фразеологизмы об интеллектуальных способностях и мышлении',
                count: '30+ выражений',
                level: 'Сложный',
                color: '#06b6d4',
                examples: ['светлая голова', 'дурью маяться', 'ума палата']
            },
            {
                id: 'frazeologizmy_money',
                icon: '💰',
                title: 'Деньги и богатство',
                description: 'Выражения о материальном достатке, богатстве и бедности',
                count: '26+ выражений',
                level: 'Средний',
                color: '#84cc16',
                examples: ['денег куры не клюют', 'сидеть на мели', 'золотые горы']
            },
            {
                id: 'frazeologizmy_house',
                icon: '🏠',
                title: 'Дом и быт',
                description: 'Фразеологизмы о домашней жизни, быте и повседневных делах',
                count: '24+ выражения',
                level: 'Легкий',
                color: '#a855f7',
                examples: ['дом полная чаша', 'на своих хлебах', 'домашний очаг']
            },
            {
                id: 'frazeologizmy_food',
                icon: '🍽️',
                title: 'Еда и питье',
                description: 'Идиомы о пище, напитках и процессе питания',
                count: '20+ выражений',
                level: 'Легкий', 
                color: '#ec4899',
                examples: ['хлеб насущный', 'заварить кашу', 'не хлебом единым']
            },
            {
                id: 'frazeologizmy_speech',
                icon: '💬',
                title: 'Речь и общение',
                description: 'Фразеологизмы о языке, разговоре и коммуникации между людьми',
                count: '35+ выражений',
                level: 'Средний',
                color: '#14b8a6',
                examples: ['слово за слово', 'язык без костей', 'молчать как рыба']
            },
            {
                id: 'frazeologizmy_religion',
                icon: '⛪',
                title: 'Религия и мифология',
                description: 'Библейские выражения и фразеологизмы с мифологическими мотивами',
                count: '18+ выражений',
                level: 'Сложный',
                color: '#f43f5e',
                examples: ['манна небесная', 'вавилонское столпотворение', 'козел отпущения']
            },
            {
                id: 'frazeologizmy_clothes_appearance',
                icon: '👔',
                title: 'Одежда и облик',
                description: 'Фразеологизмы об одежде и внешнем облике человека',
                count: '15+ выражений',
                level: 'Легкий',
                color: '#6366f1',
                examples: ['одетый с иголочки', 'в чем мать родила', 'рядиться в павлиньи перья']
            },
            {
                id: 'frazeologizmy_appearance_beauty',
                icon: '✨',
                title: 'Внешность и красота',
                description: 'Фразеологизмы о внешности, красоте и привлекательности',
                count: '20+ выражений',
                level: 'Средний',
                color: '#ec4899',
                examples: ['красота неописуемая', 'не лицом красив', 'глаз не оторвать']
            },
            {
                id: 'frazeologizmy_games_entertainment',
                icon: '🎮',
                title: 'Игры и развлечения',
                description: 'Фразеологизмы об играх, развлечениях и досуге',
                count: '25+ выражений',
                level: 'Средний',
                color: '#8b5cf6',
                examples: ['играть в кошки-мышки', 'дело не в шляпе', 'карты в руки']
            },
            {
                id: 'frazeologizmy_luck_fortune',
                icon: '🍀',
                title: 'Удача и судьба',
                description: 'Фразеологизмы об удаче, везении и судьбе',
                count: '22+ выражения',
                level: 'Средний',
                color: '#10b981',
                examples: ['фортуна улыбнулась', 'родиться под счастливой звездой', 'как карта ляжет']
            },
            {
                id: 'frazeologizmy_quantity_measure',
                icon: '📏',
                title: 'Количество и мера',
                description: 'Фразеологизмы о количестве, размере и мере',
                count: '30+ выражений',
                level: 'Средний',
                color: '#f59e0b',
                examples: ['кот наплакал', 'море по колено', 'капля в море']
            },
            {
                id: 'frazeologizmy_transport_travel',
                icon: '🚗',
                title: 'Транспорт и путешествия',
                description: 'Фразеологизмы о передвижении, транспорте и путешествиях',
                count: '18+ выражений',
                level: 'Легкий',
                color: '#06b6d4',
                examples: ['куда глаза глядят', 'на всех парусах', 'семимильными шагами']
            },
            {
                id: 'frazeologizmy_war_conflict',
                icon: '⚔️',
                title: 'Война и конфликты',
                description: 'Фразеологизмы о военных действиях и конфликтах',
                count: '24+ выражения',
                level: 'Сложный',
                color: '#ef4444',
                examples: ['как на войне', 'биться не на жизнь, а на смерть', 'держать порох сухим']
            },
            {
                id: 'frazeologizmy_weather_nature',
                icon: '🌤️',
                title: 'Погода и природа',
                description: 'Фразеологизмы о погодных явлениях и природе',
                count: '26+ выражений',
                level: 'Средний',
                color: '#84cc16',
                examples: ['дождичек в четверг', 'на улице собачья погода', 'как снег на голову']
            }
        ];
    }

    render() {
        const grid = document.getElementById('categories-grid');
        if (!grid) {
            console.error('Categories grid element not found');
            return;
        }

        grid.innerHTML = this.categories.map(category => this.createCategoryCard(category)).join('');
        
        // Add click event listeners
        this.addEventListeners();
    }

    createCategoryCard(category) {
        return `
            <div class="category-card" data-category="${category.id}" style="--category-color: ${category.color}">
                <div class="category-header">
                    <div class="category-icon">${category.icon}</div>
                    <div class="category-level level-${category.level.toLowerCase()}">${category.level}</div>
                </div>
                
                <div class="category-content">
                    <h3 class="category-title">${category.title}</h3>
                    <p class="category-description">${category.description}</p>
                    
                    <div class="category-examples">
                        <strong>Примеры:</strong>
                        <span class="examples-text">${category.examples.join(', ')}</span>
                    </div>
                    
                    <div class="category-stats">
                        <span class="category-count">${category.count}</span>
                        <span class="category-difficulty">Уровень: ${category.level}</span>
                    </div>
                </div>
                
                <button class="category-button" data-url="${category.id}.html">
                    <span>Начать изучение</span>
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                        <path d="M6 4L10 8L6 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </button>
            </div>
        `;
    }

    addEventListeners() {
        // Add click listeners to category buttons
        document.querySelectorAll('.category-button').forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const url = button.dataset.url;
                if (url) {
                    // Add loading state
                    button.classList.add('loading');
                    button.innerHTML = '<span>Загрузка...</span>';
                    
                    // Navigate after short delay for better UX
                    setTimeout(() => {
                        window.location.href = url;
                    }, 300);
                }
            });
        });

        // Add hover effects for cards
        document.querySelectorAll('.category-card').forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-4px)';
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0)';
            });
        });

        // Add keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && e.target.classList.contains('category-card')) {
                const button = e.target.querySelector('.category-button');
                if (button) button.click();
            }
        });
    }
}

// Initialize when page loads - wait for components to be ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new CategoriesPage();
    });
} else {
    new CategoriesPage();
}

// Export for potential use by other scripts
window.CategoriesPage = CategoriesPage;