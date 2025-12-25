import Head from 'next/head';
import React, { useState, useEffect } from 'react';
import SummaryCard from '../components/SummaryCard';
import CategoryTabs from '../components/CategoryTabs';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { ChevronRight, BarChart3, Users, CheckCircle } from 'lucide-react';
import { fetchReports } from '../services/api';

// ... (imports remain the same)

export default function Home() {
    const [category, setCategory] = useState('all');
    const [reports, setReports] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadReports = async () => {
            try {
                const data = await fetchReports();
                // Map backend data to frontend format if necessary
                // Backend: { id, text, source_type, timestamp, disaster_category, ... }
                // Frontend expects: { id, title, description, category, timestamp, location }

                const formattedData = data.map(r => ({
                    id: r.id,
                    title: r.disaster_category || "Unclassified Event", // Use category as title
                    description: r.text,
                    category: (r.disaster_category || "other").toLowerCase(),
                    timestamp: new Date(r.timestamp).getTime(),
                    location: r.location || "Unknown",
                    isVerified: r.is_verified,
                    verificationStatus: r.verification_status
                }));
                setReports(formattedData);
            } catch (error) {
                console.error("Failed to load reports", error);
            } finally {
                setLoading(false);
            }
        };
        loadReports();
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
                <title>Mama-Bhanjas Dashboard</title>
                <meta name="description" content="Disaster reporting and verification platform" />
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
                        Decentralized Disaster Response
                    </motion.h1>
                    <motion.p
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.1, duration: 0.4 }}
                        className="text-lg sm:text-xl text-surface-200 max-w-2xl mx-auto mb-8 leading-relaxed"
                    >
                        Verify incidents in real-time using blockchain technology. Report disasters, validate claims, and help your community faster.
                    </motion.p>
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.2 }}
                        className="flex flex-col sm:flex-row justify-center gap-4"
                    >
                        <Link href="/submit" className="inline-flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-full text-primary-700 bg-white hover:bg-gray-50 transition-all shadow-lg hover:shadow-xl">
                            Report Incident
                        </Link>
                        <Link href="/verify" className="inline-flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-full text-white bg-primary-600 bg-opacity-20 hover:bg-opacity-30 backdrop-blur-sm border-white/20 transition-all">
                            Verify Reports <ChevronRight className="ml-2 h-4 w-4" />
                        </Link>
                    </motion.div>
                </div>
            </section>

            {/* Stats Section */}
            <section className="container mx-auto px-4 sm:px-6 lg:px-8">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="bg-white dark:bg-surface-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-surface-700 flex items-center space-x-4">
                        <div className="p-3 bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded-xl">
                            <BarChart3 className="h-6 w-6" />
                        </div>
                        <div>
                            <p className="text-sm text-gray-500 dark:text-surface-400 font-medium">Total Reports</p>
                            <h4 className="text-2xl font-bold text-gray-900 dark:text-white">1,024</h4>
                        </div>
                    </div>
                    <div className="bg-white dark:bg-surface-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-surface-700 flex items-center space-x-4">
                        <div className="p-3 bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400 rounded-xl">
                            <CheckCircle className="h-6 w-6" />
                        </div>
                        <div>
                            <p className="text-sm text-gray-500 dark:text-surface-400 font-medium">Verified Events</p>
                            <h4 className="text-2xl font-bold text-gray-900 dark:text-white">856</h4>
                        </div>
                    </div>
                    <div className="bg-white dark:bg-surface-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-surface-700 flex items-center space-x-4">
                        <div className="p-3 bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400 rounded-xl">
                            <Users className="h-6 w-6" />
                        </div>
                        <div>
                            <p className="text-sm text-gray-500 dark:text-surface-400 font-medium">Active Verifiers</p>
                            <h4 className="text-2xl font-bold text-gray-900 dark:text-white">342</h4>
                        </div>
                    </div>
                </div>
            </section>

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
