"use client";

import { useEffect, useState } from "react";
import { baseURL } from "../context/axiosInstance";
import { useHistoriqueContext } from "../context/historiqueContext";

export default function Map({}) {
  const { selectedHistorique } = useHistoriqueContext();
  const [ mapUrl, setMapUrl ] = useState({})

  useEffect(()=>{    
    selectedHistorique.mapUrl == null ? setMapUrl("/assets/map.html") : setMapUrl(`${baseURL}${selectedHistorique.mapUrl}`)
  }, [selectedHistorique])

  return (
    <>
      <iframe
        className="flex items-center justify-center w-screen h-screen  -z-50"
        src={mapUrl}
        width="100%"
      ></iframe>
    </>
  );
}
