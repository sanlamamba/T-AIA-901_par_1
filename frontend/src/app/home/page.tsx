"use client";

import ResultCard from "../(components)/resultcard";
import Map from "../(components)/map";
import { useState, useEffect, use } from "react";
import useChatBar from "../(components)/chatbar";
import { processPathfinding } from "../context/requestsUtils";
import { createHistorique, getHistoriquesByUserId, Historique,  } from "@/actions/historiqueActions";
import { useAppContext } from "../context/historiqueContext";
import { useAuth } from '@clerk/nextjs'

export default function Home() {
  const user = useAuth();

  const {selectedHistorique, setSelectedHistorique,
    historiques, setHistoriques,
    userId, setUserId} = useAppContext()

  useEffect(()=> {
    setUserId(user.userId)
  },[user])
  const [mapData, setMapData] = useState({
    path: [""],
    map_url : "",
  });

  const [isNewPrompt, setIsNewPrompt] = useState(true);

  const handleSubmit = async () => {
    const optimalPath = await processPathfinding(prompt);
    setMapData(optimalPath.pathfinding_result);
    const historique: Historique = {
      userId: userId, 
      prompt: prompt, 
      mapUrl: optimalPath.pathfinding_result.map_url, // URL de la carte
      etapes: optimalPath.pathfinding_result.path.map((etape : string, index : number) => {
          return {
              ville: etape,
              duree: 10, // a remplacer 
              label: index == 0 ? 'From' : index == optimalPath.pathfinding_result.path.length - 1 ? 'Destination' : 'Step'
          };
      }),
    };

    const resultHistorique = await createHistorique(historique);
    setSelectedHistorique(resultHistorique)
    const resultHistoriques = await getHistoriquesByUserId(resultHistorique?.userId);
    setHistoriques(resultHistoriques)
    setIsNewPrompt(false);
    console.log("selected"+JSON.stringify(selectedHistorique, null, 2))
  };
  const {chatbar, prompt} = useChatBar({onClick : handleSubmit}); 
  
  return (
    <>
      <div className="absolute">
        <Map mapUrl={selectedHistorique.mapUrl || "/assets/map.html" } />
      </div>
      <div className="w-full min-h-screen p-20 flex flex-col justify-between z-10">
        
        <ResultCard mapData={selectedHistorique} />
        {chatbar}
      </div>
    </>
  );
}
