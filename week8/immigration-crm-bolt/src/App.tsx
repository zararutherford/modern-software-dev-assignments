import { useState } from 'react';
import { useAuth } from './contexts/AuthContext';
import Auth from './components/Auth';
import Layout from './components/Layout';
import Dashboard from './components/Dashboard';
import ClientList from './components/ClientList';
import ClientForm from './components/ClientForm';
import { Client } from './lib/supabase';

function App() {
  const { user, loading } = useAuth();
  const [currentView, setCurrentView] = useState<'dashboard' | 'clients'>('dashboard');
  const [selectedClient, setSelectedClient] = useState<Client | null | undefined>(undefined);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleSelectClient = (client: Client | null) => {
    setSelectedClient(client);
  };

  const handleCloseForm = () => {
    setSelectedClient(undefined);
  };

  const handleSave = () => {
    setRefreshTrigger((prev) => prev + 1);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-slate-700"></div>
      </div>
    );
  }

  if (!user) {
    return <Auth />;
  }

  return (
    <>
      <Layout currentView={currentView} onViewChange={setCurrentView}>
        {currentView === 'dashboard' ? (
          <Dashboard key={refreshTrigger} />
        ) : (
          <ClientList key={refreshTrigger} onSelectClient={handleSelectClient} />
        )}
      </Layout>

      {selectedClient !== undefined && (
        <ClientForm client={selectedClient} onClose={handleCloseForm} onSave={handleSave} />
      )}
    </>
  );
}

export default App;
