import {
  GoogleSignin,
  statusCodes,
} from "@react-native-google-signin/google-signin";

// Todo This should be moved to services

export const configureGoogleSignIn = () => {
  GoogleSignin.configure({
    webClientId: process.env.GOOGLE_CLIENT_ID,
    offlineAccess: true,
    forceCodeForRefreshToken: true,
  });
};

export const signInWithGoogle = async () => {
  try {
    await GoogleSignin.hasPlayServices();
    const userInfo = await GoogleSignin.signIn();
    return userInfo;
  } catch (error) {
    if (error.code === statusCodes.SIGN_IN_CANCELLED) {
      console.log("User cancelled the login flow");
    } else if (error.code === statusCodes.IN_PROGRESS) {
      console.log("Sign in is in progress already");
    } else if (error.code === statusCodes.PLAY_SERVICES_NOT_AVAILABLE) {
      console.log("Play services not available or outdated");
    } else {
      console.log("Some other error happened:", error);
    }
    throw error;
  }
};
