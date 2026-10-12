import { useState } from 'react';

function App() {
  const [logs, setLogs] = useState<string[]>(['[INIT] Engine Online.']);

  const addLog = (msg: string) => {
    const timestamp = new Date().toLocaleTimeString();
    setLogs((prev) => [`[${timestamp}] ${msg}`, ...prev]);
  };

  return (
    <div className="min-h-screen bg-[#0b0e14] text-[#f0f5ff] p-6">
      <header className="bg-[#121826] border border-[#1e293b] p-4 rounded-lg mb-6">
        <h1 className="text-xl font-bold text-[#00d2ff]">ROCKET LEAGUE MASTER ENGINE PRO</h1>
        <p className="text-[#00ffb4] text-sm font-bold">Safe Hotkeys: [F1] Fwd | [F2] Left | [F3] Right | [F4] Aerial</p>
      </header>

      <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-6">
        <button className="bg-[#006eb4] p-3 rounded font-bold" onClick={() => addLog("Launching RL...")}>Launch RL</button>
        <button className="bg-[#232d41] p-3 rounded font-bold text-[#00d2ff]" onClick={() => addLog("Launching G-HUB...")}>Launch G-HUB</button>
        <button className="bg-[#3b2815] p-3 rounded font-bold text-[#ffaa00]" onClick={() => addLog("Opening Pro Profiles...")}>Pro Profiles</button>
        <button className="bg-[#1d2836] p-3 rounded font-bold text-[#00ffc8]" onClick={() => addLog("Opening Config...")}>RL Config</button>
        <button className="bg-[#193732] p-3 rounded font-bold text-[#00ffb4]" onClick={() => addLog("Opening Lua Studio...")}>Lua Testing Studio</button>
      </div>

      <div className="flex gap-4 mb-6">
        <button className="flex-1 bg-[#00b478] p-4 rounded font-bold" onClick={() => addLog("MACRO ENGINE RUNNING.")}>RUN MACRO ENGINE</button>
        <button className="flex-1 bg-[#c83232] p-4 rounded font-bold" onClick={() => addLog("MACRO ENGINE STOPPED.")}>STOP MACRO ENGINE</button>
      </div>

      <div className="bg-[#070a0f] border border-[#1e293b] p-4 rounded h-64 overflow-y-auto">
        {logs.map((log, i) => <div key={i} className="text-[#64e696] font-mono text-sm">{log}</div>)}
      </div>
    </div>
  );
}

export default App;
