/**
 * Global App Logic for TrustBridge
 */

// Toast Notification System
function showToast(message, type = 'success') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = 'toast';

  if (type === 'error') {
    toast.style.borderLeftColor = '#F44336';
  } else if (type === 'warning') {
    toast.style.borderLeftColor = '#FF9800';
  }

  toast.textContent = message;
  container.appendChild(toast);

  // Remove toast after 3 seconds
  setTimeout(() => {
    toast.classList.add('hiding');
    toast.addEventListener('animationend', () => {
      toast.remove();
    });
  }, 3000);
}

// Authentication Check
function checkAuth(requiredRole = null) {
  const state = window.tbUtils.getAppState();

  // If not logged in and not on auth/index page, redirect to auth
  const currentPath = window.location.pathname;
  const isPublicPage = currentPath.endsWith('index.html') || currentPath.endsWith('auth.html') || currentPath === '/' || currentPath === '/trustbridge-frontend/';

  if (!state.userRole && !isPublicPage) {
    window.location.href = 'auth.html';
    return null;
  }

  // If logged in and on public page, redirect to dashboard
  if (state.userRole && isPublicPage) {
    window.location.href = `${state.userRole}-dashboard.html`;
    return state.userRole;
  }

  // If a specific role is required and it doesn't match, redirect to their actual dashboard
  if (requiredRole && state.userRole !== requiredRole) {
    window.location.href = `${state.userRole}-dashboard.html`;
    return null;
  }

  return state.userRole;
}

// Logout
function logout() {
  const state = window.tbUtils.getAppState();
  state.userRole = null;
  window.tbUtils.saveAppState(state);
  window.location.href = 'index.html';
}

// Setup common UI elements (like logout buttons)
document.addEventListener('DOMContentLoaded', () => {
  const logoutBtns = document.querySelectorAll('.logout-btn');
  logoutBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      logout();
    });
  });
});

window.tbApp = {
  showToast,
  checkAuth,
  logout
};
