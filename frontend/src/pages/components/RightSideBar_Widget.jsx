export default function SidebarRight() {
    return (
      <div className="flex flex-col gap-6 h-full">
        
        {/* 1. Tool Insights Widget */}
        <div className="bg-white/5 backdrop-blur-xl border border-white/10 p-8 rounded-[2rem] shadow-lg">
          <h3 className="text-white/60 text-xs font-bold uppercase tracking-[0.2em] mb-6">Tool Insights</h3>
          
          <div className="space-y-6">
            {/* Stat 1 */}
            <div>
              <div className="flex justify-between items-end mb-1">
                <span className="text-3xl font-light text-white">25</span>
                <span className="text-emerald-400 text-xs font-bold">+2 today</span>
              </div>
              <p className="text-[10px] text-white/40 uppercase tracking-widest">Bark Active Repairs</p>
              <div className="w-full h-1 bg-white/10 mt-3 rounded-full overflow-hidden">
                <div className="w-[60%] h-full bg-emerald-500 rounded-full" />
              </div>
            </div>
  
            {/* Stat 2 */}
            <div>
              <div className="flex justify-between items-end mb-1">
                <span className="text-3xl font-light text-white">40</span>
                <span className="text-white/40 text-xs">Total</span>
              </div>
              <p className="text-[10px] text-white/40 uppercase tracking-widest">Estimates This Month</p>
            </div>
  
            {/* Stat 3 - Financial */}
            <div className="pt-4 border-t border-white/10">
               <div className="flex items-center gap-2 mb-1">
                  <span className="text-white text-lg font-medium">Income</span>
                  <span className="bg-emerald-500/20 text-emerald-300 text-[10px] px-1.5 py-0.5 rounded font-bold">↑ 15%</span>
               </div>
               <p className="text-[10px] text-white/40">Compared to last month</p>
            </div>
          </div>
        </div>
  
        {/* 2. Inquire Now CTA Widget */}
        <div className="mt-auto bg-gradient-to-br from-indigo-600/20 to-purple-600/20 backdrop-blur-xl border border-white/10 p-8 rounded-[2rem] shadow-lg text-center">
          <div className="mb-4">
            <span className="text-2xl">🚀</span>
          </div>
          <h3 className="text-white font-bold text-lg mb-2">Need a Custom App?</h3>
          <p className="text-white/60 text-xs leading-relaxed mb-6">
            Does your business need a specific tool tailored to your workflow?
          </p>
          <button className="w-full py-3 bg-white text-indigo-900 rounded-xl font-bold text-sm hover:scale-105 transition-transform">
            INQUIRE NOW
          </button>
        </div>
  
      </div>
    );
  }