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

const ClientDetail = ({ client, onEdit, onDelete, onBack }) => {
  const formatDate = (dateString) => {
    if (!dateString) return 'Not set';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const formatDateTime = (dateString) => {
    if (!dateString) return 'Not set';
    return new Date(dateString).toLocaleString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit'
    });
  };

  return (
    <div className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h2>{client.firstName} {client.lastName}</h2>
        <div>
          <button className="btn" onClick={onEdit}>Edit</button>
          <button className="btn btn-danger" onClick={onDelete}>Delete</button>
        </div>
      </div>

      <div className="detail-grid">
        <div className="detail-section">
          <h3>Personal Information</h3>
          <div className="detail-item">
            <strong>Full Name:</strong>
            {client.firstName} {client.lastName}
          </div>
          <div className="detail-item">
            <strong>Email:</strong>
            <a href={`mailto:${client.email}`}>{client.email}</a>
          </div>
          <div className="detail-item">
            <strong>Phone:</strong>
            {client.phone || 'Not provided'}
          </div>
          <div className="detail-item">
            <strong>Country of Origin:</strong>
            {client.countryOfOrigin}
          </div>
        </div>

        <div className="detail-section">
          <h3>Case Information</h3>
          <div className="detail-item">
            <strong>Case Number:</strong>
            {client.caseNumber}
          </div>
          <div className="detail-item">
            <strong>Visa Type:</strong>
            {VISA_TYPE_LABELS[client.visaType]}
          </div>
          <div className="detail-item">
            <strong>Current Status:</strong>
            <span className="badge">{STATUS_LABELS[client.currentStatus]}</span>
          </div>
          <div className="detail-item">
            <strong>Filing Date:</strong>
            {formatDate(client.filingDate)}
          </div>
          <div className="detail-item">
            <strong>Priority Date:</strong>
            {formatDate(client.priorityDate)}
          </div>
        </div>
      </div>

      {client.notes && (
        <div style={{ marginTop: '2rem', paddingTop: '2rem', borderTop: '1px solid #ddd' }}>
          <h3>Notes</h3>
          <p style={{ whiteSpace: 'pre-wrap', marginTop: '1rem' }}>{client.notes}</p>
        </div>
      )}

      <div style={{ marginTop: '2rem', paddingTop: '2rem', borderTop: '1px solid #ddd', color: '#666', fontSize: '0.875rem' }}>
        <p>Created: {formatDateTime(client.createdAt)}</p>
        <p>Last Updated: {formatDateTime(client.updatedAt)}</p>
      </div>

      <div className="action-buttons">
        <button className="btn btn-secondary" onClick={onBack}>Back to List</button>
      </div>
    </div>
  );
};

export default ClientDetail;
