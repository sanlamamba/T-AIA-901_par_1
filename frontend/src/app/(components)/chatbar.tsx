"use client";

import { useCallback, useState, useEffect } from "react";
import { useReactMediaRecorder } from "react-media-recorder";
import { processAudio } from "../context/requestsUtils";
import { toast } from "react-toastify";
import { div } from "motion/react-client";

export default function useChatBar({
  onClick,
  openResultCard,
  isResultCardVisible,
  closeDisplay,
}) {
  const [prompt, setPrompt] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [recordingText, setRecordingText] = useState("Recording");
  const [indexRecordingText, setIndexRecordingText] = useState(0);

  const { startRecording, stopRecording, mediaBlobUrl } = useReactMediaRecorder(
    {
      audio: true,
    }
  );

  useEffect(() => {
    let interval;

    if (isRecording) {
      interval = setInterval(() => {
        setIndexRecordingText((prevIndex) => {
          const nextIndex = (prevIndex + 1) % 5;
          setRecordingText("Recording" + ".".repeat(nextIndex));
          return nextIndex;
        });
      }, 500);
    } else {
      setRecordingText("Recording");
      setIndexRecordingText(0);
    }

    return () => clearInterval(interval);
  }, [isRecording]);

  const startMicrophone = useCallback(() => {
    try {
      startRecording();
      setIsRecording(true);
    } catch {
      toast.error("An error occurred while starting the recording.");
    }
  }, [startRecording]);

  const stopMicrophone = useCallback(async () => {
    try {
      setIsRecording(false);
      await stopRecording();
    } catch {
      toast.error("An error occurred while stopping the recording.");
    }
  }, [stopRecording]);

  const handleSave = useCallback(async () => {
    try {
      if (!mediaBlobUrl) return;

      const audioBlob = await fetch(mediaBlobUrl).then((res) => res.blob());
      const audioFile = new File([audioBlob], "voice.wav", {
        type: "audio/wav",
      });

      const transcript = await processAudio(mediaBlobUrl);
      setPrompt(transcript);
    } catch {
      toast.error("An error occurred while processing the audio.");
    }
  }, [mediaBlobUrl]);

  const handleSend = useCallback(async () => {
    if (isRecording) {
      await stopMicrophone();
      await handleSave();
    }
    onClick(prompt);

    if (openResultCard) {
      openResultCard();
    }
  }, [
    isRecording,
    stopMicrophone,
    handleSave,
    onClick,
    prompt,
    openResultCard,
  ]);

  return {
    prompt,
    chatbar: (
      <div className="fixed bottom-10 left-1/2 transform -translate-x-1/2 z-10 max-w-6xl w-full px-4">
        <div
          className="border-solid border-2 border-slate-100 rounded-full shadow-lg px-8 py-6 bg-white"
          id="chatbar"
        >
          <form className="flex gap-4 items-center">
            {!isResultCardVisible && !isRecording ? (
              <input
                type="text"
                name="message"
                placeholder="Enter your message"
                className="flex-grow px-4 focus:outline-none"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
              />
            ) : (
              <span className="flex-grow px-4 focus:outline-none">
                {isResultCardVisible ? "" : recordingText}
              </span>
            )}

            <div className="flex gap-8 items-center">
              {isResultCardVisible ? (
                <Icon
                  onClick={closeDisplay}
                  className="cursor-pointer svgClassChatbar fill-slate-500 hover:fill-black"
                  path="M9.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.2 288 416 288c17.7 0 32-14.3 32-32s-14.3-32-32-32l-306.7 0L214.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160z"
                />
              ) : isRecording ? (
                <Icon
                  onClick={stopMicrophone}
                  className="cursor-pointer svgClassChatbar fill-red-500 hover:fill-red-700"
                  path="M135.2 17.7C140.6 6.8 151.7 0 163.8 0L284.2 0c12.1 0 23.2 6.8 28.6 17.7L320 32l96 0c17.7 0 32 14.3 32 32s-14.3 32-32 32L32 96C14.3 96 0 81.7 0 64S14.3 32 32 32l96 0 7.2-14.3zM32 128l384 0 0 320c0 35.3-28.7 64-64 64L96 512c-35.3 0-64-28.7-64-64l0-320zm96 64c-8.8 0-16 7.2-16 16l0 224c0 8.8 7.2 16 16 16s16-7.2 16-16l0-224c0-8.8-7.2-16-16-16zm96 0c-8.8 0-16 7.2-16 16l0 224c0 8.8 7.2 16 16 16s16-7.2 16-16l0-224c0-8.8-7.2-16-16-16zm96 0c-8.8 0-16 7.2-16 16l0 224c0 8.8 7.2 16 16 16s16-7.2 16-16l0-224c0-8.8-7.2-16-16-16z"
                />
              ) : (
                <>
                  <Icon
                    onClick={startMicrophone}
                    className="cursor-pointer svgClassChatbar fill-slate-500 hover:fill-black"
                    path="M192 0C139 0 96 43 96 96l0 160c0 53 43 96 96 96s96-43 96-96l0-160c0-53-43-96-96-96zM64 216c0-13.3-10.7-24-24-24s-24 10.7-24 24l0 40c0 89.1 66.2 162.7 152 174.4l0 33.6-48 0c-13.3 0-24 10.7-24 24s10.7 24 24 24l72 0 72 0c13.3 0 24-10.7 24-24s-10.7-24-24-24l-48 0 0-33.6c85.8-11.7 152-85.3 152-174.4l0-40c0-13.3-10.7-24-24-24s-24 10.7-24 24l0 40c0 70.7-57.3 128-128 128s-128-57.3-128-128l0-40z"
                  />
                </>
              )}
              <Icon
                onClick={handleSend}
                className={`cursor-pointer svgClassChatbar hover:fill-black ${
                  isRecording ? "fill-green-500" : "fill-slate-500"
                }`}
                path="M16.1 260.2c-22.6 12.9-20.5 47.3 3.6 57.3L160 376l0 103.3c0 18.1 14.6 32.7 32.7 32.7c9.7 0 18.9-4.3 25.1-11.8l62-74.3 123.9 51.6c18.9 7.9 40.8-4.5 43.9-24.7l64-416c1.9-12.1-3.4-24.3-13.5-31.2s-23.3-7.5-34-1.4l-448 256zm52.1 25.5L409.7 90.6 190.1 336l1.2 1L68.2 285.7zM403.3 425.4L236.7 355.9 450.8 116.6 403.3 425.4z"
              />
            </div>
          </form>
        </div>
      </div>
    ),
  };
}

function Icon({ onClick, className, path }) {
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
