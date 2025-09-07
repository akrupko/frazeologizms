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
        const currentPage = window.location.pathname.split('/').pop() || 'index.html';
        const navLinks = document.querySelectorAll('.nav-link');
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            const linkHref = link.getAttribute('href');
            
            if (linkHref === currentPage || 
                (currentPage === '' && linkHref === 'index.html')) {
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