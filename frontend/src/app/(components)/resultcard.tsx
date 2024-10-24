'use client'

import { FormEvent } from "react";
import { EventEmitter } from "stream";
import {circle} from "../(assets)/circle-regular.svg"

export default function ResultCard(){
    const gares = [
        { id: 0, label : "From",  nom: "Gare de Lyon", chiffre: 10 },
        { id: 1, label : "Step", nom: "Gare du Nord", chiffre: 6 },
        { id: 2, label : "Step", nom: "Sarcelles", chiffre: 8 },
        { id: 3, label : "Step", nom: "Kremlin-Bicêtre", chiffre: 2 },
        { id: 4, label : "Step", nom: "Marseille", chiffre: 16 },
        { id: 5, label : "Destination", nom: "Gare Montparnasse", chiffre : 5 },
      ];
    return(
      <>
        <div className="bg-white h-min min-h-96 max-h-128 w-1/3 border-solid border-2 border-slate-100 rounded-lg shadow-lg p-8 overflow-auto z-10">
            <div className="grid gap-y-4">
                <h1 className="text-2xl font-semibold">Votre trajet </h1>
                <hr />
            </div>

            <div className="pt-4 h-full ">
            {gares.map((gare) => (
                    <div className="w-full mb-3">
                        <div className="text-sm text-slate-500">{gare.label == "Step" ? "Arrêt " + gare.id : gare.label}</div>
                        <div className="flex justify-between items-center">
                            <div className="text-lg font-semibold">{gare.nom}</div>
                            <div className="flex justify-between gap-6 text-sm text-black-500">
                                <div>{gare.chiffre}mn</div>
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" className={`svgClass ${gare.label == "From" ? 'fill-green-500' : gare.label == "Destination" ? 'fill-red-500' : 'fill-slate-500'}`}>
                                    <path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512z"/>
                                </svg>
                            </div>
                        </div>
                    </div>
            ))}
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