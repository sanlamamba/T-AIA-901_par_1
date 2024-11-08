"use client";

import ResultCard from "./(components)/resultcard";
import Map from "./(components)/map";
import { useState, useEffect } from "react";
import useChatBar from "./(components)/chatbar";
import { processPathfinding } from "./context/requestsUtils";


export default function Home() {
  const [mapData, setMapData] = useState({
    algorithm: "AStar",
    distance: 166.47,
    explored_nodes: 13,
    average_node_time: 0.00030765166649451625,
    memory_usage: 0,
    path: ["La Douzillère", "Joué-lès-Tours", "Bressuire", "Chalonnes"],
    path_length: 4,
    tries: 13,
    time: 0.003999471664428711,
    
  });
  const handleSubmit = async () => {
    const optimalPath = await processPathfinding(prompt);
    setMapData(optimalPath.pathfinding_result)
  };
  const {chatbar, prompt} = useChatBar({onClick : handleSubmit}); 

  return (
    <>
      <div className="absolute">
        <Map mapUrl={mapData.map_url || "/assets/map.html" } />
      </div>
      <div className="w-full min-h-screen p-20 flex flex-col justify-between z-10">
        <ResultCard mapData={mapData} />
        {chatbar}
      </div>
    </>
  );
}
