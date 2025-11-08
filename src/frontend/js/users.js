// Users functionality
class Users {
    constructor() {
        this.apiBase = 'http://localhost:8000';
    }

    async loadUsers() {
        const usersList = document.getElementById('users-list');

        try {
            const response = await fetch(`${this.apiBase}/users`);
            
            if (response.ok) {
                const data = await response.json();
                this.displayUsers(data.users);
            } else {
                usersList.innerHTML = '<div class="message error">Failed to load users</div>';
            }
        } catch (error) {
            usersList.innerHTML = `<div class="message error">Network error: ${error.message}</div>`;
        }
    }

    displayUsers(users) {
        const usersList = document.getElementById('users-list');
        
        if (!users || users.length === 0) {
            usersList.innerHTML = '<div class="message">No users found</div>';
            return;
        }

        usersList.innerHTML = users.map(user => `
            <div class="user-card">
                <h3 class="user-username">${user.username}</h3>
                <p class="user-email">${this.escapeHtml(user.email)}</p>
                <small>Member since: ${new Date(user.created_at).toLocaleDateString()}</small>
            </div>
        `).join('');
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

// Initialize users
const users = new Users();