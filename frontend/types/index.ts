import { User } from "next-auth"

export interface Token {
  accessToken: string
  accessTokenExpiry: number
  refreshToken?: string
  error?: string
}

export interface Session extends Token, User {}

export interface FastAPITokenRes {
  access_token: string
  access_token_expires: number
  refresh_token: string
  refresh_token_expires: number
  // user: {
  //   id: string
  //   username: string
  //   email: string
  //   password: string
  // }
}

export interface CredentialsBody {
  username: string
  password: string
}
