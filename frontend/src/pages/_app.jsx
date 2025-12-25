import '../styles/globals.css';
import { AppProvider } from '../context/AppContext';
import { WalletProvider as LocalWalletProvider } from '../context/WalletContext';
import { ThemeProvider } from '../context/ThemeContext';
import { AuthProvider } from '../context/AuthContext';
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
        <AuthProvider>
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
                                className="flex-grow pt-20"
                            >
                                <Component {...pageProps} />
                            </motion.main>
                        </AnimatePresence>
                        <Footer />
                    </div>
                </ThemeProvider>
            </AppProvider>
        </AuthProvider>
    );
}

export default MyApp;
