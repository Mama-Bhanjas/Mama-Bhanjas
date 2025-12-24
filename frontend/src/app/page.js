"use client";
import { useEffect, useState } from 'react';
import { api } from '../utils/api';
import { CheckCircle, Clock, MapPin, Activity } from 'lucide-react';
import { useWeb3 } from '../context/Web3Context';

export default function Dashboard() {
  const [reports, setReports] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('All');

  const { connectWallet } = useWeb3();

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 10000); // Polling every 10s
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const [reportsData, statsData] = await Promise.all([
        api.getReports(),
        api.getStats()
      ]);
      setReports(reportsData);
      setStats(statsData);
      setLoading(false);
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  const categories = ["All", "Shelter", "Medical", "Food", "Road Blockages", "Other", "Unclassified"];

  const filteredReports = activeTab === 'All' 
    ? reports 
    : reports.filter(r => r.category === activeTab);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
        <div className="bg-white dark:bg-zinc-900 p-6 rounded-xl border border-zinc-200 dark:border-zinc-800 shadow-sm">
          <h3 className="text-zinc-500 font-medium text-sm uppercase tracking-wider">Total Reports</h3>
          <p className="text-4xl font-bold mt-2">{stats?.total_reports || 0}</p>
        </div>
        <div className="bg-white dark:bg-zinc-900 p-6 rounded-xl border border-zinc-200 dark:border-zinc-800 shadow-sm">
          <h3 className="text-zinc-500 font-medium text-sm uppercase tracking-wider">Verification Rate</h3>
          <p className="text-4xl font-bold mt-2 text-green-600">100%</p>
          <span className="text-xs text-zinc-400">Cryptographically Signed</span>
        </div>
        <div className="bg-white dark:bg-zinc-900 p-6 rounded-xl border border-zinc-200 dark:border-zinc-800 shadow-sm">
          <h3 className="text-zinc-500 font-medium text-sm uppercase tracking-wider">Active Wallets</h3>
          <p className="text-4xl font-bold mt-2">--</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex overflow-x-auto gap-2 pb-4 mb-6 scrollbar-hide">
        {categories.map(cat => (
          <button
            key={cat}
            onClick={() => setActiveTab(cat)}
            className={`px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-colors ${
              activeTab === cat
                ? "bg-black text-white dark:bg-white dark:text-black"
                : "bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 hover:bg-zinc-200"
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Feed */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {loading ? (
            <div className="col-span-1 lg:col-span-2 text-center py-20 text-zinc-500">
                Loading live reports...
            </div>
        ) : filteredReports.length === 0 ? (
            <div className="col-span-1 lg:col-span-2 text-center py-20 text-zinc-500">
                No reports found in this category.
            </div>
        ) : (
          filteredReports.map(report => (
            <div key={report.id} className="bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800 overflow-hidden hover:shadow-md transition-shadow">
              <div className="p-6">
                <div className="flex justify-between items-start mb-4">
                  <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase ${
                    report.category === 'Medical' ? 'bg-red-100 text-red-700' :
                    report.category === 'Shelter' ? 'bg-blue-100 text-blue-700' :
                    'bg-gray-100 text-gray-700'
                  }`}>
                    {report.category}
                  </span>
                  <div className="flex items-center gap-1 text-green-600 text-xs font-medium">
                    <CheckCircle className="w-4 h-4" /> Verified
                  </div>
                </div>

                {report.summary && (
                    <div className="bg-slate-50 dark:bg-slate-900 p-3 rounded-lg mb-4 text-sm font-medium border-l-4 border-indigo-500">
                        ✨ AI Summary: {report.summary}
                    </div>
                )}
                
                <p className="text-zinc-800 dark:text-zinc-200 mb-4 whitespace-pre-wrap">
                  {report.content}
                </p>

                <div className="flex flex-wrap items-center gap-4 text-xs text-zinc-500 border-t pt-4 dark:border-zinc-800">
                    <div className="flex items-center gap-1">
                        <MapPin className="w-3 h-3" /> {report.location || "Unknown Location"}
                    </div>
                    <div className="flex items-center gap-1">
                        <Clock className="w-3 h-3" /> {new Date(report.timestamp).toLocaleString()}
                    </div>
                    <div className="flex items-center gap-1 font-mono">
                        <Activity className="w-3 h-3" /> {report.ai_confidence ? (report.ai_confidence * 100).toFixed(0) + '%' : '0%'} Conf.
                    </div>
                    <div className="ml-auto font-mono bg-zinc-100 dark:bg-zinc-800 px-2 py-1 rounded">
                        {report.owner_address.slice(0,6)}...{report.owner_address.slice(-4)}
                    </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
