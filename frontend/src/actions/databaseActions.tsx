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
    debut : boolean
    fin : boolean 
}
async function createHistorique(historique : Historique) {
    const user = await currentUser()
  let historique_ : Prisma.HistoriqueCreateInput
    historique_ = {
        userId : user?.id,
      prompt : historique.prompt,
      mapUrl : historique.mapUrl,
      etapes: {
        create: historique.etapes.map(etape => ({
            ville: etape.ville,
            duree: etape.duree,
            debut: etape.debut,
            fin: etape.fin,
        })),
      },
    }

  const createUser = await prisma.historique.create({ data: historique_ })
}