import instance from "./instance";
import "react-native-url-polyfill/auto";
import { AuthApi, GroupApi, TopicApi, UserApi } from "./openapi-client";
import { BaseAPI } from "./openapi-client/base";

// export const BASE_URL = `${
//   process.env.API_URL
//     ? process.env.API_URL
//     : "https://vocalvibe-datamagnum.thepioneerfuture.com"
// }`;

// export const BASE_URL = "https://vocalvibe-datamagnum.thepioneerfuture.com";
export const BASE_URL = "http://10.0.2.2:9000";

console.log(BASE_URL);
export const TopicServiceClient = new TopicApi(undefined, BASE_URL, instance);
export const UserServiceClient = new UserApi(undefined, BASE_URL, instance);
export const AuthServiceClient = new AuthApi(undefined, BASE_URL, instance);
export const GroupServiceClient = new GroupApi(undefined, BASE_URL, instance);
