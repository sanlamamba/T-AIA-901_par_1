import React, { useRef, useState } from "react";
import axiosInstance from "../context/axiosInstance";

interface RecorderProps {
  isRecording: boolean;
  setIsRecording: React.Dispatch<React.SetStateAction<boolean>>;
  setPrompt: React.Dispatch<React.SetStateAction<string>>;
  setLoading: React.Dispatch<React.SetStateAction<boolean>>;
}

export const processAudio = async (
  audioFile: File
): Promise<{ transcript: string }> => {
  try {
    const formData = new FormData();
    formData.append("file", audioFile);

    const response = await axiosInstance.post("/stt/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    return response.data;
  } catch (err: any) {
    console.error("Error in processAudio:", err.response?.data || err.message);
    throw err;
  }
};

async function convertToMonoWav(blob: Blob): Promise<Blob> {
  const arrayBuffer = await blob.arrayBuffer();
  const audioContext = new OfflineAudioContext(1, 44100 * 40, 44100);
  const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);

  const numChannels = audioBuffer.numberOfChannels;
  const length = audioBuffer.length;
  const sampleRate = audioBuffer.sampleRate;
  const monoBuffer = new Float32Array(length);

  for (let channel = 0; channel < numChannels; channel++) {
    const channelData = audioBuffer.getChannelData(channel);
    for (let i = 0; i < length; i++) {
      monoBuffer[i] += channelData[i];
    }
  }

  for (let i = 0; i < length; i++) {
    monoBuffer[i] /= numChannels;
  }

  const wavBuffer = encodeWAV(monoBuffer, sampleRate);
  return new Blob([wavBuffer], { type: "audio/wav" });
}

function encodeWAV(samples: Float32Array, sampleRate: number): ArrayBuffer {
  const buffer = new ArrayBuffer(44 + samples.length * 2);
  const view = new DataView(buffer);

  const writeString = (offset: number, string: string) => {
    for (let i = 0; i < string.length; i++) {
      view.setUint8(offset + i, string.charCodeAt(i));
    }
  };

  writeString(0, "RIFF");
  view.setUint32(4, 36 + samples.length * 2, true);
  writeString(8, "WAVE");
  writeString(12, "fmt ");
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true);
  view.setUint16(22, 1, true);
  view.setUint32(24, sampleRate, true);
  view.setUint32(28, sampleRate * 2, true);
  view.setUint16(32, 2, true);
  view.setUint16(34, 16, true);
  writeString(36, "data");
  view.setUint32(40, samples.length * 2, true);

  let offset = 44;
  for (let i = 0; i < samples.length; i++) {
    let s = Math.max(-1, Math.min(1, samples[i]));
    view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7fff, true);
    offset += 2;
  }

  return buffer;
}

export default function Recorder({
  isRecording,
  setIsRecording,
  setPrompt,
  setLoading,
}: RecorderProps) {
  const [recordedURL, setRecordedURL] = useState<string>("");
  const [isCancelled, setIsCancelled] = useState<boolean>(false);

  const mediaStream = useRef<MediaStream | null>(null);
  const mediaRecorder = useRef<MediaRecorder | null>(null);
  const chunks = useRef<Blob[]>([]);

  const startRecording = async () => {
    setPrompt("");
    setRecordedURL("");
    setIsRecording(true);
    setIsCancelled(false);

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaStream.current = stream;
      mediaRecorder.current = new MediaRecorder(stream);

      mediaRecorder.current.ondataavailable = (e) => {
        if (e.data.size > 0) chunks.current.push(e.data);
      };

      mediaRecorder.current.onstop = async () => {
        if (isCancelled) {
          setIsCancelled(false);
          chunks.current = [];
          return;
        }

        const recordedBlob = new Blob(chunks.current, { type: "audio/mp3" });
        const wavBlob = await convertToMonoWav(recordedBlob);
        setRecordedURL(URL.createObjectURL(wavBlob));
        chunks.current = [];

        const audioFile = new File([wavBlob], "voice.wav", {
          type: "audio/wav",
        });
        setLoading(true);
        try {
          const result = await processAudio(audioFile);
          setPrompt(result.transcript || "");
        } catch (error) {
          console.error("Error processing audio", error);
        } finally {
          setLoading(false);
        }
      };

      mediaRecorder.current.start();
    } catch (error) {
      console.error("Error starting recording:", error);
    }
  };

  const stopRecording = () => {
    setIsRecording(false);
    if (mediaRecorder.current) {
      mediaRecorder.current.stop();
      mediaStream.current?.getTracks().forEach((track) => track.stop());
    }
  };

  const deleteRecording = () => {
    setIsCancelled(true);
    if (isRecording) stopRecording();
    setRecordedURL("");
    setPrompt("");
    chunks.current = [];
  };

  return (
    <>
      {isRecording ? (
        <Icon
          onClick={stopRecording}
          className={`cursor-pointer svgClassChatbar hover:fill-black ${
            isRecording ? "fill-green-500" : "fill-slate-500"
          }`}
          path="M16.1 260.2c-22.6 12.9-20.5 47.3 3.6 57.3L160 376l0 103.3c0 18.1 14.6 32.7 32.7 32.7c9.7 0 18.9-4.3 25.1-11.8l62-74.3 123.9 51.6c18.9 7.9 40.8-4.5 43.9-24.7l64-416c1.9-12.1-3.4-24.3-13.5-31.2s-23.3-7.5-34-1.4l-448 256zm52.1 25.5L409.7 90.6 190.1 336l1.2 1L68.2 285.7zM403.3 425.4L236.7 355.9 450.8 116.6 403.3 425.4z"
        />
      ) : (
        <Icon
          onClick={startRecording}
          className="cursor-pointer svgClassChatbar fill-slate-500 hover:fill-black"
          path="M192 0C139 0 96 43 96 96l0 160c0 53 43 96 96 96s96-43 96-96l0-160c0-53-43-96-96-96zM64 216c0-13.3-10.7-24-24-24s-24 10.7-24 24l0 40c0 89.1 66.2 162.7 152 174.4l0 33.6-48 0c-13.3 0-24 10.7-24 24s10.7 24 24 24l72 0 72 0c13.3 0 24-10.7 24-24s-10.7-24-24-24l-48 0 0-33.6c85.8-11.7 152-85.3 152-174.4l0-40c0-13.3-10.7-24-24-24s-24 10.7-24 24l0 40c0 70.7-57.3 128-128 128s-128-57.3-128-128l0-40z"
        />
      )}
    </>
  );
}

interface IconProps {
  onClick?: () => void;
  className?: string;
  path: string;
}

function Icon({ onClick, className, path }: IconProps) {
  return (
    <svg
      onClick={onClick}
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 512 512"
      className={className}
    >
      <path d={path} />
    </svg>
  );
}
