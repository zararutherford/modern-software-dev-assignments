const mongoose = require('mongoose');

const clientSchema = new mongoose.Schema(
  {
    firstName: {
      type: String,
      required: [true, 'First name is required'],
      trim: true,
    },
    lastName: {
      type: String,
      required: [true, 'Last name is required'],
      trim: true,
    },
    email: {
      type: String,
      required: [true, 'Email is required'],
      trim: true,
      lowercase: true,
      match: [/^\S+@\S+\.\S+$/, 'Please enter a valid email'],
    },
    phone: {
      type: String,
      trim: true,
    },
    caseNumber: {
      type: String,
      required: [true, 'Case number is required'],
      unique: true,
      trim: true,
    },
    visaType: {
      type: String,
      required: [true, 'Visa type is required'],
      enum: ['H1B', 'L1', 'O1', 'EB1', 'EB2', 'EB3', 'F1', 'GREEN_CARD', 'CITIZENSHIP', 'ASYLUM', 'OTHER'],
    },
    currentStatus: {
      type: String,
      required: true,
      enum: ['INITIAL_CONSULTATION', 'DOCUMENTS_GATHERING', 'APPLICATION_PREP', 'FILED', 'RFE', 'APPROVED', 'DENIED', 'WITHDRAWN'],
      default: 'INITIAL_CONSULTATION',
    },
    countryOfOrigin: {
      type: String,
      required: [true, 'Country of origin is required'],
      trim: true,
    },
    filingDate: {
      type: Date,
    },
    priorityDate: {
      type: Date,
    },
    notes: {
      type: String,
      trim: true,
    },
  },
  {
    timestamps: true,
  }
);

// Virtual for full name
clientSchema.virtual('fullName').get(function () {
  return `${this.firstName} ${this.lastName}`;
});

// Include virtuals in JSON
clientSchema.set('toJSON', { virtuals: true });
clientSchema.set('toObject', { virtuals: true });

const Client = mongoose.model('Client', clientSchema);

module.exports = Client;
