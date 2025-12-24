import React, { useState, useRef, useEffect } from 'react';
import { CATEGORIES } from '../constants/categories';
import { Send, Loader2, Upload, X, FileText, Gift, Coins } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useSuiWallet } from '../context/SuiWalletContext';
import { 
    claimAirdrop, 
    submitReport, 
    getTruthTokenBalance, 
    getTruthCoinObject,
    hashReportContent 
} from '../utils/suiInteractions';
import { formatTruthAmount, TRUTH_TOKEN_CONFIG } from '../utils/suiConfig';

export default function ReportForm() {
    const { account, isConnected, signAndExecuteTransaction, suiClient } = useSuiWallet();
    
    const [formData, setFormData] = useState({
        title: '',
        description: '',
        category: CATEGORIES[0].id,
        location: '',
    });
    const [attachedFile, setAttachedFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [truthBalance, setTruthBalance] = useState(0);
    const [showAirdropModal, setShowAirdropModal] = useState(false);
    const [airdropLoading, setAirdropLoading] = useState(false);
    const [submitStatus, setSubmitStatus] = useState(null);
    const fileInputRef = useRef(null);

    // Fetch TRUTH token balance when wallet is connected
    useEffect(() => {
        if (isConnected && account) {
            fetchBalance();
        }
    }, [isConnected, account]);

    const fetchBalance = async () => {
        if (!account || !suiClient) return;
        const balance = await getTruthTokenBalance(suiClient, account);
        setTruthBalance(balance);
    };

    const handleClaimAirdrop = async () => {
        if (!signAndExecuteTransaction) return;
        
        setAirdropLoading(true);
        try {
            await claimAirdrop(signAndExecuteTransaction);
            setSubmitStatus({ type: 'success', message: '🎉 50 TRUTH tokens claimed successfully!' });
            setShowAirdropModal(false);
            
            // Refresh balance after airdrop
            setTimeout(() => fetchBalance(), 2000);
        } catch (error) {
            console.error('Airdrop failed:', error);
            setSubmitStatus({ type: 'error', message: `Airdrop failed: ${error.message}` });
        } finally {
            setAirdropLoading(false);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        if (!isConnected) {
            setSubmitStatus({ type: 'error', message: 'Please connect your Sui wallet first' });
            return;
        }

        // Check if user has enough TRUTH tokens
        if (truthBalance < TRUTH_TOKEN_CONFIG.MIN_STAKE_AMOUNT) {
            setShowAirdropModal(true);
            return;
        }

        setLoading(true);
        setSubmitStatus(null);

        try {
            // 1. Hash the report content
            const reportHash = await hashReportContent(formData.description, formData.location);
            console.log('Report hash:', reportHash);

            // 2. Get a TRUTH coin object with at least 10 TRUTH
            const coinObject = await getTruthCoinObject(suiClient, account);
            
            if (!coinObject) {
                throw new Error('No suitable TRUTH coin found. Please try claiming an airdrop.');
            }

            // 3. Submit to Sui blockchain
            const result = await submitReport(reportHash, coinObject, signAndExecuteTransaction);
            
            console.log('Report submitted to Sui:', result);

            // 4. Submit metadata to backend (for indexing and AI processing)
            const response = await fetch('/api/submit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    ...formData,
                    reportHash,
                    txDigest: result.digest,
                    address: account,
                }),
            });

            if (!response.ok) {
                throw new Error('Backend submission failed');
            }

            setSubmitStatus({ 
                type: 'success', 
                message: '✅ Report submitted successfully! 10 TRUTH tokens staked.' 
            });

            // Reset form
            setFormData({ title: '', description: '', category: CATEGORIES[0].id, location: '' });
            setAttachedFile(null);
            
            // Refresh balance
            setTimeout(() => fetchBalance(), 3000);

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
        <>
            {/* Balance Display */}
            {isConnected && (
                <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mb-6 p-4 bg-gradient-to-r from-primary-50 to-indigo-50 dark:from-primary-900/20 dark:to-indigo-900/20 rounded-xl border border-primary-200 dark:border-primary-800/50"
                >
                    <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                            <div className="p-2 bg-primary-600 rounded-lg">
                                <Coins className="w-5 h-5 text-white" />
                            </div>
                            <div>
                                <p className="text-sm text-gray-600 dark:text-surface-400 font-medium">Your TRUTH Balance</p>
                                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                                    {formatTruthAmount(truthBalance)} TRUTH
                                </p>
                            </div>
                        </div>
                        {truthBalance < TRUTH_TOKEN_CONFIG.MIN_STAKE_AMOUNT && (
                            <button
                                onClick={() => setShowAirdropModal(true)}
                                className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors text-sm font-medium"
                            >
                                <Gift className="w-4 h-4" />
                                Get Free Tokens
                            </button>
                        )}
                    </div>
                    <p className="text-xs text-gray-500 dark:text-surface-500 mt-2">
                        Stake required: {formatTruthAmount(TRUTH_TOKEN_CONFIG.MIN_STAKE_AMOUNT)} TRUTH per report
                    </p>
                </motion.div>
            )}

            {/* Status Messages */}
            <AnimatePresence>
                {submitStatus && (
                    <motion.div
                        initial={{ opacity: 0, y: -10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -10 }}
                        className={`mb-6 p-4 rounded-xl border ${
                            submitStatus.type === 'success'
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
                            required
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
                    disabled={loading || !isConnected}
                    className="w-full flex justify-center items-center gap-2 bg-primary-600 text-white font-semibold py-3 px-4 rounded-lg hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-primary-600/20"
                >
                    {loading ? (
                        <>
                            <Loader2 className="animate-spin h-5 w-5" />
                            <span>Submitting to Sui...</span>
                        </>
                    ) : !isConnected ? (
                        <span>Please Connect Wallet</span>
                    ) : (
                        <>
                            <Send className="h-5 w-5" />
                            <span>Submit Report (Stake 10 TRUTH)</span>
                        </>
                    )}
                </button>
            </motion.form>

            {/* Airdrop Modal */}
            <AnimatePresence>
                {showAirdropModal && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4"
                        onClick={() => !airdropLoading && setShowAirdropModal(false)}
                    >
                        <motion.div
                            initial={{ scale: 0.9, y: 20 }}
                            animate={{ scale: 1, y: 0 }}
                            exit={{ scale: 0.9, y: 20 }}
                            className="bg-white dark:bg-surface-800 rounded-2xl p-8 max-w-md w-full shadow-2xl"
                            onClick={(e) => e.stopPropagation()}
                        >
                            <div className="text-center">
                                <div className="mx-auto w-16 h-16 bg-primary-100 dark:bg-primary-900/30 rounded-full flex items-center justify-center mb-4">
                                    <Gift className="w-8 h-8 text-primary-600 dark:text-primary-400" />
                                </div>
                                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Claim Free TRUTH Tokens</h3>
                                <p className="text-gray-600 dark:text-surface-400 mb-6">
                                    You need at least 10 TRUTH tokens to submit a report. Claim your free airdrop to get started!
                                </p>
                                <div className="bg-primary-50 dark:bg-primary-900/20 rounded-xl p-4 mb-6">
                                    <p className="text-sm text-gray-600 dark:text-surface-400 mb-1">You'll receive</p>
                                    <p className="text-3xl font-bold text-primary-600 dark:text-primary-400">50 TRUTH</p>
                                    <p className="text-xs text-gray-500 dark:text-surface-500 mt-1">Enough for 5 reports</p>
                                </div>
                                <div className="flex gap-3">
                                    <button
                                        onClick={() => setShowAirdropModal(false)}
                                        disabled={airdropLoading}
                                        className="flex-1 px-4 py-3 border border-gray-300 dark:border-surface-600 rounded-lg hover:bg-gray-50 dark:hover:bg-surface-700 transition-colors font-medium text-gray-700 dark:text-surface-300"
                                    >
                                        Cancel
                                    </button>
                                    <button
                                        onClick={handleClaimAirdrop}
                                        disabled={airdropLoading}
                                        className="flex-1 px-4 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium disabled:opacity-50 flex items-center justify-center gap-2"
                                    >
                                        {airdropLoading ? (
                                            <>
                                                <Loader2 className="animate-spin h-5 w-5" />
                                                <span>Claiming...</span>
                                            </>
                                        ) : (
                                            'Claim Airdrop'
                                        )}
                                    </button>
                                </div>
                            </div>
                        </motion.div>
                    </motion.div>
                )}
            </AnimatePresence>
        </>
    );
}
