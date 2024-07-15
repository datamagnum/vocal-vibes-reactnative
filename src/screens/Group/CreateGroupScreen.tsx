import React, { useState } from "react";
import { View, Text, TextInput, Button, Alert } from "react-native";
import GroupService from "../../services/group.service";
import tw from "@/twrnc.config";
import { CreateGroupRequestSchema } from "@/services/openapi-client";

const groupService = new GroupService();

function CreateGroupScreen() {
  const [groupName, setGroupName] = useState("");
  const [description, setDescription] = useState("");

  const createGroup = async () => {
    try {
      const payload: CreateGroupRequestSchema = {
        name: groupName,
        description,
      };
      const group = await GroupService.createGroup(payload);
      Alert.alert("Success", "Group created successfully");
      setGroupName("");
      setDescription("");
    } catch (error) {
      Alert.alert("Error", `Failed to create group: ${error}`);
    }
  };

  return (
    <View style={tw`flex-1 p-5`}>
      <Text style={tw`text-2xl font-bold mb-5`}>Create Group</Text>
      <TextInput
        style={tw`h-10 border border-gray-300 rounded p-2 mb-3`}
        placeholder="Group Name"
        value={groupName}
        onChangeText={setGroupName}
      />
      <TextInput
        style={tw`h-10 border border-gray-300 rounded p-2 mb-3`}
        placeholder="Description"
        value={description}
        onChangeText={setDescription}
      />
      <Button title="Create Group" onPress={createGroup} />
    </View>
  );
}

export default CreateGroupScreen;
