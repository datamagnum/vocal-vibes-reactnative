import axios from "axios";
import StorageService from "./storage.service";
import { StorageKeys } from "@/constants/storage.constant";

const instance = axios.create({
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json; charset=utf-8",
  },
});

instance.interceptors.request.use(
  async (config) => {
    const token = await StorageService.getItem(StorageKeys.AUTH_TOKEN);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    // Handle request error
    console.log(error);
    return Promise.reject(error);
  }
);

const handleUnauthorizedError = async (error: any) => {
  // Optionally, you could clear the token and redirect to a login page or refresh the token
  console.error("Unauthorized access - possibly invalid token");
  await StorageService.removeItem(StorageKeys.AUTH_TOKEN);
  return Promise.reject(error);
};

// Add a response interceptor to handle 401 errors
instance.interceptors.response.use(
  (response) => response,
  async (error) => {
    console.log(error);
    if (error.response && error.response.status === 401) {
      await handleUnauthorizedError(error);
    }
    return Promise.reject(error);
  }
);

export default instance;
