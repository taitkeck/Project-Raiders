import NextAuth, { NextAuthOptions, Session, User } from "next-auth"
import CredentialsProvider from "next-auth/providers/credentials"
import { CredentialsBody, FastAPITokenRes } from "../../../types"
import type { NextApiRequest, NextApiResponse } from "next"
import { JWT } from "next-auth/jwt"
import { Token } from "../../../types"
import { getHeaders } from "../../../utils/api"

// https://dev.to/mabaranowski/nextjs-authentication-jwt-refresh-token-rotation-with-nextauthjs-5696
async function refreshAccessToken(tokenObject: Token) {
  try {
    // Get a new set of tokens with a refreshToken
    const res = await fetch(process.env.API_URL + "auth/refresh", {
      method: "POST",
      headers: await getHeaders(null, {
        accept: "application/json",
        "Content-Type": "application/json",
        Authorization: `Bearer ${tokenObject.refreshToken}`,
      }),
    })

    const data = await res.json()

    return {
      ...tokenObject,
      accessToken: data.access_token,
      accessTokenExpiry: data.access_token_expires,
      refreshToken: data.refresh_token,
      refreshTokenExpiry: data.refresh_token_expires,
    }
  } catch (error) {
    return {
      ...tokenObject,
      error: "RefreshAccessTokenError",
    }
  }
}

const providers = [
  CredentialsProvider({
    name: "Credentials",
    authorize: async (credentials) => {
      try {
        // Authenticate user with credentials
        const resToken = await fetch(process.env.API_URL + "auth/login", {
          method: "POST",
          body: JSON.stringify({
            password: credentials!.password,
            email: credentials!.email,
          }),
          headers: await getHeaders(),
        })
        const token = await resToken.json()

        const resUser = await fetch(process.env.API_URL + "user", {
          method: "GET",
          headers: await getHeaders({
            accessToken: token.access_token,
            accessTokenExpiry: token.access_token_expires,
          }),
        })
        const user = await resUser.json()

        return { ...token, ...user }
      } catch (e) {
        throw new Error(e as string)
      }
    },
    credentials: {
      email: { label: "Email", type: "email", placeholder: "me@example.com" },
      password: { label: "Password", type: "password" },
    },
  }),
]

const callbacks = {
  jwt: async ({ token, user }: { token: JWT; user: FastAPITokenRes }) => {
    if (user) {
      // This will only be executed at login. Each next invocation will skip this part.
      token.accessToken = user.access_token
      token.accessTokenExpiry = user.access_token_expires
      token.refreshToken = user.refresh_token
    }

    // If accessTokenExpiry is 24 hours, we have to refresh token before 24 hours pass.
    const shouldRefreshTime = Math.round(
      (token.accessTokenExpiry as number) - 60 * 60 * 1000 - Date.now()
    )

    // If the token is still valid, just return it.
    if (shouldRefreshTime > 0) {
      return Promise.resolve(token)
    }

    // If the call arrives after 23 hours have passed, we allow to refresh the token.
    token = await refreshAccessToken(token)
    return Promise.resolve(token)
  },
  session: async ({
    session,
    user,
    token,
  }: {
    session: Session
    user: User
    token: JWT
  }) => {
    // Here we pass accessToken to the client to be used in authentication with your API
    // session.accessToken = token.accessToken
    // session.accessTokenExpiry = token.accessTokenExpiry
    // session.error = token.error
    const { email, ...rest } = token
    session = {
      ...rest,
      user: {
        email,
      },
      expires: new Date(
        new Date().getTime() + token.accessTokenExpiry * 60000
      ).toLocaleDateString(),
    }

    console.log(session)

    return Promise.resolve(session)
  },
}

export const options = {
  providers,
  callbacks,
  pages: {},
  secret: process.env.NEXTAUTH_SECRET,
}

const Auth = (req: NextApiRequest, res: NextApiResponse) => {
  // @ts-ignore
  NextAuth(req, res, options)
}
export default Auth
