"use client";
import Link from 'next/link';
import { useWeb3 } from '../context/Web3Context';
import { ShieldAlert } from 'lucide-react';

export default function Navbar() {
  const { account, connectWallet } = useWeb3();

  return (
    <nav className="border-b border-gray-200 dark:border-gray-800 bg-white/50 dark:bg-black/50 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center gap-2">
            <ShieldAlert className="w-8 h-8 text-red-600" />
            <span className="font-bold text-xl tracking-tight">TrustResQ</span>
          </div>
          
          <div className="flex gap-4 items-center">
            <Link href="/" className="text-sm font-medium hover:text-red-600 transition-colors">
              Dashboard
            </Link>
            <Link href="/submit" className="text-sm font-medium hover:text-red-600 transition-colors">
              Submit Report
            </Link>
            
            <button
              onClick={connectWallet}
              className={`relative overflow-hidden group px-6 py-2.5 rounded-full font-semibold text-sm transition-all duration-300 transform hover:scale-105 active:scale-95 shadow-lg ${
                account 
                  ? "bg-gradient-to-r from-emerald-500 to-teal-500 text-white shadow-emerald-500/20 border border-emerald-400/20"
                  : "bg-gradient-to-r from-violet-600 to-indigo-600 text-white shadow-indigo-500/20 hover:shadow-indigo-500/40"
              }`}
            >
              <span className="relative z-10 flex items-center gap-2">
                {account ? (
                  <>
                    <div className="w-2 h-2 rounded-full bg-white animate-pulse" />
                    {account.slice(0, 6)}...{account.slice(-4)}
                  </>
                ) : (
                  <>Connect Wallet</>
                )}
              </span>
              <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300 ease-out" />
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}
