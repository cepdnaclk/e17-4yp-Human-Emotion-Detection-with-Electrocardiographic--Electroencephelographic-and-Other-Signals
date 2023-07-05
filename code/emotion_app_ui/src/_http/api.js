import axios from "axios";

export const postReq = async (endpoint, data) => {
  const response = await axios.post(`${process.env.HOST_URL}${endpoint}`, data);
  return response.data;
};
