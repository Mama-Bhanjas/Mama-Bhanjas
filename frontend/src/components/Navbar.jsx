import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { Menu, X, Shield, Activity, FileText, LogIn, LogOut, User } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useTheme } from '../context/ThemeContext';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
    const { theme } = useTheme();
    const { user, logout, isAuthenticated } = useAuth();
    const [isOpen, setIsOpen] = useState(false);
    const [scrolled, setScrolled] = useState(false);
    const [showLogoutModal, setShowLogoutModal] = useState(false);
    const router = useRouter();

    useEffect(() => {
        const handleScroll = () => {
            setScrolled(window.scrollY > 10);
        };
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    const navLinks = [
        { name: 'Dashboard', href: '/', icon: Activity },
        { name: 'Submit Report', href: '/submit', icon: FileText },
        { name: 'Verified News', href: '/verify', icon: Shield },
    ];

    const handleLogout = () => {
        logout();
        setShowLogoutModal(false);
        router.push('/');
    };

    return (
        <>
            <nav className={`fixed w-full z-50 transition-all duration-500 shadow-2xl font-[var(--font-roboto)] ${scrolled
                ? 'bg-white/80 dark:bg-surface-950/80 backdrop-blur-md border-b border-gray-200 dark:border-surface-d800'
                : 'bg-transparent'
                }`} style={{ fontFamily: 'var(--font-roboto), Roboto, ui-sans-serif, system-ui, sans-serif' }}>
                <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between h-16 items-center">
                        <div className="flex items-center">
                            <Link href="/" className="flex-shrink-0 flex items-center space-x-2">
                                <div className="p-1 rounded-lg">
                                    <img src="/branding/logo.png" alt="D-Brief Logo" className="h-8 w-8 object-contain" />
                                </div>
                                <span className="text-xl font-sans font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary-600 to-indigo-600">
                                    D-Brief
                                </span>
                            </Link>
                            <div className="hidden md:ml-10 md:flex md:space-x-8">
                                {navLinks.map((link) => {
                                    const isActive = router.pathname === link.href;
                                    return (
                                        <Link
                                            key={link.name}
                                            href={link.href}
                                            className={`inline-flex items-center px-1 pt-1 text-sm font-medium transition-colors
                          ${isActive
                                                    ? 'text-primary-600 border-primary-600'
                                                    : 'text-surface-600 border-transparent hover:text-primary-600  dark:text-surface-400'
                                                }`}
                                        >
                                            {link.name}
                                        </Link>
                                    );
                                })}
                            </div>
                        </div>
                        <div className="hidden md:flex items-center space-x-4">
                            {isAuthenticated ? (
                                <div className="flex items-center space-x-3">
                                    <div className="flex items-center space-x-3 px-4 py-1.5 bg-surface-100 dark:bg-surface-900 rounded-2xl border border-gray-200 dark:border-surface-800 hover:border-primary-500/30 transition-all cursor-default group">
                                        <div className="relative h-8 w-8 rounded-xl bg-gradient-to-br from-primary-500 to-indigo-600 p-[1px] flex items-center justify-center overflow-hidden shadow-lg shadow-primary-500/10">
                                            <div className="absolute inset-0 bg-white dark:bg-surface-900 rounded-[10px]" />
                                            {user.avatar_url ? (
                                                <img src={user.avatar_url} alt={user.full_name} className="relative h-full w-full object-cover rounded-[10px]" />
                                            ) : (
                                                <User className="relative h-4 w-4 text-primary-600 dark:text-primary-400" />
                                            )}
                                        </div>
                                        <div className="flex flex-col">
                                            <span className="text-xs font-semibold text-gray-500 dark:text-surface-400 leading-none mb-0.5">Welcome,</span>
                                            <span className="text-sm font-bold text-gray-900 dark:text-white leading-none">
                                                {user.full_name}
                                            </span>
                                        </div>
                                    </div>
                                    <button
                                        onClick={() => setShowLogoutModal(true)}
                                        className="p-2.5 text-surface-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-950/20 rounded-xl transition-all group"
                                        title="Logout"
                                    >
                                        <LogOut className="h-5 w-5 group-hover:scale-110 transition-transform" />
                                    </button>
                                </div>
                            ) : (
                                <Link
                                    href="/login"
                                    className="inline-flex items-center px-6 py-2 border border-transparent text-sm font-bold rounded-xl text-white bg-primary-600 hover:bg-primary-700 shadow-lg shadow-primary-600/20 transition-all"
                                >
                                    <LogIn className="h-4 w-4 mr-2" />
                                    Sign In
                                </Link>
                            )}
                        </div>
                        <div className="flex items-center md:hidden">
                            <button
                                onClick={() => setIsOpen(!isOpen)}
                                className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 dark:hover:bg-surface-800 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500"
                            >
                                {isOpen ? <X className="block h-6 w-6" /> : <Menu className="block h-6 w-6" />}
                            </button>
                        </div>
                    </div>
                </div>

                {/* Mobile menu */}
                <AnimatePresence>
                    {isOpen && (
                        <motion.div
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: 'auto' }}
                            exit={{ opacity: 0, height: 0 }}
                            className="md:hidden bg-white dark:bg-surface-950 border-t border-gray-200 dark:border-surface-800 overflow-hidden"
                        >
                            <div className="pt-2 pb-3 space-y-1">
                                {navLinks.map((link) => {
                                    const isActive = router.pathname === link.href;
                                    return (
                                        <Link
                                            key={link.name}
                                            href={link.href}
                                            className={`block pl-3 pr-4 py-2 border-l-4 text-base font-medium transition-colors
                            ${isActive
                                                    ? 'bg-primary-50 dark:bg-primary-900/20 border-primary-500 text-primary-700 dark:text-primary-400'
                                                    : 'border-transparent text-gray-500 dark:text-surface-400 hover:bg-gray-50 dark:hover:bg-surface-800 hover:border-gray-300 dark:hover:border-surface-600 hover:text-gray-700 dark:hover:text-white'
                                                }`}
                                            onClick={() => setIsOpen(false)}
                                        >
                                            <div className="flex items-center space-x-2">
                                                <link.icon className="h-4 w-4" />
                                                <span>{link.name}</span>
                                            </div>
                                        </Link>
                                    );
                                })}
                                <div className="px-4 py-3 border-t border-gray-100 dark:border-surface-800">
                                    {isAuthenticated ? (
                                        <button
                                            onClick={() => setShowLogoutModal(true)}
                                            className="w-full flex items-center justify-center px-4 py-2 border border-red-200 dark:border-red-900/30 text-red-600 dark:text-red-400 font-medium rounded-xl hover:bg-red-50 dark:hover:bg-red-900/10 transition-all"
                                        >
                                            <LogOut className="h-4 w-4 mr-2" />
                                            Sign Out
                                        </button>
                                    ) : (
                                        <Link
                                            href="/login"
                                            className="w-full flex items-center justify-center px-4 py-2 bg-primary-600 text-white font-bold rounded-xl hover:bg-primary-700 shadow-lg shadow-primary-600/20 transition-all"
                                            onClick={() => setIsOpen(false)}
                                        >
                                            <LogIn className="h-4 w-4 mr-2" />
                                            Sign In
                                        </Link>
                                    )}
                                </div>
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </nav>

            {/* Logout Confirmation Modal */}
            <AnimatePresence>
                {showLogoutModal && (
                    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            onClick={() => setShowLogoutModal(false)}
                            className="absolute inset-0 bg-black/60 backdrop-blur-sm"
                        />
                        <motion.div
                            initial={{ scale: 0.9, opacity: 0, y: 20 }}
                            animate={{ scale: 1, opacity: 1, y: 0 }}
                            exit={{ scale: 0.9, opacity: 0, y: 20 }}
                            className="relative bg-white dark:bg-surface-900 rounded-3xl p-8 max-w-sm w-full shadow-2xl border border-gray-200 dark:border-surface-800"
                        >
                            <div className="text-center">
                                <div className="mx-auto w-16 h-16 bg-red-100 dark:bg-red-900/20 rounded-full flex items-center justify-center mb-4">
                                    <LogOut className="w-8 h-8 text-red-600 dark:text-red-500" />
                                </div>
                                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Sign Out?</h3>
                                <p className="text-gray-500 dark:text-surface-400 mb-8">
                                    Are you sure you want to end your current session?
                                </p>
                                <div className="flex flex-col gap-3">
                                    <button
                                        onClick={handleLogout}
                                        className="w-full py-3 bg-red-600 hover:bg-red-700 text-white font-bold rounded-xl transition-all shadow-lg shadow-red-600/20"
                                    >
                                        Yes, Sign Out
                                    </button>
                                    <button
                                        onClick={() => setShowLogoutModal(false)}
                                        className="w-full py-3 bg-gray-100 dark:bg-surface-800 text-gray-700 dark:text-surface-300 font-bold rounded-xl hover:bg-gray-200 dark:hover:bg-surface-700 transition-all"
                                    >
                                        Cancel
                                    </button>
                                </div>
                            </div>
                        </motion.div>
                    </div>
                )}
            </AnimatePresence>
        </>
    );
}
