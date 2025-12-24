import React from 'react';
import { motion } from 'framer-motion';

export default function Footer() {
    return (
        <motion.footer
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, ease: "easeOut" }}
            viewport={{ once: true }}
            className="bg-surface-950 text-white border-t border-surface-800 mt-auto"
        >
            <div className="container mx-auto px-4 py-12">
                <div className="flex flex-col items-center">
                    <div className="text-center">
                        <h3 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary-400 to-primary-200 mb-2">
                            Mama-Bhanjas
                        </h3>
                        <p className="text-sm text-surface-400 max-w-xs mx-auto">
                            Decentralized Disaster Verification. Empowering communities with truth and speed.
                        </p>
                        <p className="text-xs text-surface-500 mt-4">
                            &copy; {new Date().getFullYear()} All rights reserved.
                        </p>
                    </div>
                </div>
            </div>
        </motion.footer>
    );
}
