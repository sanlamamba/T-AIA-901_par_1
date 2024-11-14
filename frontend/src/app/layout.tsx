import './globals.css'

export const metadata = {
  title: 'MapGpt',
  description: 'Un ChatGpt pour trouver ton itinéraire !',
}
import {
  ClerkProvider,
  SignInButton,
  SignedIn,
  SignedOut,
  UserButton
} from '@clerk/nextjs'
import './globals.css'
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body>
          <div className='absolute z-50 bg-red-500'>
            <SignedOut>
              <SignInButton />
            </SignedOut>
            <SignedIn>
              <UserButton />
            </SignedIn>
          </div>
          
          {children}
        </body>
      </html>
    </ClerkProvider>
  )
}
