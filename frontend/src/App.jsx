import { Routes, Route, Navigate } from 'react-router-dom';
import ModuDashboard from '@/modules/modu/pages/Dashboard';
import BarkDashboard from '@/modules/bark/pages/BarkDashboard';

function App() {
  return (
  
      <Routes>
        {/* If user hits the root, send them to dashboard */}
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        
        {/* MODU World */}
        <Route path="/dashboard" element={<ModuDashboard />} />
        
        {/* BARK World */}
        <Route path="/bark" element={<BarkDashboard />} />
      </Routes>
  );
}

export default App;
