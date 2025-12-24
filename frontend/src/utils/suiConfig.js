// Sui Blockchain Configuration
export const SUI_CONFIG = {
  PACKAGE_ID: process.env.NEXT_PUBLIC_SUI_PACKAGE_ID,
  TREASURY_CAP: process.env.NEXT_PUBLIC_SUI_TREASURY_CAP,
  REPORT_REGISTRY: process.env.NEXT_PUBLIC_SUI_REPORT_REGISTRY,
  NETWORK: process.env.NEXT_PUBLIC_SUI_NETWORK,
  CLOCK_OBJECT: '0x6', // Standard Sui Clock object
};

// Staking and reward amounts (from smart contract)
export const TRUTH_TOKEN_CONFIG = {
  MIN_STAKE_AMOUNT: 10_000000, // 10 TRUTH (6 decimals)
  REWARD_AMOUNT: 5_000000,     // 5 TRUTH
  AIRDROP_AMOUNT: 50_000000,   // 50 TRUTH
  DECIMALS: 6,
};

// Format TRUTH amount for display
export function formatTruthAmount(amount) {
  return (amount / Math.pow(10, TRUTH_TOKEN_CONFIG.DECIMALS)).toFixed(2);
}

// Parse TRUTH amount from user input
export function parseTruthAmount(amount) {
  return Math.floor(amount * Math.pow(10, TRUTH_TOKEN_CONFIG.DECIMALS));
}
