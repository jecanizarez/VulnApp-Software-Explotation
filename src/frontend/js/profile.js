// Profile functionality
class Profile {
    constructor() {
        this.apiBase = 'http://localhost:8000';
    }

    async loadProfile() {
        const profileContent = document.getElementById('profile-content');
        const user = app.currentUser;

        if (!user) {
            profileContent.innerHTML = '<div class="message error">You must be logged in to view your profile.</div>';
            return;
        }

        try {
            // Fetch fresh data from backend using /users/{id}
            const response = await fetch(`${this.apiBase}/users/${user.id}`);
            if (response.ok) {
                const data = await response.json();
                const u = Array.isArray(data.user) ? data.user[0] : data.user; // backend returns list sometimes
                profileContent.innerHTML = `
                    <div class="profile-card">
                        <h3>${u.username}</h3>
                        <p>Email: ${this.escapeHtml(u.email)}</p>
                        <p>User ID: ${u.id}</p>
                        <p>Member since: ${new Date(u.created_at).toLocaleString()}</p>
                    </div>
                `;
            } else if (response.status === 404) {
                profileContent.innerHTML = '<div class="message error">User not found.</div>';
            } else {
                profileContent.innerHTML = '<div class="message error">Failed to load profile.</div>';
            }
        } catch (error) {
            profileContent.innerHTML = `<div class=\"message error\">Network error: ${error.message}</div>`;
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

// Initialize profile
const profile = new Profile();

