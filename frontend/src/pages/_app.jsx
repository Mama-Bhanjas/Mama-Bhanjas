import '../styles/globals.css';
import '@mysten/dapp-kit/dist/index.css';
import { SuiWalletProvider } from '../context/SuiWalletContext';
import { AppProvider } from '../context/AppContext';
import { ThemeProvider } from '../context/ThemeContext';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { AnimatePresence, motion } from 'framer-motion';
import { Outfit } from 'next/font/google';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { SuiClientProvider, WalletProvider } from '@mysten/dapp-kit';
import { getFullnodeUrl } from '@mysten/sui.js/client';

const outfit = Outfit({
  subsets: ['latin'],
  variable: '--font-outfit',
});

// Create a client for React Query
const queryClient = new QueryClient();

// Configure Sui network
const networks = {
  testnet: { url: getFullnodeUrl('testnet') },
  mainnet: { url: getFullnodeUrl('mainnet') },
  devnet: { url: getFullnodeUrl('devnet') },
};

function MyApp({ Component, pageProps, router }) {
  return (
    <QueryClientProvider client={queryClient}>
      <SuiClientProvider networks={networks} defaultNetwork="testnet">
        <WalletProvider autoConnect>
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
