// Static Recipes functionality
class StaticRecipes {
    constructor() {
        this.apiBase = 'http://localhost:8000/recipes';
        this.files = [];
        this.setupEvents();
    }

    setupEvents() {
        const searchInput = document.getElementById('static-search-input');
        const clearBtn = document.getElementById('static-search-clear');
        if (searchInput) {
            searchInput.addEventListener('input', () => this.renderList());
        }
        if (clearBtn) {
            clearBtn.addEventListener('click', () => {
                searchInput.value = '';
                this.renderList();
            });
        }
    }

    async loadStaticRecipes() {
        const statusEl = document.getElementById('static-recipes-status');
        statusEl.style.display = 'none';
        try {
            const resp = await fetch(`${this.apiBase}/static/list`);
            if (!resp.ok) {
                statusEl.textContent = 'Failed to load static recipe list';
                statusEl.className = 'message error';
                statusEl.style.display = 'block';
                return;
            }
            const data = await resp.json();
            this.files = data.files || [];
            this.renderList();
        } catch (e) {
            statusEl.textContent = `Network error: ${e.message}`;
            statusEl.className = 'message error';
            statusEl.style.display = 'block';
        }
    }

    renderList() {
        const listEl = document.getElementById('static-recipes-list');
        const searchValue = document.getElementById('static-search-input').value.toLowerCase();
        const filtered = this.files.filter(f => f.toLowerCase().includes(searchValue));

        if (filtered.length === 0) {
            listEl.innerHTML = '<li class="message">No matching static recipes found.</li>';
            return;
        }

        listEl.innerHTML = filtered.map(file => {
            const safe = this.escapeHtml(file);
            const downloadUrl = `${this.apiBase}/static?file_name=${encodeURIComponent(file)}`;
            return `<li class="static-recipe-item">📄 ${safe} <a href="${downloadUrl}" class="btn-link" download target="_blank">Download</a></li>`;
        }).join('');
    }

    escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }
}

// Initialize
const staticRecipes = new StaticRecipes();

