import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import WalletConnect from './WalletConnect';
import { Menu, X, Shield, Activity, FileText } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

export default function Navbar() {
    const { theme, toggleTheme } = useTheme();
    const [isOpen, setIsOpen] = useState(false);
    const [scrolled, setScrolled] = useState(false);
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

    return (
        <nav className={`fixed w-full z-50 transition-all duration-500 shadow-2xl ${scrolled
            ? (theme === 'dark')
            : 'bg-transparent'
            }`}>
            <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-16 items-center">
                    <div className="flex items-center">
                        <Link href="/" className="flex-shrink-0 flex items-center space-x-2">
                            <div className="bg-primary-600 p-2 rounded-lg">
                                <Shield className="h-6 w-6 text-white" />
                            </div>
                            <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary-600 to-indigo-600">
                                Mama-Bhanjas
                            </span>
                        </Link>
                        <div className="hidden md:ml-10 md:flex md:space-x-8">
                            {navLinks.map((link) => {
                                const isActive = router.pathname === link.href;
                                return (
                                    <Link
                                        key={link.name}
                                        href={link.href}
                                        className={`inline-flex items-center px-1 pt-1 text-sm font-medium transition-colors border-b-2
                      ${isActive
                                                ? 'text-primary-600 border-primary-600'
                                                : 'text-surface-600 border-transparent hover:text-primary-600 hover:border-gray-300'
                                            }`}
                                    >
                                        {link.name}
                                    </Link>
                                );
                            })}
                        </div>
                    </div>
                    <div className="hidden md:flex items-center space-x-4">
                        <WalletConnect />
                    </div>
                    <div className="flex items-center md:hidden">
                        <button
                            onClick={() => setIsOpen(!isOpen)}
                            className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500"
                        >
                            {isOpen ? <X className="block h-6 w-6" /> : <Menu className="block h-6 w-6" />}
                        </button>
                    </div>
                </div>
            </div>

            {/* Mobile menu */}
            {isOpen && (
                <div className="md:hidden bg-white/95 dark:bg-surface-950/98 backdrop-blur-xl border-t border-gray-200 dark:border-surface-800">
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
                        <div className="px-4 py-3">
                            <WalletConnect />
                        </div>
                    </div>
                </div>
            )}
        </nav>
    );
}
