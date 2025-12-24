import React, { useState } from 'react';
import Head from 'next/head';
import { motion } from 'framer-motion';
import { ShieldAlert } from 'lucide-react';

export default function Verify() {
    return (
        <div className="container mx-auto px-4 py-12">
            <Head>
                <title>Verify Reports - Mama-Bhanjas</title>
            </Head>

            <div className="text-center py-20">
                <motion.div
                    initial={{ scale: 0.8, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    className="inline-flex items-center justify-center p-4 bg-blue-50 rounded-full mb-6"
                >
                    <ShieldAlert className="h-12 w-12 text-primary-600" />
                </motion.div>
                <h1 className="text-3xl font-bold text-gray-900 mb-4">Verification Center</h1>
                <p className="text-gray-600 max-w-lg mx-auto mb-8">
                    The verification portal is currently under construction. Check back soon to start validating community reports.
                </p>
            </div>
        </div>
    );
}
