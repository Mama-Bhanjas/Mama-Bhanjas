import React from 'react';
import { ConnectButton } from '@mysten/dapp-kit';
import { useSuiWallet } from '../context/SuiWalletContext';
import { truncateAddress } from '../utils/truncateAddress';

export default function WalletConnect() {
    const { account, isConnected } = useSuiWallet();

    return (
        <div className="relative">
            <ConnectButton 
                connectText="Connect Wallet"
                className="!bg-primary-600 !text-white !font-medium !py-2 !px-4 !rounded-lg hover:!bg-primary-700 !transition-colors !border-none"
            />
            {/* We can add custom UI here if needed using the isConnected state */}
        </div>
    );
}
