import React, { useState } from 'react';
import { CATEGORIES } from '../constants/categories';
import { Send, Loader2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { submitReport } from '../services/api';

export default function ReportForm() {
    const [formData, setFormData] = useState({
        inputMode: 'text', // 'text' or 'url'
        title: '',
        description: '',
        category: CATEGORIES[0].id,
        location: '',
        url: '',
        source_type: 'WEB',
        source_identifier: 'anonymous'
    });

    const [loading, setLoading] = useState(false);
    const [submitStatus, setSubmitStatus] = useState(null);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setSubmitStatus(null);

        try {
            // Build payload based on input mode
            const payload = formData.inputMode === 'url'
                ? {
                    // URL mode: send URL as text, AI will extract content
                    text: formData.url,
                    source_type: "WEB_USER",
                    source_identifier: "anonymous_web",
                    location: formData.location || null,
                    disaster_category: formData.category
                }
                : {
                    // Text mode: combine title and description
                    text: `${formData.title}: ${formData.description}`,
                    source_type: "WEB_USER",
                    source_identifier: "anonymous_web",
                    location: formData.location || null,
                    disaster_category: formData.category
                };

            await submitReport(payload);

            setSubmitStatus({
                type: 'success',
                message: formData.inputMode === 'url'
                    ? '✅ URL submitted! Extracting and analyzing content...'
                    : '✅ Report submitted successfully!'
            });

            // Reset form
            setFormData({
                inputMode: 'text',
                title: '',
                description: '',
                category: CATEGORIES[0].id,
                location: '',
                url: '',
                source_type: 'WEB',
                source_identifier: 'anonymous'
            });

        } catch (error) {
            console.error('Submission error:', error);
            setSubmitStatus({
                type: 'error',
                message: `Submission failed: ${error.message || 'Unknown error'}`
            });
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            {/* Status Messages */}
            <AnimatePresence>
                {submitStatus && (
                    <motion.div
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -10 }}
                        className={`mb-6 p-4 rounded-xl border ${submitStatus.type === 'success'
                            ? 'bg-green-50 border-green-200 text-green-800 dark:bg-green-900/20 dark:border-green-800 dark:text-green-400'
                            : 'bg-red-50 border-red-200 text-red-800 dark:bg-red-900/20 dark:border-red-800 dark:text-red-400'
                            }`}
                    >
                        {submitStatus.message}
                    </motion.div>
                )}
            </AnimatePresence>

            <motion.form
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5 }}
                onSubmit={handleSubmit}
                className="space-y-6 max-w-lg mx-auto bg-white dark:bg-surface-800 p-8 rounded-xl shadow-md border border-gray-200 dark:border-surface-700"
            >
                {/* Input Mode Toggle */}
                <div className="flex gap-2 p-1 bg-gray-100 dark:bg-surface-900 rounded-lg">
                    <button
                        type="button"
                        onClick={() => setFormData(prev => ({ ...prev, inputMode: 'text' }))}
                        className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-all ${formData.inputMode === 'text'
                            ? 'bg-white dark:bg-surface-700 text-primary-600 dark:text-primary-400 shadow-sm'
                            : 'text-gray-600 dark:text-surface-400 hover:text-gray-900 dark:hover:text-white'
                            }`}
                    >
                        📝 Type Report
                    </button>
                    <button
                        type="button"
                        onClick={() => setFormData(prev => ({ ...prev, inputMode: 'url' }))}
                        className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-all ${formData.inputMode === 'url'
                            ? 'bg-white dark:bg-surface-700 text-primary-600 dark:text-primary-400 shadow-sm'
                            : 'text-gray-600 dark:text-surface-400 hover:text-gray-900 dark:hover:text-white'
                            }`}
                    >
                        🔗 Paste URL
                    </button>
                </div>

                {formData.inputMode === 'text' ? (
                    <>
                        <div>
                            <label className="block text-sm font-semibold text-gray-700 dark:text-surface-300 mb-1">Title</label>
                            <input
                                type="text"
                                name="title"
                                value={formData.title}
                                onChange={handleChange}
                                className="block w-full rounded-lg border-gray-200 dark:border-surface-600 bg-gray-50 dark:bg-surface-900/50 p-3 text-sm dark:text-white focus:border-primary-500 focus:ring-primary-500 transition-colors"
                                placeholder="What happened?"
                                required
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-semibold text-gray-700 dark:text-surface-300 mb-1">Description</label>
                            <textarea
                                name="description"
                                value={formData.description}
                                onChange={handleChange}
                                rows="4"
                                className="block w-full rounded-lg border-gray-200 dark:border-surface-600 bg-gray-50 dark:bg-surface-900/50 p-3 text-sm dark:text-white focus:border-primary-500 focus:ring-primary-500 transition-colors resize-none"
                                placeholder="Provide details about the incident..."
                                required
                            />
                        </div>
                    </>
                ) : (
                    <div>
                        <label className="block text-sm font-semibold text-gray-700 dark:text-surface-300 mb-1">News Article URL</label>
                        <input
                            type="url"
                            name="url"
                            value={formData.url}
                            onChange={handleChange}
                            className="block w-full rounded-lg border-gray-200 dark:border-surface-600 bg-gray-50 dark:bg-surface-900/50 p-3 text-sm dark:text-white focus:border-primary-500 focus:ring-primary-500 transition-colors"
                            placeholder="https://example.com/disaster-news-article"
                            required
                        />
                        <p className="mt-1 text-xs text-gray-500 dark:text-surface-400">
                            Paste a link to a news article - we'll extract and analyze the content automatically
                        </p>
                    </div>
                )}

                <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                    <div>
                        <label className="block text-sm font-semibold text-gray-700 dark:text-surface-300 mb-1">Category</label>
                        <div className="relative">
                            <select
                                name="category"
                                value={formData.category}
                                onChange={handleChange}
                                className="block w-full rounded-lg border-gray-200 dark:border-surface-600 bg-gray-50 dark:bg-surface-900/50 p-3 text-sm dark:text-white focus:border-primary-500 focus:ring-primary-500 appearance-none"
                            >
                                {CATEGORIES.map(cat => (
                                    <option key={cat.id} value={cat.id} className="dark:bg-surface-800">{cat.label}</option>
                                ))}
                            </select>
                            <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-500">
                                <svg className="h-4 w-4 fill-current" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" /></svg>
                            </div>
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-semibold text-gray-700 dark:text-surface-300 mb-1">Location</label>
                        <input
                            type="text"
                            name="location"
                            value={formData.location}
                            onChange={handleChange}
                            className="block w-full rounded-lg border-gray-200 dark:border-surface-600 bg-gray-50 dark:bg-surface-900/50 p-3 text-sm dark:text-white focus:border-primary-500 focus:ring-primary-500 transition-colors"
                            placeholder="City, Area (optional - AI can detect)"
                        />
                    </div>
                </div>

                <button
                    type="submit"
                    disabled={loading}
                    className="w-full flex justify-center items-center gap-2 bg-primary-600 text-white font-semibold py-3 px-4 rounded-lg hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-primary-600/20"
                >
                    {loading ? (
                        <>
                            <Loader2 className="animate-spin h-5 w-5" />
                            <span>Submitting...</span>
                        </>
                    ) : (
                        <>
                            <Send className="h-5 w-5" />
                            <span>Submit Report</span>
                        </>
                    )}
                </button>
            </motion.form>
        </>
    );
}
