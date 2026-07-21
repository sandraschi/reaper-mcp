import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AppLayout } from '@/components/layout/app-layout';
import { Dashboard } from '@/pages/dashboard';
import { Transport } from '@/pages/transport';
import { Tracks } from '@/pages/tracks';
import { Mixer } from '@/pages/mixer';
import { Settings } from '@/pages/settings';
import { Tools } from '@/pages/tools';
import { Reascript } from '@/pages/reascript';
import { Status } from '@/pages/status';
import { Help } from '@/pages/help';
import Logging from '@/pages/Logging';
import { ApiDocsPage } from './pages/api-docs';

function App() {
  return (
    <Router>
      <AppLayout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/transport" element={<Transport />} />
          <Route path="/tracks" element={<Tracks />} />
          <Route path="/mixer" element={<Mixer />} />
          <Route path="/tools" element={<Tools />} />
          <Route path="/reascript" element={<Reascript />} />
          <Route path="/status" element={<Status />} />
          <Route path="/help" element={<Help />} />
          <Route path="/api-docs" element={<ApiDocsPage />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/logs" element={<Logging />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AppLayout>
    </Router>
  );
}

export default App;
