import './globals.css'

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
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
