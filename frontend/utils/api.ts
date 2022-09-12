import { getToken } from "next-auth/jwt"
import type { NextApiRequest, NextApiResponse } from "next"
import { StatusCodes } from "http-status-codes"
import { Token } from "../types"

const secret = process.env.NEXTAUTH_SECRET

export async function getHeaders(
  token: Token | null = null,
  headers: HeadersInit | null = null
) {
  return {
    accept: "application/json",
    "Content-Type": "application/json",
    Authorization: `Bearer ${token?.accessToken}`,
    "x-api-key": process.env.API_KEY,
    ...headers,
  } as HeadersInit
}

export async function getAPIHeaders(
  req: NextApiRequest,
  headers: HeadersInit | null = null
) {
  const token = await getToken({ req, secret })
  return {
    Authorization: `Bearer ${token?.accessToken}`,
    "x-api-key": process.env.API_KEY,
    "Content-Type": "application/json",
    accept: "application/json",
    ...headers,
  } as HeadersInit
}

export async function APIFetch(
  req: NextApiRequest,
  path: string,
  success_codes: Array<StatusCodes>,
  init: RequestInit | undefined = undefined
) {
  let url = process.env.API_URL! + path
  // add query to url if exists
  if (Object.keys(req.query).length > 0) {
    // req.query might contain a list value, convert to string here
    const query = Object.fromEntries(
      Object.entries(req.query).map((entry) => [entry[0], entry[1].toString()])
    )
    url += "?" + new URLSearchParams(query)
  }

  // override default headers and method as needed
  let headers = await getAPIHeaders(req)
  let method = "GET"
  if (init) {
    headers = { ...headers, ...init.headers }
    method = init.method || method
    delete init["headers"]
    delete init["method"]
  }

  const apiRes = await fetch(url, {
    method,
    headers,
    ...init,
  })

  if (success_codes.includes(apiRes.status)) {
    const data = await apiRes.json()
    return JSON.stringify(data)
  } else {
    return apiRes
  }
}

export default APIFetch
