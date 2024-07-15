import AsyncStorage from "@react-native-async-storage/async-storage";
import { StorageKey, StorageKeys } from "@/constants/storage.constant";
import EventEmitter from 'events';

const eventEmitter = new EventEmitter();


class StorageService {
  static async setItem<T>(key: StorageKey, value: string): Promise<void> {
    try {
      await AsyncStorage.setItem(StorageKeys[key], value);
    } catch (error) {
      console.error("Error setting item in AsyncStorage", error);
    }
  }

  static async getItem<T>(key: StorageKey): Promise<String | null> {
    try {
      const value = await AsyncStorage.getItem(StorageKeys[key]);
      return value;
    } catch (error) {
      console.error("Error getting item from AsyncStorage", error);
      return null;
    }
  }

  static async removeItem(key: StorageKey): Promise<void> {
    try {
      await AsyncStorage.removeItem(StorageKeys[key]);
    } catch (error) {
      console.error("Error removing item from AsyncStorage", error);
    }
  }

  static async clear(): Promise<void> {
    try {
      await AsyncStorage.clear();
    } catch (error) {
      console.error("Error clearing AsyncStorage", error);
    }
  }
}

export default StorageService;
