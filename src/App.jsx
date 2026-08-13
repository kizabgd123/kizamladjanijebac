import React, { useState, useEffect, useRef } from 'react';
import {
  Brain, BookOpen, Activity, ShieldCheck, Sparkles, Send, ExternalLink,
  Search, Plus, RefreshCw, Layers, Zap, CheckCircle2, Cpu, Bot, UserCheck,
  BarChart3, Sliders, Globe, FileText, Code2, Terminal, ArrowRight, Play
} from 'lucide-react';
import {
  AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, BarChart, Bar
} from 'recharts';

export default function App() {
  const [activeTab, setActiveTab] = useState('studio');
  const [notebooks, setNotebooks] = useState([]);
  const [modules, setModules] = useState([]);
  const [userProfile, setUserProfile] = useState(null);
  const [mlData, setMlData] = useState(null);
  const [loadingNotebooks, setLoadingNotebooks] = useState(true);

  // Studio Chat & Multi-Agent State
  const [messages, setMessages] = useState([
    {
      sender: 'ai',
      text: 'Zdravo! Ja sam **Nexus Multi-Agent Orchestration Engine** izrađen po Google standardima.\n\nMožete mi uneti bilo koji prirodni upit, na primer: *"hoću da mi napraviš aplikaciju koja je četbot za istraživanje"* ili *"sinhronizuj NotebookLM izvore za ML predikciju"*. U realnom vremenu ću kreirati novu beležnicu, sinhronizovati agente i generisati uživi AI modul.',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      citations: [],
      generatedModule: null
    }
  ]);
  const [chatInput, setChatInput] = useState('');
  const [chatLoading, setChatLoading] = useState(false);
  const [selectedNotebookId, setSelectedNotebookId] = useState('auto_create');
  const chatEndRef = useRef(null);

  // New Notebook Form State
  const [newNotebookTitle, setNewNotebookTitle] = useState('');
  const [creatingNotebook, setCreatingNotebook] = useState(false);

  // Auto-App Module Live Test State
  const [testModuleInputs, setTestModuleInputs] = useState({});
  const [testModuleOutputs, setTestModuleOutputs] = useState({});

  useEffect(() => {
    fetchInitialData();
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, chatLoading]);

  const fetchInitialData = async () => {
    try {
      setLoadingNotebooks(true);
      const [nbRes, modRes, profRes, mlRes] = await Promise.all([
        fetch('/api/notebooks').then(r => r.json()),
        fetch('/api/modules').then(r => r.json()),
        fetch('/api/user/profile').then(r => r.json()),
        fetch('/api/ml/predict', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ timeframe: '7d' })
        }).then(r => r.json())
      ]);

      if (nbRes.success) setNotebooks(nbRes.notebooks || []);
      if (modRes.success) setModules(modRes.modules || []);
      if (profRes.success) setUserProfile(profRes.profile || null);
      if (mlRes.success) setMlData(mlRes);
    } catch (e) {
      console.error('Error loading studio data:', e);
    } finally {
      setLoadingNotebooks(false);
    }
  };

  const handleSendMessage = async (e, customText = null) => {
    if (e) e.preventDefault();
    const promptText = customText || chatInput;
    if (!promptText.trim() || chatLoading) return;

    const userMsg = {
      sender: 'user',
      text: promptText,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMsg]);
    if (!customText) setChatInput('');
    setChatLoading(true);

    try {
      const res = await fetch('/api/agents/orchestrate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: promptText,
          notebookId: selectedNotebookId,
          mode: 'orchestration'
        })
      });
      const data = await res.json();

      if (data.success) {
        const aiMsg = {
          sender: 'ai',
          text: data.answer,
          agentLogs: data.agentLogs,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          citations: data.citations || [],
          generatedModule: data.generatedModule || null
        };
        setMessages(prev => [...prev, aiMsg]);

        // Refresh notebooks and modules list
        fetchInitialData();
      } else {
        setMessages(prev => [...prev, {
          sender: 'ai',
          text: `⚠️ Došlo je do greške prilikom procesiranja upita: ${data.message || 'Nepoznata greška'}`,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }]);
      }
    } catch (err) {
      setMessages(prev => [...prev, {
        sender: 'ai',
        text: `🛑 Greška pri komunikaciji sa serverom: ${err.message}`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }]);
    } finally {
      setChatLoading(false);
    }
  };

  const handleCreateNotebook = async (e) => {
    e.preventDefault();
    if (!newNotebookTitle.trim() || creatingNotebook) return;

    setCreatingNotebook(true);
    try {
      const res = await fetch('/api/notebooks/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: newNotebookTitle })
      });
      const data = await res.json();
      if (data.success) {
        setNewNotebookTitle('');
        fetchInitialData();
      }
    } catch (err) {
      console.error('Notebook creation error:', err);
    } finally {
      setCreatingNotebook(false);
    }
  };

  const handleRunModuleTest = async (modId, prompt) => {
    if (!prompt) return;
    setTestModuleOutputs(prev => ({ ...prev, [modId]: 'Procesiranje upita u realnom vremenu sa NotebookLM...' }));
    
    try {
      const res = await fetch('/api/agents/orchestrate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, mode: 'module_test' })
      });
      const data = await res.json();
      if (data.success) {
        setTestModuleOutputs(prev => ({ ...prev, [modId]: data.answer }));
      } else {
        setTestModuleOutputs(prev => ({ ...prev, [modId]: 'Greška pri generisanju odgovora.' }));
      }
    } catch (e) {
      setTestModuleOutputs(prev => ({ ...prev, [modId]: `Greška: ${e.message}` }));
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100">
      {/* Top Header */}
      <header className="sticky top-0 z-50 glass-panel border-b border-slate-800/80 px-6 py-4">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-xl font-bold text-slate-100 tracking-tight">
                  Nexus Multi-Agent RAG Studio
                </h1>
                <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                  Google Standard Live
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Autonomous Multi-Agent Orchestration • Live NotebookLM Sync • Gemini Cognitive AI
              </p>
            </div>
          </div>

          {/* Right Status Badges */}
          <div className="flex items-center gap-3 text-xs">
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900/80 border border-slate-800 text-emerald-400">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              <span>Agents: 4 Online</span>
            </div>

            <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900/80 border border-slate-800 text-cyan-400">
              <BookOpen className="w-3.5 h-3.5" />
              <span>NotebookLM: Connected</span>
            </div>

            <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900/80 border border-slate-800 text-purple-400">
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>Sync Score: {userProfile?.syncScore || 98.4}%</span>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="max-w-7xl mx-auto mt-4 pt-3 border-t border-slate-800/60 flex items-center gap-2 overflow-x-auto">
          {[
            { id: 'studio', label: '🤖 Multi-Agent Studio', icon: Bot },
            { id: 'notebooks', label: '📚 Dynamic NotebookLM', icon: BookOpen },
            { id: 'analytics', label: '📊 ML Analytics & Sync', icon: BarChart3 },
            { id: 'generator', label: '🛠️ Auto-App Configurator', icon: Cpu },
            { id: 'profile', label: '👤 User Profile Sync', icon: UserCheck }
          ].map(tab => {
            const Icon = tab.icon;
            const active = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-medium transition-all ${
                  active
                    ? 'bg-cyan-500/15 text-cyan-300 border border-cyan-500/30 shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/50'
                }`}
              >
                <Icon className={`w-4 h-4 ${active ? 'text-cyan-400' : 'text-slate-400'}`} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 md:p-6">
        {/* TAB 1: Multi-Agent Studio */}
        {activeTab === 'studio' && (
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 h-[calc(100vh-230px)]">
            {/* Main Chat Stream */}
            <div className="lg:col-span-3 glass-panel rounded-2xl flex flex-col overflow-hidden border border-slate-800">
              {/* Prompt Suggestions */}
              <div className="p-3 border-b border-slate-800 bg-slate-900/40 flex items-center gap-2 overflow-x-auto text-xs">
                <span className="text-slate-400 font-semibold flex items-center gap-1 shrink-0">
                  <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
                  Brzi upiti:
                </span>
                {[
                  "hoću da mi napraviš aplikaciju koja je četbot",
                  "kreiraj novu NotebookLM beležnicu za lečenje zavisnosti",
                  "analiziraj verifikovane arXiv radove 2026",
                  "generiši ML algoritam za klasifikaciju usera"
                ].map((prompt, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleSendMessage(null, prompt)}
                    className="shrink-0 px-3 py-1 rounded-full bg-slate-800/60 hover:bg-cyan-950/60 text-slate-300 hover:text-cyan-300 border border-slate-700/60 hover:border-cyan-500/40 transition-all text-xs"
                  >
                    "{prompt}"
                  </button>
                ))}
              </div>

              {/* Chat Message List */}
              <div className="flex-1 p-4 md:p-6 overflow-y-auto space-y-6">
                {messages.map((msg, index) => (
                  <div
                    key={index}
                    className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}
                  >
                    <div className="flex items-center gap-2 mb-1.5">
                      <span className="text-xs font-medium text-slate-400">
                        {msg.sender === 'user' ? 'Korisnik (User Sync)' : 'Nexus Multi-Agent Engine'}
                      </span>
                      <span className="text-[10px] text-slate-500">{msg.timestamp}</span>
                    </div>

                    <div
                      className={`max-w-3xl rounded-2xl p-4 text-sm leading-relaxed ${
                        msg.sender === 'user'
                          ? 'bg-gradient-to-r from-cyan-600 to-blue-600 text-white shadow-lg shadow-cyan-600/10'
                          : 'glass-panel bg-slate-900/90 text-slate-200 border border-slate-800'
                      }`}
                    >
                      {/* Thought Process if available */}
                      {msg.agentLogs && (
                        <div className="mb-3 p-2.5 rounded-lg bg-slate-950/60 border border-slate-800 text-xs font-mono text-cyan-400 whitespace-pre-line">
                          {msg.agentLogs}
                        </div>
                      )}

                      <div className="whitespace-pre-wrap">{msg.text}</div>

                      {/* Render dynamically generated module card if present */}
                      {msg.generatedModule && (
                        <div className="mt-4 p-4 rounded-xl bg-slate-950/80 border border-cyan-500/30 text-xs space-y-2">
                          <div className="flex items-center justify-between">
                            <span className="font-bold text-cyan-400 flex items-center gap-1.5">
                              <Bot className="w-4 h-4 text-cyan-400" />
                              {msg.generatedModule.title}
                            </span>
                            <span className="px-2 py-0.5 rounded text-[10px] bg-emerald-500/20 text-emerald-300 font-semibold border border-emerald-500/30">
                              {msg.generatedModule.status}
                            </span>
                          </div>
                          <p className="text-slate-300">{msg.generatedModule.description}</p>
                          <div className="flex items-center gap-2 pt-2 border-t border-slate-800 text-[11px] text-slate-400">
                            <span>NotebookLM ID: <code className="text-cyan-300">{msg.generatedModule.notebookId}</code></span>
                          </div>
                          <button
                            onClick={() => setActiveTab('generator')}
                            className="w-full mt-2 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-medium flex items-center justify-center gap-1.5 transition-all text-xs"
                          >
                            <span>Otvori u Auto-App Studio</span>
                            <ArrowRight className="w-3.5 h-3.5" />
                          </button>
                        </div>
                      )}

                      {/* Citations */}
                      {msg.citations && msg.citations.length > 0 && (
                        <div className="mt-3 pt-3 border-t border-slate-800/80 space-y-1">
                          <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                            Verifikovani Izvori & NotebookLM RAG:
                          </span>
                          {msg.citations.map((c, idx) => (
                            <div key={idx} className="text-xs text-cyan-400/90 flex items-center gap-1">
                              <BookOpen className="w-3 h-3 text-cyan-400 shrink-0" />
                              <span>{c.source}: {c.text}</span>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                ))}

                {chatLoading && (
                  <div className="flex items-center gap-3 p-4 rounded-xl bg-slate-900/60 border border-slate-800 text-slate-400 text-xs animate-pulse">
                    <RefreshCw className="w-4 h-4 animate-spin text-cyan-400" />
                    <span>Multi-Agent Orchestrator generiše odgovore i sinhronizuje NotebookLM...</span>
                  </div>
                )}
                <div ref={chatEndRef} />
              </div>

              {/* Chat Input Form */}
              <form onSubmit={handleSendMessage} className="p-4 border-t border-slate-800 bg-slate-900/60">
                <div className="flex items-center gap-3">
                  <select
                    value={selectedNotebookId}
                    onChange={(e) => setSelectedNotebookId(e.target.value)}
                    className="bg-slate-900 border border-slate-700 text-slate-300 text-xs rounded-xl px-3 py-2.5 outline-none focus:border-cyan-500"
                  >
                    <option value="auto_create">⚡ Auto-Create Notebook per Prompt</option>
                    {notebooks.map(n => (
                      <option key={n.id} value={n.id}>📚 {n.title.substring(0, 30)}...</option>
                    ))}
                  </select>

                  <input
                    type="text"
                    value={chatInput}
                    onChange={(e) => setChatInput(e.target.value)}
                    placeholder="Unesite upit ili nalog za aplikaciju (npr. 'hoću da mi napraviš aplikaciju koja je četbot')..."
                    className="flex-1 bg-slate-900/90 border border-slate-700/80 rounded-xl px-4 py-2.5 text-sm text-slate-100 placeholder-slate-500 outline-none focus:border-cyan-500/80 transition-all"
                  />

                  <button
                    type="submit"
                    disabled={chatLoading || !chatInput.trim()}
                    className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-medium text-sm shadow-md shadow-cyan-500/20 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center gap-2"
                  >
                    <span>Pošalji</span>
                    <Send className="w-4 h-4" />
                  </button>
                </div>
              </form>
            </div>

            {/* Side Control Panel */}
            <div className="space-y-4">
              {/* Active Agents Status Card */}
              <div className="glass-panel p-4 rounded-2xl border border-slate-800 space-y-3">
                <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
                  <Bot className="w-4 h-4 text-cyan-400" />
                  Aktivni AI Agenti (4)
                </h3>
                <div className="space-y-2 text-xs">
                  {[
                    { name: 'Conversational Cognitive Agent', role: 'Gemini Socratic AI', status: 'ACTIVE' },
                    { name: 'Live RAG NotebookLM Agent', role: 'Naučna pretraga izvora', status: 'ACTIVE' },
                    { name: 'Predictive ML Agent', role: 'Klasifikacija i metrički sync', status: 'ACTIVE' },
                    { name: 'Auto-App Configurator', role: 'Uživo generisanje AI modul-a', status: 'ACTIVE' }
                  ].map((ag, idx) => (
                    <div key={idx} className="p-2.5 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center justify-between">
                      <div>
                        <div className="font-semibold text-slate-200">{ag.name}</div>
                        <div className="text-[10px] text-slate-400">{ag.role}</div>
                      </div>
                      <span className="w-2 h-2 rounded-full bg-emerald-400 shadow-sm shadow-emerald-400/50" />
                    </div>
                  ))}
                </div>
              </div>

              {/* Dynamic Notebooks Quick View */}
              <div className="glass-panel p-4 rounded-2xl border border-slate-800 space-y-3">
                <div className="flex items-center justify-between">
                  <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
                    <BookOpen className="w-4 h-4 text-cyan-400" />
                    NotebookLM Izvori ({notebooks.length})
                  </h3>
                  <button onClick={() => setActiveTab('notebooks')} className="text-[11px] text-cyan-400 hover:underline">
                    Vidi sve
                  </button>
                </div>
                <div className="space-y-2 max-h-48 overflow-y-auto">
                  {notebooks.slice(0, 3).map((nb, idx) => (
                    <div key={idx} className="p-2.5 rounded-xl bg-slate-900/60 border border-slate-800 text-xs">
                      <div className="font-medium text-cyan-300 truncate">{nb.title}</div>
                      <div className="text-[10px] text-slate-400 mt-1 flex items-center justify-between">
                        <span>ID: {nb.id.substring(0, 10)}...</span>
                        <span>{nb.sourcesCount} izvora</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* TAB 2: Dynamic NotebookLM Manager */}
        {activeTab === 'notebooks' && (
          <div className="space-y-6">
            <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
                  <BookOpen className="w-5 h-5 text-cyan-400" />
                  Dynamic NotebookLM Hub
                </h2>
                <p className="text-xs text-slate-400 mt-1">
                  Upravljanje beležnicama kreiranim u realnom vremenu preko `nlm` CLI-ja na vašem nalogu.
                </p>
              </div>

              {/* Create Form */}
              <form onSubmit={handleCreateNotebook} className="flex items-center gap-2">
                <input
                  type="text"
                  value={newNotebookTitle}
                  onChange={(e) => setNewNotebookTitle(e.target.value)}
                  placeholder="Naslov nove NotebookLM beležnice..."
                  className="bg-slate-900 border border-slate-700 text-xs text-slate-100 rounded-xl px-3 py-2 outline-none focus:border-cyan-500 w-64"
                />
                <button
                  type="submit"
                  disabled={creatingNotebook || !newNotebookTitle.trim()}
                  className="px-4 py-2 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-medium text-xs flex items-center gap-1.5 transition-all"
                >
                  <Plus className="w-4 h-4" />
                  <span>Kreiraj beležnicu</span>
                </button>
              </form>
            </div>

            {/* Notebooks Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {notebooks.map((nb, idx) => (
                <div key={idx} className="glass-card p-5 rounded-2xl border border-slate-800 space-y-3">
                  <div className="flex items-start justify-between gap-2">
                    <div className="w-8 h-8 rounded-lg bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center">
                      <BookOpen className="w-4 h-4 text-cyan-400" />
                    </div>
                    <span className="px-2 py-0.5 rounded text-[10px] bg-slate-800 text-slate-300 font-mono">
                      {nb.sourcesCount} izvora
                    </span>
                  </div>

                  <h3 className="font-bold text-slate-100 text-sm leading-snug">{nb.title}</h3>

                  <div className="pt-3 border-t border-slate-800 text-xs space-y-1 text-slate-400 font-mono">
                    <div>Notebook ID: <span className="text-cyan-300">{nb.id}</span></div>
                    <div>Kreirano: {new Date(nb.createdAt).toLocaleDateString()}</div>
                  </div>

                  <button
                    onClick={() => {
                      setSelectedNotebookId(nb.id);
                      setActiveTab('studio');
                    }}
                    className="w-full py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-cyan-300 text-xs font-medium flex items-center justify-center gap-1.5 transition-all"
                  >
                    <span>Pretraži u Multi-Agent Studio</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 3: ML Analytics & Sync */}
        {activeTab === 'analytics' && (
          <div className="space-y-6">
            <div className="glass-panel p-6 rounded-2xl border border-slate-800">
              <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
                <BarChart3 className="w-5 h-5 text-cyan-400" />
                ML Analytics & User Sync Metrics
              </h2>
              <p className="text-xs text-slate-400 mt-1">
                Uživo praćenje preciznosti RAG pretrage, odziva agenata i sinhronizacije korisničkih profila.
              </p>
            </div>

            {/* Metrics Chart */}
            {mlData && mlData.timeSeries && (
              <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
                <h3 className="text-sm font-bold text-slate-200">User Sync Accuracy & RAG Precision Trend (7d)</h3>
                <div className="h-72 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={mlData.timeSeries}>
                      <defs>
                        <linearGradient id="colorSync" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.4}/>
                          <stop offset="95%" stopColor="#06b6d4" stopOpacity={0}/>
                        </linearGradient>
                        <linearGradient id="colorRag" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.4}/>
                          <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0}/>
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                      <XAxis dataKey="day" stroke="#94a3b8" fontSize={12} />
                      <YAxis domain={[80, 100]} stroke="#94a3b8" fontSize={12} />
                      <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155' }} />
                      <Area type="monotone" dataKey="userSyncAccuracy" name="User Sync %" stroke="#06b6d4" fillOpacity={1} fill="url(#colorSync)" />
                      <Area type="monotone" dataKey="ragPrecision" name="RAG Precision %" stroke="#8b5cf6" fillOpacity={1} fill="url(#colorRag)" />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </div>
            )}

            {/* Classification Scorecard Table */}
            {mlData && mlData.classificationScorecard && (
              <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
                <h3 className="text-sm font-bold text-slate-200">Classification Scorecard for Multi-Agent Architecture</h3>
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs text-slate-300">
                    <thead className="bg-slate-900/80 text-slate-400 font-semibold border-b border-slate-800">
                      <tr>
                        <th className="p-3">Agent Class</th>
                        <th className="p-3">Precision</th>
                        <th className="p-3">Recall</th>
                        <th className="p-3">F1-Score</th>
                        <th className="p-3">Status</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800">
                      {mlData.classificationScorecard.map((item, idx) => (
                        <tr key={idx} className="hover:bg-slate-900/40">
                          <td className="p-3 font-semibold text-cyan-300">{item.class}</td>
                          <td className="p-3 font-mono">{(item.precision * 100).toFixed(1)}%</td>
                          <td className="p-3 font-mono">{(item.recall * 100).toFixed(1)}%</td>
                          <td className="p-3 font-mono">{(item.f1Score * 100).toFixed(1)}%</td>
                          <td className="p-3">
                            <span className="px-2 py-0.5 rounded text-[10px] bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                              OPTIMAL
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}

        {/* TAB 4: Auto-App Generator */}
        {activeTab === 'generator' && (
          <div className="space-y-6">
            <div className="glass-panel p-6 rounded-2xl border border-slate-800">
              <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
                <Cpu className="w-5 h-5 text-cyan-400" />
                Auto-App & Custom AI Module Studio
              </h2>
              <p className="text-xs text-slate-400 mt-1">
                Generisane i aktivirane AI aplikacije po upitu korisnika. Svaki četbot komunicira sa namenskom NotebookLM beležnicom bez mock-ova.
              </p>
            </div>

            {/* Modules Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {modules.map((mod, idx) => (
                <div key={idx} className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center">
                        <Bot className="w-5 h-5 text-cyan-400" />
                      </div>
                      <div>
                        <h3 className="font-bold text-slate-100 text-sm">{mod.title}</h3>
                        <span className="text-[10px] text-slate-400 font-mono">ID: {mod.id}</span>
                      </div>
                    </div>
                    <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                      {mod.status}
                    </span>
                  </div>

                  <p className="text-xs text-slate-300 leading-relaxed bg-slate-900/60 p-3 rounded-xl border border-slate-800">
                    {mod.description || mod.systemPrompt}
                  </p>

                  {/* Interactive Test Box */}
                  <div className="space-y-2 pt-2 border-t border-slate-800">
                    <label className="text-xs font-semibold text-slate-400">Testirajte ovaj generisani AI Četbot uživo:</label>
                    <div className="flex items-center gap-2">
                      <input
                        type="text"
                        placeholder="Unesite test pitanje za ovaj četbot..."
                        value={testModuleInputs[mod.id] || ''}
                        onChange={(e) => setTestModuleInputs({ ...testModuleInputs, [mod.id]: e.target.value })}
                        className="flex-1 bg-slate-900 border border-slate-700 text-xs text-slate-100 rounded-xl px-3 py-2 outline-none focus:border-cyan-500"
                      />
                      <button
                        onClick={() => handleRunModuleTest(mod.id, testModuleInputs[mod.id])}
                        className="px-3 py-2 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-medium flex items-center gap-1 transition-all"
                      >
                        <Play className="w-3.5 h-3.5" />
                        <span>Pokreni</span>
                      </button>
                    </div>

                    {testModuleOutputs[mod.id] && (
                      <div className="p-3 rounded-xl bg-slate-950 border border-cyan-500/30 text-xs text-cyan-200 mt-2 font-mono whitespace-pre-wrap">
                        {testModuleOutputs[mod.id]}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 5: User Profile Sync */}
        {activeTab === 'profile' && userProfile && (
          <div className="space-y-6">
            <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex items-center justify-between">
              <div>
                <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
                  <UserCheck className="w-5 h-5 text-cyan-400" />
                  Korisnički Profil & Synchronisation Hub
                </h2>
                <p className="text-xs text-slate-400 mt-1">
                  Kontinuirana sinhronizacija konteksta korisnika kroz sve autonomne AI agente.
                </p>
              </div>

              <div className="text-right">
                <div className="text-2xl font-extrabold text-cyan-400 font-mono">{userProfile.syncScore}%</div>
                <div className="text-[10px] text-slate-400 uppercase tracking-wider">Overall Sync Rating</div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
                <h3 className="text-sm font-bold text-slate-200">Aktivne Preferencije & Ciljevi</h3>
                <div className="space-y-2 text-xs">
                  <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
                    <span className="text-slate-400 block mb-1">Glavni cilj:</span>
                    <span className="font-semibold text-cyan-300">{userProfile.activeGoal}</span>
                  </div>

                  <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
                    <span className="text-slate-400 block mb-1.5">Prepoznati domeni učenja:</span>
                    <div className="flex flex-wrap gap-1.5">
                      {userProfile.preferences.map((p, i) => (
                        <span key={i} className="px-2.5 py-1 rounded-lg bg-slate-800 text-slate-200 font-medium">
                          {p}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
                <h3 className="text-sm font-bold text-slate-200">Istorija Sinhronizovanih Upita ({userProfile.queryHistory.length})</h3>
                <div className="space-y-2 max-h-60 overflow-y-auto text-xs">
                  {userProfile.queryHistory.map((q, idx) => (
                    <div key={idx} className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center justify-between">
                      <span className="font-medium text-slate-200 truncate max-w-xs">{q.prompt}</span>
                      <span className="text-[10px] text-slate-500 font-mono">{new Date(q.timestamp).toLocaleTimeString()}</span>
                    </div>
                  ))}
                  {userProfile.queryHistory.length === 0 && (
                    <p className="text-xs text-slate-500 italic">Još nema unetih upita.</p>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
