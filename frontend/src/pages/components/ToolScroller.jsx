import { motion} from 'framer-motion';


/* APP CARDS */

const APPS = [
  {
    id:'bark',
    name: 'BARK',
    logo: '/assets/Icons/Bark Favicon.png',
    badge: 'LIVE',
    badgeColor : 'bg-emerald-500 text-emerald-950',
    tagline: 'Your Personal Repair Intelligence System',
    version: 'Version 1.0',
    description: 'A centralized kernel transitioning automotive shops from static sheets to real-time data. Manage repair lifecycles, technician assignments, and turn manual logs into actionable analytics.'
  },
  {
    id: 'covy',
    name: 'COVYScope',
    logo: '/assets/Icons/COVYScope App Logo.png',
    badge: 'OFFLINE',
    badgeColor: 'bg-gray-500 text-gray-200',
    tagline: 'TBD',
    version: 'Prototyping Phase',
    description: 'Your Future AI Assisted Warehouse Tracking System with OPEN CV Coming soon.'
  },
  {
    id: 'admin',
    name: 'ADMIN',
    logo: '/assets/Icons/Admin Favicon.png',
    logoClassName: "scale-90",
    badge: 'LIVE',
    badgeColor: 'bg-blue-500 text-blue-950',
    tagline: 'System Configuration',
    version: 'v1.0',
    description: 'Manage your MODU Settings through here'
  }
];

export default function ToolScroller() {
  return (
    /* The container is now a vertical scroll area with snapping */
    <div className="h-full w-full overflow-y-auto snap-y snap-mandatory no-scrollbar flex flex-col gap-8 py-[15vh]">
      {/* Spacer to allow the first and last items to center */}
      <div className="shrink-0 h-[150px]" /> 

      {APPS.map((app) => (
        <motion.div
          key={app.id}
          initial={{ opacity: 0.3, scale: 0.9 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ amount: 0.8, margin: "-10% 0px -10% 0px" }}
          transition={{ duration: 0.4, ease: "easeOut" }}
          className="snap-center shrink-0 w-full max-w-[500px] mx-auto cursor-default rounded-[2.5rem] bg-white/5 border border-white/10 backdrop-blur-xl overflow-hidden group shadow-2xl"
        >
         
          <div className="p-10 flex flex-col items-start text-left h-full relative">

            {/* Header: Logo + Name + Badges */}
            <div className="flex items-center justify-between w-full mb-6">
              <div className="flex items-center gap-4">
                <div className="w-14 h-14 rounded-2xl bg-white/10 p-2 border border-white/10">
                  <img
                    src={app.logo}
                    className={`w-full h-full object-contain ${app.logoClassName || ""}`.trim()}
                    alt={`${app.name} logo`}
                  />
              </div>
              <div>
              <h2 className="text-3xl font-bold text-white tracking-wide">{app.name}</h2>
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${app.badgeColor}`}>
                {app.badge}
                </span>
            </div>
          </div>
          <p className="text-white/30 text xs font-mono">{app.version}</p>
        </div>

          {/* Description Body */}
            <div className="mb-8 space-y-4">
               <p className="text-emerald-400 text-xs font-bold uppercase tracking-widest">{app.tagline}</p>
               <p className="text-white/70 text-sm leading-relaxed font-light">
                 {app.description}
               </p>
            </div>

            {/* Action Button - Only shows 'Start' if LIVE */}
            <div className="w-full mt-auto">
              {app.badge === 'LIVE' ? (
                <button className="w-full py-4 bg-white text-emerald-950 rounded-xl font-bold tracking-wider hover:bg-modu-mint hover:scale-[1.02] transition-all shadow-lg">
                  START APPLICATION
                </button>
              ) : (
                <button disabled className="w-full py-4 bg-white/5 text-white/30 rounded-xl font-bold tracking-wider cursor-not-allowed border border-white/5">
                  COMING SOON
                </button>
              )}
            </div>
          </div>
        </motion.div>
      ))}
    </div>
  );
}
