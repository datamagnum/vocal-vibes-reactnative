import { useState, useEffect, useCallback, useRef } from "react";
import Voice, {
  SpeechErrorEvent,
  SpeechResultsEvent,
} from "@react-native-voice/voice/";

interface IState {
  recognized: string;
  pitch: string;
  error: string;
  end: string;
  started: string;
  results: string[];
  partialResults: string[];
  isRecording: boolean;
}

export const useVoiceRecognition = () => {
  const [state, setState] = useState<IState>({
    recognized: "",
    pitch: "",
    error: "",
    end: "",
    started: "",
    results: [],
    partialResults: [],
    isRecording: false,
  });

  const manuallyStoppedRef = useRef(false);

  const resetState = useCallback(() => {
    setState({
      recognized: "",
      pitch: "",
      error: "",
      started: "",
      results: [],
      partialResults: [],
      end: "",
      isRecording: false,
    });
  }, [setState]);

  const startRecognizing = useCallback(async () => {
    resetState();
    try {
      await Voice.start("en-US");
    } catch (e) {
      console.error("Failed to start recognizing:", e);
      setState((prevState) => ({
        ...prevState,
        error: JSON.stringify(e),
        isRecording: false,
      }));
    }
  }, [resetState]);

  const stopRecognizing = useCallback(async () => {
    try {
      await Voice.stop();
    } catch (e) {
      console.error("Failed to stop recognizing:", e);
      setState((prevState) => ({
        ...prevState,
        error: JSON.stringify(e),
        isRecording: false,
      }));
    }
  }, []);

  const cancelRecognizing = useCallback(async () => {
    try {
      await Voice.cancel();
    } catch (e) {
      console.error("Failed to cancel recognizing:", e);
    }
  }, []);

  const destroyRecognizer = useCallback(async () => {
    try {
      await Voice.destroy();
    } catch (e) {
      console.error("Failed to destroy recognizer:", e);
    }
    resetState();
  }, [resetState]);

  useEffect(() => {
    const restartRecognizing = async () => {
      if (!manuallyStoppedRef.current) {
        await startRecognizing();
      }
    };

    Voice.onSpeechStart = () => {
      setState((prevState) => ({
        ...prevState,
        started: "√",
        isRecording: true,
      }));
    };

    Voice.onSpeechRecognized = () => {
      setState((prevState) => ({ ...prevState, recognized: "√" }));
    };

    Voice.onSpeechEnd = () => {
      setState((prevState) => ({ ...prevState, end: "√", isRecording: false }));
      restartRecognizing();
    };

    Voice.onSpeechError = (e: SpeechErrorEvent) => {
      setState((prevState) => ({
        ...prevState,
        error: JSON.stringify(e.error),
        isRecording: false,
      }));
      restartRecognizing();
    };
    Voice.onSpeechResults = (e: SpeechResultsEvent) => {
      if (e.value) {
        setState((prevState) => ({ ...prevState, results: e.value! }));
      }
    };
    Voice.onSpeechPartialResults = (e: SpeechResultsEvent) => {
      if (e.value) {
        setState((prevState) => ({ ...prevState, partialResults: e.value! }));
      }
    };
    Voice.onSpeechVolumeChanged = (e: any) => {
      setState((prevState) => ({ ...prevState, pitch: e.value }));
    };

    return () => {
      manuallyStoppedRef.current = true;
      Voice.destroy().then(Voice.removeAllListeners);
    };
  }, [startRecognizing]);

  return {
    state,
    startRecognizing: async () => {
      manuallyStoppedRef.current = false;
      await startRecognizing();
    },
    stopRecognizing: async () => {
      manuallyStoppedRef.current = true;
      await stopRecognizing();
    },
    cancelRecognizing,
    destroyRecognizer: async () => {
      manuallyStoppedRef.current = true;
      await destroyRecognizer();
    },
  };
};
