'use client'
import { Historique } from '@/actions/historiqueActions';
import React, {createContext, use, useContext, useState} from 'react'
type Context = {
    selectedHistorique ?: Historique,
    historiques ?: Historique[],
    userId ?: string
}
const AppContext = createContext<any>(undefined);

export function AppWrapper({children}:{
    children : React.ReactNode
}){
    let [selectedHistorique, setSelectedHistorique] = useState({})
    let [historiques, setHistoriques] = useState({})
    let [userId, setUserId] = useState('')

    return (
        <AppContext.Provider value={
            {selectedHistorique, setSelectedHistorique,
            historiques, setHistoriques,
            userId, setUserId}
        }>
            {children}
        </AppContext.Provider>
    )
}

export function useAppContext(){
    return useContext(AppContext);
}