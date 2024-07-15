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
import { register, registerSSO } from "@/services/auth.service";
import {
  configureGoogleSignIn,
  signInWithGoogle,
} from "@/components/googleSignin/GoogleSignin";
import { SSOType } from "@/services/openapi-client";

function SignUp({ navigation }: ApplicationScreenProps) {
  // const { layout, gutters, fonts } = useTheme();
  const { t } = useTranslation(["login"]);

  const [name, setName] = React.useState("");
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [alertText, setAlertText] = React.useState("");

  const { isSuccess, isFetching, isError } = useQuery({
    queryKey: ["startup"],
    queryFn: () => {
      return Promise.resolve(true);
    },
  });

  useEffect(() => {
    configureGoogleSignIn();
  }, []);

  const onLoginNavigationClicked = () => {
    navigation.reset({
      index: 0,
      routes: [{ name: "Login" }],
    });
  };

  const handleGoogleSignUp = async () => {
    try {
      const userInfo = await signInWithGoogle();
      if (!userInfo || !userInfo.idToken) {
        setAlertText("Google Sign-Up Failed");
      }

      const response = await registerSSO({
        id_token: userInfo.idToken ? userInfo.idToken : "",
        sso_type: SSOType.Google,
      });
      
      if (response) {
        setAlertText("User Registered Successfully");
      }
    } catch (error) {
      console.log("Google Sign-In Error:", error);
      setAlertText("Google Sign-In Failed");
    }
  };

  const handleRegister = async () => {
    const payload = {
      email: email.trim(),
      password: password.trim(),
      first_name: name.trim(),
    };

    try {
      const response = await register(payload);
      setAlertText("User Registered Successfully");
      setName("");
      setEmail("");
      setPassword("");
    } catch (exception) {
      setAlertText("User Registeration Failed");
    }
  };

  return (
    <SafeScreen>
      <Snackbar visible={!!alertText} onDismiss={() => setAlertText("")}>
        {alertText}
      </Snackbar>
      <View className="flex-1 bg-white">
        <View className="">
          <Text className="font-mono color-dark-darkColor text-5xl text-center mt-10">
            VocalVibe
          </Text>
        </View>
        <View className="">
          <Text className="font-mono color-dark-darkColor text-3xl text-center mt-4">
            SignUp
          </Text>
          <Text className="font-mono color-dark-darkColor text text-center mt-4">
            Register Your Account !
          </Text>
        </View>
        <View className="pl-4 pr-4 mt-4">
          <View className="mt-4">
            <TextInput
              mode="outlined"
              label="Username"
              value={name}
              onChangeText={(text) => setName(text)}
            />
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
            <VButton text="Sign Up" onPressEvent={() => handleRegister()} />
          </View>
          <View className="mt-10 flex-row justify-center">
            <IconButton
              icon="google"
              size={20}
              mode="outlined"
              onPress={handleGoogleSignUp}
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
              Already have an account?
            </Text>
            <Text
              className="pl-1 font-mono color-dark-darkColor text-[15px] font-extrabold"
              onPress={onLoginNavigationClicked}
            >
              Login
            </Text>
          </View>
        </View>
      </View>
    </SafeScreen>
  );
}

export default SignUp;
