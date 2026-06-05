document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const message = document.getElementById('message');

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        });

        let data = {};
        try {
            data = await response.json();
        } catch (parseError) {
            message.textContent = 'Server returned an invalid response';
            message.className = 'error';
            return;
        }

        if (response.ok) {
            message.textContent = 'Login successful!';
            message.className = 'success';
            localStorage.setItem('user', JSON.stringify(data.user));
            setTimeout(() => {
                window.location.href = '/dashboard';
            }, 1000);
        } else {
            message.textContent = data.error || 'Login failed';
            message.className = 'error';
        }
    } catch (error) {
        message.textContent = 'Cannot reach server. Check your internet or Render deployment.';
        message.className = 'error';
    }
});
