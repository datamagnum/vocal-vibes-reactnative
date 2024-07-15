import { Button } from "react-native-paper";
import tw from "@/twrnc.config";

type VButtonProps = {
  text: string;
  mode?: "text" | "outlined" | "contained" | "elevated" | "contained-tonal";
  icon?: string;
  onPressEvent: () => void;
};

function VButton({ text, icon, mode, onPressEvent }: VButtonProps) {
  return (
    <Button
      style={tw`bg-light-secondary rounded-2 text-light-content`}
      mode={mode || "outlined"}
      icon={icon}
      onPress={onPressEvent}
    >
      {text || "Button"}
    </Button>
  );
}

export default VButton;
