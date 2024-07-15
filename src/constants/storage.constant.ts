export const StorageKeys = {
  USER_PROFILE: "USER_PROFILE",
  SETTINGS: "SETTINGS",
  AUTH_TOKEN: "AUTH_TOKEN",
  // Add more keys as needed
} as const;

export type StorageKey = keyof typeof StorageKeys;
