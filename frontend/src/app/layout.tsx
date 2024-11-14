// 'use client'

import './globals.css'
import {ClerkProvider} from '@clerk/nextjs'
export const metadata = {
  title: 'MapGpt',
  description: 'Un ChatGpt pour trouver ton itinéraire !',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body>
          {children}
        </body>
      </html>
    </ClerkProvider>
  )
}
