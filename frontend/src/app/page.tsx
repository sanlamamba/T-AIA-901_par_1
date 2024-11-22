"use client";

import { motion, useAnimation } from "framer-motion";
import Image from "next/image";
import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();
  const logoControls = useAnimation();

  useEffect(() => {
    const interval = setInterval(() => {
      logoControls
        .start({
          rotate: 360,
          transition: {
            duration: 1.5,
            ease: "easeInOut",
          },
        })
        .then(() => {
          logoControls.set({ rotate: 0 });
        });
    }, 500);

    return () => clearInterval(interval);
  }, [logoControls]);

  return (
    <motion.div
      className="bg-white h-screen w-full flex flex-row lg:p-16 md:p-12 p-8"
      initial={{ opacity: 0, y: 50 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8, ease: "easeOut" }}
    >
      {/* Left Section */}
      <motion.div
        className="flex flex-col flex-1 justify-center items-start space-y-8 pr-10"
        initial={{ opacity: 0, x: -50 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.8, delay: 0.2, ease: "easeOut" }}
      >
        {/* Logo Section */}
        <div className="flex items-center space-x-4">
          <motion.div
            animate={logoControls}
            className="w-12 h-12 flex justify-center items-center"
          >
            <Image
              src="/assets/chatgpt.png"
              alt="Travelgio Logo"
              width={50}
              height={50}
            />
          </motion.div>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.3 }}
          >
            <h1 className="text-3xl font-extrabold text-gray-800">Travelgio</h1>
            <p className="text-gray-500 text-sm">Your travel assistant!</p>
          </motion.div>
        </div>

        {/* Headline Section */}
        <motion.h2
          className="text-5xl font-extrabold text-gray-900 leading-tight"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.5 }}
        >
          Your Personal Travel Assistant
        </motion.h2>

        {/* Description Section */}
        <motion.p
          className="text-lg text-gray-600 leading-relaxed"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.7 }}
        >
          Discover the best travel experiences and get personalized assistance
          for your next adventure. Travelgio makes planning seamless and
          exciting.
        </motion.p>

        {/* Get Started Button */}
        <motion.button
          className="px-8 py-4 bg-black text-white text-lg font-semibold rounded-lg shadow-md hover:bg-gray-800 transition duration-200"
          whileHover={{
            scale: 1.1,
            transition: { duration: 0.1 },
          }}
          whileTap={{ scale: 0.95 }}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.9 }}
          onClick={() => router.push("/sign-up")}
        >
          Get started
        </motion.button>
      </motion.div>

      {/* Right Section */}
      <motion.div
        className="flex-1 flex justify-center items-center"
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.8, delay: 0.4, ease: "easeOut" }}
      >
        <motion.div
          className="relative w-full h-full rounded-lg overflow-hidden shadow-lg"
          whileHover={{ scale: 1.02 }}
          transition={{ duration: 0.4 }}
        >
          <Image
            src="/assets/maps1.jpg"
            alt="Map"
            fill
            className="object-cover"
          />
        </motion.div>
      </motion.div>
    </motion.div>
  );
}
