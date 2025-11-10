// Recipes functionality
class Recipes {
    constructor() {
        this.apiBase = 'http://localhost:8000';
        this.setupRecipeForms();
    }

    setupRecipeForms() {
        // New recipe form
        document.getElementById('new-recipe-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.createRecipe();
        });
    }

    async loadRecipes() {
        const token = localStorage.getItem('token');
        const recipesList = document.getElementById('recipes-list');

        if (!token) {
            recipesList.innerHTML = '<div class="message error">Please login to view recipes</div>';
            return;
        }

        try {
            const response = await fetch(`${this.apiBase}/recipes`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                this.displayRecipes(data.recipes);
            } else {
                recipesList.innerHTML = '<div class="message error">Failed to load recipes</div>';
            }
        } catch (error) {
            recipesList.innerHTML = `<div class="message error">Network error: ${error.message}</div>`;
        }
    }

    displayRecipes(recipes) {
        const recipesList = document.getElementById('recipes-list');
        
        if (!recipes || recipes.length === 0) {
            recipesList.innerHTML = '<div class="message">No recipes found</div>';
            return;
        }

        recipesList.innerHTML = recipes.map(recipe => `
            <div class="recipe-card">
                <div class="recipe-content">
                    <h3 class="recipe-title">${this.escapeHtml(recipe.title)}</h3>
                    <p class="recipe-author">By ${this.escapeHtml(recipe.author)}</p>
                    <p class="recipe-excerpt">${this.escapeHtml(recipe.content.substring(0, 100))}...</p>
                    <small>Created: ${new Date(recipe.created_at).toLocaleDateString()}</small>
                </div>
            </div>
        `).join('');
    }

    async createRecipe() {
    const title = document.getElementById('recipe-title').value;
    const content = document.getElementById('recipe-content').value;
    const token = localStorage.getItem('token');

    if (!token) {
        app.showMessage('Please login to create recipes', 'error');
        return;
    }

    try {
        const response = await fetch(`${this.apiBase}/recipes`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                title: title,
                content: content
            })
        });

        const data = await response.json();
        console.log('Create recipe response:', data);

        if (response.ok) {
            app.showMessage('Recipe created successfully!', 'success');
            document.getElementById('new-recipe-form').reset();
            app.hideCreateRecipeForm();
            this.loadRecipes(); // Refresh the recipes list
        } else {
            app.showMessage(data.error || 'Failed to create recipe', 'error');
        }
    } catch (error) {
        app.showMessage(`Network error: ${error.message}`, 'error');
    }
}
    escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
}

// Initialize recipes
const recipes = new Recipes();