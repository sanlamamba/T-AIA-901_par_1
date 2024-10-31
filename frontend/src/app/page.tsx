import Image from "next/image";
import ChatBar from "./(components)/chatbar";
import ResultCard from "./(components)/resultcard";
import Map from "./(components)/map";

export default function Home() {
  return (
    <>
      <div className="absolute">
        <Map />
      </div>
      <div className="w-full min-h-screen p-20 flex flex-col justify-between z-10">
          <ResultCard />
          <ChatBar />
      </div>      
    </>
  );
}
