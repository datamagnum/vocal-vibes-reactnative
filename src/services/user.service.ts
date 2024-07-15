import { UserServiceClient } from "./api-client";
import instance from "./instance";
import { ListUserResponseSchema, User } from "./openapi-client";

class UserService {
  static USER_PREFIX: string = "user";

  static async whoAmI(): Promise<User> {
    try {
      const response = await UserServiceClient.whoami();
      return response.data;
    } catch (error) {
      console.error("Error fetching user", error);
      throw error;
    }
  }

  static async getUsers(): Promise<ListUserResponseSchema> {
    try {
      const response = await UserServiceClient.listUsers();
      return response.data;
    } catch (error) {
      console.error("Error fetching users:", error);
      throw error;
    }
  }
}

export default UserService;
