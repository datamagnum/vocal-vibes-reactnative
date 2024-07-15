import type { StackScreenProps } from "@react-navigation/stack";
import type { DrawerScreenProps } from "@react-navigation/drawer";


export type ApplicationStackParamList = {
  Startup: undefined;
  Example: undefined;
  Login: undefined;
  SignUp: undefined;
};

export type ApplicationDrawerParamList = {
  Dashboard: undefined;
  SelfPractice: undefined;
  Sessions: undefined;
};

export type ApplicationScreenProps =
  StackScreenProps<ApplicationStackParamList>;

export type ApplicationDrawerScreenProps =
  DrawerScreenProps<ApplicationDrawerParamList>;
