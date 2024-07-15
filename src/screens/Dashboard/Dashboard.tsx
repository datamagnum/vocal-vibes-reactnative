import { SafeScreen } from "@/components/template";
import { useEffect, useState } from "react";
import {
  View,
  ActivityIndicator,
  Text,
  TouchableOpacity,
  ScrollView,
  Alert,
} from "react-native";
import { useTranslation } from "react-i18next";
import { Avatar, Button, Card } from "react-native-paper";
import tw from "@/twrnc.config";
import Sessions from "@/screens/Sessions/Sessions";

function Dashboard({ navigation }: any) {
  const { t } = useTranslation(["example", "welcome"]);

  return (
    <SafeScreen>
      <ScrollView>
        <Card>
          <Card.Title title="My Uploads" />
          <Card.Content>
            <Text>Explore old recordings and sessions</Text>
          </Card.Content>
          <Card.Actions>
            <Button
              onPress={() =>
                navigation.reset({
                  index: 0,
                  routes: [{ name: "Sessions" }],
                })
              }
            >
              Sessions
            </Button>
          </Card.Actions>
        </Card>
      </ScrollView>
    </SafeScreen>
  );
}

export default Dashboard;
