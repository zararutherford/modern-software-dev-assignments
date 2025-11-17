import React, { useState, useEffect } from 'react';
import ClientList from './components/ClientList';
import ClientDetail from './components/ClientDetail';
import ClientForm from './components/ClientForm';
import { getAllClients, getClient, createClient, updateClient, deleteClient } from './services/api';
import './App.css';

function App() {
  const [view, setView] = useState('list'); // 'list', 'detail', 'create', 'edit'
  const [clients, setClients] = useState([]);
  const [selectedClient, setSelectedClient] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchClients();
  }, []);

  const fetchClients = async () => {
    try {
      setLoading(true);
      const data = await getAllClients();
      setClients(data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch clients. Make sure the server is running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectClient = async (clientId) => {
    try {
      const client = await getClient(clientId);
      setSelectedClient(client);
      setView('detail');
    } catch (err) {
      setError('Failed to fetch client details');
      console.error(err);
    }
  };

  const handleCreateClient = async (clientData) => {
    try {
      await createClient(clientData);
      await fetchClients();
      setView('list');
      setError(null);
    } catch (err) {
      setError('Failed to create client. ' + (err.response?.data?.message || err.message));
      console.error(err);
    }
  };

  const handleUpdateClient = async (clientData) => {
    try {
      await updateClient(selectedClient._id, clientData);
      await fetchClients();
      const updated = await getClient(selectedClient._id);
      setSelectedClient(updated);
      setView('detail');
      setError(null);
    } catch (err) {
      setError('Failed to update client. ' + (err.response?.data?.message || err.message));
      console.error(err);
    }
  };

  const handleDeleteClient = async () => {
    if (window.confirm(`Are you sure you want to delete ${selectedClient.firstName} ${selectedClient.lastName}?`)) {
      try {
        await deleteClient(selectedClient._id);
        await fetchClients();
        setView('list');
        setSelectedClient(null);
        setError(null);
      } catch (err) {
        setError('Failed to delete client');
        console.error(err);
      }
    }
  };

  return (
    <div className="app">
      <nav className="navbar">
        <h1>Immigration Client CRM</h1>
        <div className="navbar-links">
          <button onClick={() => { setView('list'); setSelectedClient(null); }}>
            All Clients
          </button>
          <button onClick={() => setView('create')}>
            Add New Client
          </button>
        </div>
      </nav>

      <div className="container">
        {error && (
          <div className="error-message">
            {error}
            <button
              style={{ marginLeft: '1rem', padding: '0.25rem 0.5rem' }}
              onClick={() => setError(null)}
            >
              Dismiss
            </button>
          </div>
        )}

        {loading ? (
          <div className="loading">Loading...</div>
        ) : (
          <>
            {view === 'list' && (
              <ClientList
                clients={clients}
                onSelectClient={handleSelectClient}
              />
            )}

            {view === 'detail' && selectedClient && (
              <ClientDetail
                client={selectedClient}
                onEdit={() => setView('edit')}
                onDelete={handleDeleteClient}
                onBack={() => setView('list')}
              />
            )}

            {view === 'create' && (
              <ClientForm
                onSubmit={handleCreateClient}
                onCancel={() => setView('list')}
              />
            )}

            {view === 'edit' && selectedClient && (
              <ClientForm
                client={selectedClient}
                onSubmit={handleUpdateClient}
                onCancel={() => setView('detail')}
              />
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default App;
