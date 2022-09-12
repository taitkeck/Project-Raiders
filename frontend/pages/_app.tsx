import { SessionProvider } from "next-auth/react"
import type { AppProps } from "next/app"
import { useState } from "react"
import RefreshTokenHandler from "../utils/refreshTokenHandler"
import "./styles.css"

function MyApp({ Component, pageProps }: AppProps) {
  const [interval, setInterval] = useState(0)

  return (
    <SessionProvider session={pageProps.session} refetchInterval={interval}>
      <Component {...pageProps} />
      <RefreshTokenHandler setInterval={setInterval} />
    </SessionProvider>
  )
}

export default MyApp
