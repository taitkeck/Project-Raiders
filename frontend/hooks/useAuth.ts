import { signOut, useSession } from "next-auth/react"
import { useRouter } from "next/router"
import { useEffect, useState } from "react"

/**
 * useAuth hook, for authenticated pages
 * @param shouldRedirect when needing to redirect to /login, shouldRedirect is true
 * @returns boolean isAuthenticated
 */
export default function useAuth(shouldRedirect: boolean) {
  const { data: session } = useSession()
  const router = useRouter()
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  useEffect(() => {
    if (session?.error === "RefreshAccessTokenError") {
      signOut({ callbackUrl: "/login", redirect: shouldRedirect })
    }

    if (session === null) {
      if (router.route !== "/login") {
        router.replace("/login")
      }
      setIsAuthenticated(false)
    } else if (session !== undefined) {
      if (router.route === "/login") {
        router.replace("/")
      }
      setIsAuthenticated(true)
    }
  }, [session])

  return isAuthenticated
}
