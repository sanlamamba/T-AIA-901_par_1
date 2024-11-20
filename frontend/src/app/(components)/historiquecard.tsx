"use client";

import { FormEvent, useEffect } from "react";
import { useHistoriqueContext } from "../context/historiqueContext";

export default function HistoriqueCard({}) {
  const { historiques } = useHistoriqueContext();

  return (
    <>
      <div className="bg-white h-min min-h-96 max-h-128 w-1/3 border-solid border-2 border-slate-100 rounded-lg shadow-lg p-8 overflow-auto z-10">
        <div className="w-full bg-white sticky top-0 z-20">
          <h1 className="text-2xl font-semibold mb-4">Votre historique </h1>
        </div>

        <ul className="mt-4">
          <hr />
          {historiques && historiques.length > 0 ? (
            historiques.map((historique) => {
              const etapes = historique.etapes;
              const premiereEtape = etapes[0];
              const derniereEtape = etapes[etapes.length - 1];

              return (
                <li key={historique.id} className="mb-4">
                  <div className="bg-white border-solid border-2 border-slate-100 rounded-lg shadow-lg p-4 overflow-auto w-full flex items-center gap-2 hover:bg-neutral-100">
                    <div>
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"
                className={` cursor-pointer svgClassChatbar fill-slate-900`}
              ><path d="M96 0C43 0 0 43 0 96L0 352c0 48 35.2 87.7 81.1 94.9l-46 46C28.1 499.9 33.1 512 43 512l39.7 0c8.5 0 16.6-3.4 22.6-9.4L160 448l128 0 54.6 54.6c6 6 14.1 9.4 22.6 9.4l39.7 0c10 0 15-12.1 7.9-19.1l-46-46c46-7.1 81.1-46.9 81.1-94.9l0-256c0-53-43-96-96-96L96 0zM64 96c0-17.7 14.3-32 32-32l256 0c17.7 0 32 14.3 32 32l0 96c0 17.7-14.3 32-32 32L96 224c-17.7 0-32-14.3-32-32l0-96zM224 288a48 48 0 1 1 0 96 48 48 0 1 1 0-96z"/></svg>
                    </div>
                    <div className="w-full">
                        <h2 className="text-xs text-slate-500">{historique.prompt}</h2>
                        <div className="text-sm flex justify-between">
                        <div>{premiereEtape.ville}</div>
                        <div>{derniereEtape.ville}</div>
                        </div>
                    </div>
                  </div>
                </li>
              );
            })
          ) : (
            <p className="text-gray-500">Aucun historique disponible.</p>
          )}
        </ul>
      </div>
    </>
  );
}
