// Check if user is authenticated
function checkAuth() {
    const user = localStorage.getItem('user');
    
    if (!user) {
        window.location.href = '/';
        return null;
    }
    
    return JSON.parse(user);
}

// Load user information
function loadUserInfo() {
    const user = checkAuth();
    
    if (user) {
        document.getElementById('userEmail').textContent = user.email;
        document.getElementById('userName').textContent = user.username;
    }
}

// Logout functionality
document.getElementById('logoutBtn').addEventListener('click', function() {
    localStorage.removeItem('user');
    window.location.href = '/';
});

// Initialize dashboard
loadUserInfo();
