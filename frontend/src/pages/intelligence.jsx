import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import { motion, AnimatePresence } from 'framer-motion';
import { 
    Sparkles, 
    Search, 
    Filter, 
    X, 
    ArrowRight, 
    RefreshCcw,
    MapPin,
    Clock,
    ShieldCheck,
    Globe
} from 'lucide-react';
import { fetchRealtimeNews, triggerIntelligenceSync } from '../services/api';
import NewsCard from '../components/NewsCard';
import { CATEGORIES } from '../constants/categories';

export default function Intelligence() {
    const [news, setNews] = useState([]);
    const [loading, setLoading] = useState(true);
    const [syncing, setSyncing] = useState(false);
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedCategory, setSelectedCategory] = useState('all');
    const [selectedArticle, setSelectedArticle] = useState(null);
    const [lastUpdated, setLastUpdated] = useState(null);

    const handleManualSync = async () => {
        try {
            setSyncing(true);
            await triggerIntelligenceSync();
            await loadDailyIntelligence();
        } catch (error) {
            alert("Synchronization failed. Check if AI service is running.");
        } finally {
            setSyncing(false);
        }
    };

    const loadDailyIntelligence = async () => {
        try {
            setLoading(true);
            const response = await fetchRealtimeNews();
            if (response.success && response.data && response.data.news_intelligence) {
                const intelligenceData = response.data.news_intelligence.map((item, index) => ({
                    id: `intel-${index}`,
                    type: (item.disaster_type || item.primary_category || "news").toLowerCase(),
                    title: item.title,
                    description: item.summarization || item.summary,
                    fullContent: item.original_article || item.text,
                    location: item.location_entities?.[0] || item.location || "Nepal",
                    time: item.timestamp || "Recent",
                    author: item.source || "Global Monitoring",
                    verified: item.status && item.status.includes("Verified"),
                    confidence: item.verification?.confidence || 0.8,
                    status: item.status,
                    isNews: true
                }));
                setNews(intelligenceData);
                setLastUpdated(response.last_updated);
            }
        } catch (error) {
            console.error("Failed to load daily intelligence", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadDailyIntelligence();
    }, []);

    const filteredNews = news.filter(item => {
        const matchesSearch = item.title.toLowerCase().includes(searchQuery.toLowerCase()) || 
                             item.location.toLowerCase().includes(searchQuery.toLowerCase());
        const matchesCategory = selectedCategory === 'all' || item.type === selectedCategory;
        return matchesSearch && matchesCategory;
    });

    return (
        <div className="min-h-screen pb-20">
            <Head>
                <title>Daily Intelligence - D-Brief</title>
                <meta name="description" content="AI-driven daily disaster intelligence for Nepal" />
            </Head>

            {/* Premium Header */}
            <div className="relative overflow-hidden bg-surface-950 pt-32 pb-20">
                <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(99,102,241,0.1),transparent_50%)]" />
                <div className="absolute inset-0 bg-[radial-gradient(circle_at_bottom_left,rgba(79,70,229,0.05),transparent_50%)]" />
                
                <div className="container mx-auto px-4 relative z-10 text-center">
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="inline-flex items-center space-x-2 px-4 py-2 bg-primary-500/10 border border-primary-500/20 rounded-full text-primary-400 text-sm font-semibold mb-6"
                    >
                        <Sparkles className="h-4 w-4" />
                        <span>AI-Powered Global Disaster Monitoring</span>
                    </motion.div>
                    
                    <h1 className="text-4xl md:text-6xl font-black text-white mb-6 tracking-tight leading-tight">
                        Daily <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-400 to-indigo-400">Intelligence</span> Feed
                    </h1>
                    
                    <p className="text-surface-400 max-w-2xl mx-auto text-lg leading-relaxed mb-8">
                        Our multi-source fetcher scans global Satellites, BIPAD, ReliefWeb, and News Outlets every 24 hours. The reports below are automatically filtered for relevance to Nepal and disaster type.
                    </p>

                    <div className="flex items-center justify-center space-x-6 text-sm text-surface-500">
                        <div className="flex items-center">
                            <RefreshCcw className="h-4 w-4 mr-2" />
                            Refreshes every 24h
                        </div>
                        <div className="flex items-center">
                            <Globe className="h-4 w-4 mr-2" />
                            Nepal Coverage
                        </div>
                    </div>
                </div>
            </div>

            {/* Filter Section */}
            <div className="sticky top-16 z-30 bg-white/80 dark:bg-surface-950/80 backdrop-blur-md border-b border-gray-100 dark:border-surface-800 py-4 mb-12">
                <div className="container mx-auto px-4">
                    <div className="flex flex-col lg:flex-row gap-4 items-center justify-between">
                        <div className="relative w-full max-w-md">
                            <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-surface-500" />
                            <input 
                                type="text"
                                placeholder="Search the intelligence feed..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="w-full pl-12 pr-4 py-3 bg-white dark:bg-surface-900 border border-gray-200 dark:border-surface-800 rounded-2xl text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 outline-none transition-all shadow-sm"
                            />
                        </div>
                        
                        <div className="flex items-center space-x-2 overflow-x-auto pb-2 lg:pb-0 w-full lg:w-auto no-scrollbar">
                            <button
                                onClick={() => setSelectedCategory('all')}
                                className={`px-5 py-2.5 rounded-xl text-sm font-bold transition-all whitespace-nowrap ${
                                    selectedCategory === 'all'
                                    ? 'bg-primary-600 text-white shadow-lg shadow-primary-600/20'
                                    : 'bg-surface-100 dark:bg-surface-900 text-surface-600 dark:text-surface-400 border border-transparent'
                                }`}
                            >
                                All Intel
                            </button>
                            {CATEGORIES.map(cat => (
                                <button
                                    key={cat.id}
                                    onClick={() => setSelectedCategory(cat.id)}
                                    className={`px-5 py-2.5 rounded-xl text-sm font-bold transition-all whitespace-nowrap ${
                                        selectedCategory === cat.id
                                        ? 'bg-primary-600 text-white shadow-lg shadow-primary-600/20'
                                        : 'bg-surface-100 dark:bg-surface-900 text-surface-600 dark:text-surface-400 border border-transparent hover:bg-gray-200 dark:hover:bg-surface-800'
                                    }`}
                                >
                                    {cat.label}
                                </button>
                            ))}
                        </div>
                    </div>
                </div>
            </div>

            {/* Content Feed */}
            <div className="container mx-auto px-4">
                {loading ? (
                    <div className="py-20 flex flex-col items-center justify-center space-y-4">
                        <RefreshCcw className="h-10 w-10 text-primary-500 animate-spin" />
                        <p className="text-surface-400 font-bold tracking-widest uppercase text-xs">Synchronizing intelligence nodes...</p>
                    </div>
                ) : (
                    <div className="max-w-6xl mx-auto">
                        <div className="flex justify-between items-center mb-10">
                            <h2 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center">
                                Recent Findings
                                <span className="ml-3 px-2 py-1 bg-surface-100 dark:bg-surface-900 text-surface-500 text-xs rounded-lg font-mono">
                                    {filteredNews.length} Reports
                                </span>
                            </h2>
                            {lastUpdated && (
                                <p className="text-xs text-surface-500">
                                    Last Sync: {new Date(lastUpdated).toLocaleString()}
                                </p>
                            )}
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                            <AnimatePresence mode="popLayout">
                                {filteredNews.map((item, idx) => (
                                    <motion.div 
                                        key={item.id}
                                        layout
                                        initial={{ opacity: 0, y: 20 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        exit={{ opacity: 0, scale: 0.95 }}
                                        transition={{ duration: 0.3, delay: idx * 0.05 }}
                                    >
                                        <NewsCard 
                                            article={item} 
                                            onViewDetails={(art) => setSelectedArticle(art)}
                                        />
                                    </motion.div>
                                ))}
                            </AnimatePresence>
                        </div>

                        {filteredNews.length === 0 && (
                            <div className="py-40 text-center">
                                <div className="inline-flex items-center justify-center w-20 h-20 bg-surface-100 dark:bg-surface-900 rounded-full mb-6">
                                    <Search className="h-8 w-8 text-surface-400" />
                                </div>
                                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">No intelligence data yet</h3>
                                <p className="text-surface-500">The daily fetch cycle might still be in progress, or no disaster news was found today.</p>
                                <button 
                                    onClick={handleManualSync}
                                    disabled={syncing}
                                    className="mt-8 px-8 py-3 bg-primary-600 text-white rounded-xl font-bold hover:bg-primary-700 transition-all shadow-lg shadow-primary-600/20 disabled:opacity-50 flex items-center mx-auto"
                                >
                                    {syncing ? (
                                        <>
                                            <RefreshCcw className="animate-spin h-5 w-5 mr-2" />
                                            Synchronizing...
                                        </>
                                    ) : "Force Synchronize Now"}
                                </button>
                            </div>
                        )}
                    </div>
                )}
            </div>

            {/* Modern Article Detail Modal (Reuse design but tailored) */}
            <AnimatePresence>
                {selectedArticle && (
                    <>
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            onClick={() => setSelectedArticle(null)}
                            className="fixed inset-0 bg-black/90 backdrop-blur-sm z-[60] cursor-pointer"
                        />
                        <motion.div
                            initial={{ opacity: 0, x: '100%' }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: '100%' }}
                            transition={{ type: 'spring', damping: 30, stiffness: 200 }}
                            className="fixed right-0 top-0 h-full w-full max-w-2xl bg-white dark:bg-surface-950 z-[70] shadow-2xl overflow-y-auto"
                        >
                            <div className="sticky top-0 p-6 bg-white/80 dark:bg-surface-950/80 backdrop-blur-md flex justify-between items-center border-b border-gray-100 dark:border-surface-800 z-10">
                                <div className="flex items-center space-x-3">
                                    <div className="p-2 bg-primary-500/10 rounded-lg">
                                        <ShieldCheck className="h-5 w-5 text-primary-500" />
                                    </div>
                                    <span className="font-bold text-gray-900 dark:text-white tracking-tight uppercase text-sm">Verified Intelligence</span>
                                </div>
                                <button onClick={() => setSelectedArticle(null)} className="p-2 hover:bg-gray-100 dark:hover:bg-surface-800 rounded-full transition-colors">
                                    <X className="h-6 w-6 text-surface-500" />
                                </button>
                            </div>

                            <div className="p-8 md:p-12">
                                <div className="flex flex-wrap gap-2 mb-8">
                                    <span className="px-3 py-1 bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400 text-xs font-bold rounded-full uppercase">
                                        {selectedArticle.type}
                                    </span>
                                    <span className="px-3 py-1 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 text-xs font-bold rounded-full uppercase">
                                        Confidence: {(selectedArticle.confidence * 100).toFixed(0)}%
                                    </span>
                                </div>

                                <h2 className="text-3xl md:text-5xl font-black text-gray-900 dark:text-white mb-8 leading-tight">
                                    {selectedArticle.title}
                                </h2>

                                <div className="grid grid-cols-2 gap-6 mb-12 p-6 bg-gray-50 dark:bg-surface-900 rounded-3xl">
                                    <div>
                                        <p className="text-[10px] text-surface-500 font-bold uppercase tracking-widest mb-1">Source Agent</p>
                                        <p className="text-gray-900 dark:text-white font-bold">{selectedArticle.author}</p>
                                    </div>
                                    <div>
                                        <p className="text-[10px] text-surface-500 font-bold uppercase tracking-widest mb-1">Timestamp</p>
                                        <p className="text-gray-900 dark:text-white font-bold">{selectedArticle.time}</p>
                                    </div>
                                    <div className="col-span-2">
                                        <p className="text-[10px] text-surface-500 font-bold uppercase tracking-widest mb-1">Geolocation</p>
                                        <div className="flex items-center text-primary-600 dark:text-primary-400 font-bold">
                                            <MapPin className="h-4 w-4 mr-2" />
                                            {selectedArticle.location}
                                        </div>
                                    </div>
                                </div>

                                <div className="prose dark:prose-invert max-w-none">
                                    <h4 className="text-lg font-bold text-gray-900 dark:text-white mb-4">AI Analysis Summary</h4>
                                    <p className="text-xl text-gray-700 dark:text-surface-300 leading-relaxed mb-10 font-medium italic border-l-4 border-primary-500 pl-6">
                                        {selectedArticle.description}
                                    </p>

                                    <h4 className="text-lg font-bold text-gray-900 dark:text-white mb-4">Extracted Raw Content</h4>
                                    <div className="text-gray-600 dark:text-surface-400 leading-relaxed whitespace-pre-line text-base">
                                        {selectedArticle.fullContent}
                                    </div>
                                </div>

                            </div>
                        </motion.div>
                    </>
                )}
            </AnimatePresence>
        </div>
    );
}
