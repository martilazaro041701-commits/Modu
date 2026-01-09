import { useState, useEffect } from 'react';

export default function Sidebar() {
  // Mock Data - In real app this comes from API
  const [activities, setActivities] = useState([
    { id: 1, text: "Created new customer data", app: "BARK", time: "10m ago" },
    { id: 2, text: "Updated Montero Status: Waiting for Parts", app: "BARK", time: "25m ago" },
    { id: 3, text: "System Config Update", app: "ADMIN", time: "1h ago" }, 
  ]);

  const [time, setTime] = useState(new Date());

  // Clock Ticker
  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="flex flex-col gap-6 h-full">
      
      {/* 1. Clock & Calendar Widget */}
      <div className="bg-white/5 backdrop-blur-xl border border-white/10 p-6 rounded-[2rem] shadow-lg">
        <h2 className="text-4xl font-light text-white tracking-tight">
          {time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </h2>
        <p className="text-emerald-400 text-sm font-bold uppercase tracking-widest mt-1">
          {time.toLocaleDateString([], { weekday: 'long', month: 'long', day: 'numeric' })}
        </p>
      </div>

      {/* 2. Recent Activity Widget */}
      <div className="flex-1 bg-white/5 backdrop-blur-xl border border-white/10 p-6 rounded-[2rem] shadow-lg flex flex-col overflow-hidden">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-white/60 text-xs font-bold uppercase tracking-[0.2em]">Recents</h3>
          <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
        </div>

        <div className="flex-1 overflow-y-auto space-y-4 pr-2 custom-scrollbar">
          {activities.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-white/30">
               <span className="text-sm italic">NO RECENT ACTIVITY</span>
            </div>
          ) : (
            activities.slice(0, 5).map((activity) => (
              <div key={activity.id} className="p-4 rounded-xl bg-white/5 border border-white/5 hover:bg-white/10 transition-colors">
                <div className="flex justify-between mb-1">
                  <span className="text-[10px] bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded uppercase font-bold">{activity.app}</span>
                  <span className="text-[10px] text-white/40">{activity.time}</span>
                </div>
                <p className="text-sm text-white/90 leading-snug mt-2">
                  {activity.text}
                </p>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
