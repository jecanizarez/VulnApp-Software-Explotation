// Authentication functions
class Auth {
    constructor() {
        this.apiBase = 'http://localhost:8000';
        this.setupAuthForms();
    }

    setupAuthForms() {
        // Login form
        document.getElementById('login-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.login();
        });

        // Register form
        document.getElementById('register-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.register();
        });

        // Basic real-time sanitization for register inputs to mitigate XSS attempts
        ['register-username','register-email','register-password'].forEach(id => {
            const el = document.getElementById(id);
            if (el) {
                el.addEventListener('input', () => {
                    const original = el.value;
                    const sanitized = original.replace(/[<>]/g,'');
                    if (original !== sanitized) {
                        // show immediate warning about illegal characters
                        const warnEl = document.getElementById('register-message');
                        warnEl.innerHTML = '<div class="message error">Illegal character removed: &lt; or &gt; not allowed.</div>';
                        warnEl.style.display = 'block';
                        el.value = sanitized;
                    } else {
                        // Field-specific validation feedback
                        const warnEl = document.getElementById('register-message');
                        let err = null;
                        if (id === 'register-username') err = this.validateUsername(el.value.trim());
                        if (id === 'register-email') err = this.validateEmail(el.value.trim());
                        if (id === 'register-password') err = this.validatePassword(el.value);
                        if (err) {
                            warnEl.innerHTML = `<div class="message error">${err}</div>`;
                            warnEl.style.display = 'block';
                        } else if (!warnEl.innerHTML.includes('Registration successful')) {
                            // Clear only if not showing success message
                            warnEl.innerHTML = '';
                            warnEl.style.display = 'none';
                        }
                    }
                });
            }
        });
    }

    // ================= XSS / Input Validation Helpers =================
    validateUsername(username) {
        if (!username) return 'Username required';
        if (/[<>]/.test(username)) return 'Username contains invalid characters';
        if (!/^[A-Za-z0-9_\-]{3,30}$/.test(username)) return 'Username must be 3-30 chars (letters, numbers, _ or -)';
        if (/script/i.test(username)) return 'Username cannot contain script keyword';
        return null;
    }

    validateEmail(email) {
        if (!email) return 'Email required';
        if (/[<>]/.test(email)) return 'Email contains invalid characters';
        // Very basic email pattern
        if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return 'Invalid email format';
        return null;
    }

    validatePassword(password) {
        if (!password) return 'Password required';
        if (/[<>]/.test(password)) return 'Password contains invalid characters';
        if (password.length < 6) return 'Password must be at least 6 characters';
        return null;
    }

    async login() {
        const username = document.getElementById('login-username').value;
        const password = document.getElementById('login-password').value;
        const messageEl = document.getElementById('login-message');

        console.log('Attempting login with:', { username, password });

        try {
            const response = await fetch(`${this.apiBase}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            });

            console.log('Login response status:', response.status);
            
            const data = await response.json();
            console.log('Login response data:', data);

            if (response.ok) {
                console.log('Login successful, token:', data.access_token?.substring(0, 20) + '...');
                localStorage.setItem('token', data.access_token);
                app.setUser(data.user);
                app.showPage('recipes');
                app.showMessage('Login successful!', 'success');

            } else {
                console.log('Login failed:', data.error);
                messageEl.innerHTML = `<div class="message error">${data.error || 'Login failed'}</div>`;
            }
        } catch (error) {
            console.error('Network error during login:', error);
            messageEl.innerHTML = `<div class="message error">Network error: ${error.message}</div>`;
        }
    }


    async register() {
        const username = document.getElementById('register-username').value.trim();
        const email = document.getElementById('register-email').value.trim();
        const password = document.getElementById('register-password').value;
        const messageEl = document.getElementById('register-message');

        // Client-side validation to mitigate XSS payloads & invalid formats
        const errors = [];
        const uErr = this.validateUsername(username); if (uErr) errors.push(uErr);
        const eErr = this.validateEmail(email); if (eErr) errors.push(eErr);
        const pErr = this.validatePassword(password); if (pErr) errors.push(pErr);

        // Additional heuristic block for common XSS patterns
        const combined = `${username} ${email}`;
        if (/(onerror\s*=|onload\s*=|<script|javascript:|data:)/i.test(combined)) {
            errors.push('Potential XSS pattern detected in input');
        }

        if (errors.length > 0) {
            messageEl.innerHTML = `<div class="message error">${errors.join('<br>')}</div>`;
            return; // Do not submit
        }

        console.log('Attempting registration with (sanitized):', { username, email, passwordLength: password.length });

        try {
            const response = await fetch(`${this.apiBase}/users`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    email: email,
                    password: password
                })
            });

            console.log('Registration response status:', response.status);
            const data = await response.json();
            console.log('Registration response data:', data);

            if (response.ok) {
                messageEl.innerHTML = `<div class="message success">Registration successful! Welcome ${username}</div>`;
                document.getElementById('register-form').reset();
                setTimeout(() => {
                    app.showPage('login');
                }, 1500);
            } else {
                messageEl.innerHTML = `<div class="message error">${data.error || 'Registration failed'}</div>`;
            }
        } catch (error) {
            console.error('Network error during registration:', error);
            messageEl.innerHTML = `<div class="message error">Network error: ${error.message}</div>`;
        }
    }

    async getCurrentUser(token) {
        try {
            const response = await fetch(`${this.apiBase}/me`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                app.setUser(data.user);
            } else {
                // Token is invalid, remove it
                localStorage.removeItem('token');
            }
        } catch (error) {
            console.error('Error getting current user:', error);
            localStorage.removeItem('token');
        }
    }

    getAuthHeaders() {
        const token = localStorage.getItem('token');
        return token ? { 'Authorization': `Bearer ${token}` } : {};
    }
}

// Initialize auth
const auth = new Auth();