// Mock authentication service
const STORAGE_KEY = 'twinalai_auth';
const USERS_KEY = 'twinalai_users';

export const authService = {
  register: async (userData) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        const users = JSON.parse(localStorage.getItem(USERS_KEY) || '[]');
        
        // Check if user exists
        if (users.find(u => u.email === userData.email)) {
          resolve({ success: false, error: 'Email already registered' });
          return;
        }

        const newUser = {
          id: `user-${Date.now()}`,
          ...userData,
          createdAt: new Date().toISOString(),
        };

        users.push(newUser);
        localStorage.setItem(USERS_KEY, JSON.stringify(users));
        
        // Auto-login after registration
        localStorage.setItem(STORAGE_KEY, JSON.stringify({
          user: newUser,
          token: `token-${Date.now()}`,
          loginAt: new Date().toISOString(),
        }));

        resolve({ success: true, user: newUser });
      }, 1500); // Simulate network delay
    });
  },

  login: async (email, password, rememberMe) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        const users = JSON.parse(localStorage.getItem(USERS_KEY) || '[]');
        const user = users.find(u => u.email === email && u.password === password);

        if (!user) {
          resolve({ success: false, error: 'Invalid email or password' });
          return;
        }

        const authData = {
          user: user,
          token: `token-${Date.now()}`,
          loginAt: new Date().toISOString(),
          rememberMe: rememberMe,
        };

        localStorage.setItem(STORAGE_KEY, JSON.stringify(authData));
        resolve({ success: true, user: user });
      }, 1000);
    });
  },

  logout: () => {
    localStorage.removeItem(STORAGE_KEY);
  },

  getCurrentUser: () => {
    const auth = localStorage.getItem(STORAGE_KEY);
    return auth ? JSON.parse(auth).user : null;
  },

  isAuthenticated: () => {
    const auth = localStorage.getItem(STORAGE_KEY);
    return !!auth;
  },

  forgotPassword: async (email) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        const users = JSON.parse(localStorage.getItem(USERS_KEY) || '[]');
        const user = users.find(u => u.email === email);
        
        if (!user) {
          resolve({ success: false, error: 'Email not found' });
          return;
        }

        // In real app, send reset email
        resolve({ 
          success: true, 
          message: 'Password reset link sent to ' + email 
        });
      }, 1000);
    });
  },
};
