import { SafeAreaView, StatusBar } from "react-native";

import { useTheme } from "@/theme";

import type { PropsWithChildren } from "react";
import { View } from "react-native";
import { colorScheme, useColorScheme } from "nativewind";

function SafeScreen({ children }: PropsWithChildren) {
  // const { layout, variant, navigationTheme } = useTheme();

  const { setColorScheme } = useColorScheme();
  setColorScheme("light");

  return (
    <SafeAreaView
      className="flex-1 bg-light-base dark:bg-dark-base"
      style={
        [
          // layout.flex_1,
          // { backgroundColor: navigationTheme.colors.background },
        ]
      }
    >
      <StatusBar
      // barStyle={variant === 'dark' ? 'light-content' : 'dark-content'}
      // backgroundColor={navigationTheme.colors.background}
      />
      {children}
    </SafeAreaView>
  );
}

export default SafeScreen;
