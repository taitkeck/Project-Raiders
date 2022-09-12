import type { NextApiRequest, NextApiResponse } from "next"
import { APIFetch } from "../../../../utils/api"
import { StatusCodes } from "http-status-codes"

export default async (req: NextApiRequest, res: NextApiResponse) => {
  const response = await APIFetch(req, "cart", [StatusCodes.CREATED], {
    method: "POST",
    body: req.body,
  })
  res.send(response)
}
