// 'use client'

import { ClerkProvider } from "@clerk/nextjs";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "./globals.css";

interface Metadata {
  title: string;
  description: string;
}

export const metadata: Metadata = {
  title: "Travelgio",
  description: "Un ChatGpt pour trouver ton itinéraire !",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body>
          <ToastContainer />
          {children}
        </body>
      </html>
    </ClerkProvider>
  );
}
