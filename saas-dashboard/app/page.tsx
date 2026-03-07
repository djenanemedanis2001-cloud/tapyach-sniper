"use client"

import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { Rocket, ShieldAlert, CheckCircle2, Zap, Globe, TerminalSquare, Activity } from 'lucide-react';

export default function AdvancedGhostDashboard() {
  const [mounted, setMounted] = useState(false);
  const [url, setUrl] = useState('');
  const [orders, setOrders] = useState(1);
  const [credits, setCredits] = useState(50);
  const [isLaunching, setIsLaunching] = useState(false);
  const [liveLogs, setLiveLogs] = useState<{time: string, text: string, type: string}[]>([
    { time: new Date().toLocaleTimeString(), text: 'SYSTEM READY. AWAITING TARGET.', type: 'system' }
  ]);
  
  const logsEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll l'Logs ta3 l'Terminal
  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [liveLogs]);

  useEffect(() => {
    setMounted(true);
  }, []);

  const addLog = (text: string, type: string = 'info') => {
    setLiveLogs(prev => [...prev, { time: new Date().toLocaleTimeString(), text, type }]);
  };

  const handleLaunch = () => {
    if (!url || !url.includes('http')) return alert("⚠️ Entrez une URL de produit valide (ex: https://...) !");
    if (credits < orders) return alert("❌ Crédits insuffisants !");
    
    setIsLaunching(true);
    setCredits(prev => prev - orders);
    setLiveLogs([]); // Clear logs
    addLog(`INITIALIZING STRIKE SEQUENCE ON: ${url}`, 'system');

    // 🚀 THE LIVE CABLE (Server-Sent Events)
    // N-connectiw m3a l'API l'jdida ta3 Render bach t-jib l'ktiba f' l'waqt s7i7
    const eventSource = new EventSource(`https://tapyach-api.onrender.com/stream?url=${encodeURIComponent(url)}&orders=${orders}`);

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.type === 'detail') {
        addLog(`[PAYLOAD] Data générée -> ${data.msg}`, 'success');
      } else if (data.type === 'error') {
        addLog(`[FATAL] ${data.msg}`, 'error');
        eventSource.close();
        setIsLaunching(false);
      } else if (data.type === 'success') {
        addLog(`[MISSION COMPLETE] Toutes les commandes sont passées.`, 'success');
        eventSource.close();
        setIsLaunching(false);
      } else {
        addLog(data.msg, 'info');
      }
    };

    eventSource.onerror = () => {
      addLog(`[WARNING] Connexion Live coupée. Le Bot continue en arrière-plan.`, 'error');
      eventSource.close();
      setIsLaunching(false);
    };
  };

  if (!mounted) return null;

  return (
    <div dir="rtl" className="min-h-screen bg-[#050505] text-white font-sans selection:bg-orange-500/30 font-mono">
      
      {/* Navbar Cyberpunk */}
      <nav className="border-b border-orange-500/20 bg-black/80 backdrop-blur-md px-6 py-4 flex justify-between items-center" dir="ltr">
        <div className="flex items-center gap-3">
          <Zap size={24} className="text-orange-500 animate-pulse" />
          <h1 className="text-2xl font-black tracking-widest uppercase text-transparent bg-clip-text bg-gradient-to-r from-orange-400 to-red-600">
            GHOST<span className="text-white">ORDER.AI</span>
          </h1>
        </div>
        <div className="flex items-center gap-3 bg-orange-950/30 px-5 py-2 rounded-md border border-orange-500/30">
          <Activity size={16} className="text-orange-500" />
          <span className="text-xs font-bold text-gray-300">CRÉDITS :</span>
          <span className="text-orange-500 font-black text-lg">{credits}</span>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto p-6 mt-6 grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* --- LE RADAR (GAUCHE) --- */}
        <div className="lg:col-span-5 space-y-6">
          <div className="bg-[#0a0a0a] border border-white/10 rounded-xl p-8 shadow-2xl relative">
            <div className="flex items-center gap-2 mb-8 border-b border-white/10 pb-4">
              <Target size={20} className="text-orange-500"/> 
              <h3 className="text-xl font-bold tracking-widest text-gray-200">TARGET ACQUISITION</h3>
            </div>

            <div className="space-y-8">
              <div className="space-y-3">
                <label className="text-[10px] font-black text-orange-500/70 uppercase tracking-widest" dir="ltr">Product URL (YouCan / Shopify)</label>
                <input 
                  type="text" dir="ltr"
                  placeholder="https://store.com/product-1" 
                  className="w-full bg-black border border-white/10 focus:border-orange-500 outline-none h-14 rounded-lg text-white px-4 text-sm font-mono transition-colors"
                  value={url} onChange={(e) => setUrl(e.target.value)}
                  disabled={isLaunching}
                />
              </div>
              
              <div className="space-y-3">
                <label className="text-[10px] font-black text-orange-500/70 uppercase tracking-widest" dir="ltr">Stress Load (Orders)</label>
                <input 
                  type="number" min="1" max={credits} dir="ltr"
                  className="w-full bg-black border border-white/10 focus:border-orange-500 outline-none h-14 rounded-lg text-white px-4 text-sm font-mono transition-colors"
                  value={orders} onChange={(e) => setOrders(Number(e.target.value))}
                  disabled={isLaunching}
                />
              </div>

              <button 
                onClick={handleLaunch}
                disabled={isLaunching || !url || credits === 0}
                className="w-full h-16 bg-gradient-to-r from-orange-600 to-red-600 hover:from-orange-500 hover:to-red-500 text-white text-lg font-black tracking-widest rounded-lg shadow-[0_0_20px_rgba(234,88,12,0.4)] transition-all active:scale-95 disabled:opacity-50 flex justify-center items-center gap-3 uppercase"
              >
                {isLaunching ? (
                  <> <Zap className="animate-ping" size={20}/> STRIKING... </>
                ) : (
                  <> EXECUTE STRIKE <Rocket size={20} /> </>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* --- LE TERMINAL LIVE (DROITE) --- */}
        <div className="lg:col-span-7 bg-black border border-white/10 rounded-xl overflow-hidden flex flex-col shadow-2xl relative">
          {/* Ligne rouge l'fo9 (Style Hacker) */}
          <div className="h-1 w-full bg-gradient-to-r from-orange-500 to-red-600"></div>
          
          <div className="bg-[#111] px-4 py-3 flex items-center justify-between border-b border-white/5" dir="ltr">
            <div className="flex items-center gap-2">
              <TerminalSquare size={16} className="text-gray-400" />
              <span className="text-xs font-bold text-gray-400 tracking-widest uppercase">Live Command Feed</span>
            </div>
            <div className="flex gap-1.5">
              <div className="w-3 h-3 rounded-full bg-red-500/50"></div>
              <div className="w-3 h-3 rounded-full bg-yellow-500/50"></div>
              <div className="w-3 h-3 rounded-full bg-green-500/50"></div>
            </div>
          </div>
          
          {/* Écran d'affichage des Logs */}
          <div className="flex-1 p-6 overflow-y-auto h-[400px] text-left" dir="ltr">
            <div className="space-y-2">
              {liveLogs.map((log, index) => (
                <motion.div 
                  initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }}
                  key={index} 
                  className="text-sm font-mono"
                >
                  <span className="text-gray-600 mr-3">[{log.time}]</span>
                  <span className={`
                    ${log.type === 'system' ? 'text-blue-400 font-bold' : ''}
                    ${log.type === 'info' ? 'text-gray-300' : ''}
                    ${log.type === 'success' ? 'text-green-500 font-bold' : ''}
                    ${log.type === 'error' ? 'text-red-500 font-bold' : ''}
                  `}>
                    {log.type === 'system' ? '> ' : ''}{log.text}
                  </span>
                </motion.div>
              ))}
              <div ref={logsEndRef} />
            </div>
          </div>
        </div>

      </main>
    </div>
  );
}
