// Main application controller
class BakeApp {
    constructor() {
        this.currentUser = null;
        this.currentPage = 'home';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.checkAuthStatus();
        this.showPage('home');
    }

    setupEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const page = e.target.getAttribute('data-page');
                this.showPage(page);
            });
        });

        // Logout
        document.getElementById('logout-btn').addEventListener('click', () => {
            this.logout();
        });

        // Create recipe button
        document.getElementById('create-recipe-btn').addEventListener('click', () => {
            this.showCreateRecipeForm();
        });

        // Cancel create recipe
        document.getElementById('cancel-create').addEventListener('click', () => {
            this.hideCreateRecipeForm();
        });

        // Home page buttons
        document.querySelectorAll('[data-page]').forEach(btn => {
            if (btn.parentElement.classList.contains('hero') || btn.parentElement.classList.contains('feature-card')) {
                btn.addEventListener('click', (e) => {
                    e.preventDefault();
                    const page = btn.getAttribute('data-page');
                    this.showPage(page);
                });
            }
        });
    }

    showPage(pageName) {
        // Hide all pages
        document.querySelectorAll('.page').forEach(page => {
            page.classList.remove('active');
        });

        // Show selected page
        const targetPage = document.getElementById(`${pageName}-page`);
        if (targetPage) {
            targetPage.classList.add('active');
            this.currentPage = pageName;

            // Load page-specific content
            this.loadPageContent(pageName);
        }
    }

    loadPageContent(pageName) {
        switch (pageName) {
            case 'recipes':
                recipes.loadRecipes();
                break;
            case 'users':
                users.loadUsers();
                break;
            case 'profile':
                profile.loadProfile();
                break;
            case 'static-recipes':
                staticRecipes.loadStaticRecipes();
                break;
            case 'login':
                // Clear login form
                document.getElementById('login-form').reset();
                document.getElementById('login-message').innerHTML = '';
                break;
            case 'register':
                // Clear register form
                document.getElementById('register-form').reset();
                document.getElementById('register-message').innerHTML = '';
                break;
        }
    }

    showCreateRecipeForm() {
        document.getElementById('create-recipe-form').style.display = 'block';
        document.getElementById('create-recipe-btn').style.display = 'none';
    }

    hideCreateRecipeForm() {
        document.getElementById('create-recipe-form').style.display = 'none';
        document.getElementById('create-recipe-btn').style.display = 'block';
        document.getElementById('new-recipe-form').reset();
    }

    setUser(user) {
        this.currentUser = user;
        this.updateUI();
    }

    updateUI() {
        const authSection = document.getElementById('auth-section');
        const userSection = document.getElementById('user-section');
        const createRecipeBtn = document.getElementById('create-recipe-btn');
        const profileLink = document.getElementById('profile-link');

        if (this.currentUser) {
            authSection.style.display = 'none';
            userSection.style.display = 'flex';
            document.getElementById('user-greeting').textContent = `Hello, ${this.currentUser.username}`;
            if (createRecipeBtn) createRecipeBtn.style.display = 'block';
            if (profileLink) profileLink.style.display = 'inline-block';
        } else {
            authSection.style.display = 'flex';
            userSection.style.display = 'none';
            if (createRecipeBtn) createRecipeBtn.style.display = 'none';
            if (profileLink) profileLink.style.display = 'none';
        }
    }

    logout() {
        this.currentUser = null;
        localStorage.removeItem('token');
        this.updateUI();
        this.showPage('home');
        this.showMessage('Logged out successfully', 'success');
    }

    showMessage(message, type = 'info') {
        // Create a temporary message element
        const messageEl = document.createElement('div');
        messageEl.className = `message ${type}`;
        messageEl.textContent = message;
        
        // Add to current page
        const currentPage = document.querySelector('.page.active');
        currentPage.appendChild(messageEl);
        
        // Remove after 5 seconds
        setTimeout(() => {
            messageEl.remove();
        }, 5000);
    }

    checkAuthStatus() {
        const token = localStorage.getItem('token');
        if (token) {
            auth.getCurrentUser(token);
        }
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new BakeApp();
});