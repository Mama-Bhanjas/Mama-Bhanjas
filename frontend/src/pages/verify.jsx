import React, { useState } from 'react';
import Head from 'next/head';
import { motion, AnimatePresence } from 'framer-motion';
import {
    ShieldCheck,
    Search,
    Filter,
    X, ExternalLink, Calendar, User, Navigation, MapPin, Clock
} from 'lucide-react';
import { CATEGORIES } from '../constants/categories';
import NewsCard from '../components/NewsCard';
import newsData from '../data/news.json';

export default function Verify() {
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedCategory, setSelectedCategory] = useState('all');
    const [selectedArticle, setSelectedArticle] = useState(null);

    const filteredNews = newsData.filter(item => {
        const matchesSearch = item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
            item.location.toLowerCase().includes(searchQuery.toLowerCase());
        const matchesCategory = selectedCategory === 'all' || item.type === selectedCategory;
        return matchesSearch && matchesCategory;
    });

    return (
        <div className="min-h-screen pb-20">
            <Head>
                <title>Verified News - Mama-Bhanjas</title>
            </Head>

            {/* Header Section */}
            <div className="bg-gradient-to-b from-primary-900/20 to-transparent pt-12 pb-8">
                <div className="container mx-auto px-4 text-center">
                    <motion.div
                        initial={{ opacity: 0, y: -20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="inline-flex items-center space-x-2 px-4 py-2 bg-primary-500/10 border border-primary-500/20 rounded-full text-primary-400 text-sm font-medium mb-4"
                    >
                        <ShieldCheck className="h-4 w-4" />
                        <span>Community Authenticated Reports</span>
                    </motion.div>
                    <h1 className="text-4xl md:text-5xl font-bold text-white mb-4 tracking-tight">Verified News Feed</h1>
                    <p className="text-surface-400 max-w-2xl mx-auto text-lg">
                        Stay informed with real-time, verified incident reports from across the nation. All news is authenticated by our community members and verification algorithms.
                    </p>
                </div>
            </div>

            {/* Filter Bar */}
            <div className="container mx-auto px-4 mb-12">
                <div className="flex flex-col md:flex-row gap-4 justify-center items-center">
                    <div className="relative w-full max-w-md">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-surface-500" />
                        <input
                            type="text"
                            placeholder="Search by location or headline..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            className="w-full pl-10 pr-4 py-3 bg-surface-900 border border-surface-800 rounded-xl text-white focus:ring-2 focus:ring-primary-500 outline-none transition-all"
                        />
                    </div>
                    <div className="flex items-center space-x-2 overflow-x-auto pb-2 md:pb-0 w-full md:w-auto">
                        <Filter className="h-5 w-5 text-surface-500 mr-2 flex-shrink-0" />
                        <button
                            onClick={() => setSelectedCategory('all')}
                            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all whitespace-nowrap ${selectedCategory === 'all'
                                ? 'bg-primary-600 text-white shadow-lg shadow-primary-600/20'
                                : 'bg-surface-900 text-surface-400 border border-surface-800 hover:border-surface-600'
                                }`}
                        >
                            All Types
                        </button>
                        {CATEGORIES.map((cat) => (
                            <button
                                key={cat.id}
                                onClick={() => setSelectedCategory(cat.id)}
                                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all whitespace-nowrap ${selectedCategory === cat.id
                                    ? 'bg-primary-600 text-white shadow-lg shadow-primary-600/20'
                                    : 'bg-surface-900 text-surface-400 border border-surface-800 hover:border-surface-600'
                                    }`}
                            >
                                {cat.label}
                            </button>
                        ))}
                    </div>
                </div>
            </div>

            {/* News Feed */}
            <div className="container mx-auto px-4">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-6 max-w-6xl mx-auto">
                    {filteredNews.map((news) => (
                        <NewsCard
                            key={news.id}
                            article={news}
                            onViewDetails={(article) => setSelectedArticle(article)}
                        />
                    ))}
                </div>

                {filteredNews.length === 0 && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="text-center py-20"
                    >
                        <div className="inline-flex items-center justify-center p-4 bg-surface-900 rounded-full mb-4">
                            <Search className="h-8 w-8 text-surface-700" />
                        </div>
                        <h3 className="text-xl font-medium text-white">No verified news found</h3>
                        <p className="text-surface-500">Try adjusting your filters or search terms.</p>
                    </motion.div>
                )}
            </div>

            {/* Article Modal */}
            <AnimatePresence>
                {selectedArticle && (
                    <>
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            transition={{ duration: 0.2 }}
                            onClick={() => setSelectedArticle(null)}
                            className="fixed inset-0 bg-black/80 z-[60] cursor-pointer"
                        />
                        <motion.div
                            initial={{ opacity: 0, scale: 0.95, y: 10 }}
                            animate={{ opacity: 1, scale: 1, y: 0 }}
                            exit={{ opacity: 0, scale: 0.95, y: 10 }}
                            transition={{ type: 'spring', duration: 0.3, bounce: 0 }}
                            className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-3xl max-h-[90vh] overflow-y-auto bg-surface-950 border border-surface-800 rounded-3xl z-[70] shadow-2xl"
                        >
                            <div className="sticky top-0 right-0 p-4 bg-surface-950/90 flex justify-end z-10">
                                <button
                                    onClick={() => setSelectedArticle(null)}
                                    className="p-2 bg-surface-900 hover:bg-surface-800 rounded-full text-surface-400 hover:text-white transition-colors"
                                >
                                    <X className="h-6 w-6" />
                                </button>
                            </div>

                            <div className="px-8 pb-12">
                                <div className="flex items-center space-x-2 mb-6">
                                    <div className="px-3 py-1 bg-primary-500/10 border border-primary-500/20 rounded-full text-primary-400 text-xs font-bold uppercase tracking-wider">
                                        {selectedArticle.type}
                                    </div>
                                    <div className="flex items-center space-x-1 px-3 py-1 bg-green-500/10 border border-green-500/20 rounded-full">
                                        <ShieldCheck className="h-3 w-3 text-green-500" />
                                        <span className="text-[10px] font-bold text-green-500 uppercase tracking-wider">Verified by Platform</span>
                                    </div>
                                </div>

                                <h2 className="text-3xl md:text-4xl font-bold text-white mb-6 leading-tight">
                                    {selectedArticle.title}
                                </h2>

                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8 py-6 border-y border-surface-800">
                                    <div className="space-y-4">
                                        <div className="flex items-center text-surface-400">
                                            <MapPin className="h-5 w-5 mr-3 text-primary-500" />
                                            <div>
                                                <p className="text-xs text-surface-600 font-medium uppercase">Location</p>
                                                <p className="text-sm text-white">{selectedArticle.location}</p>
                                            </div>
                                        </div>
                                        <div className="flex items-center text-surface-400">
                                            <Clock className="h-5 w-5 mr-3 text-primary-500" />
                                            <div>
                                                <p className="text-xs text-surface-600 font-medium uppercase">Reported</p>
                                                <p className="text-sm text-white">{selectedArticle.time}</p>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="space-y-4">
                                        <div className="flex items-center text-surface-400">
                                            <User className="h-5 w-5 mr-3 text-primary-500" />
                                            <div>
                                                <p className="text-xs text-surface-600 font-medium uppercase">Source</p>
                                                <p className="text-sm text-white">{selectedArticle.author}</p>
                                            </div>
                                        </div>
                                        <div className="flex items-center text-surface-400">
                                            <Navigation className="h-5 w-5 mr-3 text-primary-500" />
                                            <div>
                                                <p className="text-xs text-surface-600 font-medium uppercase">Coordinates</p>
                                                <p className="text-sm text-white font-mono">{selectedArticle.coordinates}</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div className="prose prose-invert max-w-none">
                                    <p className="text-lg text-white font-medium mb-6 leading-relaxed">
                                        {selectedArticle.description}
                                    </p>
                                    <div className="text-surface-400 leading-relaxed whitespace-pre-line bg-surface-900/30 p-6 rounded-2xl border border-surface-800">
                                        {selectedArticle.fullContent}
                                    </div>
                                </div>

                                <div className="mt-10 flex flex-wrap gap-4">
                                    <button className="px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white rounded-xl font-bold flex items-center shadow-lg shadow-primary-600/20 transition-all">
                                        <ExternalLink className="h-4 w-4 mr-2" />
                                        Support Response
                                    </button>
                                    <button className="px-6 py-3 bg-surface-900 hover:bg-surface-800 text-white rounded-xl font-bold border border-surface-800 transition-all">
                                        Share Report
                                    </button>
                                </div>
                            </div>
                        </motion.div>
                    </>
                )}
            </AnimatePresence>
        </div>
    );
}
