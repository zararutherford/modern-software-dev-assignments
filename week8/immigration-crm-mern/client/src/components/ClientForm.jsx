import React, { useState, useEffect } from 'react';

const VISA_TYPES = [
  { value: 'H1B', label: 'H-1B Work Visa' },
  { value: 'L1', label: 'L-1 Intracompany Transfer' },
  { value: 'O1', label: 'O-1 Extraordinary Ability' },
  { value: 'EB1', label: 'EB-1 Employment Based First' },
  { value: 'EB2', label: 'EB-2 Employment Based Second' },
  { value: 'EB3', label: 'EB-3 Employment Based Third' },
  { value: 'F1', label: 'F-1 Student Visa' },
  { value: 'GREEN_CARD', label: 'Green Card' },
  { value: 'CITIZENSHIP', label: 'Citizenship' },
  { value: 'ASYLUM', label: 'Asylum' },
  { value: 'OTHER', label: 'Other' }
];

const STATUS_OPTIONS = [
  { value: 'INITIAL_CONSULTATION', label: 'Initial Consultation' },
  { value: 'DOCUMENTS_GATHERING', label: 'Documents Gathering' },
  { value: 'APPLICATION_PREP', label: 'Application Preparation' },
  { value: 'FILED', label: 'Filed' },
  { value: 'RFE', label: 'Request for Evidence' },
  { value: 'APPROVED', label: 'Approved' },
  { value: 'DENIED', label: 'Denied' },
  { value: 'WITHDRAWN', label: 'Withdrawn' }
];

const ClientForm = ({ client, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    caseNumber: '',
    visaType: 'H1B',
    currentStatus: 'INITIAL_CONSULTATION',
    countryOfOrigin: '',
    filingDate: '',
    priorityDate: '',
    notes: ''
  });

  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (client) {
      setFormData({
        firstName: client.firstName || '',
        lastName: client.lastName || '',
        email: client.email || '',
        phone: client.phone || '',
        caseNumber: client.caseNumber || '',
        visaType: client.visaType || 'H1B',
        currentStatus: client.currentStatus || 'INITIAL_CONSULTATION',
        countryOfOrigin: client.countryOfOrigin || '',
        filingDate: client.filingDate ? client.filingDate.split('T')[0] : '',
        priorityDate: client.priorityDate ? client.priorityDate.split('T')[0] : '',
        notes: client.notes || ''
      });
    }
  }, [client]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validate = () => {
    const newErrors = {};
    if (!formData.firstName.trim()) newErrors.firstName = 'First name is required';
    if (!formData.lastName.trim()) newErrors.lastName = 'Last name is required';
    if (!formData.email.trim()) newErrors.email = 'Email is required';
    if (!formData.caseNumber.trim()) newErrors.caseNumber = 'Case number is required';
    if (!formData.countryOfOrigin.trim()) newErrors.countryOfOrigin = 'Country is required';

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      onSubmit(formData);
    }
  };

  return (
    <div className="card">
      <h2>{client ? 'Update' : 'Create'} Client</h2>

      <form onSubmit={handleSubmit}>
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="firstName">First Name *</label>
            <input
              type="text"
              id="firstName"
              name="firstName"
              className="form-control"
              value={formData.firstName}
              onChange={handleChange}
              placeholder="First Name"
            />
            {errors.firstName && <div className="error-message">{errors.firstName}</div>}
          </div>

          <div className="form-group">
            <label htmlFor="lastName">Last Name *</label>
            <input
              type="text"
              id="lastName"
              name="lastName"
              className="form-control"
              value={formData.lastName}
              onChange={handleChange}
              placeholder="Last Name"
            />
            {errors.lastName && <div className="error-message">{errors.lastName}</div>}
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="email">Email *</label>
            <input
              type="email"
              id="email"
              name="email"
              className="form-control"
              value={formData.email}
              onChange={handleChange}
              placeholder="email@example.com"
            />
            {errors.email && <div className="error-message">{errors.email}</div>}
          </div>

          <div className="form-group">
            <label htmlFor="phone">Phone</label>
            <input
              type="tel"
              id="phone"
              name="phone"
              className="form-control"
              value={formData.phone}
              onChange={handleChange}
              placeholder="+1234567890"
            />
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="caseNumber">Case Number *</label>
          <input
            type="text"
            id="caseNumber"
            name="caseNumber"
            className="form-control"
            value={formData.caseNumber}
            onChange={handleChange}
            placeholder="CASE-XXX-XXXX"
          />
          {errors.caseNumber && <div className="error-message">{errors.caseNumber}</div>}
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="visaType">Visa Type *</label>
            <select
              id="visaType"
              name="visaType"
              className="form-control"
              value={formData.visaType}
              onChange={handleChange}
            >
              {VISA_TYPES.map(type => (
                <option key={type.value} value={type.value}>{type.label}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="currentStatus">Current Status *</label>
            <select
              id="currentStatus"
              name="currentStatus"
              className="form-control"
              value={formData.currentStatus}
              onChange={handleChange}
            >
              {STATUS_OPTIONS.map(status => (
                <option key={status.value} value={status.value}>{status.label}</option>
              ))}
            </select>
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="countryOfOrigin">Country of Origin *</label>
          <input
            type="text"
            id="countryOfOrigin"
            name="countryOfOrigin"
            className="form-control"
            value={formData.countryOfOrigin}
            onChange={handleChange}
            placeholder="Country"
          />
          {errors.countryOfOrigin && <div className="error-message">{errors.countryOfOrigin}</div>}
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="filingDate">Filing Date</label>
            <input
              type="date"
              id="filingDate"
              name="filingDate"
              className="form-control"
              value={formData.filingDate}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="priorityDate">Priority Date</label>
            <input
              type="date"
              id="priorityDate"
              name="priorityDate"
              className="form-control"
              value={formData.priorityDate}
              onChange={handleChange}
            />
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="notes">Notes</label>
          <textarea
            id="notes"
            name="notes"
            className="form-control"
            rows="4"
            value={formData.notes}
            onChange={handleChange}
            placeholder="Additional notes..."
          />
        </div>

        <div className="action-buttons">
          <button type="submit" className="btn">{client ? 'Update' : 'Create'} Client</button>
          <button type="button" className="btn btn-secondary" onClick={onCancel}>Cancel</button>
        </div>
      </form>
    </div>
  );
};

export default ClientForm;
