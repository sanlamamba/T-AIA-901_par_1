'use server'

import { PrismaClient, Prisma } from '@prisma/client'
import { currentUser } from '@clerk/nextjs/server'

const prisma = new PrismaClient()

export interface Historique {
    userId : number
    prompt : string,
    mapUrl : string,
    etapes : Etape[]
}
export interface Etape {
    ville : string
    duree : number
    label : string
}

export async function createHistorique(historique_ : Historique) {
    const user = await currentUser()
  let historique : Prisma.HistoriqueCreateInput
  if(user){
    historique = {
      userId : user?.id,
      prompt : historique_.prompt,
      mapUrl : historique_.mapUrl,
      etapes: {
        create: historique_.etapes.map(etape => ({
            ville: etape.ville,
            duree: etape.duree,
            label: etape.label
        })),
      },
    }
    const result = await prisma.historique.create({ data: historique })
    return result
  }
}

export async function getHistoriquesByUserId(userId_ : string | undefined){
  if(userId_){
    const result = await prisma.historique.findMany({
      where: {
        userId: {
          equals: userId_,
        },
      },
    })
  
    return result;
  }
}

export async function deleteHistoriqueById(id_ : number){
  const result = await prisma.historique.delete({
    where : {
      id : id_
    }
  })

  return result;
}