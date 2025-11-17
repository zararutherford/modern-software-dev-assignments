import axios from 'axios';

const API_URL = '/api/clients';

export const getAllClients = async () => {
  const response = await axios.get(API_URL);
  return response.data;
};

export const getClient = async (id) => {
  const response = await axios.get(`${API_URL}/${id}`);
  return response.data;
};

export const createClient = async (clientData) => {
  const response = await axios.post(API_URL, clientData);
  return response.data;
};

export const updateClient = async (id, clientData) => {
  const response = await axios.put(`${API_URL}/${id}`, clientData);
  return response.data;
};

export const deleteClient = async (id) => {
  const response = await axios.delete(`${API_URL}/${id}`);
  return response.data;
};
