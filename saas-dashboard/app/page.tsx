"use client"

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Rocket, ShieldAlert, CheckCircle2, Zap, BarChart3, Globe } from 'lucide-react';
import { AreaChart, Area, Tooltip, ResponsiveContainer } from 'recharts';

const mockData = [
  { name: '10:00', orders: 12 },
  { name: '10:05', orders: 45 },
  { name: '10:10', orders: 25 },
  { name: '10:15', orders: 80 },
  { name: '10:20', orders: 60 },
];

export default function SniperDashboard() {
  const [url, setUrl] = useState('');
  const [orders, setOrders] = useState(5);
  const [isLaunching, setIsLaunching] = useState(false);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState("READY");

  const handleLaunch = async () => {
    if (!url) return alert("⚠️ Entrez l'URL de la cible d'abord !");
    
    setIsLaunching(true);
    setProgress(0);
    setStatus("IN_PROGRESS");

    try {
      // LE FIX EST ICI : On pointe vers l'API Render !
      const res = await fetch('https://tapyach-api.onrender.com/launch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url, orders: orders })
      });

      if (res.ok) {
        setStatus("SUCCESS");
        let interval = setInterval(() => {
          setProgress((prev) => {
            if (prev >= 100) {
              clearInterval(interval);
              setIsLaunching(false);
              return 100;
            }
            return prev + 2;
          });
        }, 200);
      } else {
        setStatus("FAILED");
        setIsLaunching(false);
      }
    } catch (err) {
      alert("❌ Serveur API Hors-ligne. Vérifiez Render.");
      setStatus("FAILED");
      setIsLaunching(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#050505] text-white p-4 md:p-8 font-sans selection:bg-orange-500/30">
      <div className="max-w-7xl mx-auto space-y-8">
        
        <header className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-white/5 pb-8">
          <div>
            <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="flex items-center gap-2">
              <div className="bg-orange-600 p-2 rounded-lg shadow-[0_0_15px_rgba(234,88,12,0.4)]">
                <Zap size={24} fill="white" />
              </div>
              <h1 className="text-3xl font-black tracking-tighter uppercase italic">Tapyach <span className="text-orange-600">Sniper</span></h1>
            </motion.div>
            <p className="text-slate-500 text-sm mt-2 font-medium">Educational Load Testing System v4.0</p>
          </div>
          
          <div className="flex items-center gap-3 bg-white/5 p-1.5 rounded-2xl border border-white/10">
            <span className="bg-orange-600/10 text-orange-500 px-4 py-1.5 rounded-full text-[10px] font-black uppercase tracking-widest">
              50 FREE CREDITS
            </span>
            <button className="bg-white text-black hover:bg-slate-200 font-bold rounded-xl px-6 py-2 transition-all active:scale-95 text-sm">
              UPGRADE PRO
            </button>
          </div>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <StatCard title="Total Injections" value="1,284" icon={<Rocket className="text-orange-500" />} change="+12% today" />
          <StatCard title="Success Rate" value="99.2%" icon={<CheckCircle2 className="text-emerald-500" />} change="Perfect sync" />
          <StatCard title="Bypassed Shields" value="482" icon={<ShieldAlert className="text-blue-500" />} change="Anti-bot active" />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-1 bg-[#0a0a0a] border border-white/10 rounded-2xl p-6 shadow-2xl relative overflow-hidden group">
            <div className="flex items-center gap-2 mb-6">
              <Globe size={18} className="text-orange-500"/> 
              <h3 className="text-lg font-bold">Target Configuration</h3>
            </div>

            <div className="space-y-6 relative">
              <div className="space-y-2">
                <label className="text-xs font-bold text-slate-500 uppercase tracking-widest">Store Product URL</label>
                <input 
                  type="text"
                  placeholder="https://youcan.shop/product-link..." 
                  className="w-full bg-black border border-white/10 focus:ring-2 focus:ring-orange-600/50 outline-none transition-all h-12 rounded-xl text-white px-4 text-sm"
                  value={url} onChange={(e) => setUrl(e.target.value)}
                />
              </div>
              
              <div className="space-y-2">
                <label className="text-xs font-bold text-slate-500 uppercase tracking-widest">Traffic Intensity (Orders)</label>
                <input 
                  type="number"
                  min="1"
                  className="w-full bg-black border border-white/10 focus:ring-2 focus:ring-orange-600/50 outline-none transition-all h-12 rounded-xl text-white px-4 text-sm"
                  value={orders} onChange={(e) => setOrders(Number(e.target.value))}
                />
              </div>

              <button 
                onClick={handleLaunch}
                disabled={isLaunching || !url}
                className="w-full h-14 mt-2 bg-orange-600 hover:bg-orange-500 text-black text-lg font-black rounded-xl shadow-[0_10px_20px_rgba(234,88,12,0.2)] transition-all active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLaunching ? 'SYSTEM ATTACKING...' : 'LAUNCH SNIPER'}
              </button>

              {isLaunching && (
                <div className="space-y-2 mt-4 animate-in fade-in duration-500">
                  <div className="flex justify-between text-[10px] font-bold text-orange-500 uppercase">
                    <span>Injecting Packets...</span>
                    <span>{progress}%</span>
                  </div>
                  <div className="w-full h-1.5 bg-white/5 rounded-full overflow-hidden">
                    <div className="h-full bg-orange-500 transition-all duration-200 ease-out" style={{ width: `${progress}%` }} />
                  </div>
                </div>
              )}
            </div>
          </div>

          <div className="lg:col-span-2 bg-[#0a0a0a] border border-white/10 rounded-2xl p-6 overflow-hidden relative">
            <div className="flex justify-between items-center mb-8">
              <h3 className="font-bold flex items-center gap-2"><BarChart3 size={18} className="text-orange-500"/> Real-time Load Distribution</h3>
            </div>
            <div className="h-[250px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={mockData}>
                  <defs>
                    <linearGradient id="colorOrders" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#ea580c" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#ea580c" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <Tooltip contentStyle={{backgroundColor: '#000', border: '1px solid #333', borderRadius: '8px'}} />
                  <Area type="monotone" dataKey="orders" stroke="#ea580c" strokeWidth={3} fillOpacity={1} fill="url(#colorOrders)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({ title, value, icon, change }: any) {
  return (
    <div className="bg-[#0a0a0a] border border-white/10 rounded-2xl relative overflow-hidden group p-6">
      <div className="absolute top-0 right-0 p-4 opacity-10">{icon}</div>
      <div className="space-y-2 relative z-10">
        <p className="text-xs font-bold text-slate-500 uppercase tracking-tighter">{title}</p>
        <div className="flex items-baseline gap-2">
          <h2 className="text-3xl font-black">{value}</h2>
          <span className="text-[10px] text-slate-400 font-bold">{change}</span>
        </div>
      </div>
    </div>
  );
}
