from pydub import AudioSegment
import librosa
import numpy as np
import speech_recognition as sr

class AudioAnalysisService:
    def __init__(self, file_path):
        self.file_path = file_path
        self.audio_data, self.sample_rate = librosa.load(self.file_path, sr=None)

    def get_duration(self):
        duration = librosa.get_duration(y=self.audio_data, sr=self.sample_rate)
        return duration

    def get_tempo(self):
        onset_env = librosa.onset.onset_strength(y=self.audio_data, sr=self.sample_rate)
        tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=self.sample_rate)
        return tempo

    def get_spectral_centroid(self):
        spectral_centroid = librosa.feature.spectral_centroid(y=self.audio_data, sr=self.sample_rate)
        return np.mean(spectral_centroid)

    def get_pitch(self):
        pitches, magnitudes = librosa.core.piptrack(y=self.audio_data, sr=self.sample_rate)
        pitch = [pitches[magnitudes[:, i].argmax()] for i in range(magnitudes.shape[1]) if magnitudes[:, i].max() > 0]
        return np.mean(pitch)

    def transcribe_audio(self):
        recognizer = sr.Recognizer()
        with sr.AudioFile(self.file_path) as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                text = ""
        print(text)
        return text

    def analyze_fluency(self):
        transcript = self.transcribe_audio()
        words = len(transcript.split())
        duration_minutes = self.get_duration() / 60
        if duration_minutes > 0:
            words_per_minute = words / duration_minutes
        else:
            words_per_minute = 0
        return words_per_minute

    def analyze(self):
        duration = self.get_duration()
        tempo = self.get_tempo()
        spectral_centroid = self.get_spectral_centroid()
        pitch = self.get_pitch()
        fluency = self.analyze_fluency()

        analysis_results = {
            "duration": duration,
            "tempo": tempo,
            "spectral_centroid": spectral_centroid,
            "pitch": pitch,
            "fluency": fluency
        }

        return analysis_results

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python audio_analysis_service.py <path_to_audio_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    service = AudioAnalysisService(file_path)
    results = service.analyze()
    
    print("Analysis Results:")
    for key, value in results.items():
        print(f"{key}: {value}")
