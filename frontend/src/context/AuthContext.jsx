import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Check local storage for existing session
        const savedUser = localStorage.getItem('user');
        if (savedUser) {
            setUser(JSON.parse(savedUser));
        }
        setLoading(false);
    }, []);

    const login = async (email, password) => {
        setLoading(true);
        // Mock login - in a real app, this would hit an API
        return new Promise((resolve) => {
            setTimeout(() => {
                const userData = {
                    id: '1',
                    name: 'Guest User',
                    email: email,
                    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Lucky'
                };
                setUser(userData);
                localStorage.setItem('user', JSON.stringify(userData));
                setLoading(false);
                resolve(userData);
            }, 1000);
        });
    };

    const register = async (name, email, password) => {
        setLoading(true);
        // Mock registration
        return new Promise((resolve) => {
            setTimeout(() => {
                const userData = {
                    id: Math.random().toString(36).substr(2, 9),
                    name: name,
                    email: email,
                    avatar: `https://api.dicebear.com/7.x/avataaars/svg?seed=${name}`
                };
                setUser(userData);
                localStorage.setItem('user', JSON.stringify(userData));
                setLoading(false);
                resolve(userData);
            }, 1000);
        });
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
