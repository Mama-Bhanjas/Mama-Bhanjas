import React from 'react';
import { motion } from 'framer-motion';
import {
    ShieldCheck,
    MapPin,
    Clock,
    AlertTriangle,
    Flame,
    Droplets,
    Waves,
    Info
} from 'lucide-react';

const TYPE_ICONS = {
    earthquake: <Waves className="h-5 w-5 text-amber-500" />,
    flood: <Droplets className="h-5 w-5 text-blue-500" />,
    fire: <Flame className="h-5 w-5 text-orange-500" />,
    landslide: <AlertTriangle className="h-5 w-5 text-red-500" />,
    others: <Info className="h-5 w-5 text-gray-500" />
};

export default function NewsCard({ article, onViewDetails }) {
    if (!article) return null;

    return (
        <div
            className="group relative bg-surface-900/50 border border-surface-800 hover:border-primary-500/50 rounded-2xl p-6 transition-all hover:shadow-2xl hover:shadow-primary-900/10 cursor-pointer overflow-hidden"
            onClick={() => onViewDetails && onViewDetails(article)}
        >
            <div className="flex items-start justify-between mb-4">
                <div className="p-3 bg-surface-900 border border-surface-800 rounded-xl group-hover:border-primary-500/30 transition-colors">
                    {TYPE_ICONS[article.type] || TYPE_ICONS.other}
                </div>
                {article.verified && (
                    <div className="flex items-center space-x-1 px-3 py-1 bg-green-500/10 border border-green-500/20 rounded-full">
                        <ShieldCheck className="h-3 w-3 text-green-500" />
                        <span className="text-[10px] font-bold text-green-500 uppercase tracking-wider">Verified</span>
                    </div>
                )}
            </div>

            <h3 className="text-xl font-bold text-white mb-2 leading-tight group-hover:text-primary-400 transition-colors">
                {article.title}
            </h3>
            <p className="text-surface-400 text-sm mb-6 line-clamp-3">
                {article.description}
            </p>

            <div className="flex items-center justify-between pt-4 border-t border-surface-800">
                <div className="flex flex-wrap items-center gap-4">
                    <div className="flex items-center text-xs text-surface-500">
                        <MapPin className="h-3 w-3 mr-1 text-primary-500" />
                        {article.location}
                    </div>
                    <div className="flex items-center text-xs text-surface-500">
                        <Clock className="h-3 w-3 mr-1 text-surface-600" />
                        {article.time}
                    </div>
                </div>
                <button
                    className="text-xs font-bold text-primary-500 hover:text-primary-400 flex items-center group-hover:translate-x-1 transition-transform"
                >
                    View Details →
                </button>
            </div>
        </div>
    );
}
