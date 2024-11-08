"use client";

import { FormEvent } from "react";
import { EventEmitter } from "stream";
import Image from "next/image";
import { baseURL } from "../context/axiosInstance";

export default function Map({mapUrl}) {
  const getMap = () => {
    if (mapUrl == "/assets/map.html") return mapUrl;
    let result = baseURL + mapUrl;
    return result;
  };

  return (
    <>
      <iframe
        className="flex items-center justify-center w-screen h-screen  -z-50"
        src={getMap()}
        width="100%"
      ></iframe>
    </>
  );
}
