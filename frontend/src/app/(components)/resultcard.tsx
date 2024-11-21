"use client";

import { useHistoriqueContext } from "../context/historiqueContext";

export default function ResultCard({ close }) {
  const { selectedHistorique } = useHistoriqueContext();
  const tempsTotal =
    selectedHistorique?.etapes?.reduce(
      (total, etape) => total + etape.duree,
      0
    ) || 0;

  return (
    <div className="bg-white h-min min-h-96 max-h-128 w-1/3 border-solid border-2 border-slate-100 rounded-lg shadow-lg overflow-auto relative">
      {/* Header */}
      <div className="w-full bg-white sticky top-0 z-20 border-b-2 border-slate-100 p-4">
        <h1 className="text-2xl font-semibold mb-0">Votre trajet</h1>
        <p className="text-xs text-slate-500">
          Prompt : {selectedHistorique.prompt}
        </p>
      </div>

      {/* Étapes */}
      <div className="h-full z-10 p-4">
        <ul className="list-none">
          {selectedHistorique?.etapes &&
            selectedHistorique.etapes.map((etape) => (
              <li key={etape.id} className="w-full mb-3">
                <div className="text-sm text-slate-500 mb-1">
                  {etape.label} :
                </div>
                <div className="flex justify-between items-center">
                  {/* Ville */}
                  <div className="text-lg font-semibold">{etape.ville}</div>
                  {/* Détails */}
                  <div className="flex justify-between items-center gap-6 text-sm text-black-500">
                    <div>{etape.duree}mn</div>
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
          <div className="text-sm text-slate-500">Temps de trajet total :</div>
          <div className="flex justify-between items-center gap-6 text-sm text-black-500">
            <div className="font-bold">{tempsTotal}mn</div>
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
