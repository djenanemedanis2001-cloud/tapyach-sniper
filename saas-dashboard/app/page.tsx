"use client"

import React, { useState, useEffect, useRef } from 'react';
import { Target, Activity, Zap, ServerCrash, CheckCircle2, ShieldAlert } from 'lucide-react';

export default function ProDashboard() {
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
    if (!url || !url.includes('http')) return alert("⚠️ Veuillez entrer une URL valide !");
    if (credits < orders) return alert("❌ Crédits insuffisants !");
    
    setIsLaunching(true);
    setCredits(prev => prev - orders);
    setLiveLogs([{ time: new Date().toLocaleTimeString(), text: 'Connexion au serveur ECOM MATRIX...', type: 'system' }]);

    // Hna y-bda l'Live Feed s7i7 men l'API
    const eventSource = new EventSource(`https://tapyach-api.onrender.com/stream?url=${encodeURIComponent(url)}&orders=${orders}`);

    eventSource.onmessage = (event) => {
      // Ignorer les pings ta3 l'serveur
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
          // Coloration des mots clés f' l'Logs
          let logType = 'info';
          if (data.msg.includes('🟢') || data.msg.includes('✅')) logType = 'success';
          if (data.msg.includes('🔴') || data.msg.includes('❌')) logType = 'error';
          if (data.msg.includes('👁️')) logType = 'highlight';
          
          addLog(data.msg, logType);
        }
      } catch (e) {
        console.log("Ping reçu");
      }
    };

    eventSource.onerror = () => {
      addLog(`Fin de la transmission ou coupure réseau.`, 'system');
      eventSource.close();
      setIsLaunching(false);
    };
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 font-sans selection:bg-orange-500/30">
      
      {/* Top Navigation (Style Shopify) */}
      <nav className="bg-white border-b border-gray-200 px-8 py-4 flex justify-between items-center shadow-sm">
        <div className="flex items-center gap-2">
          <div className="bg-orange-600 p-2 rounded-lg">
            <ServerCrash size={20} className="text-white" />
          </div>
          <h1 className="text-2xl font-black tracking-tight text-gray-900">ECOM <span className="text-orange-600">MATRIX</span></h1>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 bg-gray-100 px-4 py-2 rounded-lg border border-gray-200">
            <Activity size={16} className="text-gray-500" />
            <span className="text-sm font-bold text-gray-600">Crédits Test:</span>
            <span className="text-orange-600 font-black">{credits}</span>
          </div>
          <button className="bg-gray-900 text-white px-5 py-2 rounded-lg text-sm font-bold shadow hover:bg-gray-800 transition">
            Upgrade Plan
          </button>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto p-8 mt-4 grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Panneau de Configuration */}
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-xl shadow-gray-200/50">
            <h3 className="text-lg font-black text-gray-900 mb-6 flex items-center gap-2 uppercase tracking-wide">
              <Target size={18} className="text-orange-600"/> Nouvelle Campagne
            </h3>

            <div className="space-y-5">
              <div>
                <label className="block text-xs font-bold text-gray-500 uppercase mb-2">Lien du Produit (YouCan/Shopify)</label>
                <input 
                  type="url" 
                  placeholder="https://store.com/produit" 
                  className="w-full bg-gray-50 border border-gray-300 focus:border-orange-500 focus:ring-2 focus:ring-orange-500/20 outline-none h-12 rounded-xl px-4 text-sm font-medium transition-all"
                  value={url} onChange={(e) => setUrl(e.target.value)}
                  disabled={isLaunching}
                />
              </div>
              
              <div>
                <label className="block text-xs font-bold text-gray-500 uppercase mb-2">Volume de Commandes</label>
                <input 
                  type="number" min="1" max={credits}
                  className="w-full bg-gray-50 border border-gray-300 focus:border-orange-500 focus:ring-2 focus:ring-orange-500/20 outline-none h-12 rounded-xl px-4 text-sm font-medium transition-all"
                  value={orders} onChange={(e) => setOrders(Number(e.target.value))}
                  disabled={isLaunching}
                />
              </div>

              <button 
                onClick={handleLaunch}
                disabled={isLaunching || !url || credits === 0}
                className={`w-full h-14 rounded-xl text-lg font-black uppercase tracking-wider flex justify-center items-center gap-2 transition-all ${
                  isLaunching 
                  ? 'bg-gray-200 text-gray-400 cursor-not-allowed border border-gray-300' 
                  : 'bg-orange-600 hover:bg-orange-700 text-white shadow-lg shadow-orange-600/30 hover:shadow-orange-600/50 active:scale-[0.98]'
                }`}
              >
                {isLaunching ? (
                  <> <Zap className="animate-pulse" size={20}/> EN COURS... </>
                ) : (
                  <> LANCER LE TEST </>
                )}
              </button>
            </div>
          </div>

          <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
            <h4 className="text-sm font-bold text-gray-900 mb-4">Statistiques du Mois</h4>
            <div className="space-y-4">
              <div className="flex justify-between items-center border-b border-gray-100 pb-2">
                <span className="text-sm text-gray-500">Succès Pixel Firing</span>
                <span className="font-bold text-emerald-600 flex items-center gap-1"><CheckCircle2 size={14}/> 99.8%</span>
              </div>
              <div className="flex justify-between items-center border-b border-gray-100 pb-2">
                <span className="text-sm text-gray-500">WAF Bypassed</span>
                <span className="font-bold text-blue-600 flex items-center gap-1"><ShieldAlert size={14}/> 1,402</span>
              </div>
            </div>
          </div>
        </div>

        {/* Panneau des Logs Live (Console) */}
        <div className="lg:col-span-2 bg-gray-900 rounded-2xl overflow-hidden shadow-2xl flex flex-col border border-gray-800">
          <div className="bg-gray-950 px-6 py-4 flex items-center justify-between border-b border-gray-800">
            <span className="text-xs font-bold text-gray-400 tracking-widest uppercase">Console d'Exécution Live</span>
            <div className="flex gap-2">
              <div className="w-3 h-3 rounded-full bg-red-500"></div>
              <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
              <div className="w-3 h-3 rounded-full bg-green-500"></div>
            </div>
          </div>
          
          <div className="flex-1 p-6 overflow-y-auto h-[500px] font-mono text-sm leading-relaxed">
            {liveLogs.length === 0 && (
              <div className="h-full flex items-center justify-center text-gray-600">
                Awaiting commands...
              </div>
            )}
            
            <div className="space-y-3">
              {liveLogs.map((log, index) => (
                <div key={index} className="flex gap-4 border-b border-gray-800/50 pb-2">
                  <span className="text-gray-600 shrink-0">[{log.time}]</span>
                  <span className={`
                    ${log.type === 'system' ? 'text-gray-400 font-bold' : ''}
                    ${log.type === 'info' ? 'text-gray-300' : ''}
                    ${log.type === 'highlight' ? 'text-blue-400' : ''}
                    ${log.type === 'success' ? 'text-emerald-400 font-bold bg-emerald-400/10 px-2 rounded' : ''}
                    ${log.type === 'error' ? 'text-red-400 font-bold bg-red-400/10 px-2 rounded' : ''}
                  `}>
                    {log.text}
                  </span>
                </div>
              ))}
              <div ref={logsEndRef} />
            </div>
          </div>
        </div>

      </main>
    </div>
  );
}
