import { Button } from "react-native-paper";
import tw from "@/twrnc.config";
import { View, Text } from "react-native";
import { VAvatar } from "@/components/avatars";
import { useEffect, useState } from "react";
import UserService from "@/services/user.service";

type VDrawerHeader = {};

function Topic({}: VDrawerHeader) {
  const [userInfo, setUserInfo] = useState<any>();

  const fetchData = async () => {
    const userInfo = await UserService.whoAmI();
    setUserInfo(userInfo);
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <View className="h-55 bg-[#efefef] p-4">
      <Text>
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Illo fuga,
        corporis mollitia eum, delectus reprehenderit quos exercitationem,
        consectetur dolorum unde facilis necessitatibus. Repellendus in
        accusamus ipsum eveniet impedit aliquid unde! Lorem ipsum dolor sit amet
        consectetur adipisicing elit. Impedit ut voluptatem quas vitae
        aspernatur quia molestiae, placeat nemo, atque sunt maiores, dolorum
        doloribus ducimus! Ducimus impedit porro dicta a laboriosam! Lorem ipsum
        dolor sit amet consectetur adipisicing elit. Illo fuga, corporis
        mollitia eum, delectus reprehenderit quos exercitationem, consectetur
        dolorum unde facilis necessitatibus. Repellendus in accusamus ipsum
        eveniet impedit aliquid unde! Lorem ipsum dolor sit amet consectetur
        adipisicing elit. Impedit ut voluptatem quas vitae aspernatur quia
        molestiae, placeat nemo, atque sunt maiores, dolorum doloribus ducimus!
        Ducimus impedit porro dicta a laboriosam! Lorem ipsum dolor sit amet
        consectetur adipisicing elit. Illo fuga, corporis mollitia eum, delectus
        reprehenderit quos exercitationem, consectetur dolorum unde facilis
        necessitatibus. Repellendus in accusamus ipsum eveniet impedit aliquid
        unde! Lorem ipsum dolor sit amet consectetur adipisicing elit. Impedit
        ut voluptatem quas vitae aspernatur quia molestiae, placeat nemo, atque
        sunt maiores, dolorum doloribus ducimus! Ducimus impedit porro dicta a
        laboriosam!
      </Text>
    </View>
  );
}

export default Topic;
