import ToolScroller from './components/ToolScroller';
import SideBarLeft from './components/LeftSideBar_Widget';
import SideBarRight from './components/RightSideBar_Widget';

export default function Dashboard() {
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
          <h1 className="text-3xl font-light tracking-[0.5em] text-white">MODU</h1>
        </div>

        {/* Right: Actions & Logo */}
        <div className="flex items-center gap-6">
            <button className="p-3 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 transition-colors">
              {/* Alert Icon */}
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
            </button>
            <button className="p-3 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 transition-colors">
              {/* Bell Icon */}
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg>
            </button>
            <div className="h-8 w-[1px] bg-white/20 mx-2" />
            <img src="/assets/Modu%20Favicon.png" alt="Logo" className="w-10 h-10 object-contain opacity-80" />
        </div>
      </header>

      {/* 3. Main Grid Layout */}
      <div className="relative z-10 grid grid-cols-[350px_1fr_350px] h-[calc(100vh-90px)] px-8 gap-8 pt-8">
        <aside className="h-full overflow-hidden pb-8">
          <SideBarLeft />
        </aside>

        <main className="h-full overflow-hidden relative">
           {/* Visual Guide Line for Center Stack */}
           <div className="absolute top-0 bottom-0 left-1/2 w-[1px] bg-gradient-to-b from-transparent via-white/10 to-transparent -translate-x-1/2 z-0" />
           <ToolScroller />
        </main>

        <aside className="h-full overflow-hidden pb-8">
          <SideBarRight />
        </aside>
      </div>
    </div>
  );
}
