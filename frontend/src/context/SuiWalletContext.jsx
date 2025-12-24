import React, { createContext, useContext } from 'react';
import { 
    useCurrentAccount, 
    useSignAndExecuteTransaction,
    useSuiClient 
} from '@mysten/dapp-kit';

const SuiWalletContext = createContext();

export function SuiWalletProvider({ children }) {
    const currentAccount = useCurrentAccount();
    const { mutateAsync: signAndExecuteTransaction } = useSignAndExecuteTransaction();
    const suiClient = useSuiClient();

    const value = {
        account: currentAccount?.address || null,
        currentAccount,
        signAndExecuteTransaction,
        suiClient,
        isConnected: !!currentAccount,
    };

    return (
        <SuiWalletContext.Provider value={value}>
            {children}
        </SuiWalletContext.Provider>
    );
}

export function useSuiWallet() {
    const context = useContext(SuiWalletContext);
    // If used outside provider, return default structure safely or logged warning
    if (!context) {
        console.warn('useSuiWallet used outside of SuiWalletProvider');
        return {
            account: null,
            currentAccount: null,
            signAndExecuteTransaction: async () => {},
            suiClient: null,
            isConnected: false,
        };
    }
    return context;
}
