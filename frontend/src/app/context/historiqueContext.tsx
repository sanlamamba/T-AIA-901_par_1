'use client';
import { useAuth } from '@clerk/nextjs';
import React, { createContext, useContext, useEffect, useState } from 'react';
import { getHistoriquesByUserId } from '@/actions/historiqueActions';
import { processPathfinding } from './requestsUtils';
import { Historique, createHistorique } from '@/actions/historiqueActions';

const HistoriqueContext = createContext({
  userId: null,
  selectedHistorique: {},
  historiques: {},
  fetchHistorique: () => {},
  newHistorique: () => {}, 
});

export const useHistoriqueContext = () => useContext(HistoriqueContext);

export const HistoriqueContextProvider = ({ children }) => {
  const { userId } = useAuth();
  const [selectedHistorique, setSelectedHistorique] = useState({});
  const [historiques, setHistoriques] = useState({});

  const fetchHistorique = async () => {
    try {
      if (userId) {
        const result = await getHistoriquesByUserId(userId);
        setHistoriques(result);
        //console.log('Liste des historiques :' + JSON.stringify(historiques));
      }
    } catch (error) {
      console.error('Erreur lors du chargement des historiques:', error);
    }
  };

  const newHistorique = async (prompt : string) => { 
    try {
      const optimalPath = await processPathfinding(prompt);
      const historique : Historique = {
        userId: userId ?? 'XXX',
        prompt, // Utiliser le prompt reçu
        mapUrl: optimalPath.pathfinding_result.map_url,
        etapes: optimalPath.pathfinding_result.path.map((etape, index) => ({
          ville: etape,
          duree: 10, // À remplacer par la durée réelle
          label:
            index === 0
              ? 'From'
              : index === optimalPath.pathfinding_result.path.length - 1
              ? 'Destination'
              : 'Step',
        })),
      };

      const resultHistorique = await createHistorique(historique);
      setSelectedHistorique(resultHistorique);
      //console.log('Selected histo :' + JSON.stringify(resultHistorique));
      fetchHistorique(); // Rafraîchit la liste après ajout
    } catch (error) {
      console.error('Erreur lors de la création de l’historique:', error);
    }
  };

  useEffect(() => {
    if (userId) {
      fetchHistorique();
    }
  }, [userId]);

  return (
    <HistoriqueContext.Provider
      value={{
        userId,
        selectedHistorique,
        historiques,
        fetchHistorique,
        newHistorique,
        setSelectedHistorique
      }}
    >
      {children}
    </HistoriqueContext.Provider>
  );
};
