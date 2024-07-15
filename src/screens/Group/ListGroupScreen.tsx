import React, { useState, useEffect } from "react";
import {
  View,
  Text,
  FlatList,
  Alert,
  TouchableOpacity,
  Modal,
} from "react-native";
import Icon from "react-native-vector-icons/FontAwesome5"; // Adjust as per your icon library
import GroupService from "../../services/group.service";
import UserService from "@/services/user.service";
import tw from "@/twrnc.config";
import {
  Group,
  ListUserGroupsResponseSchema,
  ListUserResponseSchema,
} from "@/services/openapi-client";
import { useFocusEffect } from "@react-navigation/native";

function ListGroupsScreen() {
  const [groupsData, setGroupsData] = useState<ListUserGroupsResponseSchema>();
  const [selectedGroup, setSelectedGroup] = useState<Group | null>(null);
  const [allUsers, setAllUsers] = useState<ListUserResponseSchema>();
  const [modalVisible, setModalVisible] = useState(false);
  const [usersInSelectedGroup, setUsersInSelectedGroup] =
    useState<ListUserResponseSchema | null>(null);

  useFocusEffect(
    React.useCallback(() => {
      fetchGroups();
      fetchAvailableUsers();
    }, [])
  );

  const fetchGroups = async () => {
    try {
      const groups = await GroupService.getUserGroups();
      setGroupsData(groups);
    } catch (error) {
      Alert.alert("Error", `Failed to fetch groups: ${error}`);
    }
  };

  const fetchAvailableUsers = async () => {
    try {
      const usersResponse = await UserService.getUsers();
      setAllUsers(usersResponse); // Assuming UserService returns an object with a 'users' array
    } catch (error) {
      Alert.alert("Error", `Failed to fetch available users: ${error}`);
    }
  };

  const openModal = async (group: Group) => {
    setSelectedGroup(group);
    setModalVisible(true);
    // Fetch users already in the selected group
    try {
      const groupUsersResponse = await GroupService.getUsersInGroup(group.id);
      setUsersInSelectedGroup(groupUsersResponse); // Assuming GroupService returns an object with a 'users' array
    } catch (error) {
      Alert.alert("Error", `Failed to fetch users in group: ${error}`);
    }
  };

  const closeModal = () => {
    setModalVisible(false);
    setSelectedGroup(null);
    setUsersInSelectedGroup(null);
  };

  const handleAddUserToGroup = async (userId: number) => {
    try {
      if (!selectedGroup) {
        Alert.alert("Please select group");
        return;
      }
      await GroupService.addUserToGroup(selectedGroup?.id, userId);
      // Refetch users in the selected group after adding a user
      const groupUsersResponse = await GroupService.getUsersInGroup(
        selectedGroup?.id
      );
      setUsersInSelectedGroup(groupUsersResponse); // Update users in the selected group
      Alert.alert("Success", "User added to group successfully");
    } catch (error) {
      Alert.alert("Error", `Failed to add user to group: ${error}`);
    }
  };

  const handleRemoveUserFromGroup = async (userId: number) => {
    try {
      if (!selectedGroup) {
        Alert.alert("Please select group");
        return;
      }

      await GroupService.removeUserFromGroup(selectedGroup.id, userId);
      const groupUsersResponse = await GroupService.getUsersInGroup(
        selectedGroup?.id
      );
      setUsersInSelectedGroup(groupUsersResponse);
      Alert.alert("Success", "User removed from group successfully");
    } catch (error) {
      Alert.alert("Error", `Failed to remove user from group: ${error}`);
    }
  };

  return (
    <View style={tw`flex-1 p-5 bg-white`}>
      <Text style={tw`text-2xl font-bold mb-5`}>List Groups</Text>
      <FlatList
        data={groupsData?.groups}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={tw`pb-20`}
        renderItem={({ item }) => (
          <TouchableOpacity
            style={tw`p-4 mb-3 bg-gray-100 rounded-lg border border-gray-300`}
            onPress={() => openModal(item)}
          >
            <Text style={tw`text-lg font-semibold`}>{item.name}</Text>
          </TouchableOpacity>
        )}
      />

      <Modal
        visible={modalVisible}
        animationType="slide"
        onRequestClose={closeModal}
      >
        <View style={tw`flex-1 p-5 bg-white`}>
          <Text style={tw`text-xl font-bold mb-5`}>Manage Group Users</Text>
          <Text style={tw`text-lg mb-3`}>Users in Group:</Text>
          <FlatList
            data={usersInSelectedGroup?.users}
            keyExtractor={(item) => item.id.toString()}
            renderItem={({ item }) => (
              <View
                className=""
                style={tw`flex-row justify-between items-center mb-2`}
              >
                <Text style={tw`mr-2`}>{item.email}</Text>

                {selectedGroup?.created_by !== item?.id && (
                  <TouchableOpacity
                    style={tw`p-2 bg-red-500 rounded-full items-center`}
                    onPress={() => handleRemoveUserFromGroup(item.id)}
                  >
                    <Icon name="user-minus" size={16} color="white" />
                  </TouchableOpacity>
                )}
              </View>
            )}
          />
          <Text style={tw`text-lg mt-3`}>Add User to Group:</Text>
          <FlatList
            data={allUsers?.users.filter(
              (user) =>
                !usersInSelectedGroup?.users
                  .map((user) => user.email)
                  .includes(user.email)
            )}
            keyExtractor={(item) => item.id.toString()}
            renderItem={({ item }) => (
              <TouchableOpacity
                style={tw`p-4 mb-3 bg-gray-100 rounded-lg border border-gray-300`}
                onPress={() => handleAddUserToGroup(item.id)}
              >
                <Text style={tw`text-lg`}>{`${item.email}`}</Text>
              </TouchableOpacity>
            )}
          />
          <TouchableOpacity
            style={tw`py-2 px-4 bg-blue-500 rounded-lg mt-3`}
            onPress={closeModal}
          >
            <Text style={tw`text-white text-center text-sm`}>Close</Text>
          </TouchableOpacity>
        </View>
      </Modal>
    </View>
  );
}

export default ListGroupsScreen;
