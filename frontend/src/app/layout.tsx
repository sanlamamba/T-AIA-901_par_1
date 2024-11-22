// 'use client'

import "./globals.css";
import { ClerkProvider } from "@clerk/nextjs";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

export const metadata = {
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
