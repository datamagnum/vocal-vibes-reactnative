import { GroupServiceClient, UserServiceClient } from "./api-client";
import {
  CreateGroupRequestSchema,
  AddUserToGroupRequestSchema,
  RemoveUserFromGroupRequestSchema,
  ListUserGroupsResponseSchema,
  ListUsersInGroupsResponseSchema,
} from "./openapi-client";

class GroupService {
  static async createGroup(groupData: CreateGroupRequestSchema) {
    try {
      console.log("Requesting group creation with payload:", groupData);
      const response = await GroupServiceClient.createGroup(groupData);
      console.log("Group created response:", response.data);
      return response.data;
    } catch (error) {
      console.error("Error creating group:", error?.response?.data || error);
      throw new Error(`Failed to create group: ${error}`);
    }
  }

  static async addUserToGroup(
    groupId: string,
    userId: number
  ) {
    try {
      const response = await GroupServiceClient.addUserToGroup(
        groupId,
        userId
      );
      return response.data;
    } catch (error) {
      throw new Error(`Failed to add user to group: ${error}`);
    }
  }

  static async removeUserFromGroup(groupId: string, userId: number) {
    try {
      const response = await GroupServiceClient.removeUserFromGroup(
        groupId,
        userId
      );
      return response.data;
    } catch (error) {
      throw new Error(`Failed to remove user from group: ${error}`);
    }
  }

  static async getUserGroups(): Promise<ListUserGroupsResponseSchema> {
    try {
      const response = await UserServiceClient.listUserGroups();
      return response.data;
    } catch (error) {
      throw new Error(`Failed to fetch user groups: ${error}`);
    }
  }

  static async getUsersInGroup(
    groupId: string
  ): Promise<ListUsersInGroupsResponseSchema> {
    try {
      const response = await GroupServiceClient.getUsersInGroup(groupId);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to fetch user groups: ${error}`);
    }
  }

  static async getGroup(groupId: string) {
    try {
      const response = await GroupServiceClient.getGroup(groupId);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to fetch group: ${error}`);
    }
  }
}

export default GroupService;
