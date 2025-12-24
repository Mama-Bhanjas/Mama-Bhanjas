import React, { useState } from 'react';
import Head from 'next/head';
import { useWallet } from '../context/WalletContext';
import { Loader2, ArrowRight } from 'lucide-react';
import { motion } from 'framer-motion';

export default function Connect() {
    const { account, connectWallet } = useWallet();
    const [isNewUser, setIsNewUser] = useState(false);
    const [isLoading, setIsLoading] = useState(false);

    // Form state
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        phone: '',
    });

    const handleConnect = async () => {
        setIsLoading(true);
        await connectWallet();
        setIsLoading(false);
        // Logic: Check if wallet exists in backend. If not, auto-switch to "Sign Up" mode
        // For now, we manually toggle or default to connected view
    };

    const handleRegister = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        // Simulate registration API call
        await new Promise(resolve => setTimeout(resolve, 1500));
        console.log("Registering user:", { ...formData, wallet: account });
        setIsLoading(false);
        // Redirect or show success
        alert("Registration successful!");
    };

    return (
        <div className="min-h-screen pt-24 pb-12 px-4 flex items-center justify-center">
            <Head>
                <title>Connect Wallet - Mama-Bhanjas</title>
            </Head>

            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="w-full max-w-md bg-white dark:bg-surface-800 rounded-2xl shadow-xl border border-gray-100 dark:border-surface-700 overflow-hidden"
            >
                <div className="p-8">
                    <div className="text-center mb-8">
                        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                            {account ? (isNewUser ? "Create Account" : "Welcome Back") : "Connect Wallet"}
                        </h2>
                        <p className="text-gray-500 dark:text-surface-400 text-sm">
                            {account
                                ? "Complete your profile to continue"
                                : "Access the platform securely with your wallet"}
                        </p>
                    </div>

                    {!account ? (
                        <div className="space-y-4">
                            <button
                                onClick={handleConnect}
                                disabled={isLoading}
                                className="w-full py-3.5 px-4 bg-primary-600 hover:bg-primary-700 text-white font-semibold rounded-xl transition-all shadow-lg hover:shadow-primary-500/30 flex items-center justify-center space-x-2"
                            >
                                {isLoading ? <Loader2 className="animate-spin h-5 w-5" /> : null}
                                <span>Connect with Metamask</span>
                            </button>
                            <p className="text-xs text-center text-gray-400 dark:text-surface-500 mt-4">
                                By connecting, you agree to our Terms of Service
                            </p>
                        </div>
                    ) : (
                        <div>
                            {/* Toggle for Demo Purposes showing simplified flow */}
                            <div className="flex justify-center mb-6 bg-gray-100 dark:bg-surface-700 p-1 rounded-lg">
                                <button
                                    onClick={() => setIsNewUser(false)}
                                    className={`flex-1 py-1.5 text-sm font-medium rounded-md transition-all ${!isNewUser ? 'bg-white dark:bg-surface-600 text-gray-900 dark:text-white shadow-sm' : 'text-gray-500 dark:text-surface-400'}`}
                                >
                                    Login
                                </button>
                                <button
                                    onClick={() => setIsNewUser(true)}
                                    className={`flex-1 py-1.5 text-sm font-medium rounded-md transition-all ${isNewUser ? 'bg-white dark:bg-surface-600 text-gray-900 dark:text-white shadow-sm' : 'text-gray-500 dark:text-surface-400'}`}
                                >
                                    Sign Up
                                </button>
                            </div>

                            {isNewUser ? (
                                <form onSubmit={handleRegister} className="space-y-4">
                                    <div>
                                        <label className="block text-xs font-semibold text-gray-500 dark:text-surface-400 uppercase mb-1">Full Name</label>
                                        <input
                                            type="text"
                                            required
                                            className="w-full p-3 bg-gray-50 dark:bg-surface-900 border border-gray-200 dark:border-surface-700 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all dark:text-white"
                                            placeholder="John Doe"
                                            value={formData.name}
                                            onChange={e => setFormData({ ...formData, name: e.target.value })}
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-xs font-semibold text-gray-500 dark:text-surface-400 uppercase mb-1">Email</label>
                                        <input
                                            type="email"
                                            required
                                            className="w-full p-3 bg-gray-50 dark:bg-surface-900 border border-gray-200 dark:border-surface-700 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all dark:text-white"
                                            placeholder="john@example.com"
                                            value={formData.email}
                                            onChange={e => setFormData({ ...formData, email: e.target.value })}
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-xs font-semibold text-gray-500 dark:text-surface-400 uppercase mb-1">Phone</label>
                                        <input
                                            type="tel"
                                            required
                                            className="w-full p-3 bg-gray-50 dark:bg-surface-900 border border-gray-200 dark:border-surface-700 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all dark:text-white"
                                            placeholder="+1 234 567 890"
                                            value={formData.phone}
                                            onChange={e => setFormData({ ...formData, phone: e.target.value })}
                                        />
                                    </div>
                                    <div className="pt-2">
                                        <button
                                            type="submit"
                                            disabled={isLoading}
                                            className="w-full py-3 px-4 bg-primary-600 hover:bg-primary-700 text-white font-semibold rounded-lg transition-all shadow-lg hover:shadow-primary-500/30 flex items-center justify-center space-x-2"
                                        >
                                            {isLoading ? <Loader2 className="animate-spin h-5 w-5" /> : (
                                                <>
                                                    <span>Create Account</span>
                                                    <ArrowRight className="h-4 w-4" />
                                                </>
                                            )}
                                        </button>
                                    </div>
                                </form>
                            ) : (
                                <div className="text-center py-6">
                                    <div className="h-16 w-16 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
                                        <div className="h-3 w-3 bg-green-500 rounded-full animate-pulse shadow-[0_0_10px_rgba(34,197,94,0.5)]"></div>
                                    </div>
                                    <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-1">Wallet Connected</h3>
                                    <p className="text-sm text-gray-500 dark:text-surface-400 font-mono bg-gray-50 dark:bg-surface-900 py-2 px-3 rounded-md mb-6 inline-block border border-gray-200 dark:border-surface-700">
                                        {account}
                                    </p>
                                    <button className="w-full py-3 px-4 bg-gray-900 dark:bg-white text-white dark:text-surface-900 font-semibold rounded-lg hover:opacity-90 transition-all">
                                        Return to Dashboard
                                    </button>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </motion.div>
        </div>
    );
}
