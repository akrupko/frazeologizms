// Navigation functionality for phraseological units trainer

class Navigation {
    constructor() {
        this.sidebar = document.getElementById('sidebar');
        this.mainContent = document.getElementById('main-content');
        this.mobileMenuBtn = document.getElementById('mobile-menu-btn');
        this.sidebarClose = document.getElementById('sidebar-close');
        this.overlay = null;
        
        this.init();
    }
    
    init() {
        this.createOverlay();
        this.setupEventListeners();
        this.handleResize();
        
        // Set active navigation link
        this.setActiveLink();
    }
    
    createOverlay() {
        this.overlay = document.createElement('div');
        this.overlay.className = 'sidebar-overlay';
        document.body.appendChild(this.overlay);
        
        this.overlay.addEventListener('click', () => {
            this.closeSidebar();
        });
    }
    
    setupEventListeners() {
        // Mobile menu button
        if (this.mobileMenuBtn) {
            this.mobileMenuBtn.addEventListener('click', () => {
                this.toggleSidebar();
            });
        }
        
        // Sidebar close button
        if (this.sidebarClose) {
            this.sidebarClose.addEventListener('click', () => {
                this.closeSidebar();
            });
        }
        
        // Window resize
        window.addEventListener('resize', () => {
            this.handleResize();
        });
        
        // Escape key to close sidebar
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.sidebar.classList.contains('open')) {
                this.closeSidebar();
            }
        });
        
        // Close sidebar when clicking nav links on mobile
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth <= 768) {
                    this.closeSidebar();
                }
            });
        });
    }
    
    toggleSidebar() {
        if (this.sidebar.classList.contains('open')) {
            this.closeSidebar();
        } else {
            this.openSidebar();
        }
    }
    
    openSidebar() {
        this.sidebar.classList.add('open');
        this.mobileMenuBtn?.classList.add('active');
        this.overlay.classList.add('active');
        
        // Prevent body scrolling on mobile
        if (window.innerWidth <= 768) {
            document.body.style.overflow = 'hidden';
        }
    }
    
    closeSidebar() {
        this.sidebar.classList.remove('open');
        this.mobileMenuBtn?.classList.remove('active');
        this.overlay.classList.remove('active');
        
        // Restore body scrolling
        document.body.style.overflow = '';
    }
    
    handleResize() {
        if (window.innerWidth >= 1024) {
            // Desktop - sidebar always visible
            this.closeSidebar();
            if (this.mainContent) {
                this.mainContent.classList.add('shifted');
            }
        } else {
            // Mobile/tablet - sidebar hidden by default
            if (this.mainContent) {
                this.mainContent.classList.remove('shifted');
            }
        }
    }
    
    setActiveLink() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.nav-link');
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            const linkHref = link.getAttribute('href');
            
            if (linkHref && (linkHref === currentPath || 
                (currentPath === '/' && linkHref === '/'))) {
                link.classList.add('active');
            }
        });
    }
}

// Initialize navigation when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.navigation = new Navigation();
});

// Smooth scroll to top function
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Add scroll to top functionality
window.addEventListener('scroll', () => {
    const scrollButton = document.getElementById('scroll-to-top');
    if (scrollButton) {
        if (window.pageYOffset > 300) {
            scrollButton.style.display = 'block';
        } else {
            scrollButton.style.display = 'none';
        }
    }
});

// Export for use in other scripts
window.Navigation = Navigation;
// Search functionality
class SearchWidget {
    constructor() {
        this.searchInput = document.getElementById('search-input');
        this.searchForm = document.getElementById('search-form');
        this.searchResults = document.getElementById('search-results');
        this.debounceTimer = null;
        
        if (this.searchInput && this.searchForm) {
            this.init();
        }
    }
    
    init() {
        this.searchInput.addEventListener('input', (e) => {
            this.handleInput(e.target.value);
        });
        
        this.searchForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.performSearch(this.searchInput.value);
        });
        
        document.addEventListener('click', (e) => {
            if (!this.searchForm.contains(e.target)) {
                this.hideResults();
            }
        });
    }
    
    handleInput(query) {
        clearTimeout(this.debounceTimer);
        
        if (query.length < 2) {
            this.hideResults();
            return;
        }
        
        this.debounceTimer = setTimeout(() => {
            this.performSearch(query);
        }, 300);
    }
    
    async performSearch(query) {
        if (!query || query.length < 2) {
            this.hideResults();
            return;
        }
        
        try {
            const response = await fetch(`/api/phrases/search?q=${encodeURIComponent(query)}&limit=5`);
            if (!response.ok) throw new Error('Search failed');
            
            const data = await response.json();
            this.displayResults(data.phrases);
        } catch (error) {
            console.error('Search error:', error);
            this.searchResults.innerHTML = '<div class="search-error">Ошибка поиска</div>';
            this.searchResults.style.display = 'block';
        }
    }
    
    displayResults(phrases) {
        if (!phrases || phrases.length === 0) {
            this.searchResults.innerHTML = '<div class="search-no-results">Ничего не найдено</div>';
            this.searchResults.style.display = 'block';
            return;
        }
        
        const html = phrases.map(phrase => `
            <div class="search-result-item" data-phrase="${phrase.phrase}">
                <div class="search-result-phrase">${phrase.phrase}</div>
                <div class="search-result-meaning">${Array.isArray(phrase.meanings) && phrase.meanings.length > 0 ? phrase.meanings[0] : 'Значение не указано'}</div>
            </div>
        `).join('');
        
        this.searchResults.innerHTML = html;
        this.searchResults.style.display = 'block';
        
        this.searchResults.querySelectorAll('.search-result-item').forEach(item => {
            item.addEventListener('click', () => {
                this.searchInput.value = item.dataset.phrase;
                this.hideResults();
            });
        });
    }
    
    hideResults() {
        this.searchResults.style.display = 'none';
    }
}

// Initialize search widget when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.searchWidget = new SearchWidget();
});
