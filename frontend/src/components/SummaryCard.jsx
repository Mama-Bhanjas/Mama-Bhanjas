import React from 'react';
import { formatTime } from '../utils/formatTime';
import { MapPin, Clock, ArrowRight, ShieldCheck, User, Sparkles } from 'lucide-react';
import { motion } from 'framer-motion';

export default function SummaryCard({ report }) {
    // Determine badge color based on category
    const getCategoryColor = (cat) => {
        switch (cat.toLowerCase()) {
            case 'flood': return 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400';
            case 'fire': return 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400';
            case 'earthquake': return 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400';
            default: return 'bg-gray-100 text-gray-700 dark:bg-gray-900/30 dark:text-gray-400';
        }
    };

    return (
        <motion.div
            whileHover={{ y: -5 }}
            className="bg-white dark:bg-surface-800 rounded-xl overflow-hidden border border-gray-100 dark:border-surface-700 shadow-sm hover:shadow-lg transition-all duration-300 flex flex-col h-full"
        >
            <div className="p-6 flex-grow">
                <div className="flex justify-between items-start mb-4">
                    <div className="flex gap-2 flex-wrap">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getCategoryColor(report.category)}`}>
                            {report.category}
                        </span>
                        {report.isVerified && (
                            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400">
                                <ShieldCheck className="h-3 w-3 mr-1" />
                                Verified
                            </span>
                        )}
                    </div>
                    <span className="flex items-center text-xs text-gray-400 dark:text-surface-400">
                        <Clock className="h-3 w-3 mr-1" />
                        {formatTime(report.timestamp)}
                    </span>
                </div>

                <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2 line-clamp-1">{report.title}</h3>
                
                {/* AI Summary if available */}
                {report.summary ? (
                    <div className="mb-3">
                        <div className="flex items-center gap-1 mb-1">
                            <Sparkles className="h-3 w-3 text-primary-500" />
                            <span className="text-xs font-medium text-primary-600 dark:text-primary-400">AI Summary</span>
                        </div>
                        <p className="text-gray-600 dark:text-surface-300 text-sm line-clamp-2">{report.summary}</p>
                    </div>
                ) : (
                    <p className="text-gray-600 dark:text-surface-300 text-sm mb-3 line-clamp-3">{report.description}</p>
                )}

                <div className="space-y-2">
                    {report.location && (
                        <div className="flex items-center text-xs text-gray-500 dark:text-surface-400">
                            <MapPin className="h-3 w-3 mr-1" />
                            {report.location}
                        </div>
                    )}
                    {report.submittedBy && (
                        <div className="flex items-center text-xs text-gray-500 dark:text-surface-400">
                            <User className="h-3 w-3 mr-1" />
                            Reported by: {report.submittedBy}
                        </div>
                    )}
                    {report.confidenceScore && (
                        <div className="flex items-center text-xs text-gray-500 dark:text-surface-400">
                            <div className="flex items-center gap-2 w-full">
                                <span>AI Confidence:</span>
                                <div className="flex-1 bg-gray-200 dark:bg-surface-700 rounded-full h-1.5">
                                    <div 
                                        className="bg-primary-600 h-1.5 rounded-full" 
                                        style={{ width: `${(report.confidenceScore * 100).toFixed(0)}%` }}
                                    ></div>
                                </div>
                                <span className="font-medium">{(report.confidenceScore * 100).toFixed(0)}%</span>
                            </div>
                        </div>
                    )}
                </div>
            </div>

            <div className="px-6 py-4 bg-gray-50 dark:bg-surface-900/50 border-t border-gray-100 dark:border-surface-700 mt-auto">
                <button className="flex items-center text-sm font-semibold text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 transition-colors">
                    View Details
                    <ArrowRight className="h-4 w-4 ml-1" />
                </button>
            </div>
        </motion.div>
    );
}
