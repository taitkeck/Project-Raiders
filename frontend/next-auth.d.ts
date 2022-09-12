import "next-auth/jwt"

// Read more at: https://next-auth.js.org/getting-started/typescript#module-augmentation

declare module "next-auth/jwt" {
  interface JWT {
    accessToken: string
    accessTokenExpiry: number
    refreshToken?: string
    error?: string
    /** The user's role. */
    // userRole?: "admin"
  }
}
