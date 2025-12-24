import React from 'react';
import { ConnectButton } from '@mysten/dapp-kit';
import { useSuiWallet } from '../context/SuiWalletContext';
import { truncateAddress } from '../utils/truncateAddress';

export default function WalletConnect() {
    const { account, isConnected } = useSuiWallet();

    return (
        <div>
            {isConnected && account ? (
                <div className="flex items-center space-x-3 bg-surface-100 dark:bg-surface-800 px-4 py-2 rounded-full border border-surface-200 dark:border-surface-700">
                    <div className="h-2 w-2 bg-green-500 rounded-full animate-pulse"></div>
                    <span className="text-sm font-medium text-surface-700 dark:text-surface-300">
                        {truncateAddress(account)}
                    </span>
                    <ConnectButton />
                </div>
            ) : (
                <ConnectButton className="!px-6 !py-2.5 !text-sm !font-semibold !text-white !bg-primary-600 !rounded-full hover:!bg-primary-700 !transition-colors !shadow-sm hover:!shadow-md" />
            )}
        </div>
    );
}
