"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter()

  useEffect(() => {
    router.push('/home')
  }, [])
  return (
    <>
      <div className="bg-black h-full w-full flex justify-center items-center">
          <h1 className="text-white">Redirection vers la page d'accueil</h1>
      </div>
    </>
  );
}
