'use server'

import { currentUser } from '@clerk/nextjs/server'
import { Prisma, PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

export interface Historique {
    userId : string,
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
    const createResult = await prisma.historique.create({ data: historique })
    const result = await getHistoriquesId(createResult.id)
    return result
  }
}

export async function getHistoriquesByUserId(userId_ : string ){
  if(userId_){
    const result = await prisma.historique.findMany({
      include: {
        etapes: true,
      },
      where: {
        userId: {
          equals: userId_,
        },
      },
      orderBy: [
        {
          id: 'desc',
        }
      ],
    })
  
    return result;
  }
}

export async function getHistoriquesId(id_ : number ){
  if(id_){
    const result = await prisma.historique.findFirst({
      include: {
        etapes: true,
      },
      where: {
        id: {
          equals: id_,
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