import { Avatar } from "react-native-paper";
import tw from "@/twrnc.config";
import { StyleProp, ViewStyle } from "react-native";

type VAvatarProps = {
  text: string;
  size?: number;
  style?: StyleProp<ViewStyle>;
};

function VAvatar({ text, size, style }: VAvatarProps) {
  return <Avatar.Text style={style} size={size || 40} label={text} />;
}

export default VAvatar;
