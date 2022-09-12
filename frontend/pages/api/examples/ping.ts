import type { NextApiRequest, NextApiResponse } from "next"
import { getHeaders, APIFetch } from "../../../utils/api"
import { StatusCodes } from "http-status-codes"

export default async (req: NextApiRequest, res: NextApiResponse) => {
  const response = await APIFetch(req, "auth/ping", [StatusCodes.OK])
  res.send(response)
}
