document.getElementById('registerForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const username = document.getElementById('username').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const message = document.getElementById('message');

    message.textContent = '';
    message.className = '';

    if (!username || !email || !password) {
        message.textContent = 'All fields are required';
        message.className = 'error';
        return;
    }

    if (password !== confirmPassword) {
        message.textContent = 'Passwords do not match';
        message.className = 'error';
        return;
    }

    try {
        const response = await fetch('http://localhost:5000/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, email, password }),
        });

        const data = await response.json();

        if (response.ok) {
            message.textContent = 'Registration successful! Redirecting to login...';
            message.className = 'success';

            setTimeout(() => {
                window.location.href = '/';
            }, 1200);
        } else {
            message.textContent = data.error || 'Registration failed';
            message.className = 'error';
        }
    } catch (error) {
        message.textContent = 'Error connecting to server';
        message.className = 'error';
    }
});

