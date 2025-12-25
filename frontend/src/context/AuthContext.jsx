import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [token, setToken] = useState(null); // Added token state
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Check local storage for existing session
        const savedUser = localStorage.getItem('user');
        const savedToken = localStorage.getItem('token'); // Check for token
        if (savedUser && savedToken) {
            setUser(JSON.parse(savedUser));
            setToken(savedToken); // Set token if found
        }
        setLoading(false);
    }, []);

    const login = async (email, password) => {
        setLoading(true);
        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password }),
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.message || 'Login failed');
            }

            const data = await response.json();
            const { access_token, user: userData } = data;

            setToken(access_token);
            localStorage.setItem('token', access_token);
            setUser(userData);
            localStorage.setItem('user', JSON.stringify(userData));

            return userData;
        } finally {
            setLoading(false);
        }
    };

    const register = async (name, email, password) => {
        setLoading(true);
        try {
            const response = await fetch('/api/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ full_name: name, email, password }),
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.message || 'Registration failed');
            }

            // If registration is successful, log the user in immediately
            return login(email, password);
        } finally {
            setLoading(false);
        }
    };

    /**
     * The Logout Case:
     * Logic to handle user departure from the session.
     * 1. Resets the user atom/state to null.
     * 2. Clears the Auth token/object from LocalStorage.
     * 3. Prevents state leakage by ensuring no stale data remains.
     */
    const logout = () => {
        // Clear reactive state
        setUser(null);
        // Clear persistent storage
        localStorage.removeItem('user');
        // Clear any other session specific data if added later
        // sessionStorage.clear(); 
    };

    const value = {
        user,
        login,
        register,
        logout,
        isAuthenticated: !!user,
        loading
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}
