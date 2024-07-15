import { Button } from "react-native-paper";
import tw from "@/twrnc.config";
import { View, Text } from "react-native";
import { VAvatar } from "@/components/avatars";
import { useEffect, useState } from "react";
import UserService from "@/services/user.service";

type VDrawerHeader = {};

function DrawerHeader({}: VDrawerHeader) {
  const [userInfo, setUserInfo] = useState<any>();

  const fetchData = async () => {
    const userInfo = await UserService.whoAmI();
    setUserInfo(userInfo);
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <View className="flex-1 h-55 bg-[#efefef] p-4">
      <Text className="p-2 font-bold text-[35px] text-center">VocalVibe</Text>
      <View className="flex-1 flex-row">
        <VAvatar text={`${userInfo?.first_name[0]?.toUpperCase()}`} />
        <Text className="p-2 font-semibold text-[15px]">{userInfo?.email}</Text>
      </View>
    </View>
  );
}

export default DrawerHeader;
