import { StorageKeys } from "@/constants/storage.constant";
import instance from "./instance";
import StorageService from "./storage.service";
import { AuthServiceClient, BASE_URL } from "./api-client";
import { AuthSSOSchema, RegisterUserSchema } from "./openapi-client";
import { AxiosError } from "axios";


const AUTH_PREFIX = `${BASE_URL}/api/v1/auth`; // TODO move this to APIClient

export const login = async (payload: any) => {
  try {
    console.log(AUTH_PREFIX);
    const response = await instance.post(`${AUTH_PREFIX}/login`, {
      ...payload,
    });
    console.log(response.data.access_token);
    await StorageService.setItem(
      StorageKeys.AUTH_TOKEN,
      response.data.access_token
    );
    return response;
  } catch (exception) {
    if (exception.response) {
      console.error('Error data:', exception.response.data);
      console.error('Error status:', exception.response.status);
      console.error('Error headers:', exception.response.headers);
    } else if (exception.request) {
      console.error('No response received:', exception.request);
    } else {
      console.error('Axios error:', exception.message);
    }
    console.error(exception);
  }
};

export const register = async (payload: any) => {
  try {
    const response = await instance.post(`${AUTH_PREFIX}/register`, {
      ...payload,
    });
    return response;
  } catch (exception) {
    console.error(exception);
    //   return false;
    throw exception;
  }
};

export const registerSSO = async (payload: AuthSSOSchema) => {
  try {
    const response = await AuthServiceClient.registerSso(payload);
    return response;
  } catch (exception) {
    console.error(exception);
    throw exception;
  }
};

export const loginSSO = async (payload: AuthSSOSchema) => {
  try {
    const response = await AuthServiceClient.loginSso(payload);
    await StorageService.setItem(
      StorageKeys.AUTH_TOKEN,
      response.data.access_token
    );
    return response;
  } catch (exception) {
    console.error(exception);
  }
};
