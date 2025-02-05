"use client";

import { useEffect, useState } from "react";
import { baseURL } from "../context/axiosInstance";
import { useHistoriqueContext } from "../context/historiqueContext";

export default function Map() {
  const selectedHistorique = useHistoriqueContext();
  const [mapUrl, setMapUrl] = useState<string>();
  useEffect(() => {
    console.log(selectedHistorique);
    if (selectedHistorique?.mapUrl === undefined) {
      setMapUrl("/assets/map.html");
    }
    if (!selectedHistorique) {
      return;
    }
    !selectedHistorique.mapUrl
      ? setMapUrl("/assets/map.html")
      : setMapUrl(`${baseURL}${selectedHistorique.mapUrl}`);
    selectedHistorique.mapUrl = undefined;
  }, [selectedHistorique]);

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
