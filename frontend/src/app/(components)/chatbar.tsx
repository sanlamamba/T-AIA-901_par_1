"use client";

import { useCallback, useState } from "react";
import { toast } from "react-toastify";
import Recorder from "./recorder";

interface Props {
  onClick: (prompt: string) => Promise<void>;
  openResultCard?: () => void;
  isResultCardVisible: boolean;
  closeDisplay: () => void;
}

export default function useChatBar({
  onClick,
  openResultCard,
  isResultCardVisible,
  closeDisplay,
}: Props) {
  const [prompt, setPrompt] = useState("");
  const [recordingText, setRecordingText] = useState("Recording");
  const [isRecording, setIsRecording] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSend = useCallback(async () => {
    if (!prompt.trim()) {
      toast.info("Please record or enter a message before sending.");
      return;
    }
    try {
      setLoading(true);
      try {
        const res = await onClick(prompt);
        console.log("PATH :", res);
        if (res.error) {
          toast.error(res.message);
        } else {
          setPrompt("");
          if (openResultCard) {
            openResultCard();
          }
        }
      } catch (err: any) {
        toast.error(err.response.data.message);
      }
    } catch (error) {
      console.error("Error sending message", error);
    } finally {
      setLoading(false);
    }
  }, [onClick, prompt, openResultCard]);

  return {
    prompt,
    chatbar: (
      <div className="relative">
        <div className="fixed bottom-10 left-1/2 transform -translate-x-1/2 z-10 max-w-6xl w-full px-4">
          <div
            className="border-solid border-2 border-slate-100 rounded-full shadow-lg px-8 py-6 bg-white relative"
            id="chatbar"
          >
            {loading ? (
              <Loader />
            ) : (
              <>
                <form
                  className="flex gap-4 items-center"
                  onSubmit={(e) => {
                    e.preventDefault();
                    handleSend();
                  }}
                >
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
                    <span className="flex-grow px-4">
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
                    ) : (
                      <Recorder
                        isRecording={isRecording}
                        setIsRecording={setIsRecording}
                        setPrompt={setPrompt}
                        setLoading={setLoading}
                      />
                    )}
                    {!isRecording && (
                      <Icon
                        onClick={handleSend}
                        className={`cursor-pointer svgClassChatbar hover:fill-blue-300 ${
                          prompt != "" ? "fill-blue-500" : "fill-slate-500"
                        }`}
                        path="M16.1 260.2c-22.6 12.9-20.5 47.3 3.6 57.3L160 376l0 103.3c0 18.1 14.6 32.7 32.7 32.7c9.7 0 18.9-4.3 25.1-11.8l62-74.3 123.9 51.6c18.9 7.9 40.8-4.5 43.9-24.7l64-416c1.9-12.1-3.4-24.3-13.5-31.2s-23.3-7.5-34-1.4l-448 256zm52.1 25.5L409.7 90.6 190.1 336l1.2 1L68.2 285.7zM403.3 425.4L236.7 355.9 450.8 116.6 403.3 425.4z"
                      />
                    )}
                  </div>
                </form>
              </>
            )}
          </div>
        </div>
      </div>
    ),
  };
}

interface IconProps {
  onClick?: () => void;
  className: string;
  path: string;
}

// A reusable Icon component.
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

// A simple Loader component. Customize the spinner as desired.
function Loader() {
  return (
    <div className="flex flex-col items-center">
      <div className="animate-spin rounded-full h-6 w-6 border-t-2 border-b-2 border-blue-500"></div>
      {/* <span className="mt-2 text-blue-500">Loading...</span> */}
    </div>
  );
}
