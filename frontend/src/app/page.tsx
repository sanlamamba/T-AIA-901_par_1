"use client";

import { useRouter } from "next/navigation";
import Image from "next/image";

export default async function Home() {
  const router = useRouter()

  return (
    <>
      <div className="bg-neutral-800 h-full w-full flex flex-col justify-center items-center gap-8">
        <div>
          <Image 
              src="/assets/chatgpt.png" 
              alt="Logo" 
              width={300}  
              height={300}
            />
        </div>

        <div className="flex gap-4">
          <button onClick={() => {router.push('/sign-in')}} className="bg-white hover:bg-neutral-200 text-black py-2 px-4 border border-neutral-700 rounded-full">
            Log in
          </button>
          <button onClick={() => {router.push('/sign-up')}} className="bg-neutral-800 hover:bg-neutral-700 text-white py-2 px-4 border border-neutral-700 rounded-full">
            Create free account
          </button>
        </div>
        
      </div>
    </>
  );
}
