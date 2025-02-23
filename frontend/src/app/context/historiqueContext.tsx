"use client";

import {
  createHistorique,
  getHistoriquesByUserId,
  Historique,
} from "@/actions/historiqueActions";
import { IEtape } from "@/types/IHistorique";
import { useAuth } from "@clerk/nextjs";
import {
  createContext,
  ReactNode,
  useCallback,
  useContext,
  useEffect,
  useState,
} from "react";
import { processPathfinding } from "./requestsUtils";

interface IHistoriqueContext {
  userId: string | null | undefined;
  selectedHistorique?: Historique;
  historiques: Historique[];
  fetchHistorique: () => Promise<void>;
  newHistorique: (prompt: string) => Promise<void>;
  setSelectedHistorique: (historique: Historique) => void;
  resetSelectedHistorique: () => void;
  mapUrl?: string;
  setMapUrl?: (url: string) => void;
  prompt?: string;
}

const HistoriqueContext = createContext<IHistoriqueContext | null | undefined>(
  undefined
);

export const useHistoriqueContext = () => useContext(HistoriqueContext);

interface HistoriqueProviderProps {
  children: ReactNode;
}
export const HistoriqueContextProvider: React.FC<HistoriqueProviderProps> = ({
  children,
}) => {
  const { userId } = useAuth();
  const [selectedHistorique, setSelectedHistorique] = useState<Historique>();
  const [historiques, setHistoriques] = useState<Historique[]>([]);
  const [mapUrl, setMapUrl] = useState<string>();

  const fetchHistorique = useCallback(async () => {
    if (!userId) return;

    try {
      const result: Historique[] | undefined = await getHistoriquesByUserId(
        userId
      );
      setHistoriques(result || []);
    } catch (error: any) {
      console.error(
        "Erreur lors du chargement des historiques:",
        error.response?.data || error.message || error
      );
    }
  }, [userId]);

  const newHistorique = useCallback(
    async (prompt: string) => {
      if (!userId) return;

      try {
        const optimalPath = await processPathfinding(prompt);
        if (optimalPath.error) {
          console.log(
            "Erreur lors de la création de l’historique:",
            optimalPath
          );
          return {
            error: true,
            message: optimalPath.message,
          };
        }

        if (optimalPath || optimalPath.pathfinding_result) {
          const historique: Historique = {
            userId,
            prompt,
            mapUrl: optimalPath.pathfinding_result.map_url,
            distance: optimalPath.pathfinding_result.distance,
            etapes: optimalPath.pathfinding_result.path.map(
              (etape: IEtape, index: number) => ({
                ville: etape,
                duree: parseInt(
                  optimalPath.pathfinding_result.path_codes[index],
                  10
                ),
                label:
                  index === 0
                    ? "From"
                    : index === optimalPath.pathfinding_result.path.length - 1
                    ? "Destination"
                    : "Step",
              })
            ),
          };
          const resultHistorique: Historique | null | undefined =
            await createHistorique(historique);
          if (!resultHistorique) {
            throw new Error("Erreur lors de la création de l’historique.");
          }
          setSelectedHistorique(resultHistorique);
          setMapUrl(resultHistorique.mapUrl);
          await fetchHistorique();
          return resultHistorique;
        }
      } catch (error: any) {
        console.error(
          "Erreur lors de la création de l’historique:",
          error.response?.data || error.message || error
        );
      }
    },
    [userId, fetchHistorique]
  );

  const resetSelectedHistorique = () => {
    setSelectedHistorique(undefined);
  };

  useEffect(() => {
    fetchHistorique().catch((error) => {
      console.error(
        "Erreur inattendue lors du chargement des historiques:",
        error
      );
    });
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
        mapUrl,
        setMapUrl,
      }}
    >
      {children}
    </HistoriqueContext.Provider>
  );
};
