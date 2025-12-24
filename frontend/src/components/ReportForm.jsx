import React, { useState, useRef } from 'react';
import { CATEGORIES } from '../constants/categories';
import { Send, Loader2, Upload, X, FileText } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function ReportForm() {
    const [formData, setFormData] = useState({
        title: '',
        description: '',
        category: CATEGORIES[0].id,
        location: '',
    });
    const [attachedFile, setAttachedFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const fileInputRef = useRef(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 2000));
        console.log("Submitting report:", { ...formData, file: attachedFile?.name });
        setLoading(false);
        // Reset form
        setFormData({ title: '', description: '', category: CATEGORIES[0].id, location: '' });
        setAttachedFile(null);
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setAttachedFile(file);
        }
    };

    const removeFile = () => {
        setAttachedFile(null);
        if (fileInputRef.current) {
            fileInputRef.current.value = '';
        }
    };

    return (
        <motion.form
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
            onSubmit={handleSubmit}
            className="space-y-6 max-w-lg mx-auto bg-white dark:bg-surface-800 p-8 rounded-xl shadow-md border border-gray-200 dark:border-surface-700"
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
                    required
                />
            </div>

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
                        placeholder="City, Area"
                    />
                </div>
            </div>

            <div>
                <label className="block text-sm font-semibold text-gray-700 dark:text-surface-300 mb-1">Description</label>
                <textarea
                    name="description"
                    value={formData.description}
                    onChange={handleChange}
                    className="block w-full rounded-lg border-gray-200 dark:border-surface-600 bg-gray-50 dark:bg-surface-900/50 p-3 text-sm dark:text-white focus:border-primary-500 focus:ring-primary-500 transition-colors"
                    rows="3"
                    placeholder="Provide more details..."
                    required
                ></textarea>
            </div>

            {/* File Upload Section */}
            <div>
                <label className="block text-sm font-semibold text-gray-700 dark:text-surface-300 mb-2">Proof / Evidence</label>
                <input
                    type="file"
                    ref={fileInputRef}
                    onChange={handleFileChange}
                    className="hidden"
                    id="file-upload"
                />

                <AnimatePresence mode="wait">
                    {!attachedFile ? (
                        <motion.label
                            key="upload-prompt"
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -10 }}
                            htmlFor="file-upload"
                            className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed border-gray-200 dark:border-surface-700 rounded-xl cursor-pointer bg-gray-50 dark:bg-surface-900/30 hover:bg-gray-100 dark:hover:bg-surface-900/50 transition-all border-hover group"
                        >
                            <div className="flex flex-col items-center justify-center pt-5 pb-6">
                                <Upload className="w-8 h-8 mb-3 text-gray-400 group-hover:text-primary-500 transition-colors" />
                                <p className="mb-2 text-sm text-gray-500 dark:text-surface-400">
                                    <span className="font-semibold text-primary-500">Click to upload</span> or drag and drop
                                </p>
                                <p className="text-xs text-gray-400 dark:text-surface-500 italic">Any file type (max 10MB)</p>
                            </div>
                        </motion.label>
                    ) : (
                        <motion.div
                            key="file-attached"
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.9 }}
                            className="flex items-center justify-between p-4 bg-primary-50 dark:bg-primary-900/20 border border-primary-200 dark:border-primary-800/50 rounded-xl"
                        >
                            <div className="flex items-center space-x-3">
                                <div className="p-2 bg-primary-100 dark:bg-primary-800 rounded-lg">
                                    <FileText className="w-5 h-5 text-primary-600 dark:text-primary-400" />
                                </div>
                                <div className="overflow-hidden">
                                    <p className="text-sm font-medium text-gray-900 dark:text-white truncate max-w-[200px]">
                                        {attachedFile.name}
                                    </p>
                                    <p className="text-xs text-primary-600 dark:text-primary-400">
                                        {(attachedFile.size / (1024 * 1024)).toFixed(2)} MB • Ready
                                    </p>
                                </div>
                            </div>
                            <button
                                type="button"
                                onClick={removeFile}
                                className="p-2 hover:bg-white dark:hover:bg-surface-800 rounded-full text-gray-400 hover:text-red-500 transition-colors"
                            >
                                <X className="w-5 h-5" />
                            </button>
                        </motion.div>
                    )}
                </AnimatePresence>
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
    );
}
