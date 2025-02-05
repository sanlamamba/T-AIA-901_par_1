"use client";

import { randomUUID } from "crypto";
import { useHistoriqueContext } from "../context/historiqueContext";

interface Props {
  close: () => void;
}
export default function ResultCard({ close }: Props) {
  const historicContext = useHistoriqueContext();
  if (!historicContext) return null;
  const distanceTrajet = historicContext.selectedHistorique?.distance || 0;
  const closeCall = () => {
    close();
    historicContext.resetSelectedHistorique();
  };
  return (
    <div className="bg-white h-min min-h-96 max-h-128 w-1/3 border-solid border-2 border-slate-100 rounded-lg shadow-lg overflow-auto relative">
      <div className="w-full bg-white sticky top-0 z-20 border-b-2 border-slate-100 p-4 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold mb-0">Votre trajet</h1>
          <p className="text-xs text-slate-500">
            Prompt : {historicContext.selectedHistorique?.prompt}
          </p>
        </div>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 384 512"
          className="svgClass cursor-pointer"
          onClick={closeCall}
        >
          <path d="M342.6 150.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L192 210.7 86.6 105.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L146.7 256 41.4 361.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L192 301.3 297.4 406.6c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L237.3 256 342.6 150.6z" />
        </svg>
      </div>

      {/* Étapes */}
      <div className="h-full z-10 p-4">
        <ul className="list-none">
          {historicContext.selectedHistorique?.etapes &&
            historicContext.selectedHistorique.etapes.map((etape) => (
              <li
                key={`${etape.ville} ${randomUUID} key`}
                className="w-full mb-3"
              >
                <div className="text-sm text-slate-500 mb-1">
                  {etape.label} :
                </div>
                <div className="flex justify-between items-center">
                  {/* Ville */}
                  <div className="text-lg font-semibold">{etape.ville}</div>
                  {/* Détails */}
                  <div className="flex justify-between items-center gap-6 text-sm text-black-500">
                    <div
                      className="text-slate-600"
                      style={{ fontSize: "0.6em" }}
                    >
                      {etape.duree}
                    </div>
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 512 512"
                      className={`svgClass w-6 h-6 ${
                        etape.label === "From"
                          ? "fill-green-500"
                          : etape.label === "Destination"
                          ? "fill-red-500"
                          : "fill-slate-500"
                      }`}
                    >
                      <path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512z" />
                    </svg>
                  </div>
                </div>
              </li>
            ))}
        </ul>
      </div>

      {/* Footer */}
      <div className="w-full mt-4 sticky bottom-0 bg-white p-4 border-t-2 border-slate-100">
        <div className="flex justify-between items-center">
          <div className="text-sm text-slate-500">
            Distance de trajet total :
          </div>
          <div className="flex justify-between items-center gap-6 text-sm text-black-500">
            <div className="font-bold">{distanceTrajet}</div>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 512 512"
              className="svgClass w-6 h-6 fill-blue-500"
            >
              <path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512z" />
            </svg>
          </div>
        </div>
      </div>
    </div>
  );
}
