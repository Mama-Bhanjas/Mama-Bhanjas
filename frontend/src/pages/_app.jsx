import '../styles/globals.css';
import { WalletProvider } from '../context/WalletContext';
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

function MyApp({ Component, pageProps, router }) {
  return (
    <WalletProvider>
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
    </WalletProvider>
  );
}

export default MyApp;
