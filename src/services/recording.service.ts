import AudioRecorderPlayer from "react-native-audio-recorder-player";
import { PermissionsAndroid, Platform } from "react-native";

class AudioRecordingService {
  static instance: AudioRecordingService;
  audioRecorderPlayer: AudioRecorderPlayer;

  constructor() {
    if (AudioRecordingService.instance) {
      return AudioRecordingService.instance;
    }
    this.audioRecorderPlayer = new AudioRecorderPlayer();
  }

  static getInstance() {
    if (!AudioRecordingService.instance) {
      AudioRecordingService.instance = new AudioRecordingService();
    }
    return AudioRecordingService.instance;
  }

  async requestPermissions() {
    if (Platform.OS === "android") {
      try {
        const granted = await PermissionsAndroid.requestMultiple([
          PermissionsAndroid.PERMISSIONS.RECORD_AUDIO,
          PermissionsAndroid.PERMISSIONS.WRITE_EXTERNAL_STORAGE,
          PermissionsAndroid.PERMISSIONS.READ_EXTERNAL_STORAGE,
        ]);
        return (
          granted[PermissionsAndroid.PERMISSIONS.RECORD_AUDIO] ===
            PermissionsAndroid.RESULTS.GRANTED &&
          granted[PermissionsAndroid.PERMISSIONS.WRITE_EXTERNAL_STORAGE] ===
            PermissionsAndroid.RESULTS.GRANTED &&
          granted[PermissionsAndroid.PERMISSIONS.READ_EXTERNAL_STORAGE] ===
            PermissionsAndroid.RESULTS.GRANTED
        );
      } catch (err) {
        console.warn(err);
        return false;
      }
    } else {
      return true;
    }
  }

  async startRecording() {
    const hasPermission = await this.requestPermissions();
    if (!hasPermission) return null;

    const result = await this.audioRecorderPlayer.startRecorder();
    this.audioRecorderPlayer.addRecordBackListener((e) => {
      console.log("Recording...", e);
    });
    return result;
  }

  async stopRecording() {
    const result = await this.audioRecorderPlayer.stopRecorder();
    this.audioRecorderPlayer.removeRecordBackListener();
    return result;
  }

  async startPlayback(uri: string) {
    console.log(uri);
    const result = await this.audioRecorderPlayer.startPlayer(uri);
    this.audioRecorderPlayer.addPlayBackListener((e) => {
      console.log("Playing...", e);
    });
    return result;
  }

  async stopPlayback() {
    const result = await this.audioRecorderPlayer.stopPlayer();
    this.audioRecorderPlayer.removePlayBackListener();
    return result;
  }
}

const audioRecordingService = AudioRecordingService.getInstance();
export default audioRecordingService;
