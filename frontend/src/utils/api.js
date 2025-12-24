import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const api = {
  submitReport: async (data) => {
    // data: { content, location, signatures, address }
    const response = await axios.post(`${API_URL}/submit`, data);
    return response.data;
  },

  getReports: async (skip = 0, limit = 50) => {
    const response = await axios.get(`${API_URL}/reports?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  getStats: async () => {
    const response = await axios.get(`${API_URL}/stats`);
    return response.data;
  }
};
