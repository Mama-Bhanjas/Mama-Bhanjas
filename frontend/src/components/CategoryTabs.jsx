import React from 'react';
import { CATEGORIES } from '../constants/categories';

export default function CategoryTabs({ activeCategory, onCategoryChange }) {
    return (
        <div className="flex space-x-1 p-1 bg-surface-100 dark:bg-surface-900/50 rounded-lg overflow-x-auto border border-transparent dark:border-surface-800">
            <button
                onClick={() => onCategoryChange('all')}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-all ${activeCategory === 'all'
                    ? 'bg-white text-primary-600 shadow-sm dark:bg-primary-600 dark:text-white dark:shadow-md dark:shadow-primary-600/20'
                    : 'text-gray-500 text-surface-600 dark:text-surface-400 hover:text-gray-900 dark:hover:text-white hover:bg-surface-200 dark:hover:bg-surface-800'
                    }`}
            >
                All
            </button>
            {CATEGORIES.map(cat => (
                <button
                    key={cat.id}
                    onClick={() => onCategoryChange(cat.id)}
                    className={`px-4 py-2 rounded-md text-sm font-medium whitespace-nowrap transition-all ${activeCategory === cat.id
                        ? 'bg-white text-primary-600 shadow-sm dark:bg-primary-600 dark:text-white dark:shadow-md dark:shadow-primary-600/20'
                        : 'text-gray-500 text-surface-600 dark:text-surface-400 hover:text-gray-900 dark:hover:text-white hover:bg-surface-200 dark:hover:bg-surface-800'
                        }`}
                >
                    {cat.label}
                </button>
            ))}
        </div>
    );
}
