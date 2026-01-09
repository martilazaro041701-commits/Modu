import { LayoutDashboard, Users, BarChart3, FileText, Settings } from 'lucide-react';

const BarkSidebar = () => {
    return(
       <div className="w-64 bg-white border-r border-gray-100 flex flex-col p-6 h-screen">
      <div className="flex items-center gap-2 mb-10">
        <div className="w-8 h-8 bg-indigo-600 rounded-lg"></div>
        <span className="text-xl font-bold">Tracker</span>
      </div>

      <nav className="flex flex-col gap-2">
        <NavItem icon={<LayoutDashboard size={20}/>} label="Dashboard" active />
        <NavItem icon={<Users size={20}/>} label="Customers" />
        <NavItem icon={<BarChart3 size={20}/>} label="Analytics" />
        <NavItem icon={<FileText size={20}/>} label="Reports" />
        <NavItem icon={<Settings size={20}/>} label="Settings" />
      </nav>
    </div>
  );
};

const NavItem = ({ icon, label, active }) => (
  <div className={`flex items-center gap-3 p-3 rounded-xl cursor-pointer transition-all ${
    active ? 'bg-bark-primary text-white shadow-lg' : 'text-gray-500 hover:bg-gray-50'
  }`}>
    {icon}
    <span className="font-semibold">{label}</span>
  </div>
); 
