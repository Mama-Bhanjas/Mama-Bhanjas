import Head from 'next/head';
import ReportForm from '../components/ReportForm';
import { motion } from 'framer-motion';

export default function Submit() {
    return (
        <div className="container mx-auto px-4 py-12">
            <Head>
                <title>Submit Report - Mama-Bhanjas</title>
            </Head>

            <div className="max-w-2xl mx-auto">
                <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="text-center mb-10"
                >
                    <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4 text-center">Submit Disaster Report</h1>
                    <p className="text-gray-600 dark:text-surface-300">
                        Provide accurate details about the incident. Your report will be verified by the community on the blockchain.
                    </p>
                </motion.div>

                <ReportForm />
            </div>
        </div>
    );
}
