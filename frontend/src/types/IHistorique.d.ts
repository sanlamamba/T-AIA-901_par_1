export interface IEtape {
    label : string,
    id : number,
    historiqueId : number,
    ville : string,
    duree : number
}

export interface IHistorics {
    id : number,
    userId : string,
    prompt : string,
    mapUrl : string,
    etapes : IEtape[]
}

// export async function getHistoriquesByUserId(userId_ : string ){
//   if(userId_){
//     const result = await prisma.historique.findMany({
//       include: {
//         etapes: true,
//       },
//       where: {
//         userId: {
//           equals: userId_,
//         },
//       },
//       orderBy: [
//         {
//           id: 'desc',
//         }
//       ],
//     })
  
//     return result;
//   }
// }


