'use client'

import { FormEvent, useState, } from "react";
import {Image} from 'next';
import { EventEmitter } from "stream";

export default function ChatBar(){
    
    const [recording, setRecording] = useState(false);

    
    async function sendChat(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();

        const formData = new FormData(event.currentTarget);
        const message = formData.get('message') as string;

        console.log("Message envoyé :", message);
    }
    
    function handleRecord() {
        setRecording(true);
        console.log("Enregistrement en cours...");
        
    }

    return(
      <>
        <div className="w-full border-solid border-2 border-slate-100 rounded-full shadow-lg p-8 bg-white z-10">
            <form onSubmit={sendChat} className="flex gap-4 items-center">
                    {/* Champ de saisie du message */}
                    <input 
                        type="text" 
                        name="message" 
                        placeholder="Entrez votre message" 
                        className="flex-grow px-4 focus:outline-none"
                    />
                    <div className="flex gap-8 items-center">
                        <div>   
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512" className={`cursor-pointer svgClassChatbar ${recording == true ? 'fill-red-500' : 'fill-slate-500'}`}>
                                <path d="M192 0C139 0 96 43 96 96l0 160c0 53 43 96 96 96s96-43 96-96l0-160c0-53-43-96-96-96zM64 216c0-13.3-10.7-24-24-24s-24 10.7-24 24l0 40c0 89.1 66.2 162.7 152 174.4l0 33.6-48 0c-13.3 0-24 10.7-24 24s10.7 24 24 24l72 0 72 0c13.3 0 24-10.7 24-24s-10.7-24-24-24l-48 0 0-33.6c85.8-11.7 152-85.3 152-174.4l0-40c0-13.3-10.7-24-24-24s-24 10.7-24 24l0 40c0 70.7-57.3 128-128 128s-128-57.3-128-128l0-40z"/>
                            </svg>                       
                        </div> 
                        <div>   
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" className="cursor-pointer svgClassChatbar fill-slate-500">
                                <path d="M16.1 260.2c-22.6 12.9-20.5 47.3 3.6 57.3L160 376l0 103.3c0 18.1 14.6 32.7 32.7 32.7c9.7 0 18.9-4.3 25.1-11.8l62-74.3 123.9 51.6c18.9 7.9 40.8-4.5 43.9-24.7l64-416c1.9-12.1-3.4-24.3-13.5-31.2s-23.3-7.5-34-1.4l-448 256zm52.1 25.5L409.7 90.6 190.1 336l1.2 1L68.2 285.7zM403.3 425.4L236.7 355.9 450.8 116.6 403.3 425.4z"/>
                            </svg>
                        </div>
                    </div>
            </form>
        </div>
      </>
    )
  }