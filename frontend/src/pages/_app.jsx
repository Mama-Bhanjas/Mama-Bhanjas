import '../styles/globals.css';
import '@mysten/dapp-kit/dist/index.css';
import { createNetworkConfig, SuiClientProvider, WalletProvider } from '@mysten/dapp-kit';
import { getFullnodeUrl } from '@mysten/sui/client';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { SuiWalletProvider } from '../context/SuiWalletContext';
import { AppProvider } from '../context/AppContext';
import { ThemeProvider } from '../context/ThemeContext';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { AnimatePresence, motion } from 'framer-motion';
import { Outfit } from 'next/font/google';

const outfit = Outfit({
  subsets: ['latin'],
  variable: '--font-outfit',
});

// Config options for the networks you want to connect to
const { networkConfig } = createNetworkConfig({
	testnet: { url: getFullnodeUrl('testnet') },
	mainnet: { url: getFullnodeUrl('mainnet') },
});

const queryClient = new QueryClient();

function MyApp({ Component, pageProps, router }) {
  return (
    <QueryClientProvider client={queryClient}>
        <SuiClientProvider networks={networkConfig} defaultNetwork="testnet">
            <WalletProvider>
                <SuiWalletProvider>
                    <AppProvider>
                        <ThemeProvider>
                            <div className={`flex flex-col min-h-screen bg-surface-50 text-surface-900 ${outfit.variable} font-sans transition-colors duration-300 dark:bg-surface-950 dark:text-white`}>
                                <Navbar />
                                <AnimatePresence mode="wait">
                                <motion.main
                                    key={router.route}
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    exit={{ opacity: 0, y: -10 }}
                                    transition={{ duration: 0.3 }}
                                    className="flex-grow pt-20" // Padding top to account for fixed navbar
                                >
                                    <Component {...pageProps} />
                                </motion.main>
                                </AnimatePresence>
                                <Footer />
                            </div>
                        </ThemeProvider>
                    </AppProvider>
                </SuiWalletProvider>
            </WalletProvider>
        </SuiClientProvider>
    </QueryClientProvider>
  );
}

export default MyApp;
