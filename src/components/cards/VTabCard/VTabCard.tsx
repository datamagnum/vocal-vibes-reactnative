import React from "react";
import { Card, Button } from "react-native-paper";
import { StyleSheet, View, Text } from "react-native";
import tw from "@/twrnc.config";

type VCardProps = {
  text: string;
  mode?: "text" | "outlined" | "contained" | "elevated" | "contained-tonal";
  icon?: string;
  onPressEvent: () => void;
};

const VCard = ({
  text,
  icon,
  mode = "contained",
  onPressEvent,
}: VCardProps) => {
  return (
    <Card
      style={tw`bg-light-content w-[90px] m-2`}
      onPress={onPressEvent}
    >
      <Text style={tw`p-2`}>{text}</Text>
    </Card>
  );
};

const styles = StyleSheet.create({
  card: {
    marginVertical: 10,
    marginHorizontal: 5,
    width: 90,
    height: 60,
    backgroundColor: "#ffffff",
  },
});

export default VCard;
