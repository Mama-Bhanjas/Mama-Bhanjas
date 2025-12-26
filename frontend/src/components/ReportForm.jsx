import React, { useState, useRef, useEffect } from 'react';
import { CATEGORIES } from '../constants/categories';
import { Send, Loader2, FileText, Link, Upload, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { submitReport } from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function ReportForm() {
    const { user } = useAuth();
    const [formData, setFormData] = useState({
        inputMode: 'text', // 'text', 'url', or 'pdf'
        title: '',
        description: '',
        category: CATEGORIES[0].id,
        location: '',
        url: '',
        source_type: 'WEB',
        source_identifier: 'anonymous',
        submitted_by: ''
    });

    // Auto-fill user name if logged in
    useEffect(() => {
        if (user && user.full_name) {
            setFormData(prev => ({ ...prev, submitted_by: user.full_name }));
        }
    }, [user]);

    const [attachedFile, setAttachedFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [submitStatus, setSubmitStatus] = useState(null);
    const fileInputRef = useRef(null);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file && file.type === 'application/pdf') {
            setAttachedFile(file);
            setSubmitStatus(null);
        } else if (file) {
            setSubmitStatus({
                type: 'error',
                message: 'Please upload a PDF file.'
            });
            e.target.value = null;
        }
    };

    const removeFile = () => {
        setAttachedFile(null);
        if (fileInputRef.current) {
            fileInputRef.current.value = null;
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setSubmitStatus(null);

        try {
            let payload;
            if (formData.inputMode === 'pdf') {
                if (!attachedFile) {
                    throw new Error('Please select a PDF file to upload.');
                }
                payload = new FormData();
                payload.append('file', attachedFile);
                payload.append('source_type', 'WEB_USER');
                payload.append('source_identifier', 'anonymous_pdf');
                payload.append('location', formData.location || '');
                payload.append('disaster_category', formData.category);
                payload.append('submitted_by', formData.submitted_by || 'Anonymous');
                payload.append('text', `PDF Report: ${attachedFile.name}`); // Fallback text
            } else if (formData.inputMode === 'url') {
                payload = {
                    text: formData.url,
                    source_type: "WEB_USER",
                    source_identifier: "anonymous_web",
                    location: formData.location || null,
                    disaster_category: formData.category,
                    submitted_by: formData.submitted_by || 'Anonymous'
                };
            } else {
                payload = {
                    text: `${formData.title}: ${formData.description}`,
                    title: formData.title,
                    source_type: "WEB_USER",
                    source_identifier: "anonymous_web",
                    location: formData.location || null,
                    disaster_category: formData.category,
                    submitted_by: formData.submitted_by || 'Anonymous'
                };
            }

            await submitReport(payload);

            setSubmitStatus({
                type: 'success',
                message: formData.inputMode === 'url'
                    ? '✅ URL submitted! Extracting and analyzing content...'
                    : formData.inputMode === 'pdf'
                        ? '✅ PDF uploaded! Analyzing content...'
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
            setAttachedFile(null);
            if (fileInputRef.current) fileInputRef.current.value = null;

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
                <div className="flex gap-2 p-1 bg-gray-100 dark:bg-surface-900 rounded-lg overflow-x-auto">
                    <button
                        type="button"
                        onClick={() => setFormData(prev => ({ ...prev, inputMode: 'text' }))}
                        className={`flex-1 flex items-center justify-center gap-2 py-2 px-4 rounded-md text-sm font-medium transition-all min-w-[100px] ${formData.inputMode === 'text'
                            ? 'bg-white dark:bg-surface-700 text-primary-600 dark:text-primary-400 shadow-sm'
                            : 'text-gray-600 dark:text-surface-400 hover:text-gray-900 dark:hover:text-white'
                            }`}
                    >
                        <FileText className="w-4 h-4" />
                        <span>Text</span>
                    </button>
                    <button
                        type="button"
                        onClick={() => setFormData(prev => ({ ...prev, inputMode: 'url' }))}
                        className={`flex-1 flex items-center justify-center gap-2 py-2 px-4 rounded-md text-sm font-medium transition-all min-w-[100px] ${formData.inputMode === 'url'
                            ? 'bg-white dark:bg-surface-700 text-primary-600 dark:text-primary-400 shadow-sm'
                            : 'text-gray-600 dark:text-surface-400 hover:text-gray-900 dark:hover:text-white'
                            }`}
                    >
                        <Link className="w-4 h-4" />
                        <span>URL</span>
                    </button>
                    <button
                        type="button"
                        onClick={() => setFormData(prev => ({ ...prev, inputMode: 'pdf' }))}
                        className={`flex-1 flex items-center justify-center gap-2 py-2 px-4 rounded-md text-sm font-medium transition-all min-w-[100px] ${formData.inputMode === 'pdf'
                            ? 'bg-white dark:bg-surface-700 text-primary-600 dark:text-primary-400 shadow-sm'
                            : 'text-gray-600 dark:text-surface-400 hover:text-gray-900 dark:hover:text-white'
                            }`}
                    >
                        <Upload className="w-4 h-4" />
                        <span>PDF</span>
                    </button>
                </div>

                <AnimatePresence mode="wait">
                    {formData.inputMode === 'text' ? (
                        <motion.div
                            key="text"
                            initial={{ opacity: 0, x: 10 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -10 }}
                            className="space-y-4"
                        >
                            <div>
                                <label className="block text-sm font-semibold text-gray-700 dark:text-surface-300 mb-1">Title</label>
                                <input
                                    type="text"
                                    name="title"
                                    value={formData.title}
                                    onChange={handleChange}
                                    className="block w-full rounded-lg border-gray-200 dark:border-surface-600 bg-gray-50 dark:bg-surface-900/50 p-3 text-sm dark:text-white focus:border-primary-500 focus:ring-primary-500 transition-colors"
                                    placeholder="What happened?"
                                    required={formData.inputMode === 'text'}
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
                                    required={formData.inputMode === 'text'}
                                />
                            </div>
                        </motion.div>
                    ) : formData.inputMode === 'url' ? (
                        <motion.div
                            key="url"
                            initial={{ opacity: 0, x: 10 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -10 }}
                        >
                            <label className="block text-sm font-semibold text-gray-700 dark:text-surface-300 mb-1">News Article URL</label>
                            <div className="relative">
                                <Link className="absolute left-3 top-3.5 h-4 w-4 text-gray-400" />
                                <input
                                    type="url"
                                    name="url"
                                    value={formData.url}
                                    onChange={handleChange}
                                    className="block w-full rounded-lg border-gray-200 dark:border-surface-600 bg-gray-50 dark:bg-surface-900/50 pl-10 pr-3 py-3 text-sm dark:text-white focus:border-primary-500 focus:ring-primary-500 transition-colors"
                                    placeholder="https://example.com/disaster-news-article"
                                    required={formData.inputMode === 'url'}
                                />
                            </div>
                            <p className="mt-1 text-xs text-gray-500 dark:text-surface-400">
                                Paste a link to a news article - we'll extract and analyze the content automatically
                            </p>
                        </motion.div>
                    ) : (
                        <motion.div
                            key="pdf"
                            initial={{ opacity: 0, x: 10 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -10 }}
                            className="space-y-4"
                        >
                            <label className="block text-sm font-semibold text-gray-700 dark:text-surface-300 mb-1">Upload PDF Report</label>
                            <div
                                onClick={() => fileInputRef.current?.click()}
                                className={`relative border-2 border-dashed rounded-xl p-8 transition-all cursor-pointer text-center
                                    ${attachedFile
                                        ? 'border-primary-500 bg-primary-50/30 dark:bg-primary-900/10'
                                        : 'border-gray-200 dark:border-surface-600 hover:border-primary-500 dark:hover:border-primary-400 bg-gray-50 dark:bg-surface-900/30'}`}
                            >
                                <input
                                    type="file"
                                    ref={fileInputRef}
                                    onChange={handleFileChange}
                                    accept=".pdf"
                                    className="hidden"
                                />
                                {attachedFile ? (
                                    <div className="flex flex-col items-center">
                                        <div className="relative">
                                            <div className="p-3 bg-primary-100 dark:bg-primary-900/40 rounded-full mb-3">
                                                <FileText className="w-8 h-8 text-primary-600 dark:text-primary-400" />
                                            </div>
                                            <button
                                                type="button"
                                                onClick={(e) => { e.stopPropagation(); removeFile(); }}
                                                className="absolute -top-1 -right-1 p-1 bg-white dark:bg-surface-800 rounded-full shadow-md border border-gray-200 dark:border-surface-600 hover:text-red-500 transition-colors"
                                            >
                                                <X className="w-3 h-3" />
                                            </button>
                                        </div>
                                        <p className="text-sm font-medium text-gray-900 dark:text-white truncate max-w-[200px]">
                                            {attachedFile.name}
                                        </p>
                                        <p className="text-xs text-gray-500 dark:text-surface-400 mt-1">
                                            {(attachedFile.size / (1024 * 1024)).toFixed(2)} MB
                                        </p>
                                    </div>
                                ) : (
                                    <div className="flex flex-col items-center">
                                        <div className="p-3 bg-gray-100 dark:bg-surface-800 rounded-full mb-3 group-hover:bg-primary-50 dark:group-hover:bg-primary-900/20 transition-colors">
                                            <Upload className="w-8 h-8 text-gray-400 dark:text-surface-500 group-hover:text-primary-500 transition-colors" />
                                        </div>
                                        <p className="text-sm font-medium text-gray-900 dark:text-white">
                                            Click to upload PDF
                                        </p>
                                        <p className="text-xs text-gray-500 dark:text-surface-400 mt-1">
                                            Max file size: 10MB
                                        </p>
                                    </div>
                                )}
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>

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
                            placeholder="City, Area (optional)"
                        />
                    </div>
                </div>

                <div>
                    <label className="block text-sm font-semibold text-gray-700 dark:text-surface-300 mb-1">Your Name (Optional)</label>
                    <input
                        type="text"
                        name="submitted_by"
                        value={formData.submitted_by}
                        onChange={handleChange}
                        disabled={!!user}
                        className={`block w-full rounded-lg border-gray-200 dark:border-surface-600 p-3 text-sm dark:text-white focus:border-primary-500 focus:ring-primary-500 transition-colors ${user ? 'bg-gray-100 dark:bg-surface-800 text-gray-500 cursor-not-allowed' : 'bg-gray-50 dark:bg-surface-900/50'}`}
                        placeholder="Leave blank to remain anonymous"
                    />
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
