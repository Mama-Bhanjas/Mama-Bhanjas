"use client";
import { useState } from 'react';
import { useWeb3 } from '../../context/Web3Context';
import { api } from '../../utils/api';
import { useRouter } from 'next/navigation';
import { AlertCircle, Loader2 } from 'lucide-react';
import { ethers } from 'ethers';
import contractData from '../../utils/contractData.json';
import CryptoJS from 'crypto-js';

export default function SubmitReport() {
  const { account, signer } = useWeb3();
  const router = useRouter();
  const [content, setContent] = useState('');
  const [location, setLocation] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!account || !signer) {
      setError("Please connect your wallet first.");
      return;
    }
    setError(null);
    setLoading(true);

    try {
      console.log("Starting submission process...");
      
      // 1. Sign (Off-chain Verification)
      console.log("Step 1: Signing message...");
      const signature = await signer.signMessage(content);
      console.log("Signature created:", signature);
      
      // 2. Submit to Blockchain (On-chain Proof)
      // Calculate has consistent with backend (SHA256)
      const hash = CryptoJS.SHA256(content).toString();
      console.log("Content Hash:", hash);
      
      if (contractData.address) {
          console.log("Step 2: Submitting to Blockchain...", contractData.address);
          try {
            const contract = new ethers.Contract(contractData.address, contractData.abi, signer);
            console.log("Contract initialized. Sending tx...");
            const tx = await contract.submitReport(hash);
            console.log("Tx sent:", tx.hash);
            await tx.wait(); // Wait for confirmation
            console.log("Tx confirmed!");
          } catch (bcError) {
             console.error("Blockchain error:", bcError);
             alert("Blockchain submission failed, but continuing to backend... Error: " + bcError.message);
          }
      } else {
          console.warn("Contract not deployed, skipping blockchain submission");
      }

      // 3. Submit to Backend
      console.log("Step 3: Submitting to Backend...");
      await api.submitReport({
        content,
        location,
        signature,
        address: account
      });
      console.log("Backend submission successful!");
      
      router.push('/');
    } catch (err) {
      console.error("Submission error:", err);
      setError(err.response?.data?.detail || err.message || "Submission failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Submit Disaster Report</h1>
      
      <div className="bg-yellow-50 border border-yellow-200 p-4 rounded-lg mb-6 flex gap-3 text-yellow-800">
        <AlertCircle className="w-5 h-5 flex-shrink-0" />
        <p className="text-sm">
          Your report will be cryptographically signed by your wallet. 
          This creates a permanent, verifiable record on our platform. 
          Misinformation can negatively impact your reputation score.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-medium mb-2">Location</label>
          <input 
            type="text" 
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            className="w-full p-3 border rounded-lg dark:bg-zinc-900 border-zinc-200 dark:border-zinc-800"
            placeholder="e.g. Kathmandu, Nepal"
            required
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium mb-2">Report Details</label>
          <textarea 
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="w-full p-3 border rounded-lg h-40 dark:bg-zinc-900 border-zinc-200 dark:border-zinc-800"
            placeholder="Describe the situation clearly..."
            required
          />
        </div>

        {error && <div className="text-red-600 text-sm">{error}</div>}

        <button 
          type="submit" 
          disabled={loading || !account}
          className="w-full py-4 bg-red-600 hover:bg-red-700 text-white rounded-lg font-bold disabled:opacity-50 disabled:cursor-not-allowed flex justify-center items-center gap-2"
        >
          {loading && <Loader2 className="w-5 h-5 animate-spin" />}
          {loading ? "Signing & Submitting..." : "Sign & Submit Report"}
        </button>
      </form>
    </div>
  );
}
