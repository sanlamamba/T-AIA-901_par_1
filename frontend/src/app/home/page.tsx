"use client";

import ResultCard from "../(components)/resultcard";
import Map from "../(components)/map";
import HistoriqueCard from "../(components)/historiquecard";
import { useEffect, useState } from "react";
import useChatBar from "../(components)/chatbar";
import { useHistoriqueContext } from "../context/historiqueContext";

export default function Home() {
  const { newHistorique } = useHistoriqueContext();
  const [selectedHistorique] = useState({});
  const [displayHistorique, setDisplayHistorique] = useState(true);
  const { chatbar, prompt } = useChatBar({
    onClick: () => newHistorique(prompt),
  });

  useEffect(()=> {
    if(selectedHistorique != {}){
     setDisplayHistorique(false)
    }
  }, [selectedHistorique])

  if (displayHistorique) {
    return (
      <>
        <div className="absolute">
          <Map />
        </div>
        <div className="w-full min-h-screen p-20 flex flex-col justify-between z-10">
          <div className="flex flex-col gap-2">
            <div className="flex gap-4">
              <div className="cursor-pointer bg-neutral-100 h-10 w-10 border-solid border-2 border-gray-400 rounded-lg shadow-lg p-1 overflow-auto z-10 flex justify-center">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className={` svgClassHome fill-slate-900`}
                  viewBox="0 0 512 512"
                >
                  <path d="M464 256A208 208 0 1 1 48 256a208 208 0 1 1 416 0zM0 256a256 256 0 1 0 512 0A256 256 0 1 0 0 256zM232 120l0 136c0 8 4 15.5 10.7 20l96 64c11 7.4 25.9 4.4 33.3-6.7s4.4-25.9-6.7-33.3L280 243.2 280 120c0-13.3-10.7-24-24-24s-24 10.7-24 24z" />
                </svg>
              </div>
              <div className={`cursor-pointer bg-white h-10 w-10 border-solid border-2 border-slate-100 rounded-lg shadow-lg p-1 overflow-auto z-10 flex justify-center`}
                onClick={()=>setDisplayHistorique(false)}
              >
                <svg xmlns="http://www.w3.org/2000/svg" className={`svgClassHome fill-slate-900`} viewBox="0 0 384 512">
                  <path d="M215.7 499.2C267 435 384 279.4 384 192C384 86 298 0 192 0S0 86 0 192c0 87.4 117 243 168.3 307.2c12.3 15.3 35.1 15.3 47.4 0zM192 128a64 64 0 1 1 0 128 64 64 0 1 1 0-128z" />
                </svg>
              </div>
            </div>

            <HistoriqueCard />
          </div>
          {chatbar}
        </div>
      </>
    );
  } else if (!displayHistorique && selectedHistorique == {}) {
    return (
      <>
        <div className="absolute">
          <Map />
        </div>
        <div className="w-full min-h-screen p-20 flex flex-col justify-between z-10">
          <div></div>
          {chatbar}
        </div>
      </>
    );
  } else if (!displayHistorique && selectedHistorique != {}) {
    return (
      <>
        <div className="absolute">
          <Map />
        </div>
        <div className="w-full min-h-screen p-20 flex flex-col justify-between z-10">
        <div className="flex flex-col gap-2">
            <div className="flex gap-4">
              <div className="cursor-pointer bg-white h-10 w-10 border-solid border-2 border-slate-100 rounded-lg shadow-lg p-1 overflow-auto z-10 flex justify-center"
                onClick={()=>setDisplayHistorique(true)}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className={`svgClassHome fill-slate-900`}
                  viewBox="0 0 512 512"
                >
                  <path d="M464 256A208 208 0 1 1 48 256a208 208 0 1 1 416 0zM0 256a256 256 0 1 0 512 0A256 256 0 1 0 0 256zM232 120l0 136c0 8 4 15.5 10.7 20l96 64c11 7.4 25.9 4.4 33.3-6.7s4.4-25.9-6.7-33.3L280 243.2 280 120c0-13.3-10.7-24-24-24s-24 10.7-24 24z" />
                </svg>
              </div>
              <div className="cursor-pointer bg-neutral-100 h-10 w-10 border-solid border-2 border-gray-400 rounded-lg shadow-lg p-1 overflow-auto z-10 flex justify-center" 
                
              >
                <svg xmlns="http://www.w3.org/2000/svg" className={`  svgClassHome fill-slate-900`} viewBox="0 0 384 512">
                  <path d="M215.7 499.2C267 435 384 279.4 384 192C384 86 298 0 192 0S0 86 0 192c0 87.4 117 243 168.3 307.2c12.3 15.3 35.1 15.3 47.4 0zM192 128a64 64 0 1 1 0 128 64 64 0 1 1 0-128z" />
                </svg>
              </div>
            </div>

            <ResultCard />
          </div>
          {chatbar}
        </div>
      </>
    );
  }
}
