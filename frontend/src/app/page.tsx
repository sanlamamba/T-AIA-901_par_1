"use client";

import Image from "next/image";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  return (
    <div className="bg-white h-screen w-full flex flex-row lg:p-16 md:p-12 p-8">
      {/* Left Section */}
      <div className="flex flex-col flex-1 justify-center items-start space-y-8 pr-10">
        <div className="flex items-center space-x-4">
          <Image
            src="/assets/chatgpt.png"
            alt="Travelgio Logo"
            width={50}
            height={50}
          />
          <div>
            <h1 className="text-3xl font-extrabold text-gray-800">Travelgio</h1>
            <p className="text-gray-500 text-sm">Your travel assistant!</p>
          </div>
        </div>

        <h2 className="text-5xl font-extrabold text-gray-900 leading-tight">
          Your Personal Travel Assistant
        </h2>

        <p className="text-lg text-gray-600 leading-relaxed">
          Discover the best travel experiences and get personalized assistance
          for your next adventure. Travelgio makes planning seamless and
          exciting.
        </p>

        <button
          onClick={() => router.push("/sign-up")}
          className="px-8 py-4 bg-black text-white text-lg font-semibold rounded-lg shadow-md hover:bg-gray-800 transition duration-200"
        >
          Get started
        </button>
      </div>

      <div className="flex-1 flex justify-center items-center">
        <div className="relative w-full h-full rounded-lg overflow-hidden shadow-lg">
          <Image
            src="/assets/maps1.jpg"
            alt="Map"
            fill
            className="object-cover"
          />
        </div>
      </div>
    </div>
  );
}
