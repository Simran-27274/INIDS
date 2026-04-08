import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000";

export const predictTraffic = async (payload) => {
  const response = await axios.post(`${BASE_URL}/predict/`, payload);
  return response.data;   
};


export const fetchStats = async () => {
  const response = await axios.get(`${BASE_URL}/stats`);
  return response.data;
};

export const fetchAlerts = async () => {
  const response = await axios.get(`${BASE_URL}/alerts`);
  return response.data.alerts || [];
};