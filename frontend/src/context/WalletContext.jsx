import React, { createContext, useContext, useState } from 'react';

const WalletContext = createContext();

export function WalletProvider({ children }) {
    const [account, setAccount] = useState(null);

    const connectWallet = async () => {
        // Placeholder for wallet connection logic
        console.log("Connecting wallet...");
        // Simulated connection
        setAccount("0x123...abc");
    };

    const disconnectWallet = () => {
        setAccount(null);
    };

    return (
        <WalletContext.Provider value={{ account, connectWallet, disconnectWallet }}>
            {children}
        </WalletContext.Provider>
    );
}

export function useWallet() {
    return useContext(WalletContext);
}
