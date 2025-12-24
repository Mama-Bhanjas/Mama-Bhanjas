import React from 'react';
import { formatTime } from '../utils/formatTime';
import { MapPin, Clock, ArrowRight } from 'lucide-react';
import { motion } from 'framer-motion';

export default function SummaryCard({ report }) {
    // Determine badge color based on category
    const getCategoryColor = (cat) => {
        switch (cat.toLowerCase()) {
            case 'flood': return 'bg-blue-100 text-blue-700';
            case 'fire': return 'bg-orange-100 text-orange-700';
            case 'earthquake': return 'bg-amber-100 text-amber-700';
            default: return 'bg-gray-100 text-gray-700';
        }
    };

    return (
        <motion.div
            whileHover={{ y: -5 }}
            className="bg-white dark:bg-surface-800 rounded-xl overflow-hidden border border-gray-100 dark:border-surface-700 shadow-sm hover:shadow-lg transition-all duration-300 flex flex-col h-full"
        >
            <div className="p-6 flex-grow">
                <div className="flex justify-between items-start mb-4">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getCategoryColor(report.category)}`}>
                        {report.category}
                    </span>
                    <span className="flex items-center text-xs text-gray-400 dark:text-surface-400">
                        <Clock className="h-3 w-3 mr-1" />
                        {formatTime(report.timestamp)}
                    </span>
                </div>

                <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2 line-clamp-1">{report.title}</h3>
                <p className="text-gray-600 dark:text-surface-300 text-sm mb-4 line-clamp-3">{report.description}</p>

                {report.location && (
                    <div className="flex items-center text-xs text-gray-500 dark:text-surface-400 mb-4">
                        <MapPin className="h-3 w-3 mr-1" />
                        {report.location}
                    </div>
                )}
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
