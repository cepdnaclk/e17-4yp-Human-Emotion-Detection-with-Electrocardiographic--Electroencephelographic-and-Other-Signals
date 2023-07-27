import axios from "axios";

export const postReq = async (endpoint, data) => {
  const response = await axios.post(`http://localhost:5000/${endpoint}`, data);
  console.log(`${process.env.REACT_APP_HOST_URL}`);
  return response.data;
};
