"use client";

import ResultCard from "../(components)/resultcard";
import Map from "../(components)/map";
import HistoriqueCard from "../(components)/historiquecard";
import { useEffect, useState } from "react";
import useChatBar from "../(components)/chatbar";
import { useHistoriqueContext } from "../context/historiqueContext";

export default function Home() {
  const { newHistorique } = useHistoriqueContext();

  const [isHistoriqueVisible, setIsHistoriqueVisible] = useState(false);
  const [isResultCardVisible, setIsResultCardVisible] = useState(false);

  // Function to open the result card
  const openResultCard = () => {
    setIsHistoriqueVisible(false);
    setIsResultCardVisible(true);
  };

  const { chatbar, prompt } = useChatBar({
    onClick: () => newHistorique(prompt),
    openResultCard,
    
  });

  const toggleDisplay = (type) => {
    if (type === "historique") {
      setIsHistoriqueVisible(true);
      setIsResultCardVisible(false);
    } else if (type === "resultCard") {
      setIsHistoriqueVisible(false);
      setIsResultCardVisible(true);
    }
  };

  const closeDisplay = () => {
    setIsHistoriqueVisible(false);
    setIsResultCardVisible(false);
  };

  const toggleButton = () => {
    if (isHistoriqueVisible || isResultCardVisible) {
      return <></>;
    }
    return (
      <div className="flex flex-col gap-2">
        <div className="flex gap-4">
          <div className="cursor-pointer bg-neutral-100 h-10 w-10 border-solid border-2 border-gray-400 rounded-lg shadow-lg p-1 overflow-auto z-10 flex justify-center">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="svgClassHome fill-slate-900"
              viewBox="0 0 512 512"
              onClick={() => toggleDisplay("historique")}
            >
              <path d="M464 256A208 208 0 1 1 48 256a208 208 0 1 1 416 0zM0 256a256 256 0 1 0 512 0A256 256 0 1 0 0 256zM232 120l0 136c0 8 4 15.5 10.7 20l96 64c11 7.4 25.9 4.4 33.3-6.7s4.4-25.9-6.7-33.3L280 243.2 280 120c0-13.3-10.7-24-24-24s-24 10.7-24 24z" />
            </svg>
          </div>
        </div>
      </div>
    );
  };

  return (
    <>
      <div className="absolute">
        <Map />
        {(!isResultCardVisible || !isHistoriqueVisible) && chatbar}
      </div>
      <div className="w-full min-h-screen p-20 flex flex-col z-10">
        {toggleButton()}
        {isHistoriqueVisible && (
          <HistoriqueCard
            close={closeDisplay}
            isHistoriqueVisible={isHistoriqueVisible}
            setIsHistoriqueVisible={setIsHistoriqueVisible}
            setIsResultCardVisible={setIsResultCardVisible}
          />
        )}
        {isResultCardVisible && <ResultCard close={closeDisplay} />}
      </div>
    </>
  );
}
