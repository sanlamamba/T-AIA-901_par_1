'use client'

import { FormEvent, useEffect } from "react";
import { useHistoriqueContext } from "../context/historiqueContext";

export default function ResultCard({}){
    const { selectedHistorique } = useHistoriqueContext();
    if (!selectedHistorique || !selectedHistorique.etapes) {
        return (
            <><div></div></>
        );
    }

    return(
      <>

        <div className="bg-white h-min min-h-96 max-h-128 w-1/3 border-solid border-2 border-slate-100 rounded-lg shadow-lg p-8 overflow-auto z-10">
            <div className="w-full bg-white sticky top-0 z-20">
                <h1 className="text-2xl font-semibold mb-4">Votre trajet </h1>
                <hr />
            </div>

            <div className="h-full z-19">
                <ul>
                {selectedHistorique.etapes && selectedHistorique.etapes.map((etape) => (
                    <li key={etape.id} className="w-full mb-3">
                        <div className="text-sm text-slate-500">{etape.label}</div>
                        <div className="flex justify-between items-center">
                            <div className="text-lg font-semibold">{etape.ville}</div>
                            <div className="flex justify-between gap-6 text-sm text-black-500">
                                <div>{etape.duree}mn</div>
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" className={`svgClass ${etape.label == "From" ? 'fill-green-500' : etape.label == "Destination" ? 'fill-red-500' : 'fill-slate-500'}`}>
                                    <path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512z"/>
                                </svg>
                            </div>
                        </div>
                    </li>
            ))}
                </ul>
            
            </div>
            <div className="w-full mt-4">
            <hr />
                <div className="flex justify-between items-center mt-2">
                    <div className="text-sm text-slate-500">Temps de trajet total</div>
                    <div className="flex justify-between gap-6 text-sm text-black-500">
                        <div>150mn</div>
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" className={`svgClass fill-white-500`}>
                            <path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512z"/>
                        </svg>
                    </div>
                </div>
            </div>          
        </div>
      </>
    )
  }