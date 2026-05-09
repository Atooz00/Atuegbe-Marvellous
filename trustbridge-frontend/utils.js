/**
 * Utility functions for TrustBridge
 */

// Format number as Naira currency
function formatNaira(amount) {
  return new Intl.NumberFormat('en-NG', {
    style: 'currency',
    currency: 'NGN',
    minimumFractionDigits: 2
  }).format(amount);
}

// Calculate TrustBridge fee (1.5%, min 150, max 5000)
function calculateFee(amount) {
  let fee = amount * 0.015;
  if (fee < 150) return 150;
  if (fee > 5000) return 5000;
  return fee;
}

// State Management via localStorage
const STATE_KEY = 'trustbridge_state';

function getAppState() {
  const defaultState = {
    userRole: null, // 'buyer', 'seller', 'admin'
    transactions: [
      {
        id: 'TB-1001',
        title: 'MacBook Pro M2',
        price: 850000,
        status: 'created', // created, funded, shipped, delivered, completed, disputed
        buyer: 'Buyer123',
        seller: 'TechStore NG',
        createdAt: new Date().toISOString(),
        deliveredAt: null
      }
    ]
  };

  const stored = localStorage.getItem(STATE_KEY);
  if (stored) {
    return JSON.parse(stored);
  }

  // Initialize with default state if none exists
  saveAppState(defaultState);
  return defaultState;
}

function saveAppState(state) {
  localStorage.setItem(STATE_KEY, JSON.stringify(state));
}

function updateTransactionStatus(id, newStatus) {
  const state = getAppState();
  const tx = state.transactions.find(t => t.id === id);
  if (tx) {
    tx.status = newStatus;
    if (newStatus === 'delivered') {
      tx.deliveredAt = new Date().toISOString();
    }
    saveAppState(state);
    return true;
  }
  return false;
}

function getTransaction(id) {
  const state = getAppState();
  return state.transactions.find(t => t.id === id);
}

// Ensure the utilities are globally available
window.tbUtils = {
  formatNaira,
  calculateFee,
  getAppState,
  saveAppState,
  updateTransactionStatus,
  getTransaction
};
