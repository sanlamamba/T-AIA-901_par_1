"use client";

import React, {
  createContext,
  useContext,
  useEffect,
  useState,
  useCallback,
} from "react";
import { useAuth } from "@clerk/nextjs";
import {
  getHistoriquesByUserId,
  createHistorique,
  Historique,
} from "@/actions/historiqueActions";
import { processPathfinding } from "./requestsUtils";

const HistoriqueContext = createContext({
  userId: null,
  selectedHistorique: {},
  historiques: [],
  fetchHistorique: () => {},
  newHistorique: () => {},
  setSelectedHistorique: () => {},
  resetSelectedHistorique: () => {}, 
});

export const useHistoriqueContext = () => useContext(HistoriqueContext);

export const HistoriqueContextProvider = ({ children }) => {
  const { userId } = useAuth();
  const [selectedHistorique, setSelectedHistorique] = useState({});
  const [historiques, setHistoriques] = useState([]);

  const fetchHistorique = useCallback(async () => {
    if (!userId) return;

    try {
      const result = await getHistoriquesByUserId(userId);
      setHistoriques(result || []);
    } catch (error) {
      console.error("Erreur lors du chargement des historiques:", error);
    }
  }, [userId]);

  const newHistorique = useCallback(
    async (prompt) => {
      if (!userId) return;

      try {
        const optimalPath = await processPathfinding(prompt);

        const historique: Historique = {
          userId,
          prompt,
          mapUrl: optimalPath.pathfinding_result.map_url,
          etapes: optimalPath.pathfinding_result.path.map((etape, index) => ({
            ville: etape,
            duree: 10,
            label:
              index === 0
                ? "From"
                : index === optimalPath.pathfinding_result.path.length - 1
                ? "Destination"
                : "Step",
          })),
        };

        const resultHistorique = await createHistorique(historique);
        setSelectedHistorique((prev) => ({ ...prev, ...resultHistorique }));

        await fetchHistorique();
      } catch (error) {
        console.error("Erreur lors de la création de l’historique:", error);
      }
    },
    [userId, fetchHistorique]
  );

  const resetSelectedHistorique = () => {
    setSelectedHistorique({});
  };

  useEffect(() => {
    fetchHistorique();
  }, [fetchHistorique]);

  return (
    <HistoriqueContext.Provider
      value={{
        userId,
        selectedHistorique,
        historiques,
        fetchHistorique,
        newHistorique,
        setSelectedHistorique,
        resetSelectedHistorique,
      }}
    >
      {children}
    </HistoriqueContext.Provider>
  );
};
