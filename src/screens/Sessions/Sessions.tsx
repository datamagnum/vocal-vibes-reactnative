import React, { useState, useEffect } from "react";
import { View, Text, FlatList } from "react-native";
import { Button } from "react-native-paper";
import RNFS from "react-native-fs";
import { Card } from "react-native-paper";
import tw from "@/twrnc.config";
import audioRecordingService from "@/services/recording.service";

function Sessions() {
  const [recordings, setRecordings] = useState<string[]>([]);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [currentRecording, setCurrentRecording] = useState<string>("");
  const [playbackTimer, setPlaybackTimer] = useState<number>(0);

  const recordingsPath = `${RNFS.DocumentDirectoryPath}/recordings`;


  // Kept this to rerender on all run
  useEffect(() => {
    const loadRecordings = async () => {
      try {
        // Get the list of files in the recordings directory
        const files = await RNFS.readdir(recordingsPath);
        // Update state with the list of recordings

        setRecordings(files);
      } catch (error) {
        console.error("Error loading recordings:", error);
      }
    };
    loadRecordings();
  });

  useEffect(() => {
    let intervalId: NodeJS.Timeout | null = null;
    if (isPlaying) {
      intervalId = setInterval(() => {
        setPlaybackTimer((prevTimer) => prevTimer + 1);
      }, 1000);
    } else {
      if (intervalId) clearInterval(intervalId);
      setPlaybackTimer(0);
    }

    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [isPlaying]);

  const playRecording = async (uri: string) => {
    try {
      if (currentRecording) {
        await audioRecordingService.stopPlayback();
      }

      setIsPlaying(true);
      setCurrentRecording(uri); // Set currently playing recording
      await audioRecordingService.startPlayback(uri);
      setIsPlaying(false);
    } catch (error) {
      console.error("Error starting playback:", error);
      setIsPlaying(false);
    }
  };

  const stopRecording = async () => {
    try {
      await audioRecordingService.stopPlayback();
      setCurrentRecording("");
    } catch (error) {
      console.error("Error stopping playback:", error);
    }
  };

  const formatTime = (seconds: number) => {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    return `${hrs < 10 ? "0" : ""}${hrs}:${mins < 10 ? "0" : ""}${mins}:${
      secs < 10 ? "0" : ""
    }${secs}`;
  };

  const renderItem = ({ item, index }: { item: string; index: number }) => (
    <View style={{ padding: 10 }}>
      <Card key={index} style={tw``}>
        <Card.Content>
          <Text>{item}</Text>
          {currentRecording === `${recordingsPath}/${item}` ? (
            <View className="flex-1">
              {/* <Text>{`Playback Timer: ${formatTime(playbackTimer)}`}</Text> */}
              <Button
                icon="stop"
                mode="elevated"
                onPress={() => stopRecording()}
              />
            </View>
          ) : (
            <Button
              icon="play"
              mode="elevated"
              onPress={() => playRecording(`${recordingsPath}/${item}`)}
            />
          )}
        </Card.Content>
      </Card>
    </View>
  );

  return (
    <View style={{ flex: 1, padding: 20 }}>
      <Text style={{ fontSize: 20, marginBottom: 10 }}>Recorded Sessions:</Text>
      {recordings.length === 0 ? (
        <Text>No recordings found</Text>
      ) : (
        <FlatList
          data={recordings}
          renderItem={renderItem}
          keyExtractor={(item, index) => index.toString()}
        />
      )}
    </View>
  );
}

export default Sessions;
