import ToolScroller from "../components/ToolScroller";
import Sidebar from "../../../components/layout/Sidebar";
import RightPanel from "../../../components/layout/RightPanel";

export default function ModuDashboard() {
  return (
    <div className="relative min-h-screen w-full font-sans overflow-hidden text-white">
      
      {/* 1. Fixed Background Layer (Fixes Visibility Issue) */}
      <div 
        className="fixed inset-0 z-0 bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage: "url('/assets/Background/ModuHome%20Background%20JAN.png')",
          backgroundSize: "contain",
          backgroundPosition: "center top",
          backgroundRepeat: "no-repeat",
        }} 
      />
      {/* Dark Overlay for readability */}
      <div className="fixed inset-0 z-0 bg-black/40 backdrop-blur-[2px]" />

      {/* 2. Distinct Header Area */}
      <header className="relative z-50 flex justify-between items-center px-10 py-6 bg-black/20 backdrop-blur-md border-b border-white/10">
        
        {/* Left: User Profile */}
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-full bg-gradient-to-tr from-emerald-400 to-blue-500 p-[2px]">
            <div className="w-full h-full rounded-full bg-gray-900 flex items-center justify-center overflow-hidden">
                {/* Placeholder for user image, using initials for now */}
                <span className="font-bold text-lg">M</span>
            </div>
          </div>
          <div>
             <h3 className="text-lg font-bold leading-none">Good Morning, Martin!</h3>
             <p className="text-xs text-white/50 uppercase tracking-wider mt-1">Cloud Engineer</p>
          </div>
        </div>

        {/* Center: Brand */}
        <div className="absolute left-1/2 -translate-x-1/2">
          <h1 className="text-3xl font-light tracking-[0.5em] text-[#3ED6A5] drop-shadow-[0_2px_12px_rgba(62,214,165,0.35)]">MODU</h1>
        </div>

        {/* Right: Actions & Logo */}
        <div className="flex items-center gap-6">
            <button className="p-3 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 transition-colors">
              {/* Alert Icon */}
              <img
                src="assets/DesignElements/alert-icon.png"
                alt="Alerts"
                className="w-6 h-6 object-contain opacity-70 group-hover:opacity-100 transition-opacity"
              />
            </button>
            <button className="p-3 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 transition-colors">
              {/* Bell Icon */}
              <img 
                src="assets/DesignElements/notif-icon.png"
                alt="Notifications"
                className="w-6 h-6 object-contain opacity-70 group-hover:opactity-100 transition-opactity"
              />
            </button>
            <div className="h-8 w-[1px] bg-white/20 mx-2" />
            <img
              src="/assets/Icons/modu-favicon.png"
              alt="Logo"
              className="w-24 h-24 object-contain opacity-100 drop-shadow-[0_2px_10px_rgba(0,0,0,0.35)]"
            />
        </div>
      </header>

      {/* 3. Main Grid Layout */}
      <div className="relative z-10 grid grid-cols-[350px_1fr_350px] h-[calc(100vh-90px)] px-8 gap-8 pt-8">
        <aside className="h-full overflow-hidden pb-8">
          <Sidebar />
        </aside>

        <main className="h-full overflow-hidden relative">
           {/* Visual Guide Line for Center Stack */}
           <div className="absolute top-0 bottom-0 left-1/2 w-[1px] bg-gradient-to-b from-transparent via-white/10 to-transparent -translate-x-1/2 z-0" />
           <ToolScroller />
        </main>

        <aside className="h-full overflow-hidden pb-8">
          <RightPanel />
        </aside>
      </div>
    </div>
  );
}
