import React from 'react';

const VISA_TYPE_LABELS = {
  H1B: 'H-1B Work Visa',
  L1: 'L-1 Intracompany Transfer',
  O1: 'O-1 Extraordinary Ability',
  EB1: 'EB-1 Employment Based First',
  EB2: 'EB-2 Employment Based Second',
  EB3: 'EB-3 Employment Based Third',
  F1: 'F-1 Student Visa',
  GREEN_CARD: 'Green Card',
  CITIZENSHIP: 'Citizenship',
  ASYLUM: 'Asylum',
  OTHER: 'Other'
};

const STATUS_LABELS = {
  INITIAL_CONSULTATION: 'Initial Consultation',
  DOCUMENTS_GATHERING: 'Documents Gathering',
  APPLICATION_PREP: 'Application Preparation',
  FILED: 'Filed',
  RFE: 'Request for Evidence',
  APPROVED: 'Approved',
  DENIED: 'Denied',
  WITHDRAWN: 'Withdrawn'
};

const ClientList = ({ clients, onSelectClient }) => {
  if (clients.length === 0) {
    return (
      <div className="empty-state">
        <p>No clients found</p>
        <p style={{ fontSize: '0.9rem', color: '#999' }}>Click "Add New Client" to get started</p>
      </div>
    );
  }

  const formatDate = (dateString) => {
    if (!dateString) return 'Not set';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  return (
    <div className="card">
      <h2>Immigration Clients</h2>
      <p style={{ color: '#666', marginBottom: '1.5rem' }}>Manage all immigration cases and client information</p>
      <table>
        <thead>
          <tr>
            <th>Case Number</th>
            <th>Client Name</th>
            <th>Visa Type</th>
            <th>Status</th>
            <th>Country</th>
            <th>Filing Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {clients.map((client) => (
            <tr key={client._id}>
              <td><strong>{client.caseNumber}</strong></td>
              <td>{client.firstName} {client.lastName}</td>
              <td>{VISA_TYPE_LABELS[client.visaType]}</td>
              <td><span className="badge">{STATUS_LABELS[client.currentStatus]}</span></td>
              <td>{client.countryOfOrigin}</td>
              <td>{formatDate(client.filingDate)}</td>
              <td>
                <button
                  className="btn btn-small"
                  onClick={() => onSelectClient(client._id)}
                >
                  View
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ClientList;
