import { SafeScreen } from "@/components/template";
import { useEffect, useState } from "react";
import { View, Text, ScrollView } from "react-native";
import { useTranslation } from "react-i18next";
import { VButton } from "@/components/buttons";
import { useVoiceRecognition } from "@/hooks/useVoiceRecognition";
import VCard from "@/components/cards/VTabCard/VTabCard";
import TopicService from "@/services/topic.service";
import { TopicsResponseSchema } from "@/services/openapi-client";
import tw from "@/twrnc.config";
import { Card } from "react-native-paper";
import audioRecordingService from "@/services/recording.service";
import RNFS from "react-native-fs";

function SelfPractice() {
  const { t } = useTranslation(["example", "welcome"]);
  const [isRecording, setIsRecording] = useState<boolean>(false);

  const [topicsData, setTopicsData] = useState<TopicsResponseSchema>();
  const [currentTopicId, setCurrentTopicId] = useState<number>();
  const [timer, setTimer] = useState<number>(0);
  const [sessionId, setSessionId] = useState<string>("");

  // const { state, startRecognizing, stopRecognizing, destroyRecognizer } =
  //   useVoiceRecognition();

  // console.log("[State]", state);

  const handleButtonPress = async () => {
    try {
      if (!isRecording) {
        // startRecognizing();
        setSessionId(generateSessionId());
        audioRecordingService.startRecording();
        setIsRecording(true);
      } else {
        // stopRecognizing();
        const filePath = await audioRecordingService.stopRecording();
        // console.log("File", filePath);
        await saveRecording(filePath, sessionId);
        setSessionId("");
        setIsRecording(false);
      }
    } catch (error) {
      console.error("Error handling voice recognition:", error);
    }
  };

  useEffect(() => {
    getTopics();
  }, []);

  const generateSessionId = () => {
    const currentTime = Math.floor(Date.now() / 1000); // Unix timestamp in seconds

    const sessionId = `${getCurrentTopicById(
      currentTopicId || 0
    )?.title.replaceAll(" ", "_")}_${currentTime}`;

    return sessionId;
  };

  useEffect(() => {
    let intervalId: NodeJS.Timeout | null = null;
    if (isRecording) {
      intervalId = setInterval(() => {
        setTimer((prevTimer) => prevTimer + 1);
      }, 1000);
    } else {
      if (intervalId) clearInterval(intervalId);
      setTimer(0);
    }

    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [isRecording]);

  const getTopics = async () => {
    const response = await TopicService.getTopics();
    if (response) {
      setCurrentTopicId(response?.topics?.[0]?.id);
      setTopicsData(response);
    }
  };

  const getCurrentTopicById = (id: number) => {
    const filteredTopic = topicsData?.topics?.filter((data) => data.id === id);
    return filteredTopic ? filteredTopic[0] : null;
  };

  // Todo: Temp method use some library for this
  const formatTime = (seconds: number) => {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    return `${hrs < 10 ? "0" : ""}${hrs}:${mins < 10 ? "0" : ""}${mins}:${
      secs < 10 ? "0" : ""
    }${secs}`;
  };

  const saveRecording = async (recordingUri: string, sessionId: string) => {
    try {
      let filePathToSave = `${RNFS.DocumentDirectoryPath}/recordings/${sessionId}.mp4`;
      // Check if the directory exists, if not, create it
      const dirExists = await RNFS.exists(
        `${RNFS.DocumentDirectoryPath}/recordings`
      );

      if (!dirExists) {
        await RNFS.mkdir(`${RNFS.DocumentDirectoryPath}/recordings`);
      }

      const recordingExists = await RNFS.exists(recordingUri);
      if (!recordingExists) {
        console.error(`Recording file does not exist at ${recordingUri}`);
        return;
      }

      const recordingStats = await RNFS.stat(recordingUri);
      if (!recordingStats.isFile()) {
        console.error(`RecordingUri is not a file: ${recordingUri}`);
        return;
      }

      // Move the recording file to the desired path
      await RNFS.moveFile(recordingUri, filePathToSave);
      console.log(
        "Recording saved successfully at:",
        `${RNFS.DocumentDirectoryPath}/recordings/${sessionId}.mp4`
      );
    } catch (error) {
      console.error("Error saving recording:", error);
    }
  };

  return (
    <SafeScreen>
      <View style={tw`flex-1`}>
        <ScrollView style={tw`flex-1`}>
          <View style={tw`p-4`}>
            <ScrollView horizontal showsHorizontalScrollIndicator={false}>
              {topicsData ? (
                topicsData?.topics?.map((topic) => (
                  <VCard
                    key={topic.id}
                    text={topic.title}
                    onPressEvent={() => {
                      setCurrentTopicId(topic.id);
                    }}
                  />
                ))
              ) : (
                <VCard text="Topic" onPressEvent={() => {}} />
              )}
            </ScrollView>

            <Text style={tw`mb-4 `}>
              {currentTopicId && topicsData
                ? getCurrentTopicById(currentTopicId)?.content
                : ""}
            </Text>
            <View style={tw`mt-4`}>
              {isRecording && (
                <View style={tw`mt-4`}>
                  <Text
                    style={tw`text-center font-bold text-[#FF4433] text-5xl	`}
                  >{`${formatTime(timer)}`}</Text>
                </View>
              )}
            </View>
          </View>
        </ScrollView>
        <View style={tw` p-4`}>
          <VButton
            text={isRecording ? "Stop Recording" : "Start Recording"}
            onPressEvent={handleButtonPress}
          />
        </View>
      </View>
    </SafeScreen>
  );
}

export default SelfPractice;
