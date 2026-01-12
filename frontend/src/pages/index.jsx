import Head from 'next/head';
import React, { useState, useEffect } from 'react';
import SummaryCard from '../components/SummaryCard';
import CategoryTabs from '../components/CategoryTabs';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { ChevronRight, BarChart3, Users, CheckCircle } from 'lucide-react';
import { fetchReports, fetchSummaries } from '../services/api';
import { Sparkles, Brain } from 'lucide-react';

export default function Home() {
    const [category, setCategory] = useState('all');
    const [reports, setReports] = useState([]);
    const [globalSummaries, setGlobalSummaries] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadDashboardData = async () => {
            try {
                const [reportsData, summariesData] = await Promise.all([
                    fetchReports(),
                    fetchSummaries()
                ]);
                
                const formattedReports = reportsData.map(r => ({
                    id: r.id,
                    title: r.title || r.disaster_category || "Unclassified Event",
                    description: r.text,
                    category: (r.disaster_category || "other").toLowerCase(),
                    timestamp: new Date(r.timestamp).getTime(),
                    location: r.location || "Unknown",
                    isVerified: r.is_verified,
                    verificationStatus: r.verification_status,
                    summary: r.summary,
                    confidenceScore: r.confidence_score,
                    submittedBy: r.submitted_by
                }));
                
                setReports(formattedReports);
                setGlobalSummaries(summariesData);
            } catch (error) {
                console.error("Failed to load dashboard data", error);
            } finally {
                setLoading(false);
            }
        };
        loadDashboardData();
    }, []);

    const filteredReports = category === 'all'
        ? reports
        : reports.filter(r => r.category === category);

    const container = {
        hidden: { opacity: 0 },
        show: {
            opacity: 1,
            transition: {
                staggerChildren: 0.1
            }
        }
    };

    const item = {
        hidden: { opacity: 0, y: 20 },
        show: { opacity: 1, y: 0 }
    };

    return (
        <div className="space-y-12 pb-12">
            <Head>
                <title>D-Brief Dashboard</title>
                <meta name="description" content="D-Brief: Decentralized disaster reporting and real-time verification platform" />
            </Head>

            {/* Hero Section */}
            <section className="relative overflow-hidden bg-surface-900 text-white rounded-xl mx-4 sm:mx-6 lg:mx-8 shadow-md">
                <div className="absolute inset-0 bg-gradient-to-br from-surface-800 to-surface-900"></div>

                <div className="relative z-10 px-8 py-12 sm:px-16 sm:py-20 text-center">
                    <motion.h1
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.4 }}
                        className="text-3xl sm:text-5xl font-bold tracking-tight mb-4"
                    >
                        D-Brief: Decentralized Response
                    </motion.h1>
                    <motion.p
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.1, duration: 0.4 }}
                        className="text-lg sm:text-xl text-surface-200 max-w-2xl mx-auto mb-8 leading-relaxed"
                    >
                        D-Brief uses decentralized AI to verify disaster incidents in real-time. Report events, validate claims, and help your community faster.
                    </motion.p>
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.2 }}
                        className="flex flex-col sm:flex-row justify-center gap-4"
                    >
                        <Link href="/submit" className="inline-flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-full text-primary-600 bg-white hover:bg-primary-600 hover:text-white transition-all shadow-lg hover:shadow-xl">
                            Report Incident
                        </Link>
                        <Link href="/verify" className="inline-flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-full text-white bg-primary-600 bg-opacity-20 hover:bg-opacity-30 backdrop-blur-sm border-white/20 transition-all">
                            Verified News
                        </Link>
                        <Link href="/intelligence" className="inline-flex items-center justify-center px-8 py-3 border border-white/20 text-base font-medium rounded-full text-white bg-white/5 hover:bg-white/10 transition-all">
                            Global Intel <Sparkles className="ml-2 h-4 w-4" />
                        </Link>
                    </motion.div>
                </div>
            </section>

            {/* Stats Section */}
            <section className="container mx-auto px-4 sm:px-6 lg:px-8">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="bg-white dark:bg-surface-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-surface-700 flex items-center space-x-4">
                        <div className="p-3 bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded-xl">
                            <BarChart3 className="h-6 w-6" />
                        </div>
                        <div>
                            <p className="text-sm text-gray-500 dark:text-surface-400 font-medium">Total Reports</p>
                            <h4 className="text-2xl font-bold text-gray-900 dark:text-white">
                                {loading ? "..." : reports.length}
                            </h4>
                        </div>
                    </div>
                    <div className="bg-white dark:bg-surface-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-surface-700 flex items-center space-x-4">
                        <div className="p-3 bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400 rounded-xl">
                            <CheckCircle className="h-6 w-6" />
                        </div>
                        <div>
                            <p className="text-sm text-gray-500 dark:text-surface-400 font-medium">Verified Events</p>
                            <h4 className="text-2xl font-bold text-gray-900 dark:text-white">
                                {loading ? "..." : reports.filter(r => r.isVerified).length}
                            </h4>
                        </div>
                    </div>
                </div>
            </section>

            {/* AI Global Intelligence Section */}
            {globalSummaries.length > 0 && (
                <section className="container mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="bg-gradient-to-r from-primary-600 to-indigo-700 rounded-3xl p-8 text-white shadow-2xl relative overflow-hidden">
                        <div className="absolute top-0 right-0 p-8 opacity-10">
                            <Brain className="w-64 h-64 rotate-12" />
                        </div>
                        <div className="relative z-10">
                            <div className="flex items-center space-x-2 mb-6">
                                <Sparkles className="h-5 w-5 text-primary-200" />
                                <span className="text-sm font-bold uppercase tracking-wider text-primary-100">Live Situation Analysis</span>
                            </div>
                            <h2 className="text-3xl font-black mb-8">Trust-Weighted Intelligence</h2>
                            
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                {globalSummaries.map((summary) => (
                                    <div key={summary.category} className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 hover:bg-white/15 transition-all group">
                                        <div className="flex justify-between items-start mb-4">
                                            <h3 className="text-xl font-bold capitalize">{summary.category} Overview</h3>
                                            <div className="px-3 py-1 bg-white/20 rounded-full text-xs font-bold">
                                                Trust Score: {summary.reputation_score.toFixed(1)}/10
                                            </div>
                                        </div>
                                        <p className="text-primary-50 text-sm leading-relaxed mb-4 group-hover:text-white transition-colors">
                                            {summary.summary_text}
                                        </p>
                                        <div className="flex items-center text-[10px] font-bold text-primary-200 uppercase tracking-widest">
                                            <CheckCircle className="h-3 w-3 mr-1" />
                                            Unified from {summary.report_ids.length} decentralized reports
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </section>
            )}

            {/* Recent Activity */}
            <section className="container mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex flex-col sm:flex-row justify-between items-center mb-8">
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4 sm:mb-0">Recent Activity</h2>
                    <CategoryTabs activeCategory={category} onCategoryChange={setCategory} />
                </div>

                <motion.div
                    variants={container}
                    initial="hidden"
                    animate="show"
                    className="grid gap-6 md:grid-cols-2 lg:grid-cols-3"
                >
                    {filteredReports.map(report => (
                        <motion.div key={report.id} variants={item}>
                            <SummaryCard report={report} />
                        </motion.div>
                    ))}
                </motion.div>
            </section>
        </div>
    );
}
