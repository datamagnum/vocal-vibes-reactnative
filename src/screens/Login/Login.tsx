import * as React from "react";
import { useEffect } from "react";
import { ActivityIndicator, Text, View } from "react-native";
import { useQuery } from "@tanstack/react-query";
import { useTranslation } from "react-i18next";
import { useTheme } from "@/theme";
import { Brand } from "@/components/molecules";
import { SafeScreen } from "@/components/template";
import { VButton } from "@/components/buttons";
import type { ApplicationScreenProps } from "@/types/navigation";
import { TextInput, IconButton, Snackbar } from "react-native-paper";
import { login, loginSSO, registerSSO } from "@/services/auth.service";
import {
  configureGoogleSignIn,
  signInWithGoogle,
} from "@/components/googleSignin/GoogleSignin";
import { SSOType } from "@/services/openapi-client";

export type LoginProps = {
  setIsLoginNavigator: (state: boolean) => void;
};

function Login({
  navigation,
  setIsLoginNavigator,
}: LoginProps & ApplicationScreenProps) {
  const { t } = useTranslation(["login"]);

  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [alertText, setAlertText] = React.useState("");

  useEffect(() => {
    configureGoogleSignIn();
  }, []);

  const { isSuccess, isFetching, isError } = useQuery({
    queryKey: ["startup"],
    queryFn: () => {
      return Promise.resolve(true);
    },
  });

  const onSignUpNavigationClicked = () => {
    navigation.reset({
      index: 0,
      routes: [{ name: "SignUp" }],
    });
  };

  const handleLogin = async () => {
    const payload = { email: email, password: password };
    const response = await login(payload);
    if (!response) {
      setAlertText("Authentication Failed");
      return;
    }

    // This is a hack
    setIsLoginNavigator(false);
  };

  const handleGoogleSignIn = async () => {
    try {
      const userInfo = await signInWithGoogle();
      if (!userInfo || !userInfo.idToken) {
        setAlertText("Google Sign-In Failed");
      }

      const response = await loginSSO({
        id_token: userInfo.idToken ? userInfo.idToken : "",
        sso_type: SSOType.Google,
      });

      if (!response) {
        setAlertText("Authentication Failed");
        return;
      }

      setIsLoginNavigator(false);
    } catch (error) {
      console.log("Google Sign-In Error:", error);
      setAlertText("Google Sign-In Failed");
    }
  };

  return (
    <SafeScreen>
      <Snackbar visible={!!alertText} onDismiss={() => setAlertText("")}>
        {alertText}
      </Snackbar>
      <View className="flex-1">
        <View className="">
          <Text className="font-mono color-dark-darkColor text-5xl text-center mt-10">
            VocalVibe
          </Text>
        </View>
        <View className="">
          <Text className="font-mono color-dark-darkColor text-3xl text-center mt-4">
            Log In
          </Text>
          <Text className="font-mono color-dark-darkColor text text-center mt-4">
            To continue your account !
          </Text>
        </View>
        <View className="pl-4 pr-4 mt-4">
          <View className="mt-4">
            <TextInput
              mode="outlined"
              label="Email"
              value={email}
              onChangeText={(text) => setEmail(text)}
            />
          </View>
          <View className="mt-4">
            <TextInput
              mode="outlined"
              label="Password"
              value={password}
              onChangeText={(text) => setPassword(text)}
              secureTextEntry
            />
          </View>
          <View className="mt-10 pl-10 pr-10">
            <VButton text="Login" onPressEvent={() => handleLogin()} />
          </View>
          <View className="mt-10 flex-row justify-center">
            <IconButton
              icon="google"
              size={20}
              mode="outlined"
              onPress={handleGoogleSignIn}
            />
            {/* <IconButton
              icon="facebook"
              mode="outlined"
              size={20}
              onPress={() => console.log("Pressed")}
            /> */}
          </View>

          <View className="flex-row justify-center mt-10">
            <Text className="font-mono color-dark-darkColor">
              Don't have an account?
            </Text>
            <Text
              className="pl-1 font-mono color-dark-darkColor text-[15px] font-extrabold"
              onPress={onSignUpNavigationClicked}
            >
              Sign Up
            </Text>
          </View>
        </View>
      </View>
    </SafeScreen>
  );
}

export default Login;
