"use client";

import ResultCard from "../(components)/resultcard";
import Map from "../(components)/map";
import { useState, useEffect, use } from "react";
import useChatBar from "../(components)/chatbar";
import { processPathfinding } from "../context/requestsUtils";
import { createHistorique, getHistoriquesByUserId, Historique,  } from "@/actions/historiqueActions";
import { useHistoriqueContext } from "../context/historiqueContext";

export default function Home() {
  const { newHistorique } = useHistoriqueContext();
  const [ selectedHistorique, setSelectedHistorique] = useState({})

  const {chatbar, prompt} = useChatBar({onClick: () => newHistorique(prompt)}); 
  // mapUrl={selectedHistorique.mapUrl || "/assets/map.html" }
  return (
    <>
      <div className="absolute">
        <Map />
      </div>
      <div className="w-full min-h-screen p-20 flex flex-col justify-between z-10">
        
        <ResultCard mapData={selectedHistorique} />
        {chatbar}
      </div>
    </>
  );
}
