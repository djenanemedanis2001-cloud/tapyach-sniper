"use client"

import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { 
  LayoutDashboard, ShoppingCart, Crosshair, Users, Settings, 
  Search, Bell, Activity, DollarSign, Package, ArrowUpRight, Target, Zap, ServerCrash, CheckCircle2, ShieldAlert
} from 'lucide-react';
import { AreaChart, Area, XAxis, Tooltip, ResponsiveContainer } from 'recharts';

const salesData = [
  { time: 'Lun', sales: 4000 }, { time: 'Mar', sales: 3000 }, 
  { time: 'Mer', sales: 5000 }, { time: 'Jeu', sales: 2780 }, 
  { time: 'Ven', sales: 6890 }, { time: 'Sam', sales: 8390 }, { time: 'Dim', sales: 9490 },
];

export default function EcomMatrixDashboard() {
  const [activeTab, setActiveTab] = useState('GhostOrder'); // B' défaut y-tftah f' GhostOrder

  return (
    <div className="min-h-screen bg-[#020202] text-zinc-300 font-sans flex selection:bg-orange-500/30">
      
      {/* 📌 SIDEBAR (Menu Latéral) */}
      <aside className="w-64 border-r border-white/5 bg-[#050505] p-6 flex flex-col hidden md:flex">
        <div className="flex items-center gap-3 mb-12">
          <div className="bg-gradient-to-br from-orange-500 to-red-600 p-2 rounded-xl shadow-[0_0_15px_rgba(234,88,12,0.3)]">
            <Activity size={20} className="text-white" />
          </div>
          <h1 className="text-xl font-black tracking-tight text-white uppercase italic">
            ECOM<span className="text-orange-500">MATRIX</span>
          </h1>
        </div>

        <nav className="flex-1 space-y-2 text-sm font-medium">
          <NavItem icon={<LayoutDashboard size={18}/>} text="Dashboard" active={activeTab === 'Dashboard'} onClick={() => setActiveTab('Dashboard')} />
          <NavItem icon={<ShoppingCart size={18}/>} text="Commandes (OMS)" active={activeTab === 'OMS'} onClick={() => setActiveTab('OMS')} />
          {/* L'Onglet ta3 GhostOrder */}
          <NavItem icon={<Crosshair size={18}/>} text="GhostOrder (Sniper)" active={activeTab === 'GhostOrder'} onClick={() => setActiveTab('GhostOrder')} />
          <NavItem icon={<Users size={18}/>} text="Clients" active={activeTab === 'Clients'} onClick={() => setActiveTab('Clients')} />
        </nav>

        <div className="mt-auto border-t border-white/5 pt-6">
          <NavItem icon={<Settings size={18}/>} text="Paramètres" active={false} onClick={() => {}} />
        </div>
      </aside>

      {/* 📌 MAIN CONTENT AREA */}
      <main className="flex-1 flex flex-col h-screen overflow-hidden">
        
        {/* Top Header */}
        <header className="h-20 border-b border-white/5 bg-[#050505]/80 backdrop-blur flex items-center justify-between px-8">
          <div className="relative w-96 hidden lg:block">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-500" size={16} />
            <input 
              type="text" 
              placeholder="Chercher une commande (#ID, Nom...)" 
              className="w-full bg-[#111] border border-white/10 rounded-full h-10 pl-10 pr-4 text-sm focus:outline-none focus:border-orange-500/50 transition-colors"
            />
          </div>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 bg-orange-500/10 px-4 py-1.5 rounded-full border border-orange-500/20">
              <span className="w-2 h-2 rounded-full bg-orange-500 animate-pulse"></span>
              <span className="text-xs font-bold text-orange-500">Live Services</span>
            </div>
            <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-zinc-800 to-zinc-700 border border-white/10 flex items-center justify-center font-bold text-white shadow-inner">
              DZ
            </div>
          </div>
        </header>

        {/* 📌 DYNAMIC CONTENT (Changement d'Onglets) */}
        <div className="flex-1 overflow-y-auto p-8 bg-[#020202]">
          
          {/* ==================================================== */}
          {/* 1. ONGLET : DASHBOARD GÉNÉRAL */}
          {/* ==================================================== */}
          {activeTab === 'Dashboard' && (
            <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="max-w-7xl mx-auto space-y-8">
              <div className="flex items-end justify-between">
                <div>
                  <h2 className="text-3xl font-black text-white tracking-tight">Vue d'Ensemble</h2>
                  <p className="text-sm text-zinc-500 mt-1">Vos performances éducatives d'aujourd'hui.</p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <KPICard title="Chiffre d'Affaires" value="482,500 DA" icon={<DollarSign size={20} className="text-emerald-500"/>} trend="+14.5%" trendUp />
                <KPICard title="Commandes" value="124" icon={<ShoppingCart size={20} className="text-orange-500"/>} trend="+5.2%" trendUp />
                <KPICard title="Taux de Livraison" value="68.2%" icon={<Package size={20} className="text-blue-500"/>} trend="-2.1%" trendUp={false} />
              </div>

              <div className="bg-[#0a0a0a] border border-white/5 rounded-2xl p-6 shadow-xl">
                <h3 className="text-sm font-bold text-zinc-400 mb-6 uppercase tracking-widest">Évolution des Ventes</h3>
                <div className="h-[300px] w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={salesData}>
                      <defs>
                        <linearGradient id="colorSales" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#ea580c" stopOpacity={0.3}/>
                          <stop offset="95%" stopColor="#ea580c" stopOpacity={0}/>
                        </linearGradient>
                      </defs>
                      <XAxis dataKey="time" stroke="#3f3f46" fontSize={12} tickLine={false} axisLine={false} />
                      <Tooltip contentStyle={{backgroundColor: '#111', border: '1px solid #333', borderRadius: '8px', color: '#fff'}} />
                      <Area type="monotone" dataKey="sales" stroke="#ea580c" strokeWidth={3} fillOpacity={1} fill="url(#colorSales)" />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </motion.div>
          )}

          {/* ==================================================== */}
          {/* 2. ONGLET : GHOSTORDER (LE SNIPER LIVE FEED) */}
          {/* ==================================================== */}
          {activeTab === 'GhostOrder' && (
            <GhostOrderModule />
          )}

        </div>
      </main>
    </div>
  );
}

// ==========================================
// COMPOSANT: GHOSTORDER MODULE (Séparé w Nqi)
// ==========================================
function GhostOrderModule() {
  const [url, setUrl] = useState('');
  const [orders, setOrders] = useState(1);
  const [credits, setCredits] = useState(50);
  const [isLaunching, setIsLaunching] = useState(false);
  const [liveLogs, setLiveLogs] = useState<{time: string, text: string, type: string}[]>([]);
  const logsEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [liveLogs]);

  const addLog = (text: string, type: string = 'info') => {
    setLiveLogs(prev => [...prev, { time: new Date().toLocaleTimeString(), text, type }]);
  };

  const handleLaunch = () => {
    if (!url || !url.includes('http')) return alert("⚠️ Veuillez entrer une URL de produit valide (ex: https://...) !");
    if (credits < orders) return alert("❌ Crédits insuffisants !");
    
    setIsLaunching(true);
    setCredits(prev => prev - orders);
    setLiveLogs([{ time: new Date().toLocaleTimeString(), text: 'Connexion au serveur GHOSTORDER (Render)...', type: 'system' }]);

    // THE LIVE CABLE
    const eventSource = new EventSource(`https://tapyach-api.onrender.com/stream?url=${encodeURIComponent(url)}&orders=${orders}`);

    eventSource.onmessage = (event) => {
      if (!event.data) return; 
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'error') {
          addLog(data.msg, 'error');
          eventSource.close();
          setIsLaunching(false);
        } else if (data.type === 'success') {
          addLog(data.msg, 'success');
          eventSource.close();
          setIsLaunching(false);
        } else {
          let logType = 'info';
          if (data.msg.includes('🟢') || data.msg.includes('✅')) logType = 'success';
          if (data.msg.includes('🔴') || data.msg.includes('❌')) logType = 'error';
          if (data.msg.includes('👁️')) logType = 'highlight';
          addLog(data.msg, logType);
        }
      } catch (e) { }
    };

    eventSource.onerror = () => {
      addLog(`Fin de la transmission Live.`, 'system');
      eventSource.close();
      setIsLaunching(false);
    };
  };

  return (
    <motion.div initial={{ opacity: 0, scale: 0.98 }} animate={{ opacity: 1, scale: 1 }} className="grid grid-cols-1 xl:grid-cols-12 gap-8 max-w-7xl mx-auto">
      
      {/* Panneau de Contrôle */}
      <div className="xl:col-span-4 space-y-6">
        <div className="bg-[#0a0a0a] border border-white/5 rounded-2xl p-6 shadow-2xl relative overflow-hidden group">
          <div className="absolute inset-0 bg-gradient-to-br from-orange-600/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
          
          <div className="flex items-center gap-2 mb-8">
            <Target size={20} className="text-orange-500"/> 
            <h3 className="text-lg font-bold tracking-wider text-white">TARGET CONFIG</h3>
          </div>

          <div className="space-y-6 relative">
            <div className="space-y-3">
              <label className="text-xs font-bold text-zinc-500 uppercase tracking-widest">Store Product URL</label>
              <input 
                type="text" placeholder="https://store.com/product" 
                className="w-full bg-[#111] border border-white/10 focus:border-orange-500 outline-none h-12 rounded-xl text-white px-4 text-sm font-mono transition-colors"
                value={url} onChange={(e) => setUrl(e.target.value)} disabled={isLaunching}
              />
            </div>
            
            <div className="space-y-3">
              <label className="text-xs font-bold text-zinc-500 uppercase tracking-widest">Stress Load (Orders)</label>
              <input 
                type="number" min="1" max={credits}
                className="w-full bg-[#111] border border-white/10 focus:border-orange-500 outline-none h-12 rounded-xl text-white px-4 text-sm font-mono transition-colors"
                value={orders} onChange={(e) => setOrders(Number(e.target.value))} disabled={isLaunching}
              />
            </div>

            <button 
              onClick={handleLaunch} disabled={isLaunching || !url || credits === 0}
              className={`w-full h-14 rounded-xl text-lg font-black uppercase tracking-wider flex justify-center items-center gap-3 transition-all ${
                isLaunching 
                ? 'bg-zinc-800 text-zinc-500 cursor-not-allowed' 
                : 'bg-gradient-to-r from-orange-600 to-red-600 hover:from-orange-500 hover:to-red-500 text-white shadow-[0_0_20px_rgba(234,88,12,0.3)] active:scale-[0.98]'
              }`}
            >
              {isLaunching ? (<><Zap className="animate-ping" size={20}/> STRIKING...</>) : (<>EXECUTE STRIKE <Rocket size={20}/></>)}
            </button>
            <p className="text-center text-xs font-bold text-zinc-500 mt-4">Crédits restants : <span className="text-orange-500">{credits}</span></p>
          </div>
        </div>
      </div>

      {/* Console Live (Terminal Hacker) */}
      <div className="xl:col-span-8 bg-[#050505] border border-white/5 rounded-2xl overflow-hidden flex flex-col shadow-2xl relative">
        <div className="h-1 w-full bg-gradient-to-r from-orange-500 to-red-600"></div>
        <div className="bg-[#0a0a0a] px-6 py-4 flex items-center justify-between border-b border-white/5">
          <span className="text-xs font-bold text-zinc-400 tracking-widest uppercase flex items-center gap-2">
            <Activity size={14} className="text-orange-500"/> Live Server Output
          </span>
          <div className="flex gap-2">
            <div className="w-3 h-3 rounded-full bg-red-500/80"></div>
            <div className="w-3 h-3 rounded-full bg-yellow-500/80"></div>
            <div className="w-3 h-3 rounded-full bg-green-500/80"></div>
          </div>
        </div>
        
        <div className="flex-1 p-6 overflow-y-auto h-[450px] font-mono text-sm leading-relaxed" style={{ scrollBehavior: 'smooth' }}>
          {liveLogs.length === 0 ? (
            <div className="h-full flex items-center justify-center text-zinc-700">Awaiting target parameters...</div>
          ) : (
            <div className="space-y-3">
              {liveLogs.map((log, index) => (
                <div key={index} className="flex gap-4 border-b border-white/5 pb-2">
                  <span className="text-zinc-600 shrink-0">[{log.time}]</span>
                  <span className={`
                    ${log.type === 'system' ? 'text-zinc-400 font-bold' : ''}
                    ${log.type === 'info' ? 'text-zinc-300' : ''}
                    ${log.type === 'highlight' ? 'text-blue-400' : ''}
                    ${log.type === 'success' ? 'text-emerald-400 font-bold' : ''}
                    ${log.type === 'error' ? 'text-red-500 font-bold' : ''}
                  `}>
                    {log.text}
                  </span>
                </div>
              ))}
              <div ref={logsEndRef} />
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
}

// ==========================================
// UTILS
// ==========================================
function NavItem({ icon, text, active, onClick }: any) {
  return (
    <div 
      onClick={onClick}
      className={`flex items-center gap-3 px-4 py-3 rounded-xl cursor-pointer transition-all duration-200 ${
        active 
        ? 'bg-orange-600/10 text-orange-500 border border-orange-500/20 shadow-inner' 
        : 'text-zinc-400 hover:text-white hover:bg-white/5'
      }`}
    >
      {icon}
      <span className="font-bold tracking-wide">{text}</span>
    </div>
  );
}

function KPICard({ title, value, icon, trend, trendUp }: any) {
  return (
    <div className="bg-[#0a0a0a] border border-white/5 rounded-2xl p-6 shadow-xl relative overflow-hidden group hover:border-orange-500/30 transition-colors">
      <div className="flex justify-between items-start mb-4">
        <div className="p-3 bg-white/5 rounded-xl border border-white/5 group-hover:scale-110 transition-transform">
          {icon}
        </div>
        <div className={`text-xs font-bold px-2 py-1 rounded-md ${trendUp ? 'bg-emerald-500/10 text-emerald-500' : 'bg-red-500/10 text-red-500'}`}>
          {trend}
        </div>
      </div>
      <div>
        <p className="text-sm font-bold text-zinc-500 uppercase tracking-widest mb-1">{title}</p>
        <h3 className="text-3xl font-black text-white">{value}</h3>
      </div>
    </div>
  );
}
