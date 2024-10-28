'use client'

import { FormEvent } from "react";
import { EventEmitter } from "stream";
import Image from 'next/image'

export default function Map(){

  const getMap= () =>{
    return "/assets/map.html"
  }
    
    return(
      <>
        <iframe className="flex items-center justify-center w-screen h-screen  -z-50" src={getMap()} width="100%"></iframe>
      </>
    )
  }