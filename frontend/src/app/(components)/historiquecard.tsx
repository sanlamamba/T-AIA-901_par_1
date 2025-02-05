"use client";

import { Historique } from "@/actions/historiqueActions";
import { AnimatePresence, motion } from "framer-motion";
import { useHistoriqueContext } from "../context/historiqueContext";

interface Props {
  close: () => void;
  isHistoriqueVisible: boolean;
  setIsHistoriqueVisible: (value: boolean) => void;
  setIsResultCardVisible: (value: boolean) => void;
}
export default function HistoriqueCard({
  close,
  isHistoriqueVisible,
  setIsHistoriqueVisible,
  setIsResultCardVisible,
}: Props) {
  const contextHistoric = useHistoriqueContext();
  if (!contextHistoric) return null;

  const handleHistoriqueClick = (historique: Historique) => {
    contextHistoric.setSelectedHistorique(historique);
    setIsHistoriqueVisible(false);
    setIsResultCardVisible(true);
  };

  // Framer motion variants for the card
  const cardVariants = {
    hidden: { x: "-100%", opacity: 0 },
    visible: {
      x: 0,
      opacity: 1,
      transition: { duration: 0.5, ease: "easeOut" },
    },
    exit: {
      x: "-100%",
      opacity: 0,
      transition: { duration: 0.4, ease: "easeIn" },
    },
  };

  // Framer motion variants for list items
  const listVariants = {
    hidden: { opacity: 0, x: -20 },
    visible: (index: number) => ({
      opacity: 1,
      x: 0,
      transition: {
        delay: 0.5 + index * 0.1, // Delay starts after card animation completes
        duration: 0.3,
        ease: "easeOut",
      },
    }),
  };

  return (
    <AnimatePresence>
      {isHistoriqueVisible && (
        <motion.div
          className="bg-white h-min min-h-96 max-h-128 w-1/3 border-solid border-2 border-slate-100 rounded-lg shadow-lg overflow-auto relative"
          variants={cardVariants}
          initial="hidden"
          animate="visible"
          exit="exit"
        >
          {/* Header */}
          <div className="w-full bg-white sticky top-0 z-20 border-b-2 border-slate-100 p-4 flex items-center justify-between">
            <h1 className="text-2xl font-semibold mb-0">Votre historique</h1>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 384 512"
              className="svgClass cursor"
              onClick={() => {
                close();
                setIsHistoriqueVisible(false);
              }}
            >
              <path d="M342.6 150.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L192 210.7 86.6 105.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L146.7 256 41.4 361.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L192 301.3 297.4 406.6c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L237.3 256 342.6 150.6z" />
            </svg>
          </div>

          {/* List of historiques with animations */}
          <ul className="p-4">
            <AnimatePresence>
              {contextHistoric.historiques && contextHistoric.historiques.length > 0 ? (
                contextHistoric.historiques.map((historique, index) => {
                  const etapes = historique.etapes;
                  const premiereEtape = etapes[0];
                  const derniereEtape = etapes[etapes.length - 1];

                  return (
                    <motion.li
                      key={`${historique.prompt} ${index}`}
                      className="mb-4"
                      initial="hidden"
                      animate="visible"
                      exit={{ opacity: 0, x: -20 }}
                      custom={index}
                      variants={listVariants}
                    >
                      <div
                        className="bg-white border-solid border-2 border-slate-100 rounded-lg shadow-md p-4 overflow-auto w-full flex items-center gap-2 hover:bg-neutral-100 transition duration-200 cursor-pointer"
                        onClick={() => handleHistoriqueClick(historique)}
                      >
                        {/* Icon */}
                        <div>
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 512 512"
                            className="fill-slate-900 w-6 h-6"
                          >
                            <path d="M96 0C43 0 0 43 0 96L0 352c0 48 35.2 87.7 81.1 94.9l-46 46C28.1 499.9 33.1 512 43 512l39.7 0c8.5 0 16.6-3.4 22.6-9.4L160 448l128 0 54.6 54.6c6 6 14.1 9.4 22.6 9.4l39.7 0c10 0 15-12.1 7.9-19.1l-46-46c46-7.1 81.1-46.9 81.1-94.9l0-256c0-53-43-96-96-96L96 0zM64 96c0-17.7 14.3-32 32-32l256 0c17.7 0 32 14.3 32 32l0 96c0 17.7-14.3 32-32 32L96 224c-17.7 0-32-14.3-32-32l0-96zM224 288a48 48 0 1 1 0 96 48 48 0 1 1 0-96z" />
                          </svg>
                        </div>
                        {/* Details */}
                        <div className="w-full">
                          <h2 className="text-xs text-slate-500">
                            {historique.prompt}
                          </h2>
                          <div className="text-sm flex justify-between">
                            <div>{premiereEtape.ville}</div>
                            <div>{derniereEtape.ville}</div>
                          </div>
                        </div>
                      </div>
                    </motion.li>
                  );
                })
              ) : (
                <motion.p
                  className="text-gray-500 mt-4"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                >
                  Aucun historique disponible.
                </motion.p>
              )}
            </AnimatePresence>
          </ul>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
