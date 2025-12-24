import React, { createContext, useContext, useState } from 'react';

const AppContext = createContext();

export function AppProvider({ children }) {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    return (
        <AppContext.Provider value={{ loading, setLoading, error, setError }}>
            {children}
        </AppContext.Provider>
    );
}

export function useApp() {
    return useContext(AppContext);
}
