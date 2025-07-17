// import axios from 'axios';

// // const API_BASE_URL = 'http://192.168.0.103:8000/api';
// const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

// export const fetchForecast = (payload) => {
//     return axios.post(`${API_BASE_URL}/forecast/`, payload);
// };

// export const fetchExportData = (hs_code, limit = 12, sort = 'asc') => {
//     return axios.get(`${API_BASE_URL}/monthly-exports/`, {
//         params: { hs_code, limit, sort }
//     });
// };


// src/services/api.js

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

export const fetchCommodities = async (searchTerm) => {
  const response = await fetch(`${API_BASE_URL}/commodities/?search=${searchTerm}`);
  if (!response.ok) throw new Error('Failed to fetch commodities');
  return await response.json();
};

export const fetchForecast = async ({ hsCode, model, validation }) => {
  const response = await fetch(`${API_BASE_URL}/forecast/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      hs_code: hsCode,
      model,
      validation
    }),
  });
  if (!response.ok) throw new Error('Failed to fetch forecast');
  return await response.json();
};
